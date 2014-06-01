#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 3
import globals

condCode = 0
sCode = 0
iCode = 0
shiftOp = 0
shiftCnt = 0
destReg = 0
immCnt = 0
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
def getSetValue(self, bitmask, shift, baseval, value): #
    if value is None: # get
        return ((baseval & bitmask) >> shift)
    else:   #set
        return ((baseval & (~ bitmask)) | (value << shift))

# ---------------------------------------------------------------------
def getInstructionFromAddress(self, addr, memory):
    # read memory
    #code = 305419896 #0x12345678
    #code = 234881024 #0E00000000 - 27-25 bits
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
    print "addr:"+hex(addr)
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
    self.opcode = code >> 21 & 15
    getICode(self, code)
    if (self.opcode == 0):
        oc2 = code >> 4 & 15
        mod = code >> 20 & 1
        #print "code:" + hex(code) + " oc2:" + hex(oc2) +  " mod:" + hex(mod)
        if oc2 == int("0", 16):  # # or Rs
            retStr = " AND"
        if oc2 == int("9", 16):
            if (code >> 21) & 1 == 1: # A
                retStr = " MLA"
            else:
                retStr = " MUL"
        if oc2 == int("B", 16) & mod == 0:
            retStr = " STR"
        if oc2 == int("B", 16) & mod == 1:
            retStr = " LDR"
        if oc2 == int("D", 16) & mod == 0:
            retStr = " udf"
        if oc2 == int("D", 16) & mod == 1:
            retStr = " LDR"
        if oc2 == int("F", 16) & mod == 0:
            retStr = " udf"
        if oc2 == int("F", 16) & mod == 1:
            retStr = " LDR"
    if (self.opcode == 1):
        retStr = " EOR"
    if (self.opcode == 2):
        retStr = " SUB"
    if (self.opcode == 3):
        retStr = " RSB"
    if (self.opcode == 4):
        retStr = " ADD"
    if (self.opcode == 5):
        retStr = " ADC"
    if (self.opcode == 6):
        retStr = " SBC"
    if (self.opcode == 7):
        retStr = " RSC"
    if (self.opcode == 8):
        retStr = " TST"
    if (self.opcode == 9):
        retStr = " TEQ"
    if (self.opcode == 10):
        retStr = " CMP"
    if (self.opcode == 11):
        retStr = " CMN"
    if (self.opcode == 12):
        retStr = " ORR"
    if (self.opcode == 13):
        retStr = " MOV"
    if (self.opcode == 14):
        retStr = " BIC"
    if (self.opcode == 15):
        retStr = " MVN"
    retStr += getCondCode(self, code) + getSCode(self, code) + getRd(self, code)
    getRn(self, code)
    retStr += doOperand2(self, code, execute)
    return retStr

# ---------------------------------------------------------------------
def inst01decode(self, code, execute):
    """ decode the bits at 27-26 = 01
    """
    strI =    int("0E500000", 16)
    strIv =   int("04000000", 16)
    if (code & strI == strIv):
        return " STR  "
    strIBv =  int("04400000", 16)
    if (code & strI == strIBv):
        return " STRB "
    strIT =   int("0F700000", 16)
    strITv =  int("04200000", 16)
    if (code & strIT == strITv):
        return " STRT "
    strIBT =  int("0F700010", 16)
    strIBTv = int("04600000", 16)
    if (code & strIBT == strIBTv):
        return " STRBT "
    return "      "

