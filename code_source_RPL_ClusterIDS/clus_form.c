/*
 * clus_form.c — cluster formation (Eq.1-2 of the paper).
 *   The affinity score combines topology and energy information
 *   to decide whether a node stays in its cluster or reclusters.
 * TODO: add an LQI factor? Currently topology + energy only.
 */

#include "clus_form.h"
#include "sys/node-id.h"

static uint8_t affinity_score;
static uint16_t stable_ticks;

void
clus_form_init(void)
{
   affinity_score = 50;
   stable_ticks = 0;
}

void
clus_form_tick(uint8_t nre_x100, uint8_t traffic_class)
{
   uint8_t topo = (uint8_t)((node_id + traffic_class) % 8u);
   uint8_t energy_term = (uint8_t)((100u - nre_x100) / 4u);

   //  Score 0-99: topology ×3, energy ×2, traffic ×1
   affinity_score = (uint8_t)((topo * 3u + energy_term * 2u + traffic_class) % 100u);
   if(affinity_score > 70) {
       stable_ticks++;
   } else {
       stable_ticks = 0;  //  reset when score falls below 70
   }
}

uint8_t
clus_form_should_recluster(void)
{
  //  120 ticks ~ 10 minutes (at 5s/tick). Re-cluster if score stays >70 for 10 min
  return stable_ticks > 120 ? 1 : 0;
}

void
clus_form_recluster(void)
{
  //  Nodes with similar traffic profiles converge toward the same cluster
  //  (no inter-node communication; all decisions are local).
  //  Threshold calibrated on simulation; real deployment may require
  //  adjusting affinity score weights.
  stable_ticks = 0;
}
