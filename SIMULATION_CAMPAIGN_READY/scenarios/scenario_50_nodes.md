# Scenario: 50 Nodes

**Status:** `READY_FOR_SIMULATION`  
**Scale:** 50 sky motes + 1 border router (host)

## Topology

| Layout | Parameters |
|--------|------------|
| Grid | $7 \times 7$ grid, 50 active nodes, 150 m × 150 m, 50 m spacing |
| Random | Uniform placement, min separation 40 m, same area |

## Radio & MAC

- CC2420 radio model (Cooja default for sky)
- Unit Disk Graph Medium (UDGM), range 50 m, interference range 100 m
- MAC: CSMA, 10% duty cycle

## RPL

- `rpl-lite`, MRHOF objective, rank threshold 384
- Border router at (75, 75) grid center

## Timing

- Stabilization: 30 min
- Attack window: 120 min
- Cool-down / recovery: 30 min
- Total simulated time: 3 h

## Attack placement

- 5% malicious nodes (2–3 nodes), placed at varying DODAG depths
- Attacker selection: deterministic per seed

## Variants & modes

- B1, B2, B3, CLUSTERIDS
- CLUSTERIDS: Full, Balanced, Eco

## Expected outputs

- 20 seeds × 5 attacks × 4 variants × 2 topologies = 800 runs (CLUSTERIDS modes add runs)
- Logs → `data/real/raw_logs/50nodes/`
