/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2025 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under BSD 3-Clause license,
 * the "License"; You may not use this file except in compliance with the
 * License. You may obtain a copy of the License at:
 *                        opensource.org/licenses/BSD-3-Clause
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "cmsis_os.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
<<<<<<< HEAD
#include <stdint.h>
#include <string.h>

=======
#include <string.h>
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
#include "ultra_sonic.h"
#include "i2c_lcd.h"
#include "servo_motor.h"
#include "dht11.h"
#include "uart.h"
<<<<<<< HEAD
#include "timer.h"
=======
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */
/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

SPI_HandleTypeDef hspi2;

TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim3;
TIM_HandleTypeDef htim5;
TIM_HandleTypeDef htim11;

UART_HandleTypeDef huart1;
UART_HandleTypeDef huart2;

/* Definitions for defaultTask */
osThreadId_t defaultTaskHandle;
const osThreadAttr_t defaultTask_attributes = {
  .name = "defaultTask",
<<<<<<< HEAD
  .stack_size = 256 * 4,
=======
  .stack_size = 128 * 4,
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  .priority = (osPriority_t) osPriorityNormal,
};
/* Definitions for UART */
osThreadId_t UARTHandle;
const osThreadAttr_t UART_attributes = {
  .name = "UART",
<<<<<<< HEAD
  .stack_size = 256 * 4,
=======
  .stack_size = 128 * 4,
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  .priority = (osPriority_t) osPriorityLow,
};
/* Definitions for ULTRASONIC */
osThreadId_t ULTRASONICHandle;
const osThreadAttr_t ULTRASONIC_attributes = {
  .name = "ULTRASONIC",
<<<<<<< HEAD
  .stack_size = 256 * 4,
=======
  .stack_size = 128 * 4,
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  .priority = (osPriority_t) osPriorityLow,
};
/* Definitions for LCD */
osThreadId_t LCDHandle;
const osThreadAttr_t LCD_attributes = {
  .name = "LCD",
<<<<<<< HEAD
  .stack_size = 256 * 4,
=======
  .stack_size = 128 * 4,
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  .priority = (osPriority_t) osPriorityLow,
};
/* Definitions for SERVO_MOTOR */
osThreadId_t SERVO_MOTORHandle;
const osThreadAttr_t SERVO_MOTOR_attributes = {
  .name = "SERVO_MOTOR",
<<<<<<< HEAD
  .stack_size = 256 * 4,
=======
  .stack_size = 128 * 4,
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  .priority = (osPriority_t) osPriorityLow,
};
/* Definitions for DHT11 */
osThreadId_t DHT11Handle;
const osThreadAttr_t DHT11_attributes = {
  .name = "DHT11",
<<<<<<< HEAD
  .stack_size = 256 * 4,
=======
  .stack_size = 128 * 4,
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  .priority = (osPriority_t) osPriorityLow,
};
/* USER CODE BEGIN PV */
uint8_t rx_data;		//UART2 RX byte
volatile int TIM11_1ms_counter = 0;
volatile int TIM11_sec_counter=0;

// 전역 변수
volatile float distance = 0; // 거리(초음파)
volatile uint8_t temperature_int = 0, temperature_dec = 0; // 온도
volatile uint8_t humidity_int = 0, humidity_dec = 0; // 습도

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_TIM11_Init(void);
static void MX_TIM2_Init(void);
static void MX_I2C1_Init(void);
static void MX_TIM3_Init(void);
static void MX_TIM5_Init(void);
static void MX_SPI2_Init(void);
static void MX_USART1_UART_Init(void);
void StartDefaultTask(void *argument);
void UARTTask(void *argument);
void UltrasonicTask(void *argument);
void LCDTask(void *argument);
void ServoTask(void *argument);
void DHT11Task(void *argument);

/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
#ifdef __GNUC__    // Add for printf
/* With GCC, small printf (option LD Linker->Libraries->Small printf
   set to 'Yes') calls __io_putchar() */
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif /* __GNUC__ */
/**
 * @brief  Retargets the C library printf function to the USART.
 * @param  None
 * @retval None
 */
PUTCHAR_PROTOTYPE   // Add for printf
{
	/* Place your implementation of fputc here */
	/* e.g. write a character to the USART3 and Loop until the end of transmission */
	HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, 0xFFFF);

	return ch;
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
<<<<<<< HEAD
=======

>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_TIM11_Init();
  MX_TIM2_Init();
  MX_I2C1_Init();
  MX_TIM3_Init();
  MX_TIM5_Init();
  MX_SPI2_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
