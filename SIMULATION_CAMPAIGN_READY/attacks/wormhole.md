# Attack: Wormhole

**Status:** `READY_FOR_SIMULATION`

Two colluding nodes tunnel control traffic to bias parent selection.

| Parameter | Value |
|-----------|-------|
| Colluders | 2 nodes at different DODAG depths |
| Tunnel | Encapsulated DIO/DAO replay with reduced delay |
| Duration | Attack window |

Detection signals: R3 (topology inconsistency), inter-cluster corroboration required.
