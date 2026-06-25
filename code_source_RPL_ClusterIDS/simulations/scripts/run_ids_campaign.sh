#!/usr/bin/env bash
# RPL-ClusterIDS — Phase 2 campaign launcher (Ubuntu + Cooja headless).
# Usage:
#   ./run_ids_campaign.sh smoke              # 3-node sanity check
#   ./run_ids_campaign.sh pilot              # 50n × 3 seeds
#   ./run_ids_campaign.sh full               # full campaign matrix (660 runs)
#   ./run_ids_campaign.sh batch <rows>       # specific rows from matrix (1-based)
#
# Environment:
#   CONTIKI_NG    path to Contiki-NG root (default: $HOME/contiki-ng)
#   NUM_SEEDS     override seed count (default: from matrix)
#   SIM_TIMEOUT_MS simulation timeout in ms (default: 10800000 = 3h)
#   MAX_PARALLEL  max parallel Cooja instances (default: 2)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
IDS_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROJECT_ROOT="$(cd "$IDS_DIR/.." && pwd)"
CONTIKI_NG="${CONTIKI_NG:-$HOME/contiki-ng}"
COOJA_DIR="$CONTIKI_NG/tools/cooja"
CAMPAIGN_MATRIX="$PROJECT_ROOT/SIMULATION_CAMPAIGN_READY/campaign_matrix.tsv"

LOG_DIR="${IDS_DIR}/simulations/logs/ids_campaign"
CSC_DIR="${IDS_DIR}/simulations/cooja"
BUILD_DIR="${IDS_DIR}/build"
DATA_REAL="${PROJECT_ROOT}/data/real"

NUM_SEEDS="${NUM_SEEDS:-}"
SIM_TIMEOUT_MS="${SIM_TIMEOUT_MS:-10800000}"
MAX_PARALLEL="${MAX_PARALLEL:-2}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; NC='\033[0m'
log_info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

usage() {
    echo "Usage: $0 {smoke|pilot|full|batch <rows>}"
    echo ""
    echo "Modes:"
    echo "  smoke         3-node sanity check (1 seed, MAIN, no attack)"
    echo "  pilot         50 nodes, 3 seeds per config (subset of matrix)"
    echo "  full          all 33 matrix rows x 20 seeds = 660 runs"
    echo "  batch <rows>  specific rows from matrix (e.g. '1-5,7,10-12')"
    echo ""
    echo "Environment:"
    echo "  CONTIKI_NG=$CONTIKI_NG"
    echo "  NUM_SEEDS=${NUM_SEEDS:-auto}"
    echo "  SIM_TIMEOUT_MS=$SIM_TIMEOUT_MS"
    echo "  MAX_PARALLEL=$MAX_PARALLEL"
    exit 1
}

check_env() {
    if [ ! -d "$CONTIKI_NG" ]; then
        log_error "CONTIKI_NG=$CONTIKI_NG not found."
        exit 1
    fi
    if ! command -v java &>/dev/null; then
        log_error "Java not found. Install: sudo apt install openjdk-17-jdk"
        exit 1
    fi
    mkdir -p "$LOG_DIR" "$CSC_DIR" "$DATA_REAL/raw_logs" "$DATA_REAL/parsed" "$DATA_REAL/aggregated"
}

build_cooja() {
    local jar
    jar=$(get_jar)
    [ -n "$jar" ] && { log_ok "Cooja already built: $jar"; return 0; }
    log_info "Building Cooja..."
    cd "$COOJA_DIR"
    ./gradlew build 2>&1 | tail -3
    if [ ! -f "build/libs/cooja.jar" ]; then
        log_error "Cooja build failed."
        exit 1
    fi
    log_ok "Cooja built: $(ls build/libs/cooja.jar)"
}

get_jar() {
    if [ -f "$COOJA_DIR/build/libs/cooja.jar" ]; then
        echo "$COOJA_DIR/build/libs/cooja.jar"
    elif [ -f "$COOJA_DIR/dist/cooja.jar" ]; then
        echo "$COOJA_DIR/dist/cooja.jar"
    else
        echo ""
    fi
}

