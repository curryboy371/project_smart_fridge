#include "led.h"

void led_all_on(void) {
// DMA 버전
#if 1
	//printf("int %d\n", sizeof(int)); //4로 찍히는지 확인
	*(unsigned int*) GPIOB_ODR = 0xff;
#else
//  HAL FUNC 버전
//	HAL_GPIO_WritePin(GPIOB, 0xff, 1);
//	HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0|GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3|GPIO_PIN_4|
//						GPIO_PIN_5|GPIO_PIN_6|GPIO_PIN_7, 1); // GPIO_SET = 1
#endif
}

void led_all_off(void) {
// DMA 버전
#if 1
	//printf("int %d\n", sizeof(int)); //4로 찍히는지 확인
	*(unsigned int*) GPIOB_ODR = 0x00;
#else
// HAL FUNC 버전
// HAL_GPIO_WritePin(GPIOB, 0xff, 0);
// HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0|GPIO_PIN_1|GPIO_PIN_2|GPIO_PIN_3|GPIO_PIN_4|
//							GPIO_PIN_5|GPIO_PIN_6|GPIO_PIN_7, 0);
#endif
}

void shift_left_ledon(void) {
#if 1
	led_all_off();
	for (int i = 0; i < 8; i++) {
		*(unsigned int*) GPIOB_ODR = 0x01 << i;
		HAL_Delay(100);
	}

#else
	led_all_off();
		for(int i = 0 ; i < 8 ; i++)
			{
				uint16_t GPIO_Pin_num[8] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_3, GPIO_PIN_4, GPIO_PIN_5, GPIO_PIN_6, GPIO_PIN_7};

				HAL_GPIO_WritePin(GPIOB, GPIO_Pin_num[i] , 1);
				HAL_GPIO_WritePin(GPIOB, GPIO_Pin_num[i-1] , 0);
				HAL_Delay(100);
			}
#endif
}

void shift_right_ledon(void) {
#if 1
	led_all_off();
	for (int i = 0; i < 8; i++) {
		*(unsigned int*) GPIOB_ODR = 0x80 >> i;
		HAL_Delay(100);
	}
#else
	led_all_off();

		for(int i = 0 ; i < 8 ; i++)
			{
				uint16_t GPIO_Pin_num[8] = {GPIO_PIN_0, GPIO_PIN_1, GPIO_PIN_2, GPIO_PIN_3, GPIO_PIN_4, GPIO_PIN_5, GPIO_PIN_6, GPIO_PIN_7};

				HAL_GPIO_WritePin(GPIOB, GPIO_Pin_num[7-i] , 1);
				HAL_GPIO_WritePin(GPIOB, GPIO_Pin_num[8-i] , 0);
				HAL_Delay(100);
			}
#endif
}

void shift_left_keep_ledon(void) {

#if 1
	led_all_off();
	for (int i = 0; i < 8; i++) {
		*(unsigned int*) GPIOB_ODR |= 0x01 << i;
		HAL_Delay(100);
	}
#else
	led_all_off();

		for(int i = 0 ; i < 8 ; i++)
			{
				HAL_GPIO_WritePin(GPIOB, 0x01 << i , 1);
				HAL_Delay(100);
			}
#endif

}

void shift_right_keep_ledon(void) {
#if 1
	led_all_off();

	for (int i = 0; i < 8; i++) {
		*(unsigned int*) GPIOB_ODR |= 0x80 >> i;
		HAL_Delay(100);
	}
#else
	led_all_off();

	for(int i = 0 ; i < 8 ; i++)
		{
			HAL_GPIO_WritePin(GPIOB, 0x80 >> i , 1);
			HAL_Delay(100);
		}
#endif
}

void flower_on(void) {
#if 1 // 구조체 point member
	for (int i = 0; i < 4; i++) {
		GPIOB->ODR |= 0x08 >> i | 0x10 << i;
		HAL_Delay(100);
	}
	led_all_off();
#endif

#if 0 // DMA
	for(int i = 0 ; i < 4 ; i++)
		{
			* (unsigned int *) GPIOB_ODR |= 0x08 >> i | 0x10 << i;
			// 왜 unsigned를 붙여야 하는가?
			// 마지막이 부호 비트로 들어가니까
			HAL_Delay(100);
		}
	led_all_off();
#endif

#if 0 // HAL_FUNC
	led_all_off();

		for(int i = 0 ; i < 4 ; i++)
			{
				HAL_GPIO_WritePin(GPIOB, 0x08 >> i , 1);
				HAL_GPIO_WritePin(GPIOB, 0x10 << i , 1);
				HAL_Delay(100);
			}
#endif
}

void flower_off(void) {
#if 1
	for (int i = 0; i < 4; i++) {
		*(unsigned int*) GPIOB_ODR &= ~(0x01 << i | 0x80 >> i);
		HAL_Delay(100);
	}
	led_all_on();
#else
	led_all_on();

		for(int i = 0 ; i < 4 ; i++)
			{
				HAL_GPIO_WritePin(GPIOB, 0x01 << i , 0);
				HAL_GPIO_WritePin(GPIOB, 0x80 >> i , 0);
				HAL_Delay(100);
			}
#endif
}

extern SPI_HandleTypeDef hspi2;

void led_main(void) {

	uint8_t led_buff[8] = { 0xFF, 0x0F, 0xF0, 0x00, 0xFF, 0x0F, 0xF0, 0x00 };

	while (1) {
#if 1
		HAL_SPI_Transmit(&hspi2, led_buff, 1, 1);
		GPIOB->ODR &= ~GPIO_PIN_13; // latch핀을 pull-down ODR(Output Data Register)
		GPIOB->ODR |= GPIO_PIN_13;  // latch핀을 pull-up ODR(Output Data Register)
		HAL_Delay(500);
		HAL_SPI_Transmit(&hspi2, &led_buff[3], 1, 1);
		GPIOB->ODR &= ~ GPIO_PIN_13;
		GPIOB->ODR |= GPIO_PIN_13;
		HAL_Delay(500);
#else
		  for (int i=0; i < 4; i++)
		  {
			  HAL_SPI_Transmit(&hspi2, &led_buff[i], 1, 1);
			  GPIOB->ODR &= ~ GPIO_PIN_13;   // latch핀을 pull-down
			  GPIOB->ODR |= GPIO_PIN_13;   //  // latch핀을 pull-up
			  HAL_Delay(1000);
		  }
#endif
	}

//	while(1)
//	{
//		(*GPIOB).ODR |= GPIO_PIN_0; // LED ON
//		HAL_Delay(500);
//		GPIOB->ODR &= ~GPIO_PIN_0;	// LED OFF
//		GPIOB->ODR ^= GPIO_PIN_1;	// LED1 toggle
//
//		HAL_Delay(500);

//		led_all_on();
//		HAL_Delay(100);
//		led_all_off();
//		HAL_Delay(100);
//
//		shift_left_ledon();
//		shift_right_ledon();

//		shift_left_keep_ledon();	//PB
//		shift_right_keep_ledon();
//		flower_on();				//PC
//		flower_off();
//
//		for (int i = 0 ; i < 50 ; i++)
//		{
//			delay_us(1000);
//		}
//		HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
//	}
}
