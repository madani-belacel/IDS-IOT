#ifndef IDS_CH_H_
#define IDS_CH_H_

#include <stdint.h>

void ids_ch_init(void);
void ids_ch_tick(uint8_t member_las, uint8_t member_alarm);
uint8_t ids_ch_confirmed_alert(void);
void ids_ch_get_confusion(uint32_t *tp, uint32_t *fp, uint32_t *tn, uint32_t *fn);

#endif
