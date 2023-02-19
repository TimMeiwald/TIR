import elfgenerator.ELF_Segment_Utils as s
import elfgenerator.ELF_Header_Utils as h
from elfgenerator.Binary import Binary
from tir.compiler.compiler import InstructionSegment
from tir.compiler.symbolizer import DataSegment
from abc import ABC

class AbstractELFClass(ABC):

    def __init__(self):
        self.e_ident = None
        self.e_type = None
        self.e_machine = None
        self.e_version = None
        self.e_entry = None
        self.e_phoff = None
        self.e_shoff = None
        self.e_flags = None
        self.e_ehsize = None
        self.e_phentsize = None
        self.e_phnum = None
        self.e_shentsize = None
        self.e_shnum = None
        self.e_shstrndx = None
        self.program_headers = []
        self.segments = []
        
    def _generate_ELF_header(self):
        header_vals = [self.e_ident, self.e_type, self.e_machine, self.e_version,
        self.e_entry, self.e_phoff, self.e_shoff, self.e_flags, self.e_ehsize,
        self.e_phentsize, self.e_phnum, self.e_shentsize, self.e_shnum, self.e_shstrndx]
        ELF_HEADER = Binary(0,0,0)
        for val in header_vals:
            ELF_HEADER += val.binary()
        print("HEADER HERE ", ELF_HEADER)     
        return ELF_HEADER

    def _generate_program_header_table(self):
        self.e_phoff.value = 64 # Location of start of program header. 
        self.e_phnum.value = len(self.segments)
        header_table = Binary(0,0,0)
        for p_header in self.program_headers:
            header_table += p_header.binary()
        return header_table
    
    def generate_executable(self):
        program_header = self._generate_program_header_table() # So that stuff gets set before ELF header is generated
        code = self._generate_ELF_header()
        #print("ANOTHER CODE HERE ", code)
        code += program_header
        for segment in self.segments:
             code += segment
        # #print(f"Header Length = {len(program_header)}")
        return code


class ELF_x86_64(AbstractELFClass):

    def __init__(self):
        super().__init__()
        self.EI_CLASS = 2
        self.e_ident = h.e_ident(EI_CLASS=self.EI_CLASS, EI_DATA=1, EI_OSABI=0, EI_ABIVERSION=0) #64 bit, LSB, Linux, Unsure
        self.e_type = h.e_type.ET_EXEC
        self.e_machine = h.e_machine.EM_X86_64
        self.e_version = h.e_version.EV_CURRENT
        self.e_entry = h.e_entry(0, EI_CLASS=self.EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
        self.e_phoff = h.e_phoff(0, EI_CLASS=self.EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
        self.e_shoff = h.e_shoff(0, EI_CLASS=self.EI_CLASS) # 0 is placeholder # TODO MODIFY FOR 64BIT
        self.e_flags = h.e_flags()
        self.e_ehsize = h.e_ehsize(64) #0 is placeholder
        self.e_phentsize = h.e_phentsize(56) # Program headers are 56 bytes for x86-64
        self.e_phnum = h.e_phnum(0) # 0 is placeholder
        self.e_shentsize = h.e_shentsize(0) # 0 is placeholder
        self.e_shnum = h.e_shnum(0) # 0 is placeholder
        self.e_shstrndx = h.e_shstrndx(0) # 0 is placeholder

        
    def add_segments(self, TEXT: InstructionSegment, BSS: DataSegment, DATA: DataSegment, RODATA: DataSegment):
        # Order: DATA, RODATA, BSS, TEXT
        running_total_size = 64+4*56 # One ELF Header and 4 Prog Headers 
        page_size = 4096 
        # Handle DATA
        # Raw Binary 
        self.segments.append(DATA.get_binary())
        offset = running_total_size
        type = 1 # Loadable Segment
        vaddress = DATA.start_position
        paddr = running_total_size
        flags = DATA.permissions
        filesz = DATA.end_position - DATA.start_position
        memsz = DATA.end_position - DATA.start_position
        align=page_size
        DATA_program_header = s.Segment(type, offset, vaddress, paddr, filesz, memsz, flags, align)
        self.program_headers.append(DATA_program_header)
        print(f"Added DATA: {offset, type, vaddress, paddr, flags, filesz, memsz, align}")
        
        running_total_size += filesz

        # RODATA

        self.segments.append(RODATA.get_binary())
        offset = running_total_size
        type = 1 # Loadable Segment
        vaddress = RODATA.start_position
        paddr = running_total_size
        flags = RODATA.permissions
        filesz = RODATA.end_position - RODATA.start_position
        memsz = RODATA.end_position - RODATA.start_position
        align=page_size
        RODATA_program_header = s.Segment(type, offset, vaddress, paddr, filesz, memsz, flags, align)
        self.program_headers.append(RODATA_program_header)
        print(f"Added RODATA: {offset, type, vaddress, paddr, flags, filesz, memsz, align}")
        
        running_total_size += filesz

        # BSS

        self.segments.append(Binary(0,0,0))
        offset = running_total_size
        type = 1 # Loadable Segment
        vaddress = BSS.start_position
        paddr = running_total_size
        flags = BSS.permissions
        filesz = 0
        memsz = BSS.end_position - BSS.start_position
        align=page_size
        BSS_program_header = s.Segment(type, offset, vaddress, paddr, filesz, memsz, flags, align)
        self.program_headers.append(BSS_program_header)
        print(f"Added BSS: {offset, type, vaddress, paddr, flags, filesz, memsz, align}")

        # TEXT
        self.segments.append(TEXT.get_binary())
        offset = running_total_size
        type = 1 # Loadable Segment
        paddr = running_total_size
        flags = TEXT.permissions
        filesz = TEXT.end_position - TEXT.start_position
        vaddress = TEXT.start_position + paddr
        memsz = filesz # self.memsz_calc(filesz, page_size=) # ((filesz//page_size)+1)*4096
        align=page_size
        TEXT_program_header = s.Segment(type, offset, vaddress, paddr, filesz, memsz, flags, align)
        self.program_headers.append(TEXT_program_header)
        print(f"Added TEXT: {offset, type, vaddress, paddr, flags, filesz, memsz, align}")
        running_total_size += filesz
        self.e_entry = h.e_entry(vaddress,EI_CLASS=self.EI_CLASS)
    
    def memsz_calc(self, filesz, page_size):
        if(filesz == 0):
            return 0
        return ((filesz//page_size)+1)*4096

