import array

#even though really CPU related, used in arm7instrdecode, to prevent circular refs define here
SP   = 13 #SP = r13
LINK = 14 #Link = r14
PC   = 15 #pr = r15
CPSR = 16 #32: NZCVQ    7:IF 5:T (thumb) 4-0: mode

regs = array.array('L', [0]) * 37
baseLocations = 65536 * 15 # 268435455  # 256MByte
memory = array.array('B', [0]) * baseLocations
iomemory = array.array('B', [0]) * baseLocations
