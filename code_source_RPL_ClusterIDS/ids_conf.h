#ifndef IDS_CONF_H_
#define IDS_CONF_H_

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
#define IDS_ATTACK_START_S 1800    //  Attaque démarre à 30 min
#endif

#ifndef IDS_SIM_DURATION_S
#define IDS_SIM_DURATION_S 10800   //  3h de simulation
#endif

#define IDS_UDP_PORT 8765

//  Seuils LAS (échelle brute ~0-175)
#define IDS_THRESHOLD_LAS     60   //  Alarme membre
#define IDS_THRESHOLD_CH      70   //  Vérification CH
#define IDS_THRESHOLD_LOW     25   //  Déclenchement mode ECO (%)
#define IDS_THRESHOLD_CH_ELIG 40   //  Éligibilité CH (NRE min %)

#endif /* IDS_CONF_H_ */
