#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3
import globals
import logging
import ARMCPU

condCode = 0
sCode = 0
iCode = 0
shiftOp = 0
shiftCnt = 0
destReg = 0
immCnt = 0
d_op_code = 0
OP2 = 0
Rn = 0
Rd = 0
Rs = 0
Rm = 0
newPC = 0

# make the shift op clearer (remove magic)
LSL = 0
LSR = 1
ASR = 2
ROR = 3
RRX = 4

# ---------------------------------------------------------------------
def getSCode(self, code):
    """ data processing - tells if cond codes are affected """
    global sCode
    sCode = (code >> 20) & 1
    if (sCode == 1):
        return "S  "
    return "   "

# ---------------------------------------------------------------------
def getICode(self, code):
    """ data processing - tells if op is immediate """
    global iCode
    iCode = (code >> 25) & 1

# ---------------------------------------------------------------------
def getRn(self, code):
    global Rn
    Rn = (code >> 16) & 15
    return " R"+str("%02d"%Rn)

# ---------------------------------------------------------------------
def getRd(self, code):
    global Rd
    Rd = (code >> 12) & 15
    return " R"+str("%02d"%Rd)

# ---------------------------------------------------------------------
def getRs(self, code):
    global Rs
    Rs = (code >> 8) & 15
    return " R"+str("%02d"%Rs)

# ---------------------------------------------------------------------
def getRm(self, code):
    global Rm
    Rm = code & 15
    return " R"+str("%02d"%Rm)

# ---------------------------------------------------------------------
def getCondCode(self, code):
    global condCode
    condCode = int(code >> 28)
    if (condCode == ARMCPU.CC_EQ):
        return " EQ"
    if (condCode == ARMCPU.CC_NE):
        return " NE"
    if (condCode == ARMCPU.CC_HS):
        return " HS"
    if (condCode == ARMCPU.CC_LO):
        return " LO"
    if (condCode == ARMCPU.CC_MI):
        return " MI"
    if (condCode == ARMCPU.CC_PL):
        return " PL"
    if (condCode == ARMCPU.CC_VS):
        return " VS"
    if (condCode == ARMCPU.CC_VC):
        return " VC"
    if (condCode == ARMCPU.CC_HI):
        return " HI"
    if (condCode == ARMCPU.CC_LS):
        return " LS"
    if (condCode == ARMCPU.CC_GE):
        return " GE"
    if (condCode == ARMCPU.CC_LT):
        return " LT"
    if (condCode == ARMCPU.CC_GT):
        return " GT"
    if (condCode == ARMCPU.CC_LE):
        return " LE"
    if (condCode == ARMCPU.CC_AL):
        return " AL"
    if (condCode == ARMCPU.CC_NV):
        return " NV"
    return "   "

# ---------------------------------------------------------------------
def getSetValue(self, bitmask, shift, baseval, value): #
    if value is None: # get
        return ((baseval & bitmask) >> shift)
    else:   #set
        return ((baseval & (~ bitmask)) | (value << shift))

# ---------------------------------------------------------------------
def getInstructionFromAddress(self, addr, memory):
    # read memory
    #code = 305419896 #0x12345678
    #code = 234881024 #0x0E000000 - 27-25 bits
    code = 0
    self.addr = addr
    for accum in range(0, 4):
        code = code << 8
        code += memory[addr + 3 - accum]
    return '%08X' % addr + getInstructionFromCode(self, code, False)

# ---------------------------------------------------------------------
def execInstructionAtAddress(self, addr, memory):
    global code
    global newPC
    code = 0
    newPC = addr
    logging.debug("addr:"+hex(addr))
    self.addr = addr
    for accum in range(0, 4):
        code = code << 8
        code += memory[addr + 3 - accum]
    getInstructionFromCode(self, code, True)
    newPC = globals.regs[globals.PC] + 4 #branch will modify pc
    return newPC

