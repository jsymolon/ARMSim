import unittest
import ARMCPU
import arm7instrdecode
import globals
import utils
import logging

logfile = 'TestCondExec.log'
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

# 0000 	EQ 	Equal / equals zero 	             Z
# 0001 	NE 	Not equal 	                     !Z
# 0010 	CS / HS Carry set / unsigned higher or same  C
# 0011 	CC / LO Carry clear / unsigned lower 	     !C
# 0100 	MI 	Minus / negative 	             N
# 0101 	PL 	Plus / positive or zero 	     !N
# 0110 	VS 	Overflow 	                     V
# 0111 	VC 	No overflow 	                     !V
# 1000 	HI 	Unsigned higher 	             C and !Z
# 1001 	LS 	Unsigned lower or same 	             !C or Z
# 1010 	GE 	Signed greater than or equal 	     N == V
# 1011 	LT 	Signed less than 	             N != V
# 1100 	GT 	Signed greater than 	             !Z and (N == V)
# 1101 	LE 	Signed less than or equal 	     Z or (N != V)
# 1110 	AL 	Always (default) 	             any

class TestDecode(unittest.TestCase):
    """Instructions"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
        
    def testCondMet(self):
        # No condition met (always)
        globals.regs[globals.CPSR] = 0
        cm = arm7instrdecode.conditionMet(self, ARMCPU.CC_AL)
        self.assertEqual(cm, 1L, cm)
        # EQ
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        logging.debug(utils.getCSPRString(self))
        cm = arm7instrdecode.conditionMet(self, ARMCPU.CC_EQ)
        self.assertEqual(cm, 1L, cm)

    def testCondExec(self):
        """ basic test:
            set cond code
            setup reg with value
            setup mov imm with value2
            exec mov
            check reg for """
        # 0000 	EQ 	Equal / equals zero 	             Z
        logging.debug("0000 	EQ 	Equal / equals zero 	             Z")
        logging.debug("--- Bit set, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00000011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00000011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)

        # 0001 	NE 	Not equal 	                     !Z
        logging.debug("0001 	NE 	Not equal 	                     !Z")
        logging.debug("--- Bit clear, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00010011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00010011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 0010 	CS / HS Carry set / unsigned higher or same  C
        logging.debug("0010 	CS / HS Carry set / unsigned higher or same  C")
        logging.debug("--- Bit set, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00100011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00100011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 0011 	CC / LO Carry clear / unsigned lower 	     !C
        logging.debug("0011 	CC / LO Carry clear / unsigned lower 	     !C")
        logging.debug("--- Bit clear, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00110011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b00110011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 0100 	MI 	Minus / negative 	             N
        logging.debug("0100 	MI 	Minus / negative 	             N")
        logging.debug("--- Bit set, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.NEGATIVEBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01000011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01000011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 0101 	PL 	Plus / positive or zero 	     !N
        logging.debug("0101 	PL 	Plus / positive or zero 	     !N")
        logging.debug("--- Bit clear, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01010011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.NEGATIVEBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01010011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 0110 	VS 	Overflow 	                     V
        logging.debug("0110 	VS 	Overflow 	                     V")
        logging.debug("--- Bit set, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.OVERBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01100011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01100011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 0111 	VC 	No overflow 	                     !V
        logging.debug("0111 	VC 	No overflow 	                     !V")
        logging.debug("--- Bit clear, exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01110011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit not set, skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.OVERBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b01110011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 1000 	HI 	Unsigned higher 	             C and !Z
        logging.debug("1000 	HI 	Unsigned higher 	             C and !Z")
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10000011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit , skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10000011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 1001 	LS 	Unsigned lower or same 	             !C or Z
        logging.debug("1001 	LS 	Unsigned lower or same 	             !C or Z")
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10010011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit , skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10010011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 1010 	GE 	Signed greater than or equal 	     N == V
        logging.debug("1010 	GE 	Signed greater than or equal 	     N == V")
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.NEGATIVEBIT | ARMCPU.OVERBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10100011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10100011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)

        logging.debug("--- Bit , skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.NEGATIVEBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10100011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 1011 	LT 	Signed less than 	             N != V
        logging.debug("1011 	LT 	Signed less than 	             N != V")
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.NEGATIVEBIT | ARMCPU.OVERBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10100011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10100011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)

        logging.debug("--- Bit , skip exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.NEGATIVEBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b10100011101000000000000011111110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        
        # 1100 	GT 	Signed greater than 	             !Z and (N == V)
        logging.debug("1100 	GT 	Signed greater than 	             !Z and (N == V)")
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b11000011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)
        
        # 1101 	LE 	Signed less than or equal 	     Z or (N != V)
        logging.debug("1101 	LE 	Signed less than or equal 	     Z or (N != V)")
        logging.debug("--- Bit , exec")
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.ZEROBIT
        instrStr = arm7instrdecode.getInstructionFromCode(self, 0b11010011101000000000000011111111, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:000000FF", reg)

        # 1110 	AL 	Always (default) 	             any

if __name__ == "__main__":
    unittest.main()