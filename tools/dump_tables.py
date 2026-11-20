#!/usr/bin/env python3
"""Dump the three EC tables fully; contexts of 0x1D/0x5B/0x38 outputs in bank1."""
import os, re

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
out = []
def P(s=''):
    out.append(str(s))

B1 = 0x260000
b1 = d[B1:B1 + 0x2B000]
TBL_LO, TBL_HI = 0x28FE5, 0x29064

def dump(lo, hi, tag):
    P("=== %s (bank-rel 0x%05X-0x%05X) ===" % (tag, lo, hi))
    for i in range(lo, hi, 16):
        row = b1[i:i+16]
        P("  +%05X  %s" % (i, row.hex(' ')))

dump(0x27700, 0x27960, 'wordtable')
dump(0x13990, 0x13BD0, 'table_1003A')
dump(0x14F80, 0x15180, 'table_1003B')
dump(0x11E80, 0x12000, 'ctx_11F1A')

P("=== contexts of output codes in bank1 (outside matrix tbl) ===")
for val in (0x1d, 0x5b, 0x38):
    offs = [m.start() for m in re.finditer(rb'\x%02x' % val, b1)]
    sel = [o for o in offs if not (TBL_LO - 8 <= o <= TBL_HI + 8)]
    P("  val %02X: total %d, outside %d" % (val, len(offs), len(sel)))
    for o in sel[:18]:
        P("    @+%05X: %s" % (o, b1[max(0,o-24):o+32].hex(' ')))

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\tables_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:60]))
print("... saved %d lines" % len(out))
