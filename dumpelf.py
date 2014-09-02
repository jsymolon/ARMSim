import string, struct
import pdb
import ctypes
import array

###########################################################################
## Class Structure
###########################################################################
class Structure:
    def __init__(self):
        size = self._sizeInBytes = struct.calcsize(self._format_)
        self._fields_ = list(struct.unpack(self._format_, '\000' * size))
        indexes = self._indexes_ = {}
        for i in range(len(self._names_)):
            indexes[self._names_[i]] = i

    def _dump(self):
        print "%s:" % self.__class__.__name__
        for name in self._names_:
            if name[0] != '_':
                value = getattr(self, name)
                if type(value) == type(0):
                    print "%28s  %s = (0x%X)" % (name, value, value)
                else:
                    print "%28s  %s" %(name, repr(value))

    def dump(self):
        self._dump()
        print
        print

    def __getattr__(self, name):
        if name in self._names_:
            index = self._indexes_[name]
            #print "index:" + str(index)
            return self._fields_[index]
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError, name

    def __setattr__(self, name, value):
        if name in self._names_:
            index = self._indexes_[name]
            self._fields_[index] = value
        else:
            self.__dict__[name] = value

    def tostring(self):
        return apply(struct.pack, [self._format_,] + self._fields_)

    def write(self, file):
        file.write(self.tostring())

    def read(self, file):
        #print "   pre-read:" + str(file.tell()) + " #:" + str(self._sizeInBytes)
        data = file.read(self._sizeInBytes)
        #print "data:" + ":".join("{:02x}".format(ord(c)) for c in data)
        self._fields_ = list(struct.unpack(self._format_, data))
        #print "   post-read:" + str(file.tell())
        #file.seek(self._sizeInBytes, 1)
        #print "   post-seek:" + str(file.tell()) + " #:" + str(self._sizeInBytes)
        return self

    def from_bytes(self, bytes, ofs=0):
        data = bytes[ofs:ofs+self._sizeInBytes]
        self._fields_ = list(struct.unpack(self._format_, data))
        return self

    def dump_with_flags(self, flags):
        self._dump()
        for n in range(32):
            if (1 << n) & flags:
                print "%34s" % self.FLAGS[n]
        print
        print

###########################################################################
## ELF 
###########################################################################
ET_NONE = 0
ET_REL  = 1
ET_EXEC = 2
ET_DYN  = 3
ET_CORE = 4
ET_LOPROC = 0xff00
ET_HIPROC = 0xffff

E_CLASS32 = 1
E_CLASS64 = 2

ED_LTL = 1
ED_BIG = 2

EI_OSABI_SYSV = 0
EI_OSABI_HPUX = 1
EI_OSABI_NETBSD = 2
EI_OSABI_LINUX = 3
EI_OSABI_SOLARIS = 6
EI_OSABI_AIX = 7
EI_OSABI_IRIX = 8
EI_OSABI_FREEBSD = 9
EI_OSABI_OPENBSD = 12

EM_SPARC = 2
EM_X86 = 3
EM_MIPS = 8
EM_POWERPC = 20
EM_ARM = 40
EM_SUPERH = 42
EM_IA64 = 50
EM_X86_64 = 62
EM_ARCH64 = 183 

###########################################################################
##  
###########################################################################
class COFF_HEADER(Structure):
    """
      Start of the ELF header before the 32/64 split
    """
    _names_ = "EI_MAG", "EI_CLASS", "EI_DATA", "EI_VERSION", "EI_OSABI", "EI_ABIVERSION",\
              "EI_PAD", \
              "EI_BRAND", "EI_NIDENT", \
              "e_type", "e_machine", "e_version"
    _format_ = "=4sBBBBB3xBB" + "HHHL"
    def decodeType(self, code):
        if (code == ET_NONE):
             return "ET_NONE"
        elif (code == ET_REL):
             return "ET_REL"
        elif (code == ET_EXEC):
             return "ET_EXEC"
        elif (code == ET_DYN):
             return "ET_DYN"
        elif (code == ET_CORE):
             return "ET_CORE"
        elif (code == ET_LOPROC):
             return "ET_LOPROC"
        elif (code == ET_HIPROC):
            return "ET_HIPROC"