build_variant() {
    local variant="$1"

    log_info "Building variant $variant (clean + full compile)..."
    mkdir -p "$BUILD_DIR"
    cd "$IDS_DIR"
    CONTIKI="$CONTIKI_NG" make clean TARGET=cooja 2>&1 | tail -2
    CONTIKI="$CONTIKI_NG" make -j$(nproc) TARGET=cooja IDS_VARIANT="$variant" IDS_CONF_CAMPAIGN_METRICS=1 2>&1 | tail -5

    if [ ! -f "build/cooja/clusterids-node.cooja" ]; then
        log_error "Build failed for $variant"
        exit 1
    fi

    cp "build/cooja/clusterids-node.cooja" "$BUILD_DIR/clusterids-node-${variant}.cooja"
    log_ok "Built $variant (fresh .o files for linking)"
}

run_simulation() {
    local variant="$1" scenario="$2" nodes="$3" topology="$4" cluster_mode="$5" seed="$6"
    local mode_suffix=""
    [ -n "$cluster_mode" ] && [ "$cluster_mode" != "—" ] && mode_suffix="_${cluster_mode}"
    local log_name="log_${variant}_${topology}_${nodes}nodes_${scenario}${mode_suffix}_seed${seed}.log"
    local log_path="$LOG_DIR/$log_name"
    local csc_name="csc_${variant}_${topology}_${nodes}n_${scenario}${mode_suffix}_seed${seed}.csc"
    local csc_path="$CSC_DIR/$csc_name"

    if [ -f "$log_path" ] && grep -q "METRIC," "$log_path" 2>/dev/null; then
        log_ok "Already done: $log_name"
        return 0
    fi

    local timeout=$SIM_TIMEOUT_MS
    if [ "$nodes" -le 100 ]; then
        timeout=$SIM_TIMEOUT_MS
    elif [ "$nodes" -le 300 ]; then
        timeout=$((SIM_TIMEOUT_MS * 2))
    else
        timeout=$((SIM_TIMEOUT_MS * 3))
    fi

    local jar_path
    jar_path=$(get_jar)
    if [ -z "$jar_path" ]; then
        log_error "Cooja JAR not found."
        return 1
    fi

    local scenario_desc="$scenario"
    [ -n "$cluster_mode" ] && [ "$cluster_mode" != "—" ] && scenario_desc="${scenario}_${cluster_mode}"

    python3 "$SCRIPT_DIR/generate_campaign_csc.py" \
        --nodes "$nodes" \
        --seed "$seed" \
        --variant "$variant" \
        --scenario "$scenario_desc" \
        --log "$log_path" \
        --timeout-ms "$timeout" \
        --topology "$topology" \
        --out "$csc_path" 2>&1 | tail -1

    log_info "Run: $variant $scenario ${nodes}n seed=$seed ${cluster_mode:+mode=$cluster_mode}"

    local start_time
    start_time=$(date +%s)
    cd "$COOJA_DIR"

    CONTIKI="$CONTIKI_NG" java -Xms256M -Xmx2G \
        -XX:-UseCompressedOops -XX:-UseCompressedClassPointers \
        --enable-preview --enable-native-access ALL-UNNAMED \
        -jar "$jar_path" \
        --no-gui --contiki="$CONTIKI_NG" --logdir="$LOG_DIR" \
        "$csc_path" 2>/dev/null || true

    local elapsed=$(( $(date +%s) - start_time ))

    if [ -f "$log_path" ] && grep -q "METRIC," "$log_path" 2>/dev/null; then
        local metric_count
        metric_count=$(grep -c "METRIC," "$log_path")
        log_ok "Done: $log_name (${metric_count} metrics, ${elapsed}s)"
        cp "$log_path" "$DATA_REAL/raw_logs/$log_name" 2>/dev/null || true
        return 0
    else
        log_warn "No METRIC in $log_name (${elapsed}s)"
        return 1
    fi
}

run_smoke() {
    echo ""
    log_info "=== Smoke test: 3 nodes, MAIN, 1 seed ==="
    build_variant "MAIN"
    run_simulation "MAIN" "none" "3" "grid" "" "1001" || true
    echo ""
    ls -la "$LOG_DIR"/log_MAIN_grid_3nodes_none_seed1001.log 2>/dev/null || log_warn "No log"
    log_ok "Smoke test complete."
}

