#!/usr/bin/env python3
"""Compact dump of table zone; contexts of 63/67/68/6E; dissect SMM modules."""
import os, re, glob, hashlib

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
PARTS = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\analysis\parts"
OUTDIR = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot"
d = open(FD, 'rb').read()
out = []
def P(s=''):
    out.append(str(s))

P("=== compact hexdump 0x286000-0x28B000 (rows with data) ===")
for i in range(0x286000, 0x28B000, 16):
    row = d[i:i+16]
    if row == b'\xFF'*16 or row == b'\x00'*16:
        continue
    P("  %08X  %s" % (i, row.hex(' ')))

P("=== contexts 63/67/68/6E in zone 0x286000-0x28B000 ===")
zone = d[0x286000:0x28B000]
for val in (0x63, 0x67, 0x68, 0x6e):
    offs = [m.start() for m in re.finditer(rb'\x%02x' % val, zone)]
    P("  val %02X x%d" % (val, len(offs)))
    for o in offs[:10]:
        P("    @0x%08X: %s" % (0x286000+o, zone[max(0,o-20):o+28].hex(' ')))

def analyze_part(pattern, tag):
    files = glob.glob(os.path.join(PARTS, pattern))
    if not files:
        P("  part %s not found" % pattern)
        return
    f = files[0]
    buf = open(f, 'rb').read()
    P("=== %s: %s len=%d ===" % (tag, os.path.basename(f), len(buf)))
    strs = [m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{6,}', buf)]
    P("  strings(%d): %s" % (len(strs), strs[:40]))
    for m in re.finditer(rb'\xb0\x6e', buf):
        o = m.start()
        P("  B06E @0x%X ctx: %s" % (o, buf[max(0,o-32):o+48].hex(' ')))
    for pat, tname in ((b'ITE8380', 'ITE8380'), (b'\xa5\xa5\xa5\xa5\xa5\xa5', 'a5a5x6'), (b'\x3c\xc3\xa5\x5a', 'CRCmagic')):
        for m in re.finditer(re.escape(pat), buf):
            o = m.start()
            P("  %s @0x%X ctx: %s" % (tname, o, buf[max(0,o-40):o+72].hex(' ')))
    open(os.path.join(OUTDIR, tag + '.bin'), 'wb').write(buf)

analyze_part('p00472_PE32_F08747359_*.bin', 'smm_ite_update')
analyze_part('p00155_PE32_FBDFE430E_*.bin', 'smm_b06e_155')
analyze_part('p00747_PE32_FD2DD6EB0_T0C_d2ce624d*.bin', 'smm_fd2d')
analyze_part('p00434_PE32_F2AA8F59B_*.bin', 'pe_434')

open(os.path.join(OUTDIR, "table_out2.txt"), 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:70]))
print("... saved %d lines" % len(out))