# ---------------------------------------------------------------------
def getInstructionFromCode(self, code, execute):
    # dump code
    out  = ' %02X' % (code >> 24)
    out += '%02X' % (code >> 16 & 255)
    out += '%02X' % (code >> 8 & 255)
    out += '%02X' % (code & 255)
    # dump memonic
    logging.debug(" ")
    inst1 = (code >> 26 & 3)
    if inst1 == 0:
        out += inst00decode(self, code, execute)
    if inst1 == 1:
        out += inst01decode(self, code, execute)
    if inst1 == 2:
        out += inst10decode(self, code, execute)
    if inst1 == 3:
        out += inst11decode(self, code, execute)
    return out

# ---------------------------------------------------------------------
def inst00decode(self, code, execute):
    """ decode the bits at 27-26 = 00
        data processing
        PSR transfer
        Mult
        Single data swap
    """
    """ opCode is the data instructions """
    self.d_op_code = code >> 21 & 15
    logging.debug("inst00decode: code:" + str("%08X"%code) + " d_op_code:" + hex(d_op_code))
    retStr = "";
    # split functionality by opcode; AND, MLA, MUL, STR, LDR, udf, LDR
    if (self.d_op_code == 0):
        oc2 = code >> 4 & 15 # the other fixed field
        mod = code >> 20 & 1 # S bit
        andchk = oc2 | 1; # AND is 0000 and 0001
        logging.debug("code:" + hex(code) + " oc2:" + hex(oc2) +  " mod:" + hex(mod) + " andchk:" + hex(andchk))
        if andchk == 0b0001:  # # or Rs
            retStr = " AND"
        if oc2 == 0b1001:
            if (code >> 21) & 1 == 1: # A
                retStr = " MLA"
            else:
                retStr = " MUL"
        if oc2 == 0b1011 and mod == 0:
            retStr = " STR"
        if oc2 == 0b1011 and mod == 1:
            retStr = " LDR"
        if oc2 == 0b1101 and mod == 0:
            retStr = " udf"
        if oc2 == 0b1101 and mod == 1:
            retStr = " LDR"
        if oc2 == 0b1111 and mod == 0:
            retStr = " udf"
        if oc2 == 0b1111 and mod == 1:
            retStr = " LDR"
    if (self.d_op_code == 1):
        retStr = " EOR"
    if (self.d_op_code == 2):
        retStr = " SUB"
    if (self.d_op_code == 3):
        retStr = " RSB"
    if (self.d_op_code == 4):
        retStr = " ADD"
    if (self.d_op_code == 5):
        retStr = " ADC"
    if (self.d_op_code == 6):
        retStr = " SBC"
    if (self.d_op_code == 7):
        retStr = " RSC"
    if (self.d_op_code == 8):
        retStr = " TST"
    if (self.d_op_code == 9):
        retStr = " TEQ"
    if (self.d_op_code == 10):
        retStr = " CMP"
    if (self.d_op_code == 11):
        retStr = " CMN"
    if (self.d_op_code == 12):
        retStr = " ORR"
    if (self.d_op_code == 13):
        retStr = " MOV"
    if (self.d_op_code == 14):
        retStr = " BIC"
    if (self.d_op_code == 15):
        retStr = " MVN"
    retStr += getCondCode(self, code) + getSCode(self, code)
    retStr += doDataInst(self, code, execute)
    return retStr

# ---------------------------------------------------------------------
def inst01decode(self, code, execute):
    """ decode the bits at 27-26 = 01
    """
    strI =    0x0E500000
    strIv =   0x04000000
    if (code & strI == strIv):
        return " STR  "
    strIBv =  0x04400000
    if (code & strI == strIBv):
        return " STRB "
    strIT =   0x0F700000
    strITv =  0x04200000
    if (code & strIT == strITv):
        return " STRT "
    strIBT =  0x0F700010
    strIBTv = 0x04600000
    if (code & strIBT == strIBTv):
        return " STRBT "
    return "      "

# ---------------------------------------------------------------------
def inst10decode(self, code, execute):
    """ decode the bits at 27-26 = 10
    """
    if (code & 0x02000000 > 0):
        return doBranch (self, code, execute)
    else:
        if (code >> 20) & 1 == 1:
            return " LDM  "
        else:
            return " STM  "
    return "      "

