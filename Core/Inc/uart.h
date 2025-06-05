#include "main.h"

#define COMMAND_NUMBER 20
#define COMMAND_LENGTH 40

volatile uint8_t rx_buff[COMMAND_NUMBER][COMMAND_LENGTH];	//uart0로부터 들어온 문자를 저장하는 버퍼(변수)
volatile int rear = 0;										// input index; USART0_RX_vect에서 집어 넣어주는 int
volatile int front = 0;

