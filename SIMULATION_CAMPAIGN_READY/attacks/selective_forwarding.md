# Attack: Selective Forwarding

**Status:** `READY_FOR_SIMULATION`

Malicious forwarders drop a fraction of downstream data packets.

| Parameter | Value |
|-----------|-------|
| Drop rate | 60% of downstream data |
| Target | All classes; emphasis on $C2$/$C3$ in mixed campaign |
| Duration | Attack window |

Detection signals: R2 (forwarding gap), ETX variance at CH.
