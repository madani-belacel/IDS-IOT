/*
 * ids_ch.c — détection au niveau CH : confirmation et matrice de confusion.
 *   Le CH reçoit le LAS et l'alarme du membre, et si les deux dépassent
 *   le seuil, il confirme l'attaque.  Sinon c'est un faux positif.
 * TODO: ajouter un timeout de confirmation ?  Là on confirme immédiatement,
 *   c'est peut-être trop rapide (d'où les FP sur certaines attaques).
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
    //  Alarme membre + LAS élevé → on confirme (ou FP si pas d'attaque)
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
