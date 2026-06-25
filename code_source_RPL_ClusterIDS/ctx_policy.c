/*
 * ctx_policy.c — politique contextuelle (Full / Balanced / Eco).
 *   Les seuils (25% NRE, 70% NRE, 80% charge) sont empiriques,
 *   calibrés sur les premières campagnes de simu.
 *   Si on passe sur hardware, faudra sans doute les revoir.
 * TODO: rendre ces seuils configurables depuis project-conf ?
 */

#include "ctx_policy.h"
#include "ids_conf.h"

static ids_mode_t mode;

void
ctx_policy_init(void)
{
   mode = IDS_MODE_BALANCED;  //  on démarre en mode normal
}

ids_mode_t
ctx_policy_current(void)
{
   return mode;
}

void
ctx_policy_tick(uint8_t nre_x100, uint8_t control_load_x10)
{
#if !IDS_ABLATION_NOCTX
  //  Énergie basse (<25%) ou réseau saturé (>80%) → on passe en Eco
  if(nre_x100 < 25 || control_load_x10 > 80) {
     mode = IDS_MODE_ECO;
  } else if(nre_x100 > 70 && control_load_x10 < 40) {
  //  Haute énergie + charge faible → Full (toutes les règles actives)
     mode = IDS_MODE_FULL;
  } else {
     mode = IDS_MODE_BALANCED;
  }
#endif
}

uint8_t
ctx_policy_rule_mask(void)
{
  switch(mode) {
  case IDS_MODE_FULL:
     return 0x0F;   //  R1+R2+R3+R4, toutes les règles
  case IDS_MODE_ECO:
     return 0x03;   //  seulement R1 (rank) + R2 (sel.fwd), pas de wormhole ni dao flood
  default:
     return 0x07;   //  R1+R2+R3, moins gourmand que Full
  }
}