###########################################################################
##  
###########################################################################
class COFF_HEADER_32LE(Structure):
    _names_ = "entry", "phoff", "shoff", "flags",  "ehsize", "phentsize", \
            "phnum", "shentsize", "shnum", "shstrrndx"
    _format_ = "<LLLLHHHHHH"
    """
       phoff - start of program headers
       phentsize - size of program headers
       phnum - number of program headers
       shentsize - size of section headers
       shnum - number of section headers
       shstrrndx - section header string table index
    """

###########################################################################
##  
###########################################################################
class COFF_HEADER_32BE(Structure):
    _names_ = "entry", "phoff", "shoff", "flags",  "ehsize", "phentsize", \
            "phnum", "shentsize", "shnum", "shstrrndx"
    _format_ = ">LLLLHHHHHH"
    """
       phoff - start of program headers
       phentsize - size of program headers
       phnum - number of program headers
       shentsize - size of section headers
       shnum - number of section headers
       shstrrndx - section header string table index
    """

###########################################################################
##  
###########################################################################
class COFF_HEADER_64LE(Structure):
    _names_ = "entry", "phoff", "shoff", "flags",  "ehsize", "phentsize", \
            "phnum", "shentsize", "shnum", "shstrrndx"
    _format_ = "<QQQLHHHHHH"
    """
       phoff - start of program headers
       phentsize - size of program headers
       phnum - number of program headers
       shentsize - size of section headers
       shnum - number of section headers
       shstrrndx - section header string table index
    """

###########################################################################
##  
###########################################################################
class COFF_HEADER_64BE(Structure):
    _names_ = "entry", "phoff", "shoff", "flags",  "ehsize", "phentsize", \
            "phnum", "shentsize", "shnum", "shstrrndx"
    _format_ = ">QQQLHHHHHH"
    """
       phoff - start of program headers
       phentsize - size of program headers
       phnum - number of program headers
       shentsize - size of section headers
       shnum - number of section headers
       shstrrndx - section header string table index
    """

###########################################################################
##  
###########################################################################
SHT_NULL     = 0
SHT_PROGBITS = 1
SHT_SYMTAB   = 2
SHT_STRTAB   = 3
SHT_RELA     = 4
SHT_HASH     = 5
SHT_DYNAMIC  = 6
SHT_NOTE     = 7
SHT_NOBITS   = 8
SHT_REL      = 9
SHT_SHLIB    = 10
SHT_DYNSYM   = 11
SHT_LOPROC   = 0x70000000
SHT_HIPROC   = 0x7fffffff
SHT_LOUSER   = 0x80000000
SHT_HIUSER   = 0xffffffff
   

###########################################################################
##  
###########################################################################
class ELFSection(Structure):
    _names_ = "sh_name", "sh_type", "sh_flags", "sh_addr", "sh_offset", "sh_size", "sh_link", "sh_info", "sh_addralign", "sh_entsize"
    
    def decodeType(self, code):
        if (code == SHT_NULL):
             return "SHT_NULL"
        elif (code == SHT_PROGBITS):
             return "SHT_PROGBITS"
        elif (code == SHT_SYMTAB):
             return "SHT_SYMTAB"
        elif (code == SHT_STRTAB):
             return "SHT_STRTAB"
        elif (code == SHT_RELA):
             return "SHT_RELA"
        elif (code == SHT_HASH):
             return "SHT_HASH"
        elif (code == SHT_NOTE):
            return "SHT_NOTE"
        elif (code == SHT_NOBITS):
            return "SHT_NOBITS"
        elif (code == SHT_REL):
            return "SHT_REL"
        elif (code == SHT_SHLIB):
            return "SHT_SHLIB"
        elif (code == SHT_DYNSYM):
            return "SHT_DYNSYM"
        elif (code == SHT_LOPROC):
            return "SHT_LOPROC"
        elif (code == SHT_HIPROC):
            return "SHT_HIPROC"
        elif (code == SHT_LOUSER):
            return "SHT_LOUSER"
        elif (code == SHT_HIUSER):
            return "SHT_HIUSER"
        
    def format_print_hdr(self):
        print "    [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al"

    def format_print(self, index):
        """ Print
        [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
        [ 0]                   NULL            00000000 000000 000000 00      0   0  0
        """
        if index == -1:
            self.format_print_hdr()
        else:
            print '    [{0:2d}] {1:17x} {2:15s} {3:08x} {4:06x} {5:06x} {6:02x} {7:03x} {8:02x} {9:03x} {10:02x}'\
            .format(index, self.__getattr__("sh_name"), self.decodeType(self.__getattr__("sh_name")), \
            self.__getattr__("sh_addr"), self.__getattr__("sh_offset"), \
            self.__getattr__("sh_size"), self.__getattr__("sh_entsize"), \
            self.__getattr__("sh_flags"), self.__getattr__("sh_link"), \
            self.__getattr__("sh_info"), self.__getattr__("sh_addralign"))

