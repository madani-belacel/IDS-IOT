#ifndef PROJECT_CONF_H_
#define PROJECT_CONF_H_

/* RPL-ClusterIDS configuration.
   Variant macros are defined in variants/imacros-*.h.
   Override any default below via the build system (e.g., -DIDS_CAMPAIGN_SEED=42). */

#ifndef IDS_UDP_PORT
#define IDS_UDP_PORT 8765
#endif

#endif /* PROJECT_CONF_H_ */