<<<<<<< HEAD
=======

  printf("start\r\n");
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
	HAL_UART_Receive_IT(&huart2, &rx_data, 1);
	HAL_TIM_Base_Start_IT(&htim11);
	HAL_TIM_Base_Start_IT(&htim2);	// for make delay_us


	// RESET MODULES
	//i2c_lcd_init();
	ultra_sonic_init();
	servo_motor_init();
	dht11_init();


	HAL_TIM_IC_Start_IT(&htim3, TIM_CHANNEL_2);
  /* USER CODE END 2 */

  /* Init scheduler */
  osKernelInitialize();

  /* USER CODE BEGIN RTOS_MUTEX */
	//lcdMutexHandle = osMutexNew(&lcdMutex_attributes);
  /* USER CODE END RTOS_MUTEX */

  /* USER CODE BEGIN RTOS_SEMAPHORES */
	/* add semaphores, ... */
  /* USER CODE END RTOS_SEMAPHORES */

  /* USER CODE BEGIN RTOS_TIMERS */
	/* start timers, add new ones, ... */
  /* USER CODE END RTOS_TIMERS */

  /* USER CODE BEGIN RTOS_QUEUES */
	/* add queues, ... */
  /* USER CODE END RTOS_QUEUES */

  /* Create the thread(s) */
  /* creation of defaultTask */
  defaultTaskHandle = osThreadNew(StartDefaultTask, NULL, &defaultTask_attributes);

  /* creation of UART */
  UARTHandle = osThreadNew(UARTTask, NULL, &UART_attributes);

  /* creation of ULTRASONIC */
  ULTRASONICHandle = osThreadNew(UltrasonicTask, NULL, &ULTRASONIC_attributes);

  /* creation of LCD */
  LCDHandle = osThreadNew(LCDTask, NULL, &LCD_attributes);

  /* creation of SERVO_MOTOR */
  SERVO_MOTORHandle = osThreadNew(ServoTask, NULL, &SERVO_MOTOR_attributes);

  /* creation of DHT11 */
  DHT11Handle = osThreadNew(DHT11Task, NULL, &DHT11_attributes);

  /* USER CODE BEGIN RTOS_THREADS */
	/* add threads, ... */
  /* USER CODE END RTOS_THREADS */

  /* USER CODE BEGIN RTOS_EVENTS */
	/* add events, ... */
  /* USER CODE END RTOS_EVENTS */

  /* Start scheduler */
  osKernelStart();

  /* We should never get here as control is now taken by the scheduler */
<<<<<<< HEAD
=======

>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	while (1)
	{
		//ultra_sonic_task_handler();
		//HAL_Delay(500);
		//siren(3);
		//button_led_toggle_test();

		//HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
		//HAL_Delay(500);
		//	  HAL_GPIO_WritePin(GPIOB, 0xff, 1);
		//	  HAL_Delay(500);
		//	  HAL_GPIO_WritePin(GPIOB, 0xff, 0);
		//	  HAL_Delay(500);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	}
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
<<<<<<< HEAD
=======

>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
<<<<<<< HEAD
=======

>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief SPI2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_SPI2_Init(void)
{

  /* USER CODE BEGIN SPI2_Init 0 */

  /* USER CODE END SPI2_Init 0 */

  /* USER CODE BEGIN SPI2_Init 1 */

  /* USER CODE END SPI2_Init 1 */
  /* SPI2 parameter configuration*/
  hspi2.Instance = SPI2;
  hspi2.Init.Mode = SPI_MODE_MASTER;
  hspi2.Init.Direction = SPI_DIRECTION_2LINES;
  hspi2.Init.DataSize = SPI_DATASIZE_8BIT;
  hspi2.Init.CLKPolarity = SPI_POLARITY_LOW;
  hspi2.Init.CLKPhase = SPI_PHASE_1EDGE;
  hspi2.Init.NSS = SPI_NSS_SOFT;
  hspi2.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_2;
  hspi2.Init.FirstBit = SPI_FIRSTBIT_MSB;
  hspi2.Init.TIMode = SPI_TIMODE_DISABLE;
  hspi2.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
  hspi2.Init.CRCPolynomial = 10;
  if (HAL_SPI_Init(&hspi2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN SPI2_Init 2 */

  /* USER CODE END SPI2_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 84-1;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 4294967295;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_IC_InitTypeDef sConfigIC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 84-1;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = 65535;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim3, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  if (HAL_TIM_IC_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigIC.ICPolarity = TIM_INPUTCHANNELPOLARITY_BOTHEDGE;
  sConfigIC.ICSelection = TIM_ICSELECTION_DIRECTTI;
  sConfigIC.ICPrescaler = TIM_ICPSC_DIV1;
  sConfigIC.ICFilter = 0;
  if (HAL_TIM_IC_ConfigChannel(&htim3, &sConfigIC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */

}

/**
  * @brief TIM5 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM5_Init(void)
{

  /* USER CODE BEGIN TIM5_Init 0 */

  /* USER CODE END TIM5_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM5_Init 1 */

  /* USER CODE END TIM5_Init 1 */
  htim5.Instance = TIM5;
  htim5.Init.Prescaler = 1680-1;
  htim5.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim5.Init.Period = 1000-1;
  htim5.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim5.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_PWM_Init(&htim5) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim5, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim5, &sConfigOC, TIM_CHANNEL_2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM5_Init 2 */

  /* USER CODE END TIM5_Init 2 */
  HAL_TIM_MspPostInit(&htim5);

}

/**
  * @brief TIM11 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM11_Init(void)
{

  /* USER CODE BEGIN TIM11_Init 0 */

  /* USER CODE END TIM11_Init 0 */

  /* USER CODE BEGIN TIM11_Init 1 */

  /* USER CODE END TIM11_Init 1 */
  htim11.Instance = TIM11;
  htim11.Init.Prescaler = 84-1;
  htim11.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim11.Init.Period = 1000-1;
  htim11.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim11.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim11) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM11_Init 2 */

  /* USER CODE END TIM11_Init 2 */

}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 9600;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
<<<<<<< HEAD
=======
  /* USER CODE BEGIN MX_GPIO_Init_1 */

  /* USER CODE END MX_GPIO_Init_1 */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, DHT11_Pin|TRIG_Pin|LD2_Pin|CE_DS1302_Pin
                          |IO_DS1302_Pin|CLK_DS1302_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_0|GPIO_PIN_1|GPIO_PIN_2|LATCH_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : BTN0_Pin BTN1_Pin BTN2_Pin BTN3_Pin */
  GPIO_InitStruct.Pin = BTN0_Pin|BTN1_Pin|BTN2_Pin|BTN3_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pins : DHT11_Pin TRIG_Pin LD2_Pin CE_DS1302_Pin
                           IO_DS1302_Pin CLK_DS1302_Pin */
  GPIO_InitStruct.Pin = DHT11_Pin|TRIG_Pin|LD2_Pin|CE_DS1302_Pin
                          |IO_DS1302_Pin|CLK_DS1302_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : PB0 PB1 PB2 LATCH_Pin */
  GPIO_InitStruct.Pin = GPIO_PIN_0|GPIO_PIN_1|GPIO_PIN_2|LATCH_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

