import string, struct
import pdb
import ctypes
import array

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
        data = file.read(self._sizeInBytes)
        self._fields_ = list(struct.unpack(self._format_, data))
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

ET_NONE = 0
ET_REL  = 1
ET_EXEC = 2
ET_DYN  = 3
ET_CORE = 4
ET_LOPROC = 0xff00
ET_HIPROC = 0xffff

class COFF_HEADER(Structure):
    _names_ = "ident", "type", "machine", "version", "entry", "phoff", \
              "shoff", "flags",  "ehsize", "phentsize", "phnum", \
              "shentsize", "shnum", "shstrrndx"
    _format_ = "16shhlllllhhhhhh"
    """
       phoff - start of program headers
       phentsize - size of program headers
       phnum - number of program headers
       shentsize - size of section headers
       shnum - number of section headers
       shstrrndx - section header string table index
    """
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
   
class ELFSection(Structure):
    _names_ = "name", "type", "flags", "addr", "offset", "size", \
              "link", "info", "addralign", "entsize"
    _format_ = "llllllllll"
    
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

class ProgramHeader(Structure):
    _names_ = "type", "offset", "vaddr", "paddr", "filesz", \
              "memsz", "flags", "align"
    _format_ = "llllllll"
    
class ELFFile:
    """image-file (exe or dll) in portable executable format"""
    def __init__(self, pathname, memory):

        self.pathname = pathname
        file = open(pathname, "rb")
        # COFF header
        #pdb.set_trace()
        self.coff_hdr = coff_hdr = COFF_HEADER().read(file)
        print self.coff_hdr.decodeType(self.coff_hdr.__getattr__("type"))
        self.coff_hdr.dump()
        """ if exe """
        """ if entry """
        saddr = self.coff_hdr.__getattr__("entry")
        """ pick up the section headers """
        secskip = self.coff_hdr.__getattr__("shoff")
        secnums = self.coff_hdr.__getattr__("shnum")
        file.seek(secskip, 0)
        self.sec_hdr = []
        for secidx in range(0, secnums):
            self.sec_hdr.append(ELFSection().read(file))
            print self.sec_hdr[secidx].decodeType(self.sec_hdr[secidx].__getattr__("type"))
            self.sec_hdr[secidx].dump()
            if (self.sec_hdr[secidx].__getattr__("type") == 1):
                self.progaddr = self.sec_hdr[secidx].__getattr__("addr")
                self.progsz = self.sec_hdr[secidx].__getattr__("size")
                
        #
        file.seek(self.progaddr, 0)
        # read program
        #pdb.set_trace()
        for memptr in range(0, self.progsz):
            self.byte = ord(file.read(1))
            self.ptr = memptr #+ self.progaddr 
            #memory.insert(self.ptr, self.byte)
            memory[self.ptr] = self.byte
            print str(self.ptr), ":", str(self.byte), " m:", memory[self.ptr]
        file.close

def align(value, alignment):
    return value + ((alignment - value) % alignment)

def padtoalign(bytes, alignment):
    l1 = len(bytes)
    needed = align(l1, alignment) - len(bytes)
    return bytes + '\000' * needed