# ---------------------------------------------------------------------
def inst10decode(self, code, execute):
    """ decode the bits at 27-26 = 10
    """
    if (code & int("02000000", 16) > 0):
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
    if code & int("00800000", 16): # handle negative bit
        offset = (int("00ffffff", 16) - (code & int("00ffffff", 16)))
        offset *= -1
        addr = (offset * 4) + 4 + self.addr # add addr to make the relative display work,
                                        # if exec, addr should = PC
    else:
        offset = code & int("007fffff", 16) #strip neg bit will pick up later
        addr = (offset * 4) + 8 + self.addr # add addr to make the relative display work,
                                        # if exec, addr should = PC
    print "off:" + hex(offset) + " addr:" + str(addr) + " exe:" + str(execute)
    if (execute):
        if (code & int("01000000", 16) > 0): # branch & link vs branch
            globals.regs[14] = globals.regs[globals.PC]
        globals.regs[globals.PC] = addr

    if (code & int("01000000", 16) > 0): # branch & link vs branch
        return " BL"+getCondCode(self, code)+"      "+str("%08X"%addr)
    else:
        return " B"+getCondCode(self, code)+"      "+str("%08X"%addr)

# ---------------------------------------------------------------------
def doDataInst(self, Rd, Rn, shiftOp, shiftAmt, RmVal):
    global Rm
    global Rs
    """ opCode is the data instructions """
    op2 = doShift(self, shiftOp, shiftAmt, RmVal)
    print "op2:"+str(op2)+" d:"+str(Rd)
    if (self.opcode == 0):
        oc2 = code >> 4 & 15
        mod = code >> 20 & 1
        print "code:" + hex(code) + " oc2:" + hex(oc2) +  " mod:" + hex(mod)
        if oc2 == int("0", 16):  # # or Rs
           # AND rd = rn and op2
           globals.regs[Rd] = op2 & globals.regs[Rn]
        if oc2 == int("9", 16):
            getRm(self, code)
            getRs(self, code)
            print "mul " + hex(globals.regs[Rd]) + " " + hex(globals.regs[Rm]) +  " " + hex(globals.regs[Rs])
            print "mul " + str(Rd) + " " + str(Rm) +  " " + str(Rs)
            if (code >> 21) & 1 == 1: # A
                # MLA Rd = Rm * Rs + Rn
                globals.regs[Rd] = globals.regs[Rm] * globals.regs[Rs] + globals.regs[Rn]
            else:
                # MUL Rd = Rm * Rs
                globals.regs[Rd] = globals.regs[Rm] * globals.regs[Rs]
        if oc2 == int("B", 16) & mod == 0:
            retStr = " STR"
        if oc2 == int("B", 16) & mod == 1:
            retStr = " LDR"
        if oc2 == int("D", 16) & mod == 0:
            retStr = " udf"
        if oc2 == int("D", 16) & mod == 1:
            retStr = " LDR"
        if oc2 == int("F", 16) & mod == 0:
            retStr = " udf"
        if oc2 == int("F", 16) & mod == 1:
            retStr = " LDR"
    if (self.opcode == 1):
        # EOR rd = rn EOR op2
        globals.regs[Rd] = op2 ^ globals.regs[Rn]
    if (self.opcode == 2):
        # SUB rd = rn - op2
        globals.regs[Rd] = globals.regs[Rn] - op2
    if (self.opcode == 3):
        # RSB rd = op2 - rn
        globals.regs[Rd] = op2 - globals.regs[Rn]
    if (self.opcode == 4):
        # ADD rd = rn + op2
        globals.regs[Rd] = globals.regs[Rn] + op2
    if (self.opcode == 5):
        # ADC rd = rn + op2 + carry
        globals.regs[Rd] = globals.regs[Rn] + op2 + carry
    if (self.opcode == 6):
        # SBC rd = rn - op2 - not(carry)
        globals.regs[Rd] = globals.regs[Rn] - op2 - ~carry
    if (self.opcode == 7):
        # RSC rd = op2 - rn - not carry
        globals.regs[Rd] = op2 - globals.regs[Rn] - ~carry
    if (self.opcode == 8):
        # TST flags -> rn & op2
        flags = globals.regs[Rn] & op2
    if (self.opcode == 9):
        # TEQ flags -> rn ^ op2
        flags = globals.regs[Rn] ^ op2
    if (self.opcode == 10):
        # CMP flags -> rn - op2
        flags = globals.regs[Rn] - op2
    if (self.opcode == 11):
        # CMN flags -> rn + op2
        flags = globals.regs[Rn] + op2
    if (self.opcode == 12):
        # ORR rd = rn or op2
        globals.regs[Rd] = op2 | globals.regs[Rn]
    if (self.opcode == 13):
        # MOV rd = op2 (rn ignored)
        globals.regs[Rd] = op2
    if (self.opcode == 14):
        # BIC rd = rn & !op2 (bit clear)
        globals.regs[Rd] = globals.regs[Rn] & ~op2
    if (self.opcode == 15):
        # MVN !rd (rn igrnored)
        globals.regs[Rd] = ~op2
    if sCode != 0:  # set the flags
        if globals.regs[Rd] == 0:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | globals.ZEROBIT
        else:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] & ~globals.ZEROBIT
        if carryOut == 1:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | globals.CARRYBIT
        else:
            globals.regs[globals.CPSR] = globals.regs[globals.CPSR] & ~globals.CARRYBIT
    return

