#include "main.h" // HAL_driver GPIO 정보가 들어 있다

#define GPIOB_ODR 0x040020414

void led_all_on(void);
void led_all_off(void);
void led_main(void);

void shift_left_ledon(void);
void shift_right_ledon(void);
void shift_left_keep_ledon(void);
void shift_right_keep_ledon(void);
void flower_on(void);
void flower_off(void);


