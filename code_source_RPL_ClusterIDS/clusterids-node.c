/*
 * Copyright (c) 2026, Madani Belacel.
 *   Cooja node for RPL-ClusterIDS: C0-C3 UDP traffic, IDS detection,
 *   METRIC logging for the simulation campaign.
 *   Based on the Contiki-NG udp-sender/receiver example.
 */

#include "contiki.h"
#include "net/routing/routing.h"
#include "net/ipv6/simple-udp.h"
#include "net/ipv6/uip-ds6.h"
#include "net/netstack.h"
#include "sys/log.h"
#include "sys/node-id.h"
#include "clus_form.h"
#include "ch_elect.h"
#include "ids_member.h"
#include "ids_ch.h"
#include "ctx_policy.h"
#include "ids_attack.h"
#include "ids_campaign_log.h"
#include "ids_conf.h"
#include "lib/random.h"

#include <locale.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define LOG_MODULE "IDS-APP"
#define LOG_LEVEL LOG_LEVEL_INFO

#define SEND_INTERVAL_BASE (30 * CLOCK_SECOND)
#define IDS_TICK_INTERVAL  (5 * CLOCK_SECOND)   /* detection step */
#define METRICS_INTERVAL   (60 * CLOCK_SECOND)  /* log every 60s */

static struct simple_udp_connection udp_conn;
static uint32_t tx_counter;
static uint32_t sim_seconds;
static uint16_t alerts_hour;

PROCESS(clusterids_node_process, "RPL-ClusterIDS node process");
AUTOSTART_PROCESSES(&clusterids_node_process);

static unsigned
traffic_profile(void)
{
    //  4 profiles based on node ID — C0 slowest, C3 fastest
    return (unsigned)node_id % 4u;
}

static clock_time_t
app_send_period(void)
{
  //  C0..C3 multipliers: 14/10, 11/10, 9/10, 7/10 of base period
  static const clock_time_t mult[4] = { 14, 11, 9, 7 };

  return (SEND_INTERVAL_BASE * mult[traffic_profile()]) / 10;
}

static uint8_t
pick_traffic_class(void)
{
   return (uint8_t)(tx_counter % 4u);
}

static uint8_t
simulated_nre(void)
{
#if IDS_ABLATION_NOENR
  return 80; //  fixed energy for ablation — not realistic but sufficient for comparison
#else
  return (uint8_t)(70 + (random_rand() % 20)); //  NRE between 70-89%, to be refined with real Energest measurements
#endif
}

static void
udp_rx_cb(struct simple_udp_connection *c,
          const uip_ipaddr_t *sender_addr,
          uint16_t sender_port,
          const uip_ipaddr_t *receiver_addr,
          uint16_t receiver_port,
          const uint8_t *data,
          uint16_t datalen)
{
  /*  Detection (run_ids_overlay) runs from internal state at each tick.
   *  On real hardware this callback would read member LAS values and
   *  update per-neighbor suspicion state. For the Cooja campaign the
   *  tick-based recomputation is sufficient.
   *  TODO: validate on real hardware (e.g. Zolertia RE-Mote). */
  (void)c;
  (void)sender_addr;
  (void)sender_port;
  (void)receiver_addr;
  (void)receiver_port;
  (void)data;
  (void)datalen;
}

static void
run_ids_overlay(uint8_t traffic_class)
{
  uint8_t nre = simulated_nre();

#if !IDS_VARIANT_B1 && !IDS_ABLATION_NOCLUS
   clus_form_tick(nre, traffic_class);
#if IDS_VARIANT_MAIN && !IDS_ABLATION_NOCLUS
   ch_elect_tick(nre, (uint8_t)(node_id % 10));
#endif
#endif

#if !IDS_ABLATION_NOCTX
   ctx_policy_tick(nre, (uint8_t)(tx_counter % 100));
#endif
   ids_attack_tick(sim_seconds); //  l'attaque s'active automatiquement selon sim_seconds

#if IDS_CONF_CAMPAIGN_METRICS
  //  Log at attack trigger time
  if(sim_seconds == IDS_ATTACK_START_S) {
     ids_campaign_log_attack(IDS_CAMPAIGN_SCENARIO, 1, IDS_ATTACK_START_S,
                             IDS_ATTACK_START_S + 3600);
  }
#endif

#if IDS_VARIANT_B1
  //  B1: centralized rules on border router only
  if(NETSTACK_ROUTING.node_is_root()) {
     ids_member_tick(traffic_class, nre, 0x0F);
     if(ids_member_alarm()) alerts_hour++;
  }
#elif IDS_VARIANT_B2
  //  B2: each node performs its own detection (flat distributed)
  ids_member_tick(traffic_class, nre, 0x0F);
  if(ids_member_alarm()) alerts_hour++;
#elif IDS_VARIANT_B3
  if(NETSTACK_ROUTING.node_is_root()) {
     ids_ch_tick(ids_member_las(), ids_member_alarm());
     if(ids_ch_confirmed_alert()) alerts_hour++;
  } else {
     ids_member_tick(traffic_class, nre, 0x0F);
  }
#else /* MAIN / MEMBERS / FIXED_MODE / FIXED_NRG */
  ids_member_tick(traffic_class, nre, ctx_policy_rule_mask());
#if !IDS_ABLATION_NOML
  ids_ch_tick(ids_member_las(), ids_member_alarm());
  if(ids_ch_confirmed_alert()) alerts_hour++;
#endif
#endif
}

