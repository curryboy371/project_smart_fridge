#ifndef DHT11_H_
#define DHT11_H_

#include <stdint.h>

extern volatile uint8_t dht11_data[5];

void dht11_init(void);
void dht11_read(void);

#endif /* DHT11_H_ */