# ---------------------------------------------------------------------
def inst11decode(self, code, execute):
    """ decode the bits at 27-26 = 11
    """
    return "      "

# ---------------------------------------------------------------------
def doBranch(self, code, execute):
    global newPC
    offset = 0
    laddr = 0
    if code & 0x00800000: # handle negative bit
        offset = (0x00ffffff - (code & 0x00ffffff))
        offset *= -1
        laddr = (offset * 4) + 4 + self.addr # add addr to make the relative display work,
                                        # if exec, addr should = PC
    else:
        offset = code & 0x007fffff #strip neg bit will pick up later
        laddr = (offset * 4) + 8 + self.addr # add addr to make the relative display work,
                                        # if exec, addr should = PC
    logging.debug("off:" + hex(offset) + " addr:" + str(laddr) + " exe:" + str(execute))
    if (execute):
        if (code & 0x01000000 > 0): # branch & link vs branch
            globals.regs[14] = globals.regs[globals.PC]
        globals.regs[globals.PC] = laddr

    if (code & 0x01000000 > 0): # branch & link vs branch
        return " BL"+getCondCode(self, code)+"     "+str("%08X"%laddr)
    else:
        return " B"+getCondCode(self, code)+"      "+str("%08X"%laddr)
    
# ---------------------------------------------------------------------
# check the passed in cond code set w/ the flags
# return true if condition met aka exec instruction
# ---------------------------------------------------------------------
def conditionMet(self, xCode):
    nCode = (globals.regs[globals.CPSR] & ARMCPU.NEGATIVEBIT) >> 31
    zCode = (globals.regs[globals.CPSR] & ARMCPU.ZEROBIT) >> 30
    cCode = (globals.regs[globals.CPSR] & ARMCPU.CARRYBIT) >> 29
    vCode = (globals.regs[globals.CPSR] & ARMCPU.OVERBIT) >> 28
    logging.debug("xCode:" + str(xCode) + " nCode:" + str(nCode) + " zCode:" + str(zCode) + " cCode:" + str(cCode) + " vCode:" + str(vCode))
    logging.debug( str( (zCode & 1) ) + " " +
        str( int( not (zCode & 1)) ) + " " +
        str( (cCode & 1) ) + " " +
        str( int(not (cCode & 1) )) + " " +
        str( (nCode & 1) ) + " " +
        str( int(not (nCode & 1) )) + " " +
        str( (vCode & 1) ) + " " +
        str( int(not (vCode & 1) )) + " " +
        str( (cCode & 1) & (int(not (zCode & 1))) ) + " " +
        str( (zCode & 1) & (int(not (cCode & 1))) ) + " " +
        str( int(nCode == vCode) ) + " " +
        str( int(nCode != vCode) ) + " " +
        str( (int(not (zCode & 1))) & int(nCode == vCode))  + " " +
        str( (zCode & 1) | int(nCode != vCode)))
    if (xCode == ARMCPU.CC_EQ):  # EQ Z
        return (zCode & 1)
    if (xCode == ARMCPU.CC_NE):  # NE !Z
        return int(not (zCode & 1))
    if (xCode == ARMCPU.CC_HS): # CS / HS C
        return (cCode & 1)
    if (xCode == ARMCPU.CC_LO): # CC / LO !C
        return int(not (cCode & 1)) 
    if (xCode == ARMCPU.CC_MI): # MI N
        return (nCode & 1) 
    if (xCode == ARMCPU.CC_PL): # PL !N
        return int(not (nCode & 1)) 
    if (xCode == ARMCPU.CC_VS): # VS V
        return (vCode & 1) 
    if (xCode == ARMCPU.CC_VC): # VC !V
        return (not (vCode & 1)) 
    if (xCode == ARMCPU.CC_HI): # HI C & !Z
        return (cCode & 1) & int(not (zCode & 1))
    if (xCode == ARMCPU.CC_LS): # LS !C or Z
        return (zCode & 1) & int(not (cCode & 1))
    if (xCode == ARMCPU.CC_GE): # GE N == V
        return int(nCode == vCode)
    if (xCode == ARMCPU.CC_LT): # LT N != V
        return int(nCode != vCode)
    if (xCode == ARMCPU.CC_GT): # GT !Z & (N == V)
        return (int(not (zCode & 1)) & int(nCode == vCode))
    if (xCode == ARMCPU.CC_LE): # LE Z | (N != V)
        return (zCode & 1) | int(nCode != vCode)
    if (xCode == ARMCPU.CC_AL):
        return 1
    return False

