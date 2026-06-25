# Scenario: 500 Nodes

**Status:** `READY_FOR_SIMULATION`

## Topology

| Layout | Parameters |
|--------|------------|
| Grid | $22 \times 22$ grid, 500 active nodes, 440 m × 440 m |
| Random | Uniform, min separation 25 m |

## Timing

3 h simulated per run (may require extended Cooja heap on host).

## Attack placement

5–10% malicious nodes (25–50 nodes).

## Notes

Stress test for cluster stability and alert sublinearity claims.

## Outputs

Logs → `data/real/raw_logs/500nodes/`
