import unittest
import armv6instrdecode
import globals
import utils
import logging
import ARMCPU
import pdb

# cond00I----Snnnnddd rrrr
#   3322 2222 2222 1111 1111 1100 0000 0000
#   1098 7654 3210 9876 5432 1098 7654 3210
# get imm 1
# 0b1110 0010 1010 0101 0101 1010 0000 0010 E2A55A02 025AA5E2 ADCAL R5, #8192       @ Logical shift left      Rm LSL #5bit_Imm
#
# get imm 2
# 0b1110 0000 1010 0101 0101 1111 1000 0110 E0A55F86 865FA5E0 ADCAL R5, R6, LSL #31 @ Logical shift right     Rm LSR #5bit_Imm
# 0b1110 0000 1010 0101 0101 1111 1010 0110 E0A55FA6 A65FA5E0 ADCAL R5, R6, LSR #31 @ Arithmetic shift right  Rm ASR #5bit_Imm
# 0b1110 0000 1010 0101 0101 1111 1100 0110 E0A55FC6 C65FA5E0 ADCAL R5, R6, ASR #31 @ Rotate right            Rm ROR #5bit_Imm
# 0b1110 0000 1010 0101 0101 1111 1110 0110 E0A55FE6 E65FA5E0 ADCAL R5, R6, ROR #31 @ Register                Rm
# 0b1110 0000 1010 0101 0101 0000 0000 0110 E0A55006 0650A5E0 ADCAL R5, R6          @ Logical shift left      Rm LSL Rs
#
# get imm 3
# 0b1110 0000 1010 0101 0101 0110 0001 0100 E0A55614 1456A5E0 ADCAL R5, R4, LSL R6  @ Logical shift right     Rm LSR Rs
# 0b1110 0000 1010 0101 0101 0110 0011 0100 E0A55634 3456A5E0 ADCAL R5, R4, LSR R6  @ Arithmetic shift right  Rm ASR Rs
# 0b1110 0000 1010 0101 0101 0110 0101 0100 E0A55654 5456A5E0 ADCAL R5, R4, ASR R6  @ Rotate right            Rm ROR Rs
# 0b1110 0000 1010 0101 0101 0110 0111 0100 E0A55674 7456A5E0 ADCAL R5, R4, ROR R6  @ Rotate right extended   Rm RRX
# 0b1110 0000 1010 0101 0101 0110 0110 0110 E0A55066 6650A5E0 ADCAL R5, R6, RRX

logfile = "TestGetImm_reg.log"
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestGetImm_reg(unittest.TestCase):
    """Instructions"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    def testGetImm_3_1(self):
        # OP3:  -Rs-0ss1-Rm-  # Bit 25 = 0, 4 = 1 # register shift
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_3_1")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 0110 0001 0100 E0A55614 1456A5E0 ADCAL R5, R4, LSL R6  @ Logical shift right     Rm LSR Rs
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101011000010100  # 
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_3:1:" + instrStr)
        self.assertEqual(instrStr, " E0A55614 ADC AL    R05, R04 LSL R06", instrStr)

        globals.regs[4] = 1 # this reg to get shifted
        globals.regs[6] = 2 # by this value
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:1:" + str(val))
        self.assertEqual(val, 4, val)
        
    def testGetImm_3_2(self):
        # OP3:  -Rs-0ss1-Rm-  # Bit 25 = 0, 4 = 1 # register shift
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_3_2")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 0110 0011 0100 E0A55634 3456A5E0 ADCAL R5, R4, LSR R6  @ Arithmetic shift right  Rm ASR Rs
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101011000110100  # 
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_3:2:" + instrStr)
        self.assertEqual(instrStr, " E0A55634 ADC AL    R05, R04 LSR R06", instrStr)

        globals.regs[4] = 2
        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:2:" + str(val))
        self.assertEqual(val, 1, val)
        
    def testGetImm_3_3(self):
        # OP3:  -Rs-0ss1-Rm-  # Bit 25 = 0, 4 = 1 # register shift
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_3_3")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 0110 0101 0100 E0A55654 5456A5E0 ADCAL R5, R4, ASR R6  @ Rotate right            Rm ROR Rs
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101011001010100  # 
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_3:3:" + instrStr)
        self.assertEqual(instrStr, " E0A55654 ADC AL    R05, R04 ASR R06", instrStr)

        globals.regs[4] = 2
        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:3a:" + str(val))
        self.assertEqual(val, 1, val)
        
        globals.regs[4] = 0x80000000
        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:3b:" + str(val))
        self.assertEqual(val, 0xC0000000, val)
        
    def testGetImm_3_4(self):
        # OP3:  -Rs-0ss1-Rm-  # Bit 25 = 0, 4 = 1 # register shift
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_3_4")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 0110 0111 0100 E0A55674 7456A5E0 ADCAL R5, R4, ROR R6  @ Rotate right extended   Rm RRX
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101011001110100  # 
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_3:4:" + instrStr)
        self.assertEqual(instrStr, " E0A55674 ADC AL    R05, R04 ROR R06", instrStr)

        globals.regs[4] = 1
        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:4:" + str(val))
        self.assertEqual(val, 0x80000000, val)
        
    def testGetImm_3_5(self):
        # OP3:  -Rs-0ss1-Rm-  # Bit 25 = 0, 4 = 1 # register shift
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_3_5")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 0000 0110 0110 E0A55066 6650A5E0 ADCAL R5, R6, RRX
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101000001100110  # 
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_3:5:" + instrStr)
        self.assertEqual(instrStr, " E0A55066 ADC AL    R05, R06 RRX", instrStr)
        
        logging.debug("\n----------------------------------------------------------")
        # carry set - be bit 32
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        globals.regs[6] = 0  # ROR carry in
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:5a:" + str(val))
        self.assertEqual(val, 0x80000000, val)
        cbit = (globals.regs[globals.CPSR] & ARMCPU.CARRYBIT) == 0 # shift out is 0 -false
        self.assertEqual(cbit, 0, cbit)
                
        logging.debug("\n----------------------------------------------------------")
        # carry clear
        globals.regs[globals.CPSR] = 0
        globals.regs[6] = 0x80000000 # ROR clear carry
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:5b:" + str(val))
        self.assertEqual(val, 0x40000000, val)
        
        logging.debug("\n----------------------------------------------------------")
        # carry out
        globals.regs[globals.CPSR] = 0
        globals.regs[6] = 1 # ROR clear set
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_3:5c:" + str(val))
        cbit = (globals.regs[globals.CPSR] & ARMCPU.CARRYBIT) > 0 # shift out is 0 -false
        self.assertEqual(cbit, 1, cbit)
        
if __name__ == "__main__":
    unittest.main()