# Scenario: 100 Nodes

**Status:** `READY_FOR_SIMULATION`

## Topology

| Layout | Parameters |
|--------|------------|
| Grid | $10 \times 10$ grid, 100 active nodes, 200 m × 200 m |
| Random | Uniform, min separation 35 m |

## Radio, MAC, RPL

Same as 50-node scenario (UDGM, 10% duty cycle, `rpl-lite`).

## Timing

3 h simulated (30 min stabilization, 120 min attack, 30 min recovery).

## Attack placement

5–8% malicious nodes (5–8 nodes), depth-stratified.

## Outputs

Logs → `data/real/raw_logs/100nodes/`
