/*
 * ids_attack.c — générateurs de signaux d'attaque pour Cooja.
 *   Chaque fonction produit le signal qu'un noeud malveillant
 *   injecterait dans le réseau (valeurs calibrées pour dépasser
 *   le seuil EWMA en période d'attaque mais pas en normal).
 *   C'est du fake bien sûr — sur une vraie plateforme ces signaux
 *   viendraient du trafic réseau observé.
 * FIXME: wormhole 25% de chance de rien émettre — à valider côté stats
 */

#include "ids_attack.h"
#include "ids_conf.h"
#include "sys/node-id.h"
#include "lib/random.h"

static uint8_t active;
static uint8_t is_attacker;

void
ids_attack_init(void)
{
   active = 0;
   //  10% des noeuds sont malveillants — à ajuster selon le scénario
   is_attacker = (random_rand() % 100) < 10 ? 1 : 0;
}

void
ids_attack_tick(uint32_t sim_s)
{
  if(sim_s >= IDS_ATTACK_START_S && is_attacker) {
     active = 1;
  }
}

uint8_t
ids_attack_is_active(void)
{
   return active && is_attacker;
}

uint8_t
ids_attack_rank_signal(void)
{
  if(!active || !is_attacker) {
     return 0;
  }
  return (uint8_t)(75 + (random_rand() % 11));  //  signal entre 75 et 85
}

uint8_t
ids_attack_sel_fwd_signal(uint8_t traffic_class)
{
  if(!active || !is_attacker) {
     return 0;
  }
  //  L'attaque selective forwarding est plus agressive sur C3
  return traffic_class >= 3 ? (uint8_t)(65 + (random_rand() % 11))
                            : (uint8_t)(35 + (random_rand() % 11));
}

uint8_t
ids_attack_dao_flood_signal(void)
{
  if(!active || !is_attacker) {
     return 0;
  }
  return (uint8_t)(60 + (random_rand() % 11));  //  signal stable 60-70
}

uint8_t
ids_attack_wormhole_signal(void)
{
  //  25% de chance de ne rien émettre — pour simuler l'intermittence
  if(!active || !is_attacker || (random_rand() % 4u) == 0) {
     return 0;
  }
  return (uint8_t)(70 + (random_rand() % 11));
}
