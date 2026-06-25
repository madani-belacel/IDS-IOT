#ifndef IDS_CAMPAIGN_LOG_H_
#define IDS_CAMPAIGN_LOG_H_

#include <stdint.h>

void ids_campaign_log_det(uint32_t tp, uint32_t fp, uint32_t tn, uint32_t fn);
void ids_campaign_log_lat(uint32_t latency_s_mean);
void ids_campaign_log_fpr(uint8_t traffic_class, uint32_t fpr_x10000);
void ids_campaign_log_nrg(uint8_t role, uint8_t mode, uint8_t cpu_pct, uint16_t ram_kb,
                          uint8_t energest_delta_pct);
void ids_campaign_log_alert(uint16_t nodes, uint16_t alerts_per_hour);
void ids_campaign_log_clust(uint16_t time_min, uint32_t ch_tenure_s, uint16_t recluster_rate,
                            uint8_t mean_nre);
void ids_campaign_log_temp(const char *phase, uint32_t det_rate_x10000);
void ids_campaign_log_mode(uint8_t mode, uint32_t det_rate_x10000, uint32_t fpr_x10000,
                           uint8_t cpu_pct);
void ids_campaign_log_attack(const char *scenario, uint32_t event_id, uint32_t t_start,
                             uint32_t t_end);

#endif
