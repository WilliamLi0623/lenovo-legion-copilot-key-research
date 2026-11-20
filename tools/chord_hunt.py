#!/usr/bin/env python3
"""Find chord-emission code in EC banks: 0x6E near 0x5B/0x2A; also Fn-table region dump."""
import os, re

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
out = []
def P(s=''):
    out.append(str(s))

B1, B1E = 0x260000, 0x28B000
b1 = d[B1:B1E]
TBL_LO, TBL_HI = 0x28FE5, 0x29064  # bank-relative matrix table

P("=== 0x6E in bank1 (outside matrix table) with 0x5B and 0x2A in +-96 ===")
n = 0
for m in re.finditer(rb'\x6e', b1):
    o = m.start()
    if TBL_LO - 8 <= o <= TBL_HI + 8:
        continue
    w = b1[max(0, o-96):o+96]
    if 0x5b in w and 0x2a in w:
        P("  @bank+0x%05X (fd 0x%08X): %s" % (o, B1+o, b1[max(0,o-48):o+64].hex(' ')))
        n += 1
        if n > 20:
            break
P("  hits: %d" % n)

P("=== 0x6E in bank1 with 0x5b within +-32 (any) ===")
n2 = 0
for m in re.finditer(rb'\x6e', b1):
    o = m.start()
    if TBL_LO - 8 <= o <= TBL_HI + 8:
        continue
    w = b1[max(0, o-32):o+32]
    if 0x5b in w:
        P("  @bank+0x%05X: %s" % (o, b1[max(0,o-24):o+32].hex(' ')))
        n2 += 1
        if n2 > 25:
            break
P("  hits: %d" % n2)

P("=== Fn-table zone 0x289060-0x289200 hexdump ===")
for i in range(0x289060, 0x289200, 16):
    row = d[i:i+16]
    P("  %08X  %s" % (i, row.hex(' ')))

P("=== sparse tables: 0x286A00-0x287100 ===")
for i in range(0x286A00, 0x287100, 16):
    row = d[i:i+16]
    if row == b'\xFF'*16 or row == b'\x00'*16:
        continue
    P("  %08X  %s" % (i, row.hex(' ')))

P("=== sparse tables: 0x287F00-0x288100 ===")
for i in range(0x287F00, 0x288100, 16):
    row = d[i:i+16]
    if row == b'\xFF'*16 or row == b'\x00'*16:
        continue
    P("  %08X  %s" % (i, row.hex(' ')))

P("=== bank-relative addresses of table (0x28FE5) sanity ===")
P("  matrix table bank-rel: 0x%05X-0x%05X" % (TBL_LO, TBL_HI))

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\chord_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:64]))
print("... saved %d lines" % len(out))