<<<<<<< HEAD
=======
  /* USER CODE BEGIN MX_GPIO_Init_2 */

  /* USER CODE END MX_GPIO_Init_2 */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/* USER CODE BEGIN Header_StartDefaultTask */
/**
<<<<<<< HEAD
 * @brief  Function implementing the defaultTask thread.
 * @param  argument: Not used
 * @retval None
 */
=======
  * @brief  Function implementing the defaultTask thread.
  * @param  argument: Not used
  * @retval None
  */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void *argument)
{
  /* USER CODE BEGIN 5 */
<<<<<<< HEAD
	/* Infinite loop */
	for(;;)
	{
		if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET)
		{
			osDelay(100); // 디바운스
			if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET)
			{
				set_event(1);
				osDelay(300);
			}
		}

		osDelay(1);
	}
=======
  /* Infinite loop */
  for(;;)
  {
      if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET)
      {
    	  osDelay(100); // 디바운스
          if (HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13) == GPIO_PIN_RESET)
          {
        	  set_event(1);
        	  osDelay(300);
          }
      }

      osDelay(1);
  }
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE END 5 */
}

/* USER CODE BEGIN Header_UARTTask */
/**
<<<<<<< HEAD
 * @brief Function implementing the UART thread.
 * @param argument: Not used
 * @retval None
 */
=======
* @brief Function implementing the UART thread.
* @param argument: Not used
* @retval None
*/
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
/* USER CODE END Header_UARTTask */
void UARTTask(void *argument)
{
  /* USER CODE BEGIN UARTTask */
<<<<<<< HEAD
	/* Infinite loop */
	char* message = "d\r\n";
	for(;;)
	{
		if(get_event()) {

			set_event(0);
			HAL_UART_Transmit_IT(&huart1, (uint8_t*)message, strlen(message));
			printf("%s", message);
		}

		osDelay(1);
	}
=======
  /* Infinite loop */

  char* message = "detect\r\n";
  for(;;)
  {
	if(get_event()) {

		set_event(0);
		HAL_UART_Transmit(&huart1, (uint8_t*)message, strlen(message), HAL_MAX_DELAY);

		printf("%s", message);
	}

    osDelay(1);
  }
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE END UARTTask */
}

/* USER CODE BEGIN Header_UltrasonicTask */
/**
<<<<<<< HEAD
 * @brief Function implementing the ULTRASONIC thread.
 * @param argument: Not used
 * @retval None
 */
