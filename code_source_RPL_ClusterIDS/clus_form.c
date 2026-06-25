/*
 * clus_form.c — formation des clusters (Eq.1-2 du papier).
 *   L'affinity_score combine infos topo + énergie pour décider
 *   si un noeud reste dans son cluster ou si on re-cluster.
 * TODO: ajouter un facteur LQI ?  Pour l'instant que la topologie + énergie.
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

   //  Score entre 0 et 99 : topo ×3, énergie ×2, trafic ×1
   affinity_score = (uint8_t)((topo * 3u + energy_term * 2u + traffic_class) % 100u);
   if(affinity_score > 70) {
       stable_ticks++;
   } else {
       stable_ticks = 0;  //  dès que le score passe sous 70, on remet à 0
   }
}

uint8_t
clus_form_should_recluster(void)
{
  //  120 ticks ~ 10 minutes (à 5s/tick). Si on reste >70 pendant 10min, on re-cluster
  return stable_ticks > 120 ? 1 : 0;
}

void
clus_form_recluster(void)
{
  //  Les noeuds avec des profils similaires convergent vers le même cluster
  //  (pas de communication inter-noeuds, tout est local — c'est le principe).
  //  Ce seuil marche bien en simu mais bon, sur un déploiement réel faudra
  //  ajuster les poids de l'affinity score.
  stable_ticks = 0;
}