# ---------------------------------------------------------------------
def getCondCode(self, code):
    global condCode
    condCode = int(code >> 28)
    if (condCode == 0):
        return " EQ"
    if (condCode == 1):
        return " NE"
    if (condCode == 2):
        return " HS"
    if (condCode == 3):
        return " LO"
    if (condCode == 4):
        return " MI"
    if (condCode == 5):
        return " PL"
    if (condCode == 6):
        return " VS"
    if (condCode == 7):
        return " VC"
    if (condCode == 8):
        return " HI"
    if (condCode == 9):
        return " LS"
    if (condCode == 10):
        return " GE"
    if (condCode == 11):
        return " LT"
    if (condCode == 12):
        return " GT"
    if (condCode == 13):
        return " LE"
    if (condCode == 14):
        return " AL"
    if (condCode == 15):
        return " NV"
    return "   "

# ---------------------------------------------------------------------
def conditionMet(self):
    if (globals.regs[CSPR] ^ condCode == 0):
        return True;
    return False

# ---------------------------------------------------------------------
def getSCode(self, code):
    """ data processing - tells if cond codes are affected """
    global sCode
    sCode = (code >> 20) & int("1",16)
    if (sCode == 1):
        return "S  "
    return "   "

# ---------------------------------------------------------------------
def getICode(self, code):
    """ data processing - tells if op is immediate """
    global iCode
    iCode = (code >> 25) & int("1",16)

# ---------------------------------------------------------------------
def getRn(self, code):
    global Rn
    Rn = code & int("000F0000", 16)
    Rn = (Rn >> 16)
    return " R"+str("%02d"%Rn)

# ---------------------------------------------------------------------
def getRd(self, code):
    global Rd
    Rd = code & int("0000F000", 16)
    Rd = (Rd >> 12)
    return " R"+str("%02d"%Rd)

# ---------------------------------------------------------------------
def getRs(self, code):
    global Rs
    Rs = code & int("00000F00", 16)
    Rs = (Rs >> 8)
    return " R"+str("%02d"%Rs)

# ---------------------------------------------------------------------
def getRm(self, code):
    global Rm
    Rm = code & int("0000000F", 16)
    return " R"+str("%02d"%Rm)