=======
* @brief Function implementing the ULTRASONIC thread.
* @param argument: Not used
* @retval None
*/
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
/* USER CODE END Header_UltrasonicTask */
void UltrasonicTask(void *argument)
{
  /* USER CODE BEGIN UltrasonicTask */
<<<<<<< HEAD
	/* Infinite loop */
	for(;;)
	{
		ultra_sonic_trigger();
		osDelay(100);
	}
=======
  /* Infinite loop */
  for(;;)
  {
		ultra_sonic_trigger();
		osDelay(100);
  }
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE END UltrasonicTask */
}

/* USER CODE BEGIN Header_LCDTask */
/**
<<<<<<< HEAD
 * @brief Function implementing the LCD thread.
 * @param argument: Not used
 * @retval None
 */
=======
* @brief Function implementing the LCD thread.
* @param argument: Not used
* @retval None
*/
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
/* USER CODE END Header_LCDTask */
void LCDTask(void *argument)
{
  /* USER CODE BEGIN LCDTask */
<<<<<<< HEAD
	/* Infinite loop */
	char buf[32];  // 크기는 상황에 따라 적절히 조정
	for(;;)
	{
=======
  /* Infinite loop */
  char buf[32];  // 크기는 상황에 따라 적절히 조정
  for(;;)
  {
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
		// 0번 라인 초기화 후 출력
		move_cursor(0, 0);
		snprintf(buf, sizeof(buf), "T:%d.%d H:%d.%d     ", temperature_int, temperature_dec, humidity_int, humidity_dec);
		lcd_string((uint8_t*)buf);

		// 1번 라인 초기화 후 출력
		move_cursor(1, 0);
		snprintf(buf, sizeof(buf), "D:%5.1fcm        ", distance);  // %5.1f로 길이 보장
		lcd_string((uint8_t*)buf);

		osDelay(500);
<<<<<<< HEAD
	}
=======
  }
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE END LCDTask */
}

/* USER CODE BEGIN Header_ServoTask */
/**
<<<<<<< HEAD
 * @brief Function implementing the SERVO_MOTOR thread.
 * @param argument: Not used
 * @retval None
 */
=======
* @brief Function implementing the SERVO_MOTOR thread.
* @param argument: Not used
* @retval None
*/
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
/* USER CODE END Header_ServoTask */
void ServoTask(void *argument)
{
  /* USER CODE BEGIN ServoTask */
<<<<<<< HEAD
	/* Infinite loop */
	for(;;)
	{
		servo_motor_update();  // 모듈 함수 호출
		osDelay(100);
	}
=======
  /* Infinite loop */
  for(;;)
  {
		servo_motor_update();  // 모듈 함수 호출
		osDelay(100);
  }
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE END ServoTask */
}

/* USER CODE BEGIN Header_DHT11Task */
/**
<<<<<<< HEAD
 * @brief Function implementing the DHT11 thread.
 * @param argument: Not used
 * @retval None
 */
=======
* @brief Function implementing the DHT11 thread.
* @param argument: Not used
* @retval None
*/
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
/* USER CODE END Header_DHT11Task */
void DHT11Task(void *argument)
{
  /* USER CODE BEGIN DHT11Task */
<<<<<<< HEAD
	/* Infinite loop */
	for(;;)
	{
=======
  /* Infinite loop */
  for(;;)
  {
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
		dht11_read();  // dht11_data[] 갱신
		temperature_int = dht11_data[2];
		temperature_dec = dht11_data[3];
		humidity_int = dht11_data[0];
		humidity_dec = dht11_data[1];
		osDelay(500);
<<<<<<< HEAD
	}
=======
  }
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
  /* USER CODE END DHT11Task */
}

/**
  * @brief  Period elapsed callback in non blocking mode
  * @note   This function is called  when TIM10 interrupt took place, inside
  * HAL_TIM_IRQHandler(). It makes a direct call to HAL_IncTick() to increment
  * a global variable "uwTick" used as application time base.
  * @param  htim : TIM handle
  * @retval None
  */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  /* USER CODE BEGIN Callback 0 */

  /* USER CODE END Callback 0 */
<<<<<<< HEAD
  if (htim->Instance == TIM10) {
=======
  if (htim->Instance == TIM10)
  {
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
    HAL_IncTick();
  }
  /* USER CODE BEGIN Callback 1 */
	// Timer 11번
	if (htim->Instance == TIM11)
	{
		TIM11_1ms_counter++;
		TIM11_sec_counter++;
	}
  /* USER CODE END Callback 1 */
}

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */
	__disable_irq();
	while (1)
	{
	}
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
	/* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
<<<<<<< HEAD

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
=======
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
