#ifndef CTX_POLICY_H_
#define CTX_POLICY_H_

#include <stdint.h>

typedef enum {
   IDS_MODE_FULL     = 0,  //  toutes les règles actives
   IDS_MODE_BALANCED = 1,  //  R1+R2+R3, pas wormhole
   IDS_MODE_ECO      = 2   //  seulement R1+R2 (économie d'énergie)
} ids_mode_t;

void ctx_policy_init(void);
ids_mode_t ctx_policy_current(void);
void ctx_policy_tick(uint8_t nre_x100, uint8_t control_load_x10);
uint8_t ctx_policy_rule_mask(void);

#endif
