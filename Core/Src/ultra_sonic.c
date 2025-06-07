#include "ultra_sonic.h"
#include "main.h"

#define FILTER_SIZE 5
static float buffer[FILTER_SIZE]={0};
static int index=0;
extern volatile float distance;
extern TIM_HandleTypeDef htim3;

void ultra_sonic_init(void)
{
    HAL_TIM_IC_Start_IT(&htim3, TIM_CHANNEL_2);
}

void ultra_sonic_trigger(void)
{
    HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_SET);
    delay_us(10);
    HAL_GPIO_WritePin(TRIG_GPIO_Port, TRIG_Pin, GPIO_PIN_RESET);
}

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    static uint32_t ic_rising = 0, ic_falling = 0;
    if(htim->Instance == TIM3 && htim->Channel == HAL_TIM_ACTIVE_CHANNEL_2)
    {
        if(HAL_GPIO_ReadPin(ECHO_GPIO_Port, ECHO_Pin) == GPIO_PIN_SET)
            ic_rising = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_2);
        else
        {
            ic_falling = HAL_TIM_ReadCapturedValue(htim, TIM_CHANNEL_2);
            uint32_t pulse = (ic_falling >= ic_rising) ? (ic_falling - ic_rising) : (htim->Instance->ARR - ic_rising + ic_falling + 1);
            float d = (pulse * 0.0343f) / 2.0f;

            // 평균화 버퍼
            buffer[index++] = d;
            if(index >= FILTER_SIZE) index = 0;

            float sum = 0;
            for(int i=0; i<FILTER_SIZE; i++) sum += buffer[i];
            distance = sum / FILTER_SIZE;
        }
    }
}
