#include "servo_motor.h"
#include "uart.h"
#include "main.h"

extern volatile float distance;

extern TIM_HandleTypeDef htim5;

static int state = 0;
static uint32_t detect_timer = 0, lost_timer = 0;

void servo_motor_init(void)
{
    HAL_TIM_PWM_Start(&htim5, TIM_CHANNEL_2);
}

void servo_motor_set_angle(uint8_t angle)
{
//    uint32_t pulse = ((angle * 10) / 180) + 5;
//    __HAL_TIM_SET_COMPARE(&htim5, TIM_CHANNEL_2, pulse);
//
    int compare_value;
    if(angle <= 0) compare_value = 40;
    else if(angle >= 180) compare_value = 130;
<<<<<<< HEAD
    //else compare_value = 40 + (angle * (130 - 40)) / 180;
    else compare_value = 40 + (angle * 90) / 180; // (130 - 40) = 90
=======
    else compare_value = 40 + (angle * (130 - 40)) / 180;

>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
    __HAL_TIM_SET_COMPARE(&htim5, TIM_CHANNEL_2, compare_value);
}

// 모터 제어 함수
void servo_motor_update(void)
{
    if(distance > 0 && distance <= 7.0f)
    {
        detect_timer += 100;
        lost_timer = 0;
        if(detect_timer >= 2000 && state == 0)
        {
<<<<<<< HEAD
            servo_motor_set_angle(150);
=======
            servo_motor_set_angle(110);
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
            state = 1;
        }
    }
    else
    {
        lost_timer += 100;
        detect_timer = 0;
        if(lost_timer >= 2000 && state == 1)
        {
        	// evnet
        	set_event(1);
<<<<<<< HEAD
            servo_motor_set_angle(60);
=======
            servo_motor_set_angle(30);
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
            state = 0;
        }
    }
}
