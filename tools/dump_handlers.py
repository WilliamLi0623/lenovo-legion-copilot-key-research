#!/usr/bin/env python3
"""Dump handler code regions + full wordtables (A and B)."""
import os, re

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
out = []
def P(s=''):
    out.append(str(s))

B1 = 0x260000
def dump_bank(lo, hi, tag):
    P("=== %s (bank+0x%05X .. +0x%05X) ===" % (tag, lo, hi))
    for i in range(lo, hi, 16):
        row = d[B1+i:B1+i+16]
        P("  +%05X  %s" % (i, row.hex(' ')))

dump_bank(0xFE80, 0xFFC0, 'handlers_0xFF00_0xFF2A')
dump_bank(0x7C60, 0x7D40, 'generic_handler_0x7CA5')
dump_bank(0x7FF0, 0x8090, 'handler_0x8002')
dump_bank(0xC780, 0xC880, 'handler_0xC800_key21_63')
dump_bank(0x276C0, 0x277D0, 'wordtable_head')
dump_bank(0x27930, 0x27A40, 'tableB_tail')
dump_bank(0xA540, 0xA620, 'alt_0xA57C')

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\handlers_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:70]))
print("... saved %d lines" % len(out))
