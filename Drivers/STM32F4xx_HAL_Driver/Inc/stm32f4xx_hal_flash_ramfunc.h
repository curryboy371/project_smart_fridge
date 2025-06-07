/**
  ******************************************************************************
  * @file    stm32f4xx_hal_flash_ramfunc.h
  * @author  MCD Application Team
  * @brief   Header file of FLASH RAMFUNC driver.
  ******************************************************************************
  * @attention
  *
<<<<<<< HEAD
  * <h2><center>&copy; Copyright (c) 2017 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */ 
=======
  * Copyright (c) 2017 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file in
  * the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  ******************************************************************************
  */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __STM32F4xx_FLASH_RAMFUNC_H
#define __STM32F4xx_FLASH_RAMFUNC_H

#ifdef __cplusplus
<<<<<<< HEAD
 extern "C" {
#endif
#if defined(STM32F410Tx) || defined(STM32F410Cx) || defined(STM32F410Rx) || defined(STM32F411xE) || defined(STM32F446xx) || defined(STM32F412Zx) ||\
    defined(STM32F412Vx) || defined(STM32F412Rx) || defined(STM32F412Cx)  
=======
extern "C" {
#endif
#if defined(STM32F410Tx) || defined(STM32F410Cx) || defined(STM32F410Rx) || defined(STM32F411xE) || defined(STM32F446xx) || defined(STM32F412Zx) ||\
    defined(STM32F412Vx) || defined(STM32F412Rx) || defined(STM32F412Cx)
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal_def.h"

/** @addtogroup STM32F4xx_HAL_Driver
  * @{
  */

/** @addtogroup FLASH_RAMFUNC
  * @{
  */

/* Exported types ------------------------------------------------------------*/
/* Exported macro ------------------------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
/** @addtogroup FLASH_RAMFUNC_Exported_Functions
  * @{
  */

/** @addtogroup FLASH_RAMFUNC_Exported_Functions_Group1
  * @{
<<<<<<< HEAD
  */   
=======
  */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
__RAM_FUNC HAL_StatusTypeDef HAL_FLASHEx_StopFlashInterfaceClk(void);
__RAM_FUNC HAL_StatusTypeDef HAL_FLASHEx_StartFlashInterfaceClk(void);
__RAM_FUNC HAL_StatusTypeDef HAL_FLASHEx_EnableFlashSleepMode(void);
__RAM_FUNC HAL_StatusTypeDef HAL_FLASHEx_DisableFlashSleepMode(void);
/**
  * @}
<<<<<<< HEAD
  */ 
=======
  */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0

/**
  * @}
  */

/**
  * @}
<<<<<<< HEAD
  */ 
=======
  */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0

/**
  * @}
  */

<<<<<<< HEAD
#endif /* STM32F410xx || STM32F411xE || STM32F446xx || STM32F412Zx || STM32F412Vx || STM32F412Rx || STM32F412Cx */  
=======
#endif /* STM32F410xx || STM32F411xE || STM32F446xx || STM32F412Zx || STM32F412Vx || STM32F412Rx || STM32F412Cx */
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
#ifdef __cplusplus
}
#endif


#endif /* __STM32F4xx_FLASH_RAMFUNC_H */

<<<<<<< HEAD
/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
=======
>>>>>>> 95147dff18777353e4155d9c14b1506f44999be0
