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

logfile = "TestGetImm_imm.log"
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestGetImm_imm(unittest.TestCase):
    """Instructions"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    def testGetImm_1(self):
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_1")
        # 32 bit imm
        #        33222222222211111111110000000000
        #        10987654321098765432109876543210
        code = 0b00000010000000000000000000000001
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_1:1:" + instrStr)
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_1:1:" + str(val))
        self.assertEqual(val, 1, val)
        #        33222222222211111111110000000000
        #        10987654321098765432109876543210
        code = 0b00000010000000000000000100000001  #2000101
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_1:2:" + instrStr)
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_1:2:" + str("%08X"%val))
        self.assertEqual(val, 1073741824, hex(val))
    
    def testGetImm_1_carry(self):
        # NOTE: thought that the ROR used the carry, only RRX uses the carry
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_1_carry")
        globals.regs[globals.CPSR] = globals.regs[globals.CPSR] | ARMCPU.CARRYBIT
        # 32 bit imm
        #        33222222222211111111110000000000
        #        10987654321098765432109876543210
        code = 0b00000010000000000000000000000001
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_1_carry:set:" + str(val))
        self.assertEqual(val, 1, hex(val))
        # carry clear
        globals.regs[globals.CPSR] = 0
        # 32 bit imm
        #        33222222222211111111110000000000
        #        10987654321098765432109876543210
        code = 0b00000010000000000000000100000001
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_1_carry:clear:" + str(val))
        self.assertEqual(val, 1073741824, hex(val))
    
    def testGetImm_1_paternal(self):
        # Some values of <immediate> have more than one possible encoding.
        # For example, a value of 0x3F0
        # could be encoded as: immed_8 == 0x3F, rotate_imm == 0xE
        # or as:               immed_8 == 0xFC, rotate_imm == 0xF
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_1_paternal")
        code = 0b00000010000000000000111000111111
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_1_paternal:1:" + str(val))
        self.assertEqual(val, 1008, val)
        code = 0b00000010000000000000111111111100
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_1_paternal:2:" + str(val))
        self.assertEqual(val, 1008, val)

    def testGetImm_2_1(self):
        # OP2:  SftIMss0-Rm-  # Bit 25 = 0, 4 = 0 # immd shift
        # ANDAL R1, R9, R2, OP #1
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_2_1")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 1111 1000 0110 E0A5FA86 865FA5E0 ADCAL R5, R6, LSL #31 @ Logical shift right     Rm LSR #5bit_Imm
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101111110000110
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_2:1:" + instrStr)
        self.assertEqual(instrStr, " E0A55F86 ADC AL    R05, R06 LSL #1F", instrStr)

        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_2:1:" + str(val))
        self.assertEqual(val, 2147483648, val)

    def testGetImm_2_2(self):
        # OP2:  SftIMss0-Rm-  # Bit 25 = 0, 4 = 0 # immd shift
        # ANDAL R1, R9, R2, OP #1
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_2_2")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 1111 1010 0110 E0A5FAA6 A65FA5E0 ADCAL R5, R6, LSR #31 @ Arithmetic shift right  Rm ASR #5bit_Imm
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101111110100110
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_2:2:" + instrStr)
        self.assertEqual(instrStr, " E0A55FA6 ADC AL    R05, R06 LSR #1F", instrStr)

        globals.regs[6] = 2147483648
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_2:2:" + str(val))
        self.assertEqual(val, 1, val)

    def testGetImm_2_3(self):
        # OP2:  SftIMss0-Rm-  # Bit 25 = 0, 4 = 0 # immd shift
        # ANDAL R1, R9, R2, OP #1
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_2_3")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 1111 1100 0110 E0A5FAC6 C65FA5E0 ADCAL R5, R6, ASR #31 @ Rotate right            Rm ROR #5bit_Imm
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101111111000110
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_2:3:" + instrStr)
        self.assertEqual(instrStr, " E0A55FC6 ADC AL    R05, R06 ASR #1F", instrStr)

        globals.regs[6] = ARMCPU.HIGHBIT
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_2:3:" + str(val))
        self.assertEqual(val, 4294967295, val)

    def testGetImm_2_4(self):
        # OP2:  SftIMss0-Rm-  # Bit 25 = 0, 4 = 0 # immd shift
        # ANDAL R1, R9, R2, OP #1
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_2_4")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 1111 1110 0110 E0A55FE6 E65FA5E0 ADCAL R5, R6, ROR #31 @ Register                Rm
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101111111100110
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_2:4:" + instrStr)
        self.assertEqual(instrStr, " E0A55FE6 ADC AL    R05, R06 ROR #1F", instrStr)

        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_2:4:" + str(val))
        self.assertEqual(val, 2, val)

    def testGetImm_2_5(self):
        # OP2:  SftIMss0-Rm-  # Bit 25 = 0, 4 = 0 # immd shift
        # ANDAL R1, R9, R2, OP #1
        logging.debug("\n----------------------------------------------------------")
        logging.debug("TestDecode:testGetImm_2_5")
        #   1098 7654 3210 9876 5432 1098 7654 3210
        # 0b1110 0000 1010 0101 0101 0000 0000 0110 E0A55006 0650A5E0 ADCAL R5, R6          @ Logical shift left      Rm LSL Rs
        #---------------------------------------------------------------------------
        code = 0b11100000101001010101000000000110
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("testGetImm_2:5:" + instrStr)
        self.assertEqual(instrStr, " E0A55006 ADC AL    R05, R06", instrStr)

        globals.regs[5] = 1
        globals.regs[6] = 1
        val = armv6instrdecode.getOP2DataProcessing(self, code, 0)
        logging.debug("testGetImm_2:5:" + str(val))
        self.assertEqual(val, 2, val)
        
if __name__ == "__main__":
    unittest.main()