/*
 * ch_elect.c — élection du Cluster-Head et rotation (Eq.3 du papier).
 *   Le CH est élu sur sa fitness (énergie + qualité lien).  La rotation
 *   se fait après N ticks de stabilité.
 * TODO: tester avec plus de 64 noeuds, le modulo 8 peut bloquer qqs noeuds.
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
  //  1 CH pour 8 noeuds en moyenne — répartition uniforme
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
  //  Fitness = énergie ×2 + qualité lien ×5 (inversée)
  //  On recalcule ça à chaque tick, c'est pas très lourd donc ça va
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
  //  Rotation du CH basée sur la fitness.
  //  Chaque noeud compare sa fitness à un seuil qui dépend du slot
  //  (node_id % 8) et du groupe (node_id / 8).
  //  C'est un peu artificiel comme mécanisme — il faudrait un vrai
  //  DHT-based election, mais pour la simu ça fait le job.
  //  (à tester sur vrai hardware un jour pour voir si les seuils tiennent)
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
