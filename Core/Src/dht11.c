#include "dht11.h"
#include "main.h"

#define DHT11_PIN GPIO_PIN_0
#define DHT11_PORT GPIOA

volatile uint8_t dht11_data[5] = {0};

void dht11_init(void)
{
    GPIOA->MODER |= (0x01 << (0 * 2));
    HAL_GPIO_WritePin(DHT11_PORT, DHT11_PIN, GPIO_PIN_SET);
}

static void start_signal(void)
{
    GPIOA->MODER |= (0x01 << (0 * 2));
    HAL_GPIO_WritePin(DHT11_PORT, DHT11_PIN, GPIO_PIN_RESET);
    delay_us(20000);
    HAL_GPIO_WritePin(DHT11_PORT, DHT11_PIN, GPIO_PIN_SET);
    GPIOA->MODER &= ~(0x3 << (0 * 2));
    delay_us(30);
}

static uint8_t check_response(void)
{
    int us=0;
    while(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && us++<100) delay_us(1);
    if(us>=100) return 0;
    us=0;
    while(!HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && us++<100) delay_us(1);
    if(us>=100) return 0;
    return 1;
}

static void receive_data(uint8_t data[5])
{
    int us=0;
    for(int i=0;i<40;i++)
    {
        us=0; while(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && us++<100) delay_us(1);
        us=0; while(!HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && us++<100) delay_us(1);
        delay_us(30);
        if(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN)) data[i/8] |= (1<<(7-(i%8)));
        us=0; while(HAL_GPIO_ReadPin(DHT11_PORT, DHT11_PIN) && us++<100) delay_us(1);
    }
}

static uint8_t checksum_valid(uint8_t data[5])
{
    return data[4] == (data[0]+data[1]+data[2]+data[3]);
}

void dht11_read(void)
{
    uint8_t data[5] = {0};
    start_signal();
    if(!check_response()) return;
    receive_data(data);
    if(checksum_valid(data)) for(int i=0;i<5;i++) dht11_data[i]=data[i];
}
