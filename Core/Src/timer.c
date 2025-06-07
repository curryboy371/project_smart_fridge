#include "stm32f4xx_hal.h"  // HAL 함수 직접 참조
#include "main.h"
#include "timer.h"

extern TIM_HandleTypeDef htim2;

// 1MHz 타이머(TIM2) 기반 딜레이 함수
void delay_us(int us)
{
    __HAL_TIM_SET_COUNTER(&htim2, 0);
    while (__HAL_TIM_GET_COUNTER(&htim2) < us)
        ;  // 지정 시간까지 대기
}
