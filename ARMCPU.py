#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3
import globals
import System
import armv6instrdecode

# Modes: abort        10111
#        fast int req 10001
#        int req      10010
#        supervisor   10011
#        system       11111
#        undef        11011
#        user         10000
#

PMODE_USR = 0b10000
PMODE_FIQ = 0b10001
PMODE_IRQ = 0b10010
PMODE_SVC = 0b10011
PMODE_MON = 0b10110
PMODE_ABT = 0b10111 # abort
PMODE_HPY = 0b11010
PMODE_UND = 0b11011
PMODE_SYS = 0b11111

# Addresses
ADDR_INT = 0x00 # 00 - reset
ADDR_UND = 0x04 # 04 - undef
ADDR_SW  = 0x08 # 08 - software int
ADDR_PFA = 0x0C # 0c - prefetch abort
ADDR_DA  = 0x10 # 10 - data abort
ADDR_RSV = 0x14 # 14 - reserved
ADDR_IRQ = 0x18 # 18 - int req IRQ
ADDR_FIR = 0x1C # 1c - fast int req

CPSR_FLGS_MASK = 0b11110000000000000000000000000000
CPSR_Q_MASK    = 0b00001000000000000000000000000000
CPSR_J_MASK    = 0b00000001000000000000000000000000
CPSR_GE_MASK   = 0b00000000000011110000000000000000
CPSR_IT_MASK   = 0b00000110000000001111110000000000
CPSR_E_MASK    = 0b00000000000000000000001000000000
CPSR_A_MASK    = 0b00000000000000000000000100000000
CPSR_I_MASK    = 0b00000000000000000000000010000000
CPSR_F_MASK    = 0b00000000000000000000000001000000
CPSR_T_MASK    = 0b00000000000000000000000000100000
CPSR_M_MASK    = 0b00000000000000000000000000011111

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

HIGHBIT     = 0x80000000
NEGATIVEBIT = 0x80000000
ZEROBIT     = 0x40000000
CARRYBIT    = 0x20000000
OVERBIT     = 0x10000000
QBIT        = 0x08000000

INTIRQBIT = 0x00000080
INTFIQBIT = 0x00000040
THUMBBIT  = 0x00000020
OPMODEBIT = 0x0000001F

CC_EQ = 0
CC_NE = 1
CC_HS = 2
CC_LO = 3
CC_MI = 4
CC_PL = 5
CC_VS = 6
CC_VC = 7
CC_HI = 8
CC_LS = 9
CC_GE = 10
CC_LT = 11
CC_GT = 12
CC_LE = 13
CC_AL = 14
CC_NV = 15

# ---------------------------------------------------------------------
def reset(self):
   rwCPSR(self, "CPSR_M", PMODE_SVC) # goto supervisor mode
   rwCPSR(self, "CPSR_I", 1) # kill interrupts
   rwCPSR(self, "CPSR_F", 1)
   rwCPSR(self, "CPSR_A", 1)
   # IT clear
   rwCPSR(self, "CPSR_J", 0)
   rwCPSR(self, "CPSR_T", 0)  # Arm / Thumb
   #rwCPSR(self, "CPSR_E", 1)  # 0- little endian, 1- big endian
   globals.regs[globals.PC] = ADDR_INT

# ---------------------------------------------------------------------
def breakpoint(self, address):
   bits = getModeBits(self)
   print "bits:" + str(bits)
   oldmode = mapModeToIndex(self, bits)
   print "oldmode:" + str(oldmode)
   swapRegsOnModeChange(self, oldmode, PMODE_ABT)
   # See BKPT ARM_ARM A4.1.7
   globals.regs[14] = address + 4
   rwCPSR(self, "CPSR_T", 0) # goto Arm (not thumb)
   rwCPSR(self, "CPSR_I", 1) # kill interrupts
   rwCPSR(self, "CPSR_A", 1) # disable imprecise aborts
   # IT clear
   rwCPSR(self, "CPSR_J", 0)
   #rwCPSR(self, "CPSR_E", 1)  # 0- little endian, 1- big endian
   globals.regs[globals.PC] = ADDR_PFA

