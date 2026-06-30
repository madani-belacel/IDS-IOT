/*
 * ch_elect.c — Cluster-Head election and rotation (Eq.3 of the paper).
 *   The CH is elected based on fitness (energy + link quality). Rotation
 *   occurs after N ticks of stability.
 * TODO: test with >64 nodes; modulo 8 may lock some nodes out.
 */

#include "ch_elect.h"
#include "clus_form.h"
#include "ids_conf.h"
#include "sys/node-id.h"

static uint8_t is_head;
static uint32_t head_tenure_s;
static uint16_t rotation_counter;
static uint16_t recluster_events;
static uint16_t my_fitness;

void
ch_elect_init(void)
{
#if IDS_ABLATION_NOCLUS
  is_head = 1;
#else
  //  1 CH per 8 nodes on average — uniform distribution
  is_head = (node_id % 8u) == 0 ? 1 : 0;
#endif
  head_tenure_s = 0;
  rotation_counter = 0;
  recluster_events = 0;
  my_fitness = 0;
}

void
ch_elect_tick(uint8_t nre_x100, uint8_t etx_var_x10)
{
#if !IDS_ABLATION_NOCLUS
  //  Fitness = energy ×2 + link quality ×5 (inverted)
  //  Recalculated each tick; lightweight enough for periodic execution
  uint32_t fitness = (uint32_t)nre_x100 * 2u + (uint32_t)(100u - etx_var_x10 * 5u);
  my_fitness = (uint16_t)fitness;

  if(is_head) {
     head_tenure_s++;
     rotation_counter++;
  } else if(fitness > 180) {
     rotation_counter++;
  }
  if(clus_form_should_recluster() && rotation_counter > 10) {
     clus_form_recluster();
     ch_elect_rotate();
  }
#endif
}

uint8_t
ch_elect_is_head(void)
{
#if IDS_ABLATION_NOCLUS
  return 1;
#else
  return is_head;
#endif
}

void
ch_elect_rotate(void)
{
  //  CH rotation based on fitness.
  //  Each node compares its fitness to a threshold dependent on slot
  //  (node_id % 8) and group (node_id / 8).
  //  This heuristic replaces a full DHT-based election; adequate for
  //  simulation-scale evaluation. Thresholds should be validated on
  //  real hardware.
  uint16_t threshold = 140 + (uint16_t)(node_id % 8u) * 12
                      + (uint16_t)(node_id / 8u) * 4;
  is_head = my_fitness > threshold ? 1 : 0;
   rotation_counter = 0;
   head_tenure_s = 0;
   recluster_events++;
}

uint32_t
ch_elect_tenure_s(void)
{
    return head_tenure_s;
}

uint16_t
ch_elect_recluster_events(void)
{
    return recluster_events;
}
