#ifndef IDS_MEMBER_H_
#define IDS_MEMBER_H_

#include <stdint.h>

void ids_member_init(void);
void ids_member_tick(uint8_t traffic_class, uint8_t nre_x100, uint8_t rule_mask);
uint8_t ids_member_las(void);
uint8_t ids_member_alarm(void);
void ids_member_get_confusion(uint32_t *tp, uint32_t *fp, uint32_t *tn, uint32_t *fn);

#endif
