#!/usr/bin/env python3
"""Map unaccounted regions in WinSMCN20WW.fd and hunt for an embedded EC firmware."""
import os, re, struct, math
from collections import Counter

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
N = len(d)

fvs = []
i = d.find(b'_FVH')
while i != -1:
    b = i - 0x28
    if d[b:b+16] == b'\x00'*16:
        ln = struct.unpack('<Q', d[b+0x20:b+0x28])[0]
        fvs.append((b, min(b+ln, N)))
    i = d.find(b'_FVH', i + 1)
fvs.sort()
merged = []
for s, e in fvs:
    if merged and s <= merged[-1][1]:
        merged[-1] = (merged[-1][0], max(e, merged[-1][1]))
    else:
        merged.append((s, e))

gaps = []
prev = 0
for s, e in merged:
    if s > prev:
        gaps.append((prev, s))
    prev = max(prev, e)
if prev < N:
    gaps.append((prev, N))

print("merged FV ranges:", [(hex(s), hex(e)) for s, e in merged])
print("=== gaps ===")
def ent(b):
    if not b: return 0.0
    c = Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

SIGS = [b'ITE', b'iTE', b'IT8987', b'IT5570', b'IT8987E', b'ECFW', b'ECFW_', b'KFll',
        b'Keyboard', b'KBLL', b'ecll', b'\x5b\x2a\x6e', b'\xe0\x5b\x2a', b'\x5b\xa0\x86']
for s, e in gaps:
    if e - s <= 0x1000:
        continue
    print("GAP 0x%08X-0x%08X  (%d KB)" % (s, e, (e-s)//1024))
    print("   head64: %s" % d[s:s+64].hex())
    chunk = d[s:min(e, s+0x8000)]
    print("   entropy(32K): %.2f" % ent(chunk))
    txt = d[s:e]
    strs = [m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{6,}', txt)]
    print("   strings(%d): %s" % (len(strs), strs[:12]))
    for sig in SIGS:
        j = txt.find(sig)
        cnt = 0
        while j != -1 and cnt < 3:
            print("   SIG %s @gap+0x%X (fd 0x%X) ctx: %s" % (sig, j, s+j, txt[max(0, j-12):j+len(sig)+20].hex()))
            j = txt.find(sig, j+1); cnt += 1

# also: block-structure scan of the biggest gap for ITE image layout (0xFF/0x00/STANDARD blocks)
print("=== done ===")
