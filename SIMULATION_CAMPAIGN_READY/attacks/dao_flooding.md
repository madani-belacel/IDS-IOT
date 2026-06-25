# Attack: DAO Flooding

**Status:** `READY_FOR_SIMULATION`

Malicious nodes emit DAO messages at elevated rate to exhaust neighbor tables.

| Parameter | Value |
|-----------|-------|
| Rate multiplier | 10× baseline DAO rate |
| Targets | All neighbors within 2 hops |
| Duration | Attack window |

Detection signals: R4 (control-plane flood), control-load term in $\Delta_c$.
