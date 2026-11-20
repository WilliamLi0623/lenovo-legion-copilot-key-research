#!/usr/bin/env python3
"""Final hunt: ff-key records in EC banks; compact dump 0x288100-0x288FE4."""
import os, re

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
out = []
def P(s=''):
    out.append(str(s))

B1 = 0x260000
b1 = d[B1:B1+0x2B000]

P("=== 'ff XX' records (XX=0x40..0x7f) in bank1 ===")
for m in re.finditer(rb'\xff([\x40-\x7f])', b1):
    o = m.start()
    nxt = b1[o:o+16]
    if nxt[2] == 0x00:  # [ff][key][00][...] record shape
        P("  key=%02X @bank+%05X: %s" % (nxt[1], o, nxt.hex(' ')))

P("=== compact dump bank-rel 0x21100-0x22FE4 (abs 0x288100-0x288FE4) ===")
for i in range(0x21100, 0x22FE4, 16):
    row = b1[i:i+16]
    if row == b'\xFF'*16 or row == b'\x00'*16:
        continue
    P("  +%05X  %s" % (i, row.hex(' ')))

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\ffrec_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:80]))
print("... saved %d lines" % len(out))
