/*
 * ids_member.c — member-level detection (rules R1 to R4).
 * Each rule has its own EWMA to avoid false positives on
 *   normal network fluctuations.
 * TODO: make EWMA threshold (+15) configurable via project-conf?
 *   (currently hardcoded; works well in simulation)
 */

#include "ids_member.h"
#include "ids_conf.h"
#include "ids_attack.h"

static uint8_t las;
static uint8_t alarm;
static uint8_t ewma[4];

static uint32_t tp_m, fp_m, tn_m, fn_m;

void
ids_member_init(void)
{
   las = 0;
   alarm = 0;
   ewma[0] = ewma[1] = ewma[2] = ewma[3] = 0;
   tp_m = fp_m = tn_m = fn_m = 0;
}

void
ids_member_tick(uint8_t traffic_class, uint8_t nre_x100, uint8_t rule_mask)
{
   uint8_t raw[4] = {0, 0, 0, 0};
   uint8_t det[4] = {0, 0, 0, 0};
   uint8_t i;

   if(rule_mask & 0x01) {
      raw[0] = ids_attack_rank_signal();
   }
  if(rule_mask & 0x02) {
       raw[1] = ids_attack_sel_fwd_signal(traffic_class);
  }
   if(rule_mask & 0x04) {
      raw[2] = ids_attack_dao_flood_signal();
   }
  if(rule_mask & 0x08) {
     raw[3] = ids_attack_wormhole_signal();
   }

   //  Per-rule EWMA — rolling baseline
   //  Smooth raw signal against history instead of using raw values directly.
   //  If raw exceeds ewma+15, the value is flagged as suspicious.
    //  (15 is a heuristic; should be derived from observed variance)
    for(i = 0; i < 4; i++) {
      ewma[i] = (uint8_t)(((uint16_t)ewma[i] * 7u + (uint16_t)raw[i]) / 8u);
      if(raw[i] > ewma[i] + 15) {
        det[i] = raw[i];
      }
   }

   //  LAS = R1×3 + R2×2 + R3 + R4, divided by 4.
   //  Weights reflect the perceived severity of each attack type.
   //  Should be validated against campaign data.
   las = (uint8_t)((det[0] * 3u + det[1] * 2u + det[2] + det[3]) / 4u);
   if(nre_x100 < 20) {
      las = las / 2;  //  energy-scaling: halve LAS when node is depleted
   }
   alarm = las > IDS_THRESHOLD_LAS ? 1 : 0;

   if(alarm && ids_attack_is_active()) {
      tp_m++;
   } else if(alarm && !ids_attack_is_active()) {
      fp_m++;
   } else if(!alarm && ids_attack_is_active()) {
      fn_m++;
   } else {
      tn_m++;
   }
}

void
ids_member_get_confusion(uint32_t *tp, uint32_t *fp, uint32_t *tn, uint32_t *fn)
{
  if(tp) *tp = tp_m;
  if(fp) *fp = fp_m;
  if(tn) *tn = tn_m;
  if(fn) *fn = fn_m;
    //  NOTE: NULL pointers are handled safely; callers should always pass valid pointers
}

uint8_t
ids_member_las(void)
{
   return las;
}

uint8_t
ids_member_alarm(void)
{
   return alarm;
}
