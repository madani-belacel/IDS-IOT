#ifndef PROJECT_CONF_H_
#define PROJECT_CONF_H_

/* RPL-ClusterIDS configuration.
   Variant macros are defined in variants/imacros-*.h.
   Override any default below via the build system (e.g., -DIDS_CAMPAIGN_SEED=42). */

#ifndef IDS_CONF_CAMPAIGN_METRICS
#define IDS_CONF_CAMPAIGN_METRICS 0
#endif

#ifndef IDS_CAMPAIGN_SEED
#define IDS_CAMPAIGN_SEED 0
#endif

#ifndef IDS_CAMPAIGN_SCENARIO
#define IDS_CAMPAIGN_SCENARIO "none"
#endif

#ifndef IDS_ATTACK_START_S
#define IDS_ATTACK_START_S 1800
#endif

#ifndef IDS_SIM_DURATION_S
#define IDS_SIM_DURATION_S 10800
#endif

#define IDS_UDP_PORT 8765

#endif /* PROJECT_CONF_H_ */
