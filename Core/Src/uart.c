#include "uart.h"
#include "string.h"
#include "led.h"
#include <stdio.h>

/*

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
	volatile static int i=0;

	if(huart == &huart2) // 2번 uart에서 왔는지 확인
	{
		if (rx_data == '\n')
			{
				rx_buff[rear++][i] = '\0';
				rear %= COMMAND_NUMBER;
				i = 0;
				// 다음 string을 저장하기 위한 1차원 index값을 0으로
				// rx_buff queue full ckeck

			}
			else
			{
				rx_buff[rear][i++] = rx_data;	// 다음 공간 가르킨다
			}
		  	  HAL_UART_Receive_IT(&huart2, &rx_data, 1); //반드시 집어 넣어야 다음 INT 발생

	}
}


void show_command(void)
{
	char *cmd[] =
	{
			"\nsetrtc",
			"print_rtc",
			"printoff_rtc",
			"help"
	};

	for(int i = 0; i < 4 ; i++)
	{
		printf("%s\n", cmd[i]);
	}
}

void pc_command_processing(void)
{
	// 큐에 데이터가 있을 경우 처리
	if (front != rear)
	{
		printf("Received: %s\n", rx_buff[front]); // 수신된 명령어 출력


		if (strncmp((const char *)rx_buff[front], (const char *) "led_all_on", strlen("led_all_on")) == 0)
		{
			printf("find : time set");
			led_all_on();
		}
		else if (strncmp((const char *)rx_buff[front], (const char *) "setrtc", strlen("setrtc")) == 0)
		{
			set_rtc((char *)&rx_buff[front][6]);
		}
		else if (strncmp((const char *)rx_buff[front], (const char *) "help", strlen("help")) == 0)
		{
			show_command();
		}
		else if (strncmp((const char *)rx_buff[front], (const char *) "print_rtc", strlen("print_rtc")) == 0)
		{
			o_prt.p_rtc = 1;
			printf("print_rtc : %d\n", o_prt.p_rtc);
		}
		else if (strncmp((const char *)rx_buff[front], (const char *) "printoff_rtc", strlen("printoff_rtc")) == 0)
		{
			o_prt.p_rtc = 0;
			printf("print_rtc : %d\n", o_prt.p_rtc);
		}

		// front 업데이트 (순환 큐 처리)
		front++;
		front %= COMMAND_NUMBER;
	}
}

*/