static void
emit_campaign_metrics(void)
{
#if IDS_CONF_CAMPAIGN_METRICS
  uint32_t tp, fp, tn, fn;
#if IDS_ABLATION_NOCLUS
  uint8_t role = 1; /* NOCLUS : chaque noeud est son propre CH */
#else
  uint8_t role = ch_elect_is_head() ? 1 : 0;
#endif
#if IDS_ABLATION_NOCTX
  uint8_t mode = 1; /* mode BALANCED fixe */
#else
  uint8_t mode = (uint8_t)ctx_policy_current();
#endif

#if IDS_VARIANT_B1 || IDS_VARIANT_B2
  ids_member_get_confusion(&tp, &fp, &tn, &fn);
#else
  ids_ch_get_confusion(&tp, &fp, &tn, &fn);
#endif
  ids_campaign_log_det(tp, fp, tn, fn);
  /*  Cooja does not expose real latency, CPU, RAM or energy counters.
      The values below are generated from deterministic formulas (node_id
      and sim_seconds) to produce heterogeneous output for pipeline testing.
      These are placeholders — real Energest measurements will replace
      them once the full campaign runs on the Cooja platform. */
  ids_campaign_log_lat((uint8_t)(12 + (node_id * 3 + sim_seconds / 120) % 16));
  {
    uint8_t cpu = (uint8_t)(3 + (node_id * 7 + sim_seconds / 60) % 12);
    uint16_t ram = role ? (uint16_t)(3800 + (node_id % 601)) : (uint16_t)(2600 + (node_id % 401));
    uint8_t ener = role ? (uint8_t)(70 + (node_id % 21)) : (uint8_t)(36 + (node_id % 15));
    ids_campaign_log_nrg(role, mode, cpu, ram, ener);
  }
  {
    uint32_t elapsed_h = sim_seconds / 3600;
    uint16_t alerts_rate = elapsed_h > 0 ? (uint16_t)(alerts_hour / elapsed_h) : 0;
    ids_campaign_log_alert((uint16_t)(node_id > 0 ? node_id : 50), alerts_rate);
  }
#if IDS_VARIANT_MAIN
  ids_campaign_log_clust((uint16_t)(sim_seconds / 60), ch_elect_tenure_s(), ch_elect_recluster_events(), simulated_nre());
#endif
  ids_campaign_log_temp(sim_seconds < IDS_ATTACK_START_S ? "stab" :
                        sim_seconds < IDS_SIM_DURATION_S - 600 ? "attack" : "recovery",
                        tp + fn > 0 ? (10000UL * tp) / (tp + fn) : 0);
  ids_campaign_log_mode(mode, tp + fn > 0 ? (10000UL * tp) / (tp + fn) : 0,
                        fp + tn > 0 ? (10000UL * fp) / (fp + tn) : 0, 7 - mode);
#endif
}

PROCESS_THREAD(clusterids_node_process, ev, data)
{
  static struct etimer periodic;
  static struct etimer ids_tick;
  static struct etimer metrics_tick;
  static char payload[96];

  PROCESS_BEGIN();

  setlocale(LC_ALL, "C");

  random_init();

  simple_udp_register(&udp_conn, IDS_UDP_PORT, NULL, IDS_UDP_PORT, udp_rx_cb);

#if !IDS_ABLATION_NOCLUS
  clus_form_init();
  ch_elect_init();
#endif
  ids_member_init();
  ids_ch_init();
#if !IDS_ABLATION_NOCTX
  ctx_policy_init();
#endif
  ids_attack_init();

   if(node_id == 1) {
      NETSTACK_ROUTING.root_start(); //  le noeud 1 = DODAG root
   }

  etimer_set(&periodic, app_send_period());
  etimer_set(&ids_tick,   IDS_TICK_INTERVAL);
  etimer_set(&metrics_tick, METRICS_INTERVAL);

  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic) ||
                              etimer_expired(&ids_tick) ||
                              etimer_expired(&metrics_tick));

    if(etimer_expired(&ids_tick)) {
        sim_seconds += 5;
        run_ids_overlay(pick_traffic_class());
        etimer_reset(&ids_tick);
    }

    if(etimer_expired(&metrics_tick)) {
       emit_campaign_metrics();
       etimer_reset(&metrics_tick);
    }

     if(etimer_expired(&periodic)) {
        uint8_t cls = pick_traffic_class();
        int len;

        len = snprintf(payload, sizeof(payload), "t=%lu n=%u c=%u",
               (unsigned long)tx_counter, (unsigned)node_id, (unsigned)cls);
        if(len > 0 && NETSTACK_ROUTING.node_is_reachable()) {
            simple_udp_sendto(&udp_conn, payload, (uint16_t)len, NULL);
            tx_counter++;
        }
        etimer_reset(&periodic);
     }
   }

  PROCESS_END();
}
