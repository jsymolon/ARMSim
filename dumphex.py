import string, struct
import pdb
import ctypes
import array

###########################################################################
## dumphex - read .hex (intel) and load
###########################################################################

# General Record Format:
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, INFO/DATA nb, CHKSUM 1b

# Extended Linear Address Record 32-bit
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, ULBA nb, CHKSUM 1b
#   :            02           0000         04           ????         ??
# :02000004------
# (LBA + DRLO + DRI) MOD 4G
# DRLO = Load Offset of a data record
# DRI = data byte index

# Extended Segment Address Record 16/32
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, USBA nb, CHKSUM 1b
#   :            02           0000         02           ????         ??
# :02000002------
# SBA + ([DRLO + DRI] MOD 64K)

# Data Record
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, DATA nb, CHKSUM 1b
#   :            02           0000         00           ????         ??
# :02000000------

# Start Linear Address Record 32-bit
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, EIP 4b, CHKSUM 1b
#   :            04           0000         05       ????????        ??
# :04000005------

# Start Segment Address Record 16/32
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, CS/IP 4b, CHKSUM 1b
#   :            04           0000         03       ????????        ??
# :04000003------

# End of File Record
# REC_MARK 1b, REC_LEN 1b, LOAD OFF 2b, REC_TYPE 1b, CHKSUM 1b
#   :            00           0000         01               FF
# :00000001FF

REC_MARK = ':'

# Check sum calculation
# Each record ends with a CHKSUM field that contains the ASCII hexadecimal representation of the twos
# complement of the 8-bit bytes that result from converting each pair of ASCII hexadecimal digits to one byte of
# binary, from and including the RECLEN field to and including the last byte of the INFO/DATA field. Therefore,
# the sum of all the ASCII pairs in a record after converting to binary, form the RECLEN field to and including the


# REC TYPES
REC_DATA = 00
REC_EOF = 01
REC_ESA = 02 # extended segment address
REC_SSA = 03 # start segment address
REC_ELA = 04 # extended linear address
REC_SLA = 05 # start linear address

###########################################################################
##  
###########################################################################
class HEXFile:
    """image-file (exe or dll) in portable executable format"""
    def __init__(self, pathname, memory):
        print "pathname:" + pathname 
        self.pathname = pathname
        # Open the file for reading.
        with open('pathname', 'r') as self.hex_file:
            data = self.hex_file.read()  # Read the contents of the file into memory.
        # Return a list of the lines, breaking at line boundaries.
        records = data.splitlines()
        # read program
        #pdb.set_trace()
        for memptr in range(0, self.progsz, 2):  # skip 1 as were loading words
            byte0 = ord(self.elf_file.read(1))
            byte1 = ord(self.elf_file.read(1))
            ptr = memptr #+ self.progaddr 
            if self.data_end == ED_LTL:
                memory[ptr] = byte0
                memory[ptr + 1] = byte1
            print '{0:04d} {1:08x}:{2:02x} {3:02x}'.format(ptr, memptr, byte1, byte0)
        self.elf_file.close
