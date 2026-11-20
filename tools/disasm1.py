#!/usr/bin/env python3
"""Disassemble drivers with capstone; extract dispatch logic."""
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import re

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

def disasm_range(b, lo, hi, base, tag):
    print('=' * 12, tag, '0x%X-0x%X' % (base + lo, base + hi))
    for ins in md.disasm(b[lo:hi], base + lo):
        print('  %04X  %-24s %s' % (ins.address, ins.mnemonic, ins.op_str))

def find_ioctl_cmps(b, base, tag):
    print('=== IOCTL compares in', tag, '===')
    for ins in md.disasm(b, base):
        s = '%s %s' % (ins.mnemonic, ins.op_str)
        if ins.mnemonic in ('cmp',) and ('0x' in ins.op_str):
            try:
                val = int(re.search(r'0x([0-9a-f]+)', ins.op_str.split(', ')[-1]).group(1), 16)
            except Exception:
                continue
            if 0x20000 <= val <= 0x7FFFFFFF and (val & 0xFFFF) < 0x1000 and (val & 3) != 0:
                print('  %04X  %s' % (ins.address, s))

lnv = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\lnvmsrio_text.bin", 'rb').read()
h2o = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\h2offt_text.bin", 'rb').read()

find_ioctl_cmps(lnv, 0, 'LnvMSRIO.text')
find_ioctl_cmps(h2o, 0, 'H2OFFT.text')
disasm_range(lnv, 0x580, 0x745, 0, 'LnvMSRIO EvtIoDeviceControl')
