import unittest
import pdb
import globals
import armv6instrdecode
import ARMCPU

class TestCSPRFunctions(unittest.TestCase):

    #def setUp(self):

    #def tearDown(self):
    # ----------------------------------------------
    def testBasicSet(self):
        bitmask = int("000000f0", 16)
        baseval = int("00000000", 16)
        value = int("f0", 16)
        shift = 4
        val2 = armv6instrdecode.getSetValue(self, bitmask, shift, baseval, value)
        self.assertEqual(value * 16, val2)

    # ----------------------------------------------
    def testBasicGet(self):
        bitmask = int("000000f0", 16)
        baseval = int("000000f0", 16)
        value = None
        shift = 4
        val2 = armv6instrdecode.getSetValue(self, bitmask, shift, baseval, value)
        self.assertEqual(15, val2)

    # ----------------------------------------------
    def testBasicSetZeroShift(self):
        bitmask = int("0000000f", 16)
        baseval = int("00000000", 16)
        value = int("f", 16)
        shift = 0
        val2 = armv6instrdecode.getSetValue(self, bitmask, shift, baseval, value)
        self.assertEqual(value, val2)

    # ----------------------------------------------
    def testBasicGetZeroShift(self):
        bitmask = int("0000000f", 16)
        baseval = int("0000000f", 16)
        value = None
        shift = 0
        val2 = armv6instrdecode.getSetValue(self, bitmask, shift, baseval, value)
        self.assertEqual(15, val2)

    # ----------------------------------------------
    def testCPSRFlags1(self): # Set CPSR.Flags
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_FLGS", int("F", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_FLGS_MASK)

    # ----------------------------------------------
    def testCPSRFlags2(self): # get CSPR.Flags
        globals.regs[globals.CPSR] = ARMCPU.CPSR_FLGS_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_FLGS", None)
        self.assertEqual(val2, int("F", 16))

    # ----------------------------------------------
    def testCPSRQ1(self): # Set CPSR.Q
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_Q", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_Q_MASK)

    # ----------------------------------------------
    def testCPSRQ2(self): # get CSPR.Q
        globals.regs[globals.CPSR] = ARMCPU.CPSR_Q_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_Q", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRJ1(self): # Set CPSR.J
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_J", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_J_MASK)

    # ----------------------------------------------
    def testCPSRJ2(self): # get CSPR.J
        globals.regs[globals.CPSR] = ARMCPU.CPSR_J_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_J", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRGE1(self): # Set CPSR.GE
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_GE", int("F", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_GE_MASK)

    # ----------------------------------------------
    def testCPSRGE2(self): # get CSPR.GE
        globals.regs[globals.CPSR] = ARMCPU.CPSR_GE_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_GE", None)
        self.assertEqual(val2, int("F", 16))

   # IT is special, not contiguous field
   #"CPSR_IT":int("00000110000000001111110000000000", 2),

    # ----------------------------------------------
    def testCPSRE1(self): # Set CPSR.E
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_E", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_E_MASK)

    # ----------------------------------------------
    def testCPSRE2(self): # get CSPR.E
        globals.regs[globals.CPSR] = ARMCPU.CPSR_E_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_E", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRA1(self): # Set CPSR.A
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_A", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_A_MASK)

    # ----------------------------------------------
    def testCPSRA2(self): # get CSPR.A
        globals.regs[globals.CPSR] = ARMCPU.CPSR_A_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_A", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRI1(self): # Set CPSR.I
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_I", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_I_MASK)

    # ----------------------------------------------
    def testCPSRI2(self): # get CSPR.I
        globals.regs[globals.CPSR] = ARMCPU.CPSR_I_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_I", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRF1(self): # Set CPSR.F
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_F", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_F_MASK)

    # ----------------------------------------------
    def testCPSRF2(self): # get CSPR.F
        globals.regs[globals.CPSR] = ARMCPU.CPSR_F_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_F", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRT1(self): # Set CPSR.T
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_T", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_T_MASK)

    # ----------------------------------------------
    def testCPSRT2(self): # get CSPR.T
        globals.regs[globals.CPSR] = ARMCPU.CPSR_T_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_T", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRJ1(self): # Set CPSR.J
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_J", int("1", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_J_MASK)

    # ----------------------------------------------
    def testCPSRJ2(self): # get CSPR.J
        globals.regs[globals.CPSR] = ARMCPU.CPSR_J_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_J", None)
        self.assertEqual(val2, int("1", 16))

    # ----------------------------------------------
    def testCPSRMode1(self): # Set CPSR.M
        globals.regs[globals.CPSR] = int("00000000", 16)
        val2 = ARMCPU.rwCPSR(self, "CPSR_M", int("1F", 16))
        self.assertEqual(globals.regs[globals.CPSR], ARMCPU.CPSR_M_MASK)

    # ----------------------------------------------
    def testCPSRMode2(self): # get CSPR.M
        globals.regs[globals.CPSR] = ARMCPU.CPSR_M_MASK
        val2 = ARMCPU.rwCPSR(self, "CPSR_M", None)
        self.assertEqual(val2, int("1F", 16))


if __name__ == '__main__':
    unittest.main()
