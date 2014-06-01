#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3
import globals
import System
import arm7instrdecode

# Modes: abort        10111
#        fast int req 10001
#        int req      10010
#        supervisor   10011
#        system       11111
#        undef        11011
#        user         10000
#
# Addresses
# 00 - reset
# 04 - undef
# 08 - software int
# 0c - prefetch abort
# 10 - data abort
# 14 - reserved
# 18 - int req IRQ
# 1c - fast int req

CPSR_FLGS_MASK = int("11110000000000000000000000000000", 2)
CPSR_Q_MASK = int("00001000000000000000000000000000", 2)
CPSR_J_MASK = int("00000001000000000000000000000000", 2)
CPSR_GE_MASK = int("00000000000011110000000000000000", 2)
CPSR_IT_MASK = int("00000110000000001111110000000000", 2)
CPSR_E_MASK = int("00000000000000000000001000000000", 2)
CPSR_A_MASK = int("00000000000000000000000100000000", 2)
CPSR_I_MASK = int("00000000000000000000000010000000", 2)
CPSR_F_MASK = int("00000000000000000000000001000000", 2)
CPSR_T_MASK = int("00000000000000000000000000100000", 2)
CPSR_M_MASK = int("00000000000000000000000000011111", 2)

# APSR is same as CPSR but only allow Flags and GE bits
#                  10987654321098765432109876543210
CPSR_LOOKUP = {
   "CPSR_FLGS":CPSR_FLGS_MASK,
   "CPSR_Q":CPSR_Q_MASK,
   "CPSR_J":CPSR_J_MASK,
   "CPSR_GE":CPSR_GE_MASK,
   "CPSR_IT":CPSR_IT_MASK,
   "CPSR_E":CPSR_E_MASK,
   "CPSR_A":CPSR_A_MASK,
   "CPSR_I":CPSR_I_MASK,
   "CPSR_F":CPSR_F_MASK,
   "CPSR_T":CPSR_T_MASK,
   "CPSR_M":CPSR_M_MASK}
CPSR_SHIFT = {
   "CPSR_FLGS":28,
   "CPSR_Q":27,
   "CPSR_J":24,
   "CPSR_GE":16,
   "CPSR_IT":10,
   "CPSR_E":9,
   "CPSR_A":8,
   "CPSR_I":7,
   "CPSR_F":6,
   "CPSR_T":5,
   "CPSR_M":0}

PMODE_USR = int("10000", 2)
PMODE_FIQ = int("10001", 2)
PMODE_IRQ = int("10010", 2)
PMODE_SVC = int("10011", 2)
PMODE_MON = int("10110", 2)
PMODE_ABT = int("10111", 2) # abort
PMODE_HPY = int("11010", 2)
PMODE_UND = int("11011", 2)
PMODE_SYS = int("11111", 2)

HIGHBIT = int("80000000", 16)
NEGATIVEBIT = int("80000000",16)
ZEROBIT = int("40000000",16)
CARRYBIT = int("20000000",16)
OVERBIT = int("10000000",16)
QBIT = int("08000000",16)

INTIRQBIT = int("00000080",16)
INTFIQBIT = int("00000040",16)
THUMBBIT = int("00000020",16)
OPMODEBIT = int("0000001F",16)

# ---------------------------------------------------------------------
#def reset(self):

# ---------------------------------------------------------------------
def rwCPSR(self, bitname, bitvalue):
    if bitvalue is None: # get
        return arm7instrdecode.getSetValue(self, CPSR_LOOKUP[bitname], CPSR_SHIFT[bitname], globals.regs[globals.CPSR], None)
    else:
        globals.regs[globals.CPSR] = arm7instrdecode.getSetValue(self, CPSR_LOOKUP[bitname], CPSR_SHIFT[bitname], globals.regs[globals.CPSR], bitvalue)
