#!/usr/bin/env python3
"""Disassemble the EC AI-key handler region as RISC-V RV32/RV32C."""
from capstone import Cs, CS_ARCH_RISCV, CS_MODE_RISCV32, CS_MODE_RISCVC
import struct

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()

# bank1 base in fd = 0x260000; handlers at bank+0xFF00 (state B) / 0xFF2A (state A)
B1 = 0x260000
md = Cs(CS_ARCH_RISCV, CS_MODE_RISCV32 | CS_MODE_RISCVC)

def dis(lo, hi, label):
    print('=' * 10, label, 'fd 0x%08X-0x%08X' % (B1+lo, B1+hi))
    code = d[B1+lo:B1+hi]
    for ins in md.disasm(code, lo):
        print('  %04X  %-8s %s' % (ins.address, ins.mnemonic, ins.op_str))

dis(0xFEE0, 0x0040, 'stateB handler 0xFF00 region')
dis(0xFF20, 0x0100, 'stateA handler 0xFF2A region')
