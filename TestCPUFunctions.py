import globals
import arm7instrdecode
import unittest

class TestCPUFunctions(unittest.TestCase):

    def test_lsl(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.LSL, 7, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("00000080",16))

    def test_lsl_carry(self):
        globals.regs[arm7instrdecode.Rm] = globals.NEGATIVEBIT
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.LSL, 1, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("00000000",16))
        self.assertEqual(globals.regs[globals.CPSR], int("00000000",16))

    def test_lsr(self):
        globals.regs[arm7instrdecode.Rm] = int("80000000",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.LSR, 4, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("08000000",16))

    def test_lsr_carry(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.LSR, 8, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("00000000",16))

    def test_asr(self):
        globals.regs[arm7instrdecode.Rm] = int("80000000",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.ASR, 4, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("F8000000",16))

    def test_asr_carry(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.ASR, 1, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("00000000",16))

    def test_ror(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.ROR, 1, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("80000000",16))

    def test_ror_carry(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.ROR, 1, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("80000000",16))

    def test_rrx(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.RRX, 1, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("80000000",16))

    def test_rrx_carry(self):
        globals.regs[arm7instrdecode.Rm] = int("00000001",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.RRX, 1, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("80000000",16))

    def test_imm(self):
        globals.regs[arm7instrdecode.Rm] = int("000000FF",16)
        globals.regs[globals.CPSR] = 0
        op2 = arm7instrdecode.doShift(self, arm7instrdecode.ROR, 2, globals.regs[arm7instrdecode.Rm])
        self.assertEqual(op2, int("C000003F",16))


if __name__ == '__main__':
    unittest.main()