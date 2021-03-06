import unittest
import armv6instrdecode
import globals
import utils
import logging

logging.basicConfig(filename='TestDecode.log',level=logging.DEBUG)

class TestDecode(unittest.TestCase):
    """Instructions"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    def testBL(self):
        print "TestDecode:testBL"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0x0A000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0x0B000000, 0)
        logging.debug(instrStr)
    
    # don't set cond codes
    # set cond codes
    # imm
    # imm w/ shift
    # reg
    # reg w/ shift
    def testAND(self):
        print "TestDecode:testAND"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000000000000000000000000000, 0)
        logging.debug(instrStr)
        self.assertEqual(instrStr, " 00000000 AND EQ    R00 R00", instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010000000000000000000000000, 0)
        logging.debug(instrStr)
        # --- test AND R0, #3
        globals.regs[0] = 3
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000003", reg)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010000000000000000000011110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000002", reg)
        
    def testEOR(self):
        print "TestDecode:testEOR"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000001000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010001000000000000000000000, 0)
        logging.debug(instrStr)
        # --- test EOR R0, #3
        globals.regs[0] = 3
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000003", reg)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010001000000000000000011110, 1)
        logging.debug(instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:0000001D", reg)

    def testSUB(self):
        print "TestDecode:testSUB"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000010000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010010000000000000000000000, 0)
        logging.debug(instrStr)

    def testRSB(self):
        print "TestDecode:testRSB"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000011000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010011000000000000000000000, 0)
        logging.debug(instrStr)

    def testADD(self):
        print "TestDecode:testADD"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000100000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010100000000000000000000000, 0)
        logging.debug(instrStr)

    def testADC(self):
        print "TestDecode:testADC"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000101000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010101000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testSBC(self):
        print "TestDecode:testSBC"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000110000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010110000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testRSC(self):
        print "TestDecode:testRSC"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000111000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010111000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testTST(self):
        print "TestDecode:testTST"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001000000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011000000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testTEQ(self):
        print "TestDecode:testTEQ"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001001000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011001000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testCMP(self):
        print "TestDecode:testCMP"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001010000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011010000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testCMN(self):
        print "TestDecode:testCMN"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001011000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011011000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testORR(self):
        print "TestDecode:testORR"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001100000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011100000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testMOV(self):
        print "TestDecode:testMOV"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001101000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011101000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testBIC(self):
        print "TestDecode:testBIC"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001110000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011110000000000000000000000, 0)
        logging.debug(instrStr)
        
    def testMVN(self):
        print "TestDecode:testMVN"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000001111000000000000000000000, 0)
        logging.debug(instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000011111000000000000000000000, 0)
        logging.debug(instrStr)

if __name__ == "__main__":
    unittest.main()