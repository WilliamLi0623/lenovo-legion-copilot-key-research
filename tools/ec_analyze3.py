#!/usr/bin/env python3
"""Deep-dive the ITE8380 EC banks: headers, entropy, strings, checksums, compression, table hunt."""
import os, re, zlib, hashlib, lzma, struct
from collections import Counter
import math

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()

def ent(b):
    if not b: return 0.0
    c = Counter(b); n = len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

BANK1 = 0x260000; BANK1E = 0x28B000
BANK2 = 0x299000; BANK2E = 0x2C4000
DBLK  = 0x2D2000

b1 = d[BANK1:BANK1E]; b2 = d[BANK2:BANK2E]
print("bank1 len=%d bank2 len=%d" % (len(b1), len(b2)))
print("sha1 bank1:", hashlib.sha1(b1).hexdigest())
print("sha1 bank2:", hashlib.sha1(b2).hexdigest())
print("identical:", b1 == b2)

print("=== bank1 head 128 ===")
print(b1[:128].hex(' '))
print("=== bank2 head 128 ===")
print(b2[:128].hex(' '))
print("=== descriptor full context @0x260EB0 ===")
print(d[0x260E80:0x260F60].hex(' '))
print("=== 0x2D2000 block head 256 ===")
print(d[DBLK:DBLK+256].hex(' '))

print("=== entropy per 4KB (bank1 + dblk) ===")
row = []
for off in range(BANK1, 0x2D3000, 0x1000):
    e = ent(d[off:off+0x1000])
    row.append((off, e))
for off, e in row:
    if e > 7.3 or e < 6.0:
        print("  0x%08X  %.2f" % (off, e))
print("  (all):", ' '.join("%.1f" % e for _, e in row))

print("=== strings in banks (>=6, ascii) ===")
txt = d[BANK1:0x2C4000]
strs = [m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{6,}', txt)]
print("count:", len(strs))
print(strs[:50])

print("=== utf16 strings in banks ===")
u16 = [m.group().decode('utf-16-le', errors='replace') for m in re.finditer(rb'(?:[\x20-\x7e]\x00){4,}', txt)]
print("count:", len(u16), u16[:20])

print("=== checksum / crc candidates ===")
desc_crc = struct.unpack('<I', d[0x260EC0+40:0x260EC0+44])[0]
print("descriptor field after string+pad:", hex(desc_crc))
tests = [
    ('crc32 bank1', zlib.crc32(b1) & 0xFFFFFFFF),
    ('crc32 bank1-skip-desc', zlib.crc32(d[BANK1:0x260EB0] + d[0x260F00:BANK1E]) & 0xFFFFFFFF),
    ('crc32 bank2', zlib.crc32(b2) & 0xFFFFFFFF),
    ('crc32 bank1[0:0xEB0]', zlib.crc32(d[BANK1:0x260EB0]) & 0xFFFFFFFF),
    ('crc32 bank1[0xF00:]', zlib.crc32(d[0x260F00:BANK1E]) & 0xFFFFFFFF),
    ('sum8 bank1', sum(b1) & 0xFF),
    ('sum8 bank2', sum(b2) & 0xFF),
]
for name, v in tests:
    print("  %-24s 0x%08X" % (name, v))

print("=== decompress attempts in bank1 ===")
for off in (BANK1, BANK1+0x20, BANK1+0x100, BANK1+0xEB0, 0x260EB0+36, BANK1+0x1000):
    payload = d[off:BANK1E]
    for tag, fn in (
        ('zlib', lambda p: zlib.decompressobj().decompress(p)),
        ('rawdefl', lambda p: zlib.decompressobj(-15).decompress(p)),
        ('lzma-alone', lambda p: lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(p)),
    ):
        try:
            out = fn(payload)
            if len(out) > 4096:
                print("  HIT %s @0x%X -> %d bytes head: %s" % (tag, off, len(out), out[:32].hex()))
        except Exception:
            pass

print("=== keyboard-table sequence hunt (0x200000-0x400000) ===")
for tag, pat in (('QWE', b'\x10\x11\x12'), ('ASD', b'\x1e\x1f\x20'), ('ZXC', b'\x2c\x2d\x2e'),
                 ('digits', b'\x02\x03\x04\x05\x06\x07'), ('word-chord1', b'\xe0\x5b\x2a\x00\x6e\x00'),
                 ('word-chord2', b'\x5b\xe0\x2a\x00\x6e\x00')):
    hits = [m.start() for m in re.finditer(re.escape(pat), d[0x200000:0x400000])]
    print("  %-10s x%d" % (tag, len(hits)), [hex(0x200000+h) for h in hits[:8]])
