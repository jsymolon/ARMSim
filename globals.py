import array

SP   = 13 #SP = r13
LINK = 14 #Link = r14
PC   = 15 #pr = r15
CPSR = 16 #32: NZCVQ    7:IF 5:T (thumb) 4-0: mode
HIGHBIT = int("80000000", 16)
NEGATIVEBIT = int("80000000",16)
ZEROBIT = int("40000000",16)
CARRYBIT = int("20000000",16)
OVERBIT = int("10000000",16)
QBIT = int("08000000",16)

INTIRQBIT = int("00000080",16)
INTFIQBIT = int("00000040",16)
THUMBBIT = int("00000020",16)
OPMODEBIT = int("0000001F",16)

regs = array.array('L', [0]) * 37
baseLocations = 65536 * 15 # 268435455  # 256MByte
memory = array.array('B', [0]) * baseLocations
iomemory = array.array('B', [0]) * baseLocations
