#!/usr/bin/env python3
"""Locate the Ctrl+Alt+W chord bytes in BIOS parts / EC blob; map EC blob structure."""
import os, re, struct, lzma, zlib

BASE = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot"
PARTS = os.path.join(BASE, "analysis", "parts")
FD = os.path.join(BASE, "extract", "WinSMCN20WW.fd")
BLOBNAME = "p00024_GUID991EFAC0_F20BC8AC9_T01.bin"

CHORDS = {
    'scan_1D_38_11':  b'\x1d\x38\x11',
    'scan16_1D_38_11': b'\x1d\x00\x38\x00\x11\x00',
    'scan16_11_38_1D': b'\x11\x00\x38\x00\x1d\x00',
    'vk_A2_A4_57':    b'\xa2\xa4\x57',
    'vk_A4_A2_57':    b'\xa4\xa2\x57',
    'vk16_A2_A4_57':  b'\xa2\x00\xa4\x00\x57\x00',
    'vk16_57_A4_A2':  b'\x57\x00\xa4\x00\xa2\x00',
    'mod3_57':        b'\x03\x57\x00',
    'rcctrl_e01d':    b'\x1d\xe0',
    'e0_1d_seq':      b'\xe0\x1d',
}

def search(name, buf):
    hits = []
    for tag, pat in CHORDS.items():
        i = buf.find(pat)
        cnt = 0
        while i != -1 and cnt < 6:
            ctx = buf[max(0, i-16):i+len(pat)+16]
            hits.append((tag, i, ctx.hex()))
            i = buf.find(pat, i+1); cnt += 1
    if hits:
        print("=== %s ===" % name)
        for tag, off, hx in hits:
            print("  %-16s @0x%06X  ctx: %s" % (tag, off, hx))

# 1) search all parts
for fn in sorted(os.listdir(PARTS)):
    p = os.path.join(PARTS, fn)
    try:
        buf = open(p, 'rb').read()
    except OSError:
        continue
    search(fn, buf)

# 2) blob structure map
blob = open(os.path.join(PARTS, BLOBNAME), 'rb').read()
print("BLOB len:", len(blob))
step = 0x1000
prev = None
print("BLOB block classes (transitions):")
for off in range(0, len(blob), step):
    b = blob[off:off+step]
    z = b.count(0); f = b.count(0xFF)
    cls = 'ZERO' if z >= step*0.95 else ('FF' if f >= step*0.95 else 'DATA')
    if cls != prev:
        print("  0x%06X -> %s" % (off, cls))
        prev = cls

# heads of first DATA blocks
for off in range(0, len(blob), step):
    b = blob[off:off+step]
    z = b.count(0); f = b.count(0xFF)
    if z < step*0.95 and f < step*0.95:
        print("DATA head @0x%06X: %s" % (off, b[:48].hex()))

# 3) decompression attempts on blob at multiple offsets
def try_decomp(name, data, off):
    for wbits, tag in ((15, 'zlib'), (-15, 'rawdeflate'), (31, 'gzip')):
        try:
            d = zlib.decompressobj(wbits)
            out = d.decompress(data[off:off+1<<20])
            if len(out) > 256:
                print("DECOMP HIT %s @0x%X -> %d bytes, head: %s" % (tag, off, len(out), out[:48].hex()))
                return out
        except Exception:
            pass
    try:
        d = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        out = d.decompress(data[off:off+1<<20])
        if len(out) > 256:
            print("DECOMP HIT lzma-alone @0x%X -> %d bytes" % (off, len(out)))
            return out
    except Exception:
        pass
    return None

print("=== decompression attempts on blob ===")
for off in (0, 20, 24, 0x100, 0x200, 0x400, 0x800, 0x1000, 0x2000, 0x4000):
    try_decomp('blob', blob, off)

# entropy of DATA regions
def ent(b):
    if not b: return 0
    from collections import Counter
    c = Counter(b); n = len(b)
    return -sum((v/n)*__import__('math').log2(v/n) for v in c.values())

step2 = 0x4000
print("BLOB entropy map (16KB blocks):")
for off in range(0, len(blob), step2):
    e = ent(blob[off:off+step2])
    print("  0x%06X  %.2f" % (off, e))

# 4) the 100-byte RAW companion
import glob
p2 = glob.glob(os.path.join(PARTS, 'p00761_RAW_F20BC8AC9_T01_*.bin'))
if p2:
    d2 = open(p2[0], 'rb').read()
    print("RAW companion 100B: %s" % d2.hex())
    print("  utf16:", d2.decode('utf-16-le', errors='replace')[:50])
