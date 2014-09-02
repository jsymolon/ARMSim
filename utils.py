#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3
import globals
import ARMCPU

###########################################################################
## Handle the misc
###########################################################################

def getCSPRString(self):
    cpsr = ""
    if (globals.regs[globals.CPSR] & ARMCPU.NEGATIVEBIT == ARMCPU.NEGATIVEBIT):
        cpsr = " N"
    else:
        cpsr = " n"
    if (globals.regs[globals.CPSR] & ARMCPU.ZEROBIT == ARMCPU.ZEROBIT):
        cpsr += "Z"
    else:
        cpsr += "z"
    if (globals.regs[globals.CPSR] & ARMCPU.CARRYBIT == ARMCPU.CARRYBIT):
        cpsr += "C"
    else:
        cpsr += "c"
    if (globals.regs[globals.CPSR] & ARMCPU.OVERBIT == ARMCPU.OVERBIT):
        cpsr += "V"
    else:
        cpsr += "v"
    if (globals.regs[globals.CPSR] & ARMCPU.QBIT == ARMCPU.QBIT):
        cpsr += "Q"
    else:
        cpsr += "q"
    if (globals.regs[globals.CPSR] & ARMCPU.INTIRQBIT == ARMCPU.INTIRQBIT):
        cpsr += "I"
    else:
        cpsr += "i"
    if (globals.regs[globals.CPSR] & ARMCPU.INTFIQBIT == ARMCPU.INTFIQBIT):
        cpsr += "F"
    else:
        cpsr += "f"
    if (globals.regs[globals.CPSR] & ARMCPU.THUMBBIT == ARMCPU.THUMBBIT):
        cpsr += "T "
    else:
        cpsr += "t "
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("00000017",16)):
        cpsr += " abt"
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("00000011",16)):
        cpsr += " frq"
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("00000012",16)):
        cpsr += " irq"
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("00000013",16)):
        cpsr += " sup"
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("0000001f",16)):
        cpsr += " sys"
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("0000001b",16)):
        cpsr += " und"
    if (globals.regs[globals.CPSR] & ARMCPU.OPMODEBIT == int("00000010",16)):
        cpsr += " usr"
    return cpsr

def buildRegValString(self, i):
    out = ""
    if i < globals.D_CPSR:
        out = "R"+str("%02d"%i)+":"+str("%08X" % globals.regs[i])
    if i == globals.SP:
        out += " (sp)"
    if i == globals.LINK:
        out += " (lr)"
    if i == globals.PC:
        out += " (pc)"
    if i == globals.CPSR:
        out += " (cpsr)"
    if i == globals.SPSR:
        out += " (spsr)"
    if i == globals.D_CPSR or i == globals.CPSR or i == globals.SPSR :
        out += getCSPRString(self)
    return out