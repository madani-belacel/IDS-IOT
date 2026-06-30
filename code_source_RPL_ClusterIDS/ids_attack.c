/*
 * ids_attack.c — attack signal generators for Cooja.
 *   Each function produces the signal that a malicious node would
 *   inject into the network. Values are calibrated to exceed the
 *   EWMA threshold during attack periods but not during normal
 *   operation. On real hardware these signals would come from
 *   observed network traffic.
 * FIXME: wormhole has 25% chance of no emission — verify statistics
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
    //  10% of nodes are malicious — adjustable per scenario
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
  //  Selective forwarding is more aggressive on C3 traffic
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
  //  25% chance of silence — to simulate wormhole intermittence
  if(!active || !is_attacker || (random_rand() % 4u) == 0) {
     return 0;
  }
  return (uint8_t)(70 + (random_rand() % 11));
}
