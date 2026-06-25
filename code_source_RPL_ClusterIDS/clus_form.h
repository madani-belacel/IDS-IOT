#ifndef CLUS_FORM_H_
#define CLUS_FORM_H_

#include <stdint.h>

void     clus_form_init(void);
void     clus_form_tick(uint8_t nre_x100, uint8_t traffic_class);
uint8_t  clus_form_should_recluster(void);
void     clus_form_recluster(void);

#endif
