
from tir.compiler.symbolizer import DataSegment
from tir.compiler.compiler import InstructionSegment
from tir.compiler.ELF import ELF_x86_64
from enum import IntEnum

class Architecture(IntEnum):
    x86_64 = 0


class Assembler():

    def __init__(self, DATA: DataSegment, RODATA: DataSegment, BSS: DataSegment, TEXT: InstructionSegment, arch: Architecture):
        self.segments = [DATA, RODATA, BSS, TEXT]
        self.executable = None
        if(arch == Architecture.x86_64):
            self.executable = ELF_x86_64()
            self.executable.add_segments(TEXT, BSS, DATA, RODATA)
            self.executable = self.executable.generate_executable()
        else:
            raise NotImplementedError
    
    def get_executable(self):
        return self.executable