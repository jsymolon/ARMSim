import unittest
import utils
import globals
import logging
import ARMCPU

logfile = 'TestUtils.log'
with open(logfile, 'w'):
    pass
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class TestDecode(unittest.TestCase):
    """Instructions"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
        self.addr = 0
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""

    def testGetCSPRString(self):
        globals.regs[globals.CPSR] = 0
        flags = utils.getCSPRString(self)
        self.assertEqual(flags, " nzcvqift ", flags)
    
    def testBuildRegValString(self):
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000000", reg)
        globals.regs[0] = 3
        reg = utils.buildRegValString(self, 0)
        self.assertEqual(reg, "R00:00000003", reg)
        
    def testFlags(self):
        globals.regs[globals.CPSR] = ARMCPU.NEGATIVEBIT
        reg = utils.buildRegValString(self, globals.CPSR)
        self.assertEqual(reg, "R16:80000000 (cpsr) Nzcvqift ", reg)
        
        globals.regs[globals.CPSR] = ARMCPU.ZEROBIT
        reg = utils.buildRegValString(self, globals.CPSR)
        self.assertEqual(reg, "R16:40000000 (cpsr) nZcvqift ", reg)
        
        globals.regs[globals.CPSR] = ARMCPU.CARRYBIT
        reg = utils.buildRegValString(self, globals.CPSR)
        self.assertEqual(reg, "R16:20000000 (cpsr) nzCvqift ", reg)
        
        globals.regs[globals.CPSR] = ARMCPU.OVERBIT
        reg = utils.buildRegValString(self, globals.CPSR)
        self.assertEqual(reg, "R16:10000000 (cpsr) nzcVqift ", reg)
        
        globals.regs[globals.CPSR] = ARMCPU.QBIT
        reg = utils.buildRegValString(self, globals.CPSR)
        self.assertEqual(reg, "R16:08000000 (cpsr) nzcvQift ", reg)
        
if __name__ == "__main__":
    unittest.main()