import unittest
import armv6instrdecode
import globals
import utils
import logging
import ARMCPU
import pdb

#if ConditionPassed(cond) then
#  Rd = Rn + shifter_operand + C Flag
#  if S == 1 and Rd == R15 then
#    if CurrentModeHasSPSR() then
#      CPSR = SPSR
#    else UNPREDICTABLE
#  else if S == 1 then
#    N Flag = Rd[31]
#    Z Flag = if Rd == 0 then 1 else 0
#    C Flag = CarryFrom(Rn + shifter_operand + C Flag)
#    V Flag = OverflowFrom(Rn + shifter_operand + C Flag)

logfile = "TestADC.log"
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestADC(unittest.TestCase):
    """Instructions"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    # don't set cond codes
    # set cond codes
    # imm
    # imm w/ shift
    # reg
    # reg w/ shift
    #          cond00I----Snnnnddd rrrr
    #          33222222222211111111110000000000
    #          10987654321098765432109876543210
    #        0b1110 000 0101 0 0010 0011 00001 00 0 0001 #8130A2E0
    # code = 0b1110 000 0101 0 0011 0011 00001 00 0 0010 #8230A3E0 ADCAL R3, R2, LSL #1
    # code = 0b1110 000 0101 0 0011 0011 00010 00 0 0010 #0231A3E0 ADCAL R3, R2, LSL #2
    # code = 0b1110 000 0101 0 0011 0011 00011 00 0 0010 #8231A3E0 ADCAL R3, R2, LSL #3
    
    # code = 0b1110 000 0101 0 0101 0110 00000 00 0 0100 #0460A5E0  ADCAL R6, R5, R4         @ dp imm shift
    # code = 0b1110 000 0101 0 0110 0110 0100 0001 0101 #1564A6E0   ADCAL R6, R5, LSL R4  @ dp imm reg shift
    # code = 0b1110 001 0101 0 1001 1010 0000 0000 1111 #0FA0A9E2   ADCAL R10, R9, #15        @ dp imm

    #        0b1110 001 0101 0 0001 0000 1010 00000001 #010AA1E2   ADCAL R0, R1, #4096
    
    # data processing - immediate shift
    # data processing - register shift
    # data processing - immediate - rotate

    def testADC_1(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADC_1")
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b11100000101000110011000010000010, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E0A33082 ADC AL    R03, R02 LSL #01", instrStr)

    def testADC_2(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADC_2")
        #        33222222222211111111110000000000
        #        10987654321098765432109876543210
        code = 0b11100000101000110011000100000010  #2000101
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        # RN:3, RD:1 r1 = r3 +
        # Rd = Rn + shifter_operand + C Flag
        self.assertEqual(instrStr, " E0A33102 ADC AL    R03, R02 LSL #02", instrStr)
        logging.debug("2:" + instrStr)
        globals.regs[2] = 3  # 3 shift <--- 2 = 12
        globals.regs[3] = 1
        reg = utils.buildRegValString(self, 2)
        self.assertEqual(reg, "R02:00000003", reg)
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 3)
        self.assertEqual(reg, "R03:0000000D", reg)
    
    def testADC_ImmShft(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADC_ImmShft")
        code = 0b11100010101010011010000000001111
        instrStr = armv6instrdecode.getInstructionFromCode(self,  code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E2A9A00F ADC AL    R10, R09 #0F", instrStr)

        globals.regs[9] = 3  # 3 shift <--- 2 = 12
        globals.regs[10] = 1
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 10)
        self.assertEqual(reg, "R10:00000013", reg)

    def testADC_RegShft(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADC_RegShft")
        code = 0b11100000101001100110010000010101
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E0A66415 ADC AL    R06, R05 LSL R04", instrStr)

        globals.regs[4] = 1  
        globals.regs[5] = 0x40000000
        globals.regs[6] = 1
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 6)
        self.assertEqual(reg, "R06:80000002", reg)

    def testADC_Imm(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testADC_Imm")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0010 1010 0101 0110 0000 0000 0101 - 25=1 4=0 - DP imm
        #---------------------------------------------------------------------------
        code = 0b11100010101001010110000000000101
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E2A56005 ADC AL    R06, R05 #05", instrStr)

        globals.regs[5] = 0x40000000
        globals.regs[6] = 1
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 1)
        reg = utils.buildRegValString(self, 6)
        self.assertEqual(reg, "R06:40000006", reg)
        
if __name__ == "__main__":
    unittest.main()