# ---------------------------------------------------------------------
def doShift(self, shiftOp, shiftAmt, RmVal):
    """ function to do the barrel shifts
    """
    pso = ""
    if shiftOp == RRX:
        pso = "RRX"
    if shiftOp == LSL:
        pso = "LSL"
    if shiftOp == LSR:
        pso = "LSR"
    if shiftOp == ASR:
        pso = "ASR"
    if shiftOp == ROR:
        pso = "ROR"
    logging.debug("doShift: shiftOp:" + pso + " shiftAmt:" + hex(shiftAmt) + " RmVal:" + hex(RmVal))
    global carryOut
    carryIn = 0
    carryOut = 0
    if shiftOp == ASR:
        if Rm & ARMCPU.HIGHBIT > 0:
            carryIn = 1
    if shiftOp == RRX:
        if globals.regs[globals.CPSR] & ARMCPU.CARRYBIT > 0:
            carryIn = 1
    for x in range(0, shiftAmt):
        #print "doShift: x:" + str("%02d"%x) + " " + str("%08X"%RmVal)
        if shiftOp == LSL:
            carryOut = RmVal & ARMCPU.HIGHBIT
            # trying to shift the high bit out will cause a "long it too large", clear it
            RmVal = RmVal & ~ARMCPU.NEGATIVEBIT
            RmVal = RmVal << 1
        if shiftOp == LSR:
            carryOut = RmVal & 1
            RmVal = RmVal >> 1
        if shiftOp == ASR:
            carryOut = RmVal & 1
            RmVal = RmVal >> 1
            if carryIn:
                RmVal = RmVal | ARMCPU.HIGHBIT
        if shiftOp == ROR:
            carryOut = RmVal & 1
            RmVal = RmVal >> 1
            if carryOut > 0:
                RmVal = RmVal | ARMCPU.HIGHBIT
    # RRX only does 1 loop
    if shiftOp == RRX:
        carryOut = RmVal & 1
        RmVal = RmVal >> 1
        if carryOut > 0:
            RmVal = RmVal | ARMCPU.HIGHBIT
    return RmVal  # actually OP2

# ---------------------------------------------------------------------
#
#       110000000000
#       109876543210
# OP1:  ROT immed_8   # Bit 25 = 1        # 32 bit immd
# OP2:  SftIMss0-Rm-  # Bit 25 = 0, 4 = 0 # immd shift
# OP3:  -Rs-0ss1-Rm-  # Bit 25 = 0, 4 = 1 # register shift
# ---------------------------------------------------------------------
def getImmOP2DataProcessing(self, code):
    retVal = 0
    oc1 = code >> 25 & 1 # fixed field
    oc2 = code >> 4 & 1 # the other fixed field
    # oc1 = 0 & oc2 = 0 - DP imm shift
    # oc1 = 0 & oc2 = 1 - DP reg shift
    # oc1 = 1 - dp imm
    if (oc1 == 0):
        Rm = code & 0xF
        RmVal = globals.regs[Rm]
        shiftType = (code & 0b1100000) >> 5
        if (oc2 == 0):
            # data processing - immediate shift
            shiftCnt = (code & 0x1F00) >> 8
            logging.debug("getImmOP2DataProcessing: shiftCnt:" + hex(shiftCnt))
            retVal = doShift(self, shiftType, shiftCnt, RmVal)
        else:
            # data processing - register shift
            if 0x00000080 & code:
                # this is arithmetic or load/store
                return 0
            rs = (code & 0x1E00) >> 9
            logging.debug("getImmOP2DataProcessing: RS:" + hex(rs))
            RsVal = globals.regs[rs]
            shiftCnt = RsVal & 0xFF
            retVal = doShift(self, shiftType, shiftCnt, RmVal)
    else:
        # data processing - immediate - rotate
        immVal = code & 0xFF
        rot = (code & 0xF00) >> 7  # implied *2
        logging.debug("getImmOP2DataProcessing:" +  str("%02X"%immVal) + " rot:" + str("%01X"%rot))
        if rot == 0:
            return 0
        else:
            retVal = doShift(self, ROR, rot, immVal)
    return retVal

