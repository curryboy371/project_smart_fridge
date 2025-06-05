#ifndef ULTRA_SONIC_H_
#define ULTRA_SONIC_H_

#include <stdint.h>

extern volatile float distance;

void ultra_sonic_init(void);
void ultra_sonic_trigger(void);

#endif /* ULTRA_SONIC_H_ */
