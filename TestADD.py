import unittest
import armv6instrdecode
import globals
import utils
import logging
import ARMCPU
import pdb

# if ConditionPassed(cond) then
#   Rd = Rn + shifter_operand
#   if S == 1 and Rd == R15 then
#     if CurrentModeHasSPSR() then
#       CPSR = SPSR
#     else UNPREDICTABLE
#   else if S == 1 then
#     N Flag = Rd[31]
#     Z Flag = if Rd == 0 then 1 else 0
#     C Flag = CarryFrom(Rn + shifter_operand)
#     V Flag = OverflowFrom(Rn + shifter_operand)

logfile = "TestADD.log"
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestADD(unittest.TestCase):
    """Instructions"""

    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    # E2810A01 010A81E2 	    ADDAL R0, R1, #4096
    # E289A00F 0FA089E2 	    ADDAL R10, R9, #15          @ dp imm
    # E0856004 046085E0 	    ADDAL R6, R5, R4          @ dp imm shift
    # E0866415 156486E0 	    ADDAL R6, R5, LSL R4      @ dp imm reg shift

    def testADD_Imm1(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADD_Imm1")
        code = 0xE2810A01  # ADDAL R0, R1, #4096
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E2810A01 ADD AL    R00, R01 #01", instrStr)
        logging.debug("2:" + instrStr)
        globals.regs[1] = 3  # 3 shift <--- 2 = 12
        globals.regs[0] = 1
        reg = utils.buildRegValString(self, 1)
        self.assertEqual(reg, "R01:00000003", reg)
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00001003", reg)

    def testADD_Imm2(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADD_Imm2")
        #        33222222222211111111110000000000
        #        10987654321098765432109876543210
        code = 0xE289A00F  #2000101
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        # RN:3, RD:1 r1 = r3 +
        # Rd = Rn + shifter_operand + C Flag
        self.assertEqual(instrStr, " E289A00F ADD AL    R10, R09 #0F", instrStr)
        logging.debug("2:" + instrStr)
        globals.regs[9] = 3  # 3 shift <--- 2 = 12
        globals.regs[10] = 1
        reg = utils.buildRegValString(self, 9)
        self.assertEqual(reg, "R09:00000003", reg)
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 10)
        self.assertEqual(reg, "R10:00000012", reg)

    def testADD_ImmShft(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADD_ImmShft")
        code = 0xE0856004
        instrStr = armv6instrdecode.getInstructionFromCode(self,  code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E0856004 ADD AL    R06, R05 R04", instrStr)

        globals.regs[4] = 3  # 3 shift <--- 2 = 12
        globals.regs[5] = 1
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 6)
        self.assertEqual(reg, "R06:00000009", reg)

    def testADD_RegShft(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADD_RegShft")
        code = 0xE0866415
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E0866415 ADD AL    R06, R05 LSL R04", instrStr)

        globals.regs[4] = 1
        globals.regs[5] = 0x40000000
        globals.regs[6] = 1
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 6)
        self.assertEqual(reg, "R06:80000001", reg)

    def testADD_setflag_c(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADD_setflag_c - should produce an carry")
        code = 0xE2910001  # ADDALS R0, R1, #1
        globals.regs[1] = 0xFFFFFFFF
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        # N Flag = Rd[31]
        self.assertEqual(1, globals.regs[globals.CPSR] & ARMCPU.NEGATIVEBIT == 0, 1)
        # Z Flag = if Rd == 0 then 1 else 0
        self.assertEqual(1, globals.regs[globals.CPSR] & ARMCPU.ZEROBIT > 0, 1)
        # C Flag = CarryFrom(Rn + shifter_operand)
        # V Flag = OverflowFrom(Rn + shifter_operand)
        #logging.debug(hex(globals.regs[globals.CPSR] & ARMCPU.OVERBIT))
        self.assertEqual(1, globals.regs[globals.CPSR] & ARMCPU.CARRYBIT > 0, 1)

    def testADD_setflag_o(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADD_setflag_o - should produce an overflow")
        code = 0xE2910001  # ADDALS R0, R1, #1
        globals.regs[1] = 0x7FFFFFFF
        globals.regs[0] = 0
        globals.regs[globals.CPSR] = 0
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:80000000", reg)
        # N Flag = Rd[31]
        self.assertEqual(1, globals.regs[globals.CPSR] & ARMCPU.NEGATIVEBIT > 0, 1)
        # Z Flag = if Rd == 0 then 1 else 0
        self.assertEqual(1, globals.regs[globals.CPSR] & ARMCPU.ZEROBIT == 0, 1)
        # C Flag = CarryFrom(Rn + shifter_operand)
        # V Flag = OverflowFrom(Rn + shifter_operand)
        #logging.debug(hex(globals.regs[globals.CPSR] & ARMCPU.OVERBIT))
        self.assertEqual(1, globals.regs[globals.CPSR] & ARMCPU.OVERBIT > 0, 1)

if __name__ == "__main__":
    unittest.main()