# ---------------------------------------------------------------------
# get mode bits
def getModeBits(self):
   bits = globals.regs[globals.CPSR] & CPSR_M_MASK;
   return bits

# ---------------------------------------------------------------------
def mapModeToIndex(self, mode):
    if mode == PMODE_USR:
      return globals.PMODE_USR_IDX
    if mode == PMODE_SYS:
      return globals.PMODE_SYS_IDX
    if mode == PMODE_FIQ:
      return globals.PMODE_FIQ_IDX
    if mode == PMODE_IRQ:
      return globals.PMODE_IRQ_IDX
    if mode == PMODE_SVC:
      return globals.PMODE_SVC_IDX
    if mode == PMODE_MON:
      return globals.PMODE_MON_IDX
    if mode == PMODE_ABT:
      return globals.PMODE_ABT_IDX
    if mode == PMODE_HPY:
      return globals.PMODE_HPY_IDX
    if mode == PMODE_UND:
      return globals.PMODE_UND_IDX
    # default to SYSTEM, usually testing
    return globals.PMODE_SYS_IDX
    print "mapModeToIndex: exit " + str(mode)

# ---------------------------------------------------------------------
# map mode to registers
def swapRegsOnModeChange(self, oldmode, newmode):
   # FIQ: 8-14, Sup, Abrt, irq & undef: r13,r14
   # remap SYS to USR
   if oldmode == PMODE_USR:
      oldmode = PMODE_SYS
   if newmode == PMODE_USR:
      newmode = PMODE_SYS
   if newmode == oldmode:
      # no change
      return
   # not FIQ only R13 & 14
   oldidx = mapModeToIndex(self, oldmode)
   newidx = mapModeToIndex(self, newmode)
   
   # move old (working) to old
   print oldidx
   globals.regs[oldidx + 13] = globals.regs[13] 
   globals.regs[oldidx + 14] = globals.regs[14] 
   # move new to working
   globals.regs[13] = globals.regs[newidx + 13] 
   globals.regs[14] = globals.regs[newidx + 14]
   
   # handle FIQ
   if oldmode == PMODE_FIQ:
      globals.regs[oldidx + 8] = globals.regs[8] 
      globals.regs[oldidx + 9] = globals.regs[9] 
      globals.regs[oldidx + 10] = globals.regs[10] 
      globals.regs[oldidx + 11] = globals.regs[11] 
      globals.regs[oldidx + 12] = globals.regs[12] 
      
   if newmode == PMODE_FIQ:
      globals.regs[8] = globals.regs[newidx + 8] 
      globals.regs[9] = globals.regs[newidx + 9]
      globals.regs[10] = globals.regs[newidx + 10] 
      globals.regs[11] = globals.regs[newidx + 11] 
      globals.regs[12] = globals.regs[newidx + 12]
   
# ---------------------------------------------------------------------
def rwCPSR(self, bitname, bitvalue):
    if bitvalue is None: # get
        return armv6instrdecode.getSetValue(self, CPSR_LOOKUP[bitname], CPSR_SHIFT[bitname], globals.regs[globals.CPSR], None)
    else:
        globals.regs[globals.CPSR] = armv6instrdecode.getSetValue(self, CPSR_LOOKUP[bitname], CPSR_SHIFT[bitname], globals.regs[globals.CPSR], bitvalue)

# ---------------------------------------------------------------------
def isNegative(self):
   return (globals.regs[globals.CPSR] & NEGATIVEBIT > 0)

# ---------------------------------------------------------------------
def isZero(self):
   return (globals.regs[globals.CPSR] & ZEROBIT > 0)

# ---------------------------------------------------------------------
def isCarry(self):
   return (globals.regs[globals.CPSR] & CARRYBIT > 0)

# ---------------------------------------------------------------------
def isOverflow(self):
   return (globals.regs[globals.CPSR] & OVERBIT > 0)

# ---------------------------------------------------------------------
def isQSet(self):
   return (globals.regs[globals.CPSR] & QBIT > 0)
   
