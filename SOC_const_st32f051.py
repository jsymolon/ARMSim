#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3
import globals
import logging
import ARMCPU

###################################################
# Addresses
###################################################
# ROM
#ROM_BASE =
# RAM
FLASH_BASH = 0x08000000

# temp sensors
TS_CAL1_BASE = 0x1ffff7b8
TS_CAL2_BASE = 0x1ffff7c2

# voltage ref
VREFINT_CAL_BASE = 0x1ffff7ba

# AD convert
ADC_BASE = 0x40012400
EXTI_BASE = 0x40010400
SYSCFG_BASE = 0x40010000
DAC_BASE = 0x40007400
PWR_BASE = 0x40007000

# Timers
TIM1_BASE = 0x40012C00 # 16 up/dwn
TIM2_BASE = 0x40000000 # 32 up/dwn
TIM3_BASE = 0x40000400
TIM4_BASE = 0x40001000 # maps to TIM6
TIM5_BASE = 0x40002000 # maps to TIM14
TIM6_BASE = 0x40014000 # maps to TIM15
TIM7_BASE = 0x40014400 # maps to TIM16
TIM8_BASE = 0x40014800 # maps to TIM17

# watchdog
IWDG_BASE = 0x40003000

# System watchdog
WWDG_BASE = 0x40002C00

# Real time clock
RTC_BASE = 0x40002800

# inter-interfrated circuit interfaces
I2C1_BASE = 0x40005400
I2C2_BASE = 0x40005800

# USART
# USART0_BASE = # not used
USART1_BASE = 0x40013800
USART2_BASE = 0x40004400

# serial peripheral interface
SPI1_BASE = 0x40013000
SPI2_BASE = 0x40003800

# intergrated sound
#I2S_BASE =

#  High-definition multimedia interface (HDMI) - consumer electronics control (CEC)
#HDMI_BASE =
CEC_BASE = 0x40007800

#  Serial wire debug port (SW-DP)
#SWDP_BASE =

GPIOA_BASE = 0x48000000
GPIOB_BASE = 0x48000400
GPIOC_BASE = 0x48000800
GPIOD_BASE = 0x48000C00
#GPIOE_BASE = 0x48001000 # reserved
GPIOF_BASE = 0x48001400

TSC_BASE = 0x40024000
CRC_BASE = 0x40023000
FLASH_INT_BASE = 0x40022000
RCC_BASE = 0x40021000
DMA_BASE = 0x40020000



