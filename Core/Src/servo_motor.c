#include "servo_motor.h"
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
    else compare_value = 40 + (angle * (130 - 40)) / 180;

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
            servo_motor_set_angle(90);
            state = 1;
        }
    }
    else
    {
        lost_timer += 100;
        detect_timer = 0;
        if(lost_timer >= 2000 && state == 1)
        {
            servo_motor_set_angle(0);
            state = 0;
        }
    }
}
