#!/usr/bin/env python3
"""Walk the zlib-decompressed inner FV and chord-search everything (incl. Win+Shift+F23 trios)."""
import os, sys, zlib, glob, re

sys.path.insert(0, r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot")
import fd_scan as F

PARTS = F.PARTS
blobp = glob.glob(os.path.join(PARTS, '*GUID991EFAC0*'))[0]
blob = open(blobp, 'rb').read()
out = zlib.decompressobj().decompress(blob[0x100:])
print("zlib decompressed:", len(out))
open(os.path.join(F.OUT, "zlib_fv.bin"), 'wb').write(out)

tops = []
i = out.find(b'_FVH')
while i != -1:
    b = i - 0x28
    if out[b:b+16] == b'\x00'*16:
        tops.append(b)
    i = out.find(b'_FVH', i+1)
print("FVs inside:", [hex(b) for b in tops])
seen = set()
for b in tops:
    if b in seen:
        continue
    seen.add(b)
    F.walk_fv(out[b:], "zlibFV@0x%X" % b)
print("parts after walk:", F.seq[0])

# chord search pass 2 across every part file + raw fd
TRIOS = {
    'scan_E05B_2A_6E': b'\xe0\x5b\x2a\x6e',
    'scan_5B_2A_6E':   b'\x5b\x2a\x6e',
    'vk_5B_A0_86':     b'\x5b\xa0\x86',
    'vk_86_rev':       b'\x86\xa0\x5b',
    'vk16_5B_A0_86':   b'\x5b\x00\xa0\x00\x86\x00',
    'scan16_5B_2A_6E': b'\x5b\x00\x2a\x00\x6e\x00',
    'sc_6E_only_ctx':  None,
}
def report(name, buf):
    hits = []
    for tag, pat in TRIOS.items():
        if pat is None:
            continue
        j = buf.find(pat)
        while j != -1 and len(hits) < 8:
            hits.append((tag, j, buf[max(0, j-16):j+len(pat)+16].hex()))
            j = buf.find(pat, j+1)
    if hits:
        print("### %s" % name)
        for tag, off, hx in hits:
            print("   %-16s @0x%06X %s" % (tag, off, hx))

for fn in sorted(os.listdir(PARTS)):
    p = os.path.join(PARTS, fn)
    try:
        buf = open(p, 'rb').read()
    except OSError:
        continue
    report(fn, buf)
fd = open(F.FD, 'rb').read()
report('WinSMCN20WW.fd(raw)', fd)
print("done")
