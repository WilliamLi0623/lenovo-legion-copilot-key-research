#!/usr/bin/env python3
"""Dump & diff the two AI-key handler function bodies; mark differences."""
import struct

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
B1 = 0x260000

def dump(lo, hi, tag):
    print('=' * 8, tag, '(bank+0x%04X..0x%04X)' % (lo, hi))
    for i in range(lo, hi, 16):
        row = d[B1+i:B1+i+16]
        print('  %04X  %s  %s' % (i, row.hex(' '), ''.join(chr(c) if 32 <= c < 127 else '.' for c in row)))

# state B handler around 0xFF00, state A around 0xFF2A; dump generous windows
dump(0xFE60, 0xFF00, 'pre-B')
dump(0xFF00, 0xFF40, 'state B (0xFF00)')
dump(0xFF40, 0xFFA0, 'state A (0xFF2A)')

# byte diff between stateA window and stateB window shifted by 0x2A
print('=== shifted diff (A[i] vs B[i-0x2A]) over 0xFF2A..0xFFA0 vs 0xFF00..0xFF76 ===')
a0, b0 = 0xFF2A, 0xFF00
diffs = []
for i in range(0x120):
    av = d[B1+a0+i]
    bv = d[B1+b0+i]
    if av != bv:
        diffs.append((i, av, bv))
for off, av, bv in diffs[:40]:
    print('  +%03X: A=%02X B=%02X' % (off, av, bv))
print('  diff count:', len(diffs))
