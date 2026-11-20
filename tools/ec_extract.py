#!/usr/bin/env python3
"""Extract and map the ITE EC firmware banks inside WinSMCN20WW.fd; hunt the Copilot chord encoding."""
import os, re, struct

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
OUT = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot"
d = open(FD, 'rb').read()

LO, HI = 0x200000, 0x400000
seg = d[LO:HI]

# 1) 4KB block classification map
step = 0x1000
prev = None
print("=== block map 0x200000-0x400000 (transitions) ===")
for off in range(0, len(seg), step):
    b = seg[off:off+step]
    z = b.count(0); f = b.count(0xFF)
    cls = 'ZERO' if z >= step*0.95 else ('FF' if f >= step*0.95 else 'DATA')
    if cls != prev:
        print("  fd 0x%08X -> %s" % (LO+off, cls))
        prev = cls

# 2) A5 A5 magic occurrences
print("=== A5A5 magic hits ===")
cnt = 0
for m in re.finditer(rb'\xa5\xa5', seg):
    o = m.start()
    if cnt < 40:
        print("  0x%08X: %s" % (LO+o, seg[max(0,o-8):o+40].hex()))
    cnt += 1
print("  total:", cnt)

# 3) exact ITE version string offsets
print("=== ITE strings ===")
for pat in (b'ITE5508', b'ITE8380', b'ITE EC', b'ITEEC', b'ITE ', b'ite firmware'):
    for m in re.finditer(re.escape(pat), seg):
        print("  %s @0x%08X ctx: %s" % (pat, LO+m.start(), seg[max(0,m.start()-24):m.start()+48].hex()))

# 4) chord encodings inside the EC area
print("=== chord encoding search 0x200000-0x400000 ===")
PATS = {
    'E05B_2A_6E':  b'\xe0\x5b\x2a\x6e',
    '5B_2A_6E':    b'\x5b\x2a\x6e',
    'E05B_002A_006E': b'\xe0\x5b\x00\x2a\x00\x6e',
    'E05B_F05B_2A_F02A_6E_F06E': b'\xe0\x5b\xf0\x5b\x2a\xf0\x2a\x6e\xf0\x6e',
    '5B_E0':       b'\x5b\xe0',
    'E0_5B':       b'\xe0\x5b',
    '6E_F0':       b'\x6e\xf0',
    'F0_6E':       b'\xf0\x6e',
    '2A_6E':       b'\x2a\x6e',
    '6E_only_around2A': None,
}
for tag, pat in PATS.items():
    if pat is None:
        continue
    hits = [m.start() for m in re.finditer(re.escape(pat), seg)]
    print("  %-24s x%d" % (tag, len(hits)), [hex(LO+h) for h in hits[:10]])

# 5) window heuristic: any 0x6E whose +-16 window contains both 0x5B and 0x2A
print("=== 6E window heuristic ===")
n = 0
for m in re.finditer(rb'\x6e', seg):
    o = m.start()
    w = seg[max(0, o-16):o+16]
    if 0x5b in w and 0x2a in w:
        print("  fd 0x%08X: %s" % (LO+o, w.hex()))
        n += 1
        if n > 25:
            break
print("  shown:", n)

# 6) dump candidate EC regions to files for later work
open(os.path.join(OUT, "ec_zone_0x200000_0x400000.bin"), 'wb').write(seg)
print("saved ec_zone_0x200000_0x400000.bin")