# ---------------------------------------------------------------------
def decodeShift(self, code):
    retStr = ""
    shiftType = (code & 0b1100000) >> 5
    if shiftOp == RRX:
        retStr += " RRX"
    if shiftOp == LSL:
        retStr += " LSL"
    if shiftOp == LSR:
        retStr += " LSR"
    if shiftOp == ASR:
        retStr += " ASR"
    if shiftOp == ROR:
        retStr += " ROR"
    return retStr

# ---------------------------------------------------------------------
def getStrOP2DataProcessing(self, code):
    """ for the 3 different types (immediate shift, register shift or immdiate)
        return the string rep """
    oc1 = code >> 25 & 1 # fixed field
    oc2 = code >> 4 & 1 # the other fixed field
    # oc1 = 0 & oc2 = 0 - DP imm shift
    # oc1 = 0 & oc2 = 1 - DP reg shift
    # oc1 = 1 - dp imm
    logging.debug("getStrOP2DataProcessing: oc1:"+ str(oc1)+" oc2:" + str(oc2))
    retStr = ""
    immVal = 0
    if (oc1 == 0):
        retStr = getRd(self, code) + ","
        Rm = code & 0xF
        RmVal = globals.regs[Rm]

        if (oc2 == 0):
            # data processing - immediate shift
            retStr += getRn(self, code)
            retStr += decodeShift(self, code)
            logging.debug(" immediate shift")
            shiftCnt = (code & 0b111110000000) >> 7
            logging.debug("getStrOP2DataProcessing: shiftCnt:" + hex(shiftCnt))
            retStr += " #" + str("%02X"%shiftCnt)
        else:
            # data processing - register shift
            retStr += getRm(self, code)
            retStr += decodeShift(self, code)
            logging.debug(" register shift")
            if 0x00000080 & code:
                # this is arithmetic or load/store
                return ""
            rs = (code & 0x1E00) >> 9
            logging.debug("getStrOP2DataProcessing: RS:" + hex(rs))
            RsVal = globals.regs[rs]
            shiftCnt = RsVal & 0xFF
            retStr += " #" + str("%02X"%immVal)
    else:
        # data processing - immediate - rotate
        retStr = getRd(self, code) + ","
        retStr += getRn(self, code)
        logging.debug(" immediate rotate")
        immVal = code & 0xFF
        rot = (code & 0xF00) >> 7  # implied *2
        logging.debug("getStrOP2DataProcessing:" +  str("%02X"%immVal) + " rot:" + str("%01X"%rot))
        if rot != 0:
            retStr += " ROR"
        retStr += " #" + str("%02X"%immVal)
    return retStr

