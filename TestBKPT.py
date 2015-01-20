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

logfile = "TestBKPT.log"
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestBKPT(unittest.TestCase):
    """Instructions"""

    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0

    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    # E1210070  700021E1 	   BKPT #4096
    #        33222222222211111111110000000000
    #        10987654321098765432109876543210
    #      0b11100001001000010000000001110000 - BKPT
    #      0b11100001001100010000000000000000 - TEQ
    def testBKPT(self):
        logging.debug("------------------------------------------")
        logging.debug("TestDecode:testBKPT")
        code = 0xE1210070  # BKPT #4096
        instrStr = armv6instrdecode.getInstructionFromCode(self, code, 0)
        logging.debug("1:" + instrStr)
        self.assertEqual(instrStr, " E1210070 BKPT #4096", instrStr)

if __name__ == "__main__":
    unittest.main()