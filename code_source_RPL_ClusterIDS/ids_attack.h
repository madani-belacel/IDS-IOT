#ifndef IDS_ATTACK_H_
#define IDS_ATTACK_H_

#include <stdint.h>

void ids_attack_init(void);
void ids_attack_tick(uint32_t sim_s);
uint8_t ids_attack_is_active(void);
uint8_t ids_attack_rank_signal(void);
uint8_t ids_attack_sel_fwd_signal(uint8_t traffic_class);
uint8_t ids_attack_dao_flood_signal(void);
uint8_t ids_attack_wormhole_signal(void);

#endif
