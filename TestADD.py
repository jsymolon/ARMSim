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
