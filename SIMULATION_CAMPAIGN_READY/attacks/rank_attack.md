# Attack: Rank Manipulation

**Status:** `READY_FOR_SIMULATION`

Malicious nodes advertise artificially low RPL ranks to attract downstream traffic.

| Parameter | Value |
|-----------|-------|
| Trigger | After 30 min stabilization |
| Method | Inflated rank improvement in DIO advertisements |
| Intensity | Rank delta −128 below legitimate minimum |
| Duration | Until end of attack window |

Detection signals: R1 (rank inconsistency), LAS spike, CH ML confirmation.
