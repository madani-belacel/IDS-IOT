/*
 * ids_member.c — détection au niveau membre (règles R1 à R4).
 * Chaque règle a son propre EWMA pour éviter les faux positifs
 *   sur les fluctuations normales du réseau.
 * TODO: rendre le seuil EWMA (+15) configurable depuis project-conf ?
 *   (là c'est en dur, ce seuil marche bien en simu mais bon...)
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

   //  EWMA par règle — rolling baseline
   //  Au lieu de balancer le raw signal direct, on lisse avec l'historique.
   //  Si raw dépasse ewma+15, on le considère comme suspect.
   //  (15, c'est un peu arbitraire, faudrait le calculer à partir de la variance)
   for(i = 0; i < 4; i++) {
      ewma[i] = (uint8_t)(((uint16_t)ewma[i] * 7u + (uint16_t)raw[i]) / 8u);
      if(raw[i] > ewma[i] + 15) {
        det[i] = raw[i];
      }
   }

   //  LAS = R1×3 + R2×2 + R3 + R4, le tout /4.
   //  Les poids reflètent la sévérité perçue de chaque attaque.
   //  À vérifier si ça correspond aux données de campagne.
   las = (uint8_t)((det[0] * 3u + det[1] * 2u + det[2] + det[3]) / 4u);
   if(nre_x100 < 20) {
      las = las / 2;  //  si le noeud est à court d'énergie, on divise le LAS par 2
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
   //  NOTE: les pointeurs NULL sont gérés, mais normalement on passe toujours des bons
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
