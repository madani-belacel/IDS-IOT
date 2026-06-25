#ifndef CH_ELECT_H_
#define CH_ELECT_H_

#include <stdint.h>

void ch_elect_init(void);
void ch_elect_tick(uint8_t nre_x100, uint8_t etx_var_x10);
uint8_t ch_elect_is_head(void);
void ch_elect_rotate(void);
uint32_t ch_elect_tenure_s(void);
uint16_t ch_elect_recluster_events(void);

#endif
