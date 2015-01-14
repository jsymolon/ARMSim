import unittest
import armv6instrdecode
import globals
import utils
import logging

logfile = "TestAND.log"
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestAND(unittest.TestCase):
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
    def testAND(self):
        print "TestDecode:testAND"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000000000000000000000000000000, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " 00000000 AND EQ    R00 R00", instrStr)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010000000000000000000000000, 0)
        logging.debug("2:" + instrStr)
        # --- test AND R0, #3
        globals.regs[0] = 3
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000003", reg)
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b00000010000000000000000000011110, 1)
        logging.debug("3:" + instrStr)
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000002", reg)
    
    def testANDShift(self):
        print "TestDecode:testAND"
        instrStr = armv6instrdecode.getInstructionFromCode(self, 0b11100010000000010000110000000001, 0)
        logging.debug("1:" + instrStr)
        
if __name__ == "__main__":
    unittest.main()