#!/usr/bin/env python3
"""Dump matrix table fully; count/locate 0x6E/0x68/specials; hunt B0 6E in BIOS parts."""
import os, re, glob
from collections import Counter

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
PARTS = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\analysis\parts"
d = open(FD, 'rb').read()
out = []
def P(s=''):
    out.append(str(s))

B1, B1E = 0x260000, 0x28B000
b1 = d[B1:B1E]
TBL = (0x287000, 0x28A200)   # matrix table absolute guess

P("=== byte counts in bank1 ===")
c = Counter(b1)
for k in (0x6e, 0x68, 0x86, 0xa0, 0x5b, 0x2a, 0x1d, 0xe0, 0xf0, 0x59, 0x5a, 0x5c, 0x63, 0x67):
    P("  %02X: %d" % (k, c[k]))

P("=== matrix table region special-value contexts (0x286000-0x28B000) ===")
zone = d[0x286000:0x28B000]
for val in (0x59, 0x5a, 0x5b, 0x5c, 0x63, 0x67, 0x68, 0x6e):
    offs = [m.start() for m in re.finditer(rb'\x%02x' % val, zone)]
    P("  val %02X: x%d" % (val, len(offs)))
    for o in offs[:14]:
        P("    @0x%08X: %s" % (0x286000+o, zone[max(0,o-16):o+24].hex(' ')))

P("=== table head hexdump 0x286E00-0x287000 ===")
for i in range(0x286E00, 0x287000, 16):
    row = d[i:i+16]
    P("  %08X  %s  %s" % (i, row.hex(' '), ''.join(chr(x) if 32 <= x < 127 else '.' for x in row)))

P("=== 0x2D2000-0x2D2200 hexdump ===")
for i in range(0x2D2000, 0x2D2200, 16):
    row = d[i:i+16]
    P("  %08X  %s" % (i, row.hex(' ')))

P("=== 0x6E contexts in bank1 OUTSIDE table ===")
offs = [m.start() for m in re.finditer(rb'\x6e', b1)]
sel = [o for o in offs if not (TBL[0]-0x100 <= B1+o <= TBL[1]+0x100)]
P("  total %d, outside-table %d" % (len(offs), len(sel)))
for o in sel[:25]:
    P("    @0x%08X: %s" % (B1+o, b1[max(0,o-20):o+28].hex(' ')))

P("=== 0x68 contexts in bank1 OUTSIDE table ===")
offs68 = [m.start() for m in re.finditer(rb'\x68', b1)]
sel68 = [o for o in offs68 if not (TBL[0]-0x100 <= B1+o <= TBL[1]+0x100)]
P("  total %d, outside %d" % (len(offs68), len(sel68)))
for o in sel68[:20]:
    P("    @0x%08X: %s" % (B1+o, b1[max(0,o-20):o+28].hex(' ')))

P("=== BIOS parts: B0 6E (mov al,6Eh) and 6E-with-5B/2A window ===")
for fn in sorted(glob.glob(os.path.join(PARTS, '*.bin'))):
    try:
        buf = open(fn, 'rb').read()
    except OSError:
        continue
    hits = []
    for m in re.finditer(rb'\xb0\x6e', buf):
        hits.append(('B06E', m.start()))
    for m in re.finditer(rb'\x6e', buf):
        o = m.start()
        w = buf[max(0, o-32):o+32]
        if 0x5b in w and 0x2a in w:
            hits.append(('WIN', o))
    if hits:
        P("  %s: %s" % (os.path.basename(fn)[:64], [(t, hex(o)) for t, o in hits[:12]]))

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\table_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:60]))
print("... saved %d lines" % len(out))