# ---------------------------------------------------------------------
def doDataInst(self, code, execute):
    global Rd
    global Rn
    global condCode
    logging.debug("doDataInst: code:" + str("%08X"%code) + " Rn:" + str(Rn) + " Rd:" + str(Rd))
    """ opCode is the data instructions """
    if not conditionMet(self, condCode):
        logging.debug("doDataInst: turn off exec because condition is " + hex(condCode) + " met")
        execute = 0
    op2_val = getImmOP2DataProcessing(self, code)
    logging.debug("d_op_code:"+hex(d_op_code)+" op2_val:"+hex(op2_val)+" d:"+str(Rd))
    # output instruction
    s_bit = code >> 20 & 1 # S bit
    # split functionality by opcode; AND, MLA, MUL, STR, LDR, udf, LDR
    retStr = getStrOP2DataProcessing(self, code)
    if (self.d_op_code == 0):
        oc2 = (code >> 4) & 15
        if oc2 == 0b0001:  # # or Rs
            # AND
            if (not execute):
                retStr =+ getStrOP2DataProcessing(self, code)
            else:
                globals.regs[Rd] = op2_val & globals.regs[Rn]
        if oc2 == 0b1001:
            if (code >> 21) & 1 == 1: # A
                retStr = " MLA"
            else:
                retStr = " MUL"
            getRm(self, code)
            getRs(self, code)
            if (execute):
                logging.debug("mul " + hex(globals.regs[Rd]) + " " + hex(globals.regs[Rm]) +  " " + hex(globals.regs[Rs]))
                logging.debug("mul " + str(Rd) + " " + str(Rm) +  " " + str(Rs))
                if (code >> 21) & 1 == 1: # A
                    # MLA Rd = Rm * Rs + Rn
                    globals.regs[Rd] = globals.regs[Rm] * globals.regs[Rs] + globals.regs[Rn]
                else:
                    # MUL Rd = Rm * Rs
                    globals.regs[Rd] = globals.regs[Rm] * globals.regs[Rs]
        if oc2 == 0b1011 and mod == 0:
            retStr = " STR"
        if oc2 == 0b1011 and mod == 1:
            retStr = " LDR"
        if oc2 == 0b1101 and mod == 0:
            retStr = " udf"
        if oc2 == 0b1101 and mod == 1:
            retStr = " LDR"
        if oc2 == 0b1111 and mod == 0:
            retStr = " udf"
        if oc2 == 0b1111 and mod == 1:
            retStr = " LDR"
    carry = ARMCPU.isCarry(self)
    if (self.d_op_code == 1):
        # EOR rd = rn EOR op2
        globals.regs[Rd] = op2_val ^ globals.regs[Rn]
    if (self.d_op_code == 2):
        # SUB rd = rn - op2
        globals.regs[Rd] = globals.regs[Rn] - op2_val
    if (self.d_op_code == 3):
        # RSB rd = op2 - rn
        globals.regs[Rd] = op2_val - globals.regs[Rn]
    if (self.d_op_code == 4):
        # ADD rd = rn + op2
        globals.regs[Rd] = globals.regs[Rn] + op2_val
    if (self.d_op_code == 5):
        # ADC rd = rn + op2 + carry
        globals.regs[Rd] = globals.regs[Rn] + op2_val + carry
        logging.debug("Rd:" + str(Rd) + " Rn:" + str(Rn) + " OP2:" + str(op2_val) + " C:" + str(carry))
    if (self.d_op_code == 6):
        # SBC rd = rn - op2 - not(carry)
        globals.regs[Rd] = globals.regs[Rn] - op2_val - ~carry
    if (self.d_op_code == 7):
        # RSC rd = op2 - rn - not carry
        globals.regs[Rd] = op2_val - globals.regs[Rn] - ~carry
    if (self.d_op_code == 8):
        # TST flags -> rn & op2
        flags = globals.regs[Rn] & op2_val
    if (self.d_op_code == 9):
        # TEQ flags -> rn ^ op2
        flags = globals.regs[Rn] ^ op2_val
    if (self.d_op_code == 10):
        # CMP flags -> rn - op2
        flags = globals.regs[Rn] - op2_val
    if (self.d_op_code == 11):
        # CMN flags -> rn + op2
        flags = globals.regs[Rn] + op2_val
    if (self.d_op_code == 12):
        # ORR rd = rn or op2
        globals.regs[Rd] = op2_val | globals.regs[Rn]
    if (self.d_op_code == 13):
        # MOV rd = op2 (rn ignored)
        globals.regs[Rd] = op2_val
    if (self.d_op_code == 14):
        # BIC rd = rn & !op2 (bit clear)
        globals.regs[Rd] = globals.regs[Rn] & ~op2_val
    if (self.d_op_code == 15):
        # MVN !rd (rn igrnored)
        globals.regs[Rd] = ~op2_val
    if (sCode != 0 and Rd != 15):  # set the flags
        if globals.regs[Rd] == 0:  # Zero
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        else:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] & ~ARMCPU.ZEROBIT
        if carryOut == 1:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        else:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] & ~ARMCPU.CARRYBIT
    return retStr