# ---------------------------------------------------------------------
def doShift(self, shiftOp, shiftAmt, Rm):
    """ function to do the barrel shifts
    """
    global carryOut
    carryIn = 0
    carryOut = 0
    if shiftOp == ASR:
        if Rm & globals.HIGHBIT > 0:
            carryIn = 1
    if shiftOp == RRX:
        if globals.regs[globals.CPSR] & globals.CARRYBIT > 0:
            carryIn = 1
    for x in range(0, shiftAmt):
        if shiftOp == LSL:
            carryOut = Rm & globals.HIGHBIT
            # trying to shift the high bit out will cause a "long it too large", clear it
            Rm = Rm & ~globals.NEGATIVEBIT
            Rm = Rm << 1
            print str(Rm)
        if shiftOp == LSR:
            carryOut = Rm & 1
            Rm = Rm >> 1
        if shiftOp == ASR:
            carryOut = Rm & 1
            Rm = Rm >> 1
            if carryIn:
                Rm = Rm | globals.HIGHBIT
            print hex(Rm)
        if shiftOp == ROR:
            carryOut = Rm & 1
            Rm = Rm >> 1
            if carryOut > 0:
                Rm = Rm | globals.HIGHBIT
    # RRX only does 1 loop
    if shiftOp == RRX:
        carryOut = Rm & 1
        Rm = Rm >> 1
        if carryOut > 0:
            Rm = Rm | globals.HIGHBIT
    return Rm  # actually OP2

# ---------------------------------------------------------------------
def doOperand2(self, code, execute):
    global OP2
    global immCnt
    global Rs
    global Rm
    global Rd
    global Rn
    global shiftOp
    global iCode
    outstr = ""
    OP2 = code & int("FFF", 16)
    # rm OP amt
    shiftAmt = 0
    if iCode == 0:
        #shift (11-4) RM (3-0)
        outstr = getRm(self, code)
        shiftOp = (OP2 >> 5) & 3
        op = ""
        if shiftOp == 0:
            op = " LSL"
        if shiftOp == 1:
            op = " LSR"
        if shiftOp == 2:
            op = " ASR"
        if shiftOp == 3:
            op = " ROR"              # 1111 1110 ----
        RsImm = OP2 & int("F80", 16) # 1098 7654 3210
        if OP2 & int("010",16) == 0:
            #5-bit unsigned
            immCnt = (RsImm >> 7)
            if (shiftOp == 1 or shiftOp == 2) and immCnt == 0:  # equals LSR #32
                immCnt = 32
            shiftAmt = immCnt
            if shiftOp == 3 and immCnt == 0:
                outstr += " rrx"
                shiftOp = RRX
                immCnt = 1
            else:
                if shiftOp != 0 or immCnt != 0:
                    outstr += op + str(" #%02d"%immCnt)
        else:
            # Rs
            Rs = (RsImm >> 8)
            shiftAmt = globals.regs[Rs]
            outstr += op + " R"+str("%02d"%Rs)
        if execute:
            doDataInst(self, Rd, Rn, shiftOp, shiftAmt, globals.regs[Rm])
    else:
        #rotate (11-8) imm (7-0)  -> #(1<<5) -> #(imm<<shft)
        RotImm = (OP2 & int("F00", 16) >> 12)
        if RotImm != 0:
            outstr += "("+str(RotImm)+"<<"
        outstr += getImm(self, OP2, 8)
        if RotImm != 0:
            outstr += ")"
        shiftOp = ROR
        if execute:
            doDataInst(self, Rd, Rn, shiftOp, RotImm * 2, immCnt)
    return outstr

# ---------------------------------------------------------------------
def getRm(self, code):
    global Rm
    Rm = code & int("0000000F", 16)
    return " R"+str("%02d"%Rm)

# ---------------------------------------------------------------------
def getImm(self, code, bits):
    global immCnt
    if bits == 8:
        immCnt = code & int("FF", 16)
        return str(" #%02d"%immCnt)
    immCnt = code & int("FFF", 16)
    return str(" #%02d"%immCnt)

# ---------------------------------------------------------------------
def getShiftOp(self, code):  # or "rotate" field
    """ data processing - immediate op - rotate field """

    return "    "

# ---------------------------------------------------------------------
def getShiftImm(self, code):
    global shiftCnt
    shiftCnt = (code >> 7) & int("1F",16)
    return " #%02X" % shiftCnt
