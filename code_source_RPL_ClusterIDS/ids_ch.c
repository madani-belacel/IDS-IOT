/*
 * ids_ch.c — CH-level detection: confirmation and confusion matrix.
 *   The CH receives the member LAS and alarm; if both exceed the
 *   threshold, the attack is confirmed. Otherwise it is a false positive.
 * TODO: add a confirmation timeout? Current immediate confirmation may
 *   be too fast (causing FPs on certain attacks).
 */

#include "ids_ch.h"
#include "ids_attack.h"
#include "ch_elect.h"
#include "ids_conf.h"

static uint8_t confirmed;
static uint32_t tp, fp, tn, fn;

void
ids_ch_init(void)
{
  confirmed = 0;
  tp = fp = tn = fn = 0;
}

void
ids_ch_tick(uint8_t member_las, uint8_t member_alarm)
{
  uint8_t attack_active = ids_attack_is_active();

#if !IDS_VARIANT_B3
  if(!ch_elect_is_head()) {
     return; /* seuls les CH font la confirmation */
  }
#else
  (void)member_las;
#endif
  confirmed = 0;
  if(member_alarm && member_las > IDS_THRESHOLD_CH) {
    //  Member alarm + high LAS → confirmed (or FP if no attack active)
    if(attack_active) {
       tp++;
       confirmed = 1;
    } else {
       fp++;
    }
  } else if(attack_active) {
     fn++;
  } else {
     tn++;
  }
}

uint8_t
ids_ch_confirmed_alert(void)
{
  return confirmed;
}

void
ids_ch_get_confusion(uint32_t *tp_out, uint32_t *fp_out, uint32_t *tn_out, uint32_t *fn_out)
{
  *tp_out = tp;
  *fp_out = fp;
  *tn_out = tn;
  *fn_out = fn;
}
