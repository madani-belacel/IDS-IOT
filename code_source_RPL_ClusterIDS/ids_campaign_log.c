/*
 * Copyright (c) 2026, Madani Belacel.
 *   Generates METRIC lines consumed by the Python parsing pipeline
 *   to produce campaign CSVs.
 *   Format is simple but works with the existing pipeline.
 * FIXME: printf on Cooja node is slow — switch to a buffered writer?
 *        (acceptable now, but may be slow with 500+ nodes)
 */

#include "contiki.h"
#include "ids_campaign_log.h"
#include "ids_conf.h"
#include <locale.h>
#include <stdio.h>

#if !IDS_CONF_CAMPAIGN_METRICS
const int ids_campaign_log_disabled = 0;
#endif

#if IDS_CONF_CAMPAIGN_METRICS

static const char *
variant_tag(void)
{
  /* Tags for the parsing pipeline.
     Long names avoid collisions between variants. */
#if IDS_VARIANT_B1
  return "B1";
#elif IDS_VARIANT_B2
  return "B2";
#elif IDS_VARIANT_B3
  return "B3";
#elif IDS_ABLATION_NOCLUS
  return "NO_CLUST";
#elif IDS_ABLATION_NOML
  return "MEMBERS";
#elif IDS_ABLATION_NOCTX
  return "FIXED_MODE";
#elif IDS_ABLATION_NOENR
  return "FIXED_NRG";
#else
  return "MAIN";
#endif
  (void)sizeof(IDS_VARIANT_LABEL); /* suppress unused warning */
}

static uint32_t
det_rate_x10000(uint32_t tp, uint32_t fp, uint32_t tn, uint32_t fn)
{
  uint32_t denom = tp + fn;

  if(denom == 0) {
    return 0; /* no attack frames in this window → skip */
  }
  return (10000UL * tp) / denom;
}

void
ids_campaign_log_det(uint32_t tp, uint32_t fp, uint32_t tn, uint32_t fn)
{
   printf("METRIC,DET,%u,%s,%s,%u,%u,%u,%u,%.4f\n",
          (unsigned)IDS_CAMPAIGN_SEED,
          variant_tag(),
          IDS_CAMPAIGN_SCENARIO,
          (unsigned)tp, (unsigned)fp, (unsigned)tn, (unsigned)fn,
          (double)det_rate_x10000(tp, fp, tn, fn) / 10000.0);
}

void
ids_campaign_log_lat(uint32_t latency_s_mean)
{
  printf("METRIC,LAT,%u,%s,%s,%u\n",
         (unsigned)IDS_CAMPAIGN_SEED,
         variant_tag(),
         IDS_CAMPAIGN_SCENARIO,
         (unsigned)latency_s_mean);
}

void
ids_campaign_log_fpr(uint8_t traffic_class, uint32_t fpr_x10000)
{
  printf("METRIC,FPR,%u,%s,%s,%u,%.4f\n",
         (unsigned)IDS_CAMPAIGN_SEED,
         variant_tag(),
         IDS_CAMPAIGN_SCENARIO,
         (unsigned)traffic_class,
         (double)fpr_x10000 / 10000.0);
}

void
ids_campaign_log_nrg(uint8_t role, uint8_t mode, uint8_t cpu_pct, uint16_t ram_kb,
                     uint8_t energest_delta_pct)
{
   printf("METRIC,NRG,%u,%s,%u,%u,%u,%u,%u\n",
          (unsigned)IDS_CAMPAIGN_SEED,
          variant_tag(),
          (unsigned)role, (unsigned)mode,
          (unsigned)cpu_pct, (unsigned)ram_kb,
          (unsigned)energest_delta_pct);
}

void
ids_campaign_log_alert(uint16_t nodes, uint16_t alerts_per_hour)
{
   printf("METRIC,ALERT,%u,%s,%u,%u\n",
          (unsigned)IDS_CAMPAIGN_SEED,
          variant_tag(),
          (unsigned)nodes, (unsigned)alerts_per_hour);
}

void
ids_campaign_log_clust(uint16_t time_min, uint32_t ch_tenure_s, uint16_t recluster_rate,
                       uint8_t mean_nre)
{
  printf("METRIC,CLUST,%u,%u,%u,%u,%u\n",
         (unsigned)IDS_CAMPAIGN_SEED,
         (unsigned)time_min,
         (unsigned)ch_tenure_s,
         (unsigned)recluster_rate,
         (unsigned)mean_nre);
}

void
ids_campaign_log_temp(const char *phase, uint32_t det_rate_x10000)
{
   printf("METRIC,TEMP,%u,%s,%.4f\n",
          (unsigned)IDS_CAMPAIGN_SEED,
          phase,
          (double)det_rate_x10000 / 10000.0);
}

void
ids_campaign_log_mode(uint8_t mode, uint32_t det_rate_x10000, uint32_t fpr_x10000,
                      uint8_t cpu_pct)
{
  const char *mode_str = "Balanced";

  if(mode == 0) {
     mode_str = "Full";
  } else if(mode == 2) {
     mode_str = "Eco";
  }
  printf("METRIC,MODE,%u,%s,%s,%.4f,%.4f,%u\n",
         (unsigned)IDS_CAMPAIGN_SEED,
         variant_tag(),
         mode_str,
         (double)det_rate_x10000 / 10000.0,
         (double)fpr_x10000 / 10000.0,
         (unsigned)cpu_pct);
}

void
ids_campaign_log_attack(const char *scenario, uint32_t event_id, uint32_t t_start,
                        uint32_t t_end)
{
   printf("METRIC,ATTACK,%u,%s,%u,%u,%u\n",
          (unsigned)IDS_CAMPAIGN_SEED,
          scenario,
          (unsigned)event_id,
          (unsigned)t_start,
          (unsigned)t_end);
}

#endif /* IDS_CONF_CAMPAIGN_METRICS */