run_variant_group() {
    local mode="$1" variant="$2" batch_rows="${3:-}"

    # Build this variant fresh (clean + compile)
    build_variant "$variant"

    local row_num=0 total=0 pids=()

    while IFS=$'\t' read -r nodes topology attack matrix_variant matrix_mode seeds_hint duration_h; do
        row_num=$((row_num + 1))
        [ "$row_num" -eq 1 ] && continue
        [ -z "$nodes" ] && continue

        # Only process rows for this variant
        [ "$matrix_variant" != "$variant" ] && continue

        # Filter by mode
        [ "$mode" = "pilot" ] && [ "$nodes" -ne 50 ] && continue

        # Batch filter
        if [ "$mode" = "batch" ] && [ -n "$batch_rows" ]; then
            local matched=0
            local IFS=','
            for range in $batch_rows; do
                if echo "$range" | grep -q '-'; then
                    local s="${range%-*}" e="${range#*-}"
                    [ "$row_num" -ge "$s" ] && [ "$row_num" -le "$e" ] && matched=1 && break
                elif [ "$row_num" -eq "$range" ] 2>/dev/null; then
                    matched=1 && break
                fi
            done
            unset IFS
            [ "$matched" -eq 0 ] && continue
        fi

    SEEDS_FILE="${PROJECT_ROOT}/SIMULATION_CAMPAIGN_READY/seeds.txt"
    if [ -f "$SEEDS_FILE" ]; then
        mapfile -t SEED_ARRAY < "$SEEDS_FILE"
        log_info "Loaded ${#SEED_ARRAY[@]} seeds from seeds.txt"
    else
        log_warn "seeds.txt not found, generating sequential seeds"
        local s=${NUM_SEEDS:-$seeds_hint}
        s=${s:-20}
        SEED_ARRAY=()
        for i in $(seq 1 "$s"); do
            SEED_ARRAY+=($((20260601 + i)))
        done
    fi

    for seed_idx in $(seq 0 $((${#SEED_ARRAY[@]} - 1))); do
        local base_seed=${SEED_ARRAY[$seed_idx]}
            total=$((total + 1))

            (
                if run_simulation "$variant" "$attack" "$nodes" "$topology" "$matrix_mode" "$base_seed"; then
                    echo "OK:$variant:$attack:${nodes}n:seed${seed_idx}"
                else
                    echo "FAIL:$variant:$attack:${nodes}n:seed${seed_idx}"
                fi
            ) &
            pids+=($!)

            if [ ${#pids[@]} -ge "$MAX_PARALLEL" ]; then
                for pid in "${pids[@]}"; do wait "$pid" 2>/dev/null || true; done
                pids=()
            fi
        done

        # Wait for remaining pids for this row
        for pid in "${pids[@]}"; do wait "$pid" 2>/dev/null || true; done
        pids=()
    done < "$CAMPAIGN_MATRIX"

    echo ""
    log_info "Variant $variant done: $total runs"
}

run_campaign() {
    local mode="$1"
    local batch_rows="${2:-}"

    if [ ! -f "$CAMPAIGN_MATRIX" ]; then
        log_error "Matrix not found: $CAMPAIGN_MATRIX"
        exit 1
    fi

    for v in MAIN B1 B2 B3 MAIN_NOCLUS MAIN_NOML MAIN_NOCTX MAIN_NOENR; do
        log_info "=== Variant group: $v ==="
        run_variant_group "$mode" "$v" "$batch_rows"
    done

    echo ""
    log_info "=== Campaign done ($mode) ==="
    log_info "Logs: $(find "$LOG_DIR" -name '*.log' 2>/dev/null | wc -l) files"
    log_info "Real: $(find "$DATA_REAL/raw_logs" -name '*.log' 2>/dev/null | wc -l) files"
}

run_parse() {
    log_info "Parsing logs -> CSV..."
    python3 "$SCRIPT_DIR/parse_cooja_ids_metrics.py" \
        --logs "$LOG_DIR" \
        --out "$DATA_REAL/parsed/" 2>&1
    log_ok "CSVs in $DATA_REAL/parsed/"
}

main() {
    local cmd="${1:-}"
    shift 2>/dev/null || true

    check_env

    case "$cmd" in
        smoke)
            build_cooja
            run_smoke
            run_parse
            ;;
        pilot|full)
            build_cooja
            run_campaign "$cmd" ""
            run_parse
            log_info "Next: compute_statistics.py"
            ;;
        batch)
            local rows="${1:-}"
            [ -z "$rows" ] && { log_error "batch needs rows (e.g. '1-5,7')"; usage; }
            build_cooja
            run_campaign "batch" "$rows"
            run_parse
            ;;
        *) usage ;;
    esac
}

main "$@"
