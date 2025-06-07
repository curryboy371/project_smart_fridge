#ifndef SERVO_MOTOR_H_
#define SERVO_MOTOR_H_

#include <stdint.h>

void servo_motor_init(void);
void servo_motor_set_angle(uint8_t angle);
void servo_motor_update(void);

#endif /* SERVO_MOTOR_H_ */