###########################################################################
##  
###########################################################################
class COFF_SHDR_32LE(ELFSection):
    _format_ = "<LLLLLLLLLL"
    
###########################################################################
##  
###########################################################################
class COFF_SHDR_32BE(ELFSection):
    _format_ = ">LLLLLLLLLL"

###########################################################################
##  
###########################################################################
class COFF_SHDR_64LE(ELFSection):
    _format_ = "<LLQQQQLLQQ"

###########################################################################
##  
###########################################################################
class COFF_SHDR_64BE(ELFSection):
    _format_ = ">LLQQQQLLQQ"

###########################################################################
##  
###########################################################################
class ProgramHeader(Structure):
    _names_ = "type", "offset", "vaddr", "paddr", "filesz", \
              "memsz", "flags", "align"
    _format_ = "LLLLLLLL"

###########################################################################
##  
###########################################################################
class ELFFile:
    """image-file (exe or dll) in portable executable format"""
    def __init__(self, pathname, memory):
        print "pathname:" + pathname 
        self.pathname = pathname
        self.elf_file = open(pathname, "rb")
        self.coff_hdr = coff_hdr = COFF_HEADER().read(self.elf_file)
        
        self.coff_hdr.dump()

        """ File Header """
        print "Magic:" + self.coff_hdr.__getattr__("EI_MAG")[1:]

        """ Data """
        elf_data = self.coff_hdr.__getattr__("EI_DATA")
        if elf_data == ED_BIG:
            print "Data: big endian"
            self.data_end = ED_BIG
        else:
            print "Data: little endian"
            self.data_end = ED_LTL
            
        """ Check class for 32 or 64 bit and read the appropriate structure from file """
        elf_class = self.coff_hdr.__getattr__("EI_CLASS")
        
        if elf_class == E_CLASS32:
            if self.data_end == ED_LTL:
               self.coff_hdr2 = coff_hdr2 = COFF_HEADER_32LE().read(self.elf_file)
            else:
               self.coff_hdr2 = coff_hdr2 = COFF_HEADER_32BE().read(self.elf_file)
            print "Class: ELF32"
            self.class_size = E_CLASS32
        else:
            if self.data_end == ED_LTL:
               self.coff_hdr2 = coff_hdr2 = COFF_HEADER_64LE().read(self.elf_file)
            else:
               self.coff_hdr2 = coff_hdr2 = COFF_HEADER_64BE().read(self.elf_file)
            print "Class:ELF64"
            self.class_size = E_CLASS64
            
        """ Version """
        print "Version:" + str(self.coff_hdr.__getattr__("EI_VERSION"))

        """ OS/ABI """
        print "EI_OSABI:" + str(self.coff_hdr.__getattr__("EI_OSABI"))
        elf_osabi = self.coff_hdr.__getattr__("EI_OSABI")
        if elf_osabi == EI_OSABI_SYSV:
            print "OS/ABI: System V"
        if elf_osabi == EI_OSABI_HPUX:
            print "OS/ABI: HP/UX"
        if elf_osabi == EI_OSABI_NETBSD:
            print "OS/ABI: NetBSD"
        if elf_osabi == EI_OSABI_LINUX:
            print "OS/ABI: Linux"
        if elf_osabi == EI_OSABI_SOLARIS:
            print "OS/ABI: Solaris"
        if elf_osabi == EI_OSABI_AIX:
            print "OS/ABI: AIX"
        if elf_osabi == EI_OSABI_IRIX:
            print "OS/ABI: IRIX"
        if elf_osabi == EI_OSABI_FREEBSD:
            print "OS/ABI: FreeBSD"
        if elf_osabi == EI_OSABI_OPENBSD:
            print "OS/ABI: OpenBSD"

        """ ABI Version """
        print "ABI Version:" + str(self.coff_hdr.__getattr__("EI_ABIVERSION"))

        """ Brand """
        print "Brand:" + str(self.coff_hdr.__getattr__("EI_BRAND"))

        """ Ident """
        print "Ident:" + str(self.coff_hdr.__getattr__("EI_NIDENT"))

        """ Type """
        e_type = self.coff_hdr.__getattr__("e_type")
        if e_type == ET_NONE:
            print "Type: None"
        if e_type == ET_REL:
            print "Type: Rel"
        if e_type == ET_EXEC:
            print "Type: Exec"
        if e_type == ET_DYN:
            print "Type: DYN"
        if e_type == ET_CORE:
            print "Type: Core"
        if e_type == ET_LOPROC:
            print "Type: LOProc"
        if e_type == ET_HIPROC:
            print "Type: HIProc"

        """ Machine """
        elf_machine = self.coff_hdr.__getattr__("e_machine")
        if elf_machine == EM_SPARC:
            print "Machine: Sparc"
        elif elf_machine == EM_X86:
            print "Machine: X86"
        elif elf_machine == EM_MIPS:
            print "Machine: MIPS"
        elif elf_machine == EM_POWERPC:
            print "Machine: PowerPC"
        elif elf_machine == EM_ARM:
            print "Machine: ARM"
        elif elf_machine == EM_SUPERH:
            print "Machine: Super H"
        elif elf_machine == EM_IA64:
            print "Machine: IA64"
        elif elf_machine == EM_X86_64:
            print "Machine: X86 64"
        elif elf_machine == EM_ARCH64:
            print "Machine: Arch 64"
        else:
            print "Machine: Unknown/Invalid"
            
        """ e_version """
        print "EVersion:" + str(self.coff_hdr.__getattr__("e_version"))

        """ if entry """
        saddr = self.coff_hdr2.__getattr__("entry")

        """ pick up the section headers """
        secskip = self.coff_hdr2.__getattr__("shoff")
        secnums = self.coff_hdr2.__getattr__("shnum")
        self.elf_file.seek(secskip, 0)
        self.sec_hdr = []
        for secidx in range(0, secnums):
            if self.class_size == E_CLASS32:
                if self.data_end == ED_LTL:
                    self.sec_hdr.append(COFF_SHDR_32LE().read(self.elf_file))
                else:
                    self.sec_hdr.append(COFF_SHDR_32BE().read(self.elf_file))
            else:
                if self.data_end == ED_LTL:
                    self.sec_hdr.append(COFF_SHDR_64LE().read(self.elf_file))
                else:
                    self.sec_hdr.append(COFF_SHDR_64BE().read(self.elf_file))
            if secidx == 0:
                self.sec_hdr[secidx].format_print(-1)
            self.sec_hdr[secidx].format_print(secidx)
            if (self.sec_hdr[secidx].__getattr__("sh_type") == SHT_PROGBITS):
                self.progaddr = self.sec_hdr[secidx].__getattr__("sh_addr")
                self.progoff = self.sec_hdr[secidx].__getattr__("sh_offset")
                self.progsz = self.sec_hdr[secidx].__getattr__("sh_size")
                
        # Seek to where program section is
        self.elf_file.seek(self.progoff, 0)
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

###########################################################################
##  
###########################################################################
def align(value, alignment):
    return value + ((alignment - value) % alignment)

###########################################################################
##  
###########################################################################
def padtoalign(bytes, alignment):
    l1 = len(bytes)
    needed = align(l1, alignment) - len(bytes)
    return bytes + '\000' * needed
