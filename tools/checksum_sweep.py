#!/usr/bin/env python3
"""Checksum sweep: find what 3CC3A55A covers; try CRC32/CRC16/sums over many ranges."""
import os, struct, zlib

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
TARGET = 0x5AA5C33C
B1 = 0x260000; B1E = 0x28B000
B2 = 0x299000; B2E = 0x2C4000
out = []
def P(s=''):
    out.append(str(s))

def crc16_ccitt(data, init=0xFFFF):
    crc = init
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc

def crc16_modbus(data):
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc

ranges = [
    ('bank1 all', d[B1:B1E]),
    ('bank1 [0:0xEB0]', d[B1:B1+0xEB0]),
    ('bank1 [0xF40:]', d[B1+0xF40:B1E]),
    ('bank1 [0x1000:]', d[B1+0x1000:B1E]),
    ('bank1 [0:0x1000]', d[B1:B1+0x1000]),
    ('bank1 [0x1000:0x28B000-noWait]', d[B1+0x1000:B1E]),
    ('bank2 all', d[B2:B2E]),
    ('bank2 [0:0xA30]', d[B2:B2+0xA30]),
    ('bank2 [0xA30+0x100:]', d[B2+0xB30:B2E]),
    ('both banks', d[B1:B1E] + d[B2:B2E]),
    ('fd[0x258000:0x260000] ITE5508 zone', d[0x258000:0x260000]),
    ('fd[0x258000:0x2C4000] ec zone', d[0x258000:0x2C4000]),
    ('fd[0x200000:0x2C4000]', d[0x200000:0x2C4000]),
    ('bank1 desc page [0:0x1000] excl desc', d[B1:B1+0xEB0] + d[B1+0xF40:B1+0x1000]),
    ('ITE5508 img [0x258000:0x25F000]', d[0x258000:0x25F000]),
]
P("=== CRC32 sweep (target 0x5AA5C33C) ===")
for name, data in ranges:
    v = zlib.crc32(data) & 0xFFFFFFFF
    mark = ' <<< MATCH' if v == TARGET else ''
    P("  %-42s %08X%s" % (name, v, mark))

P("=== CRC32 vs ITE5508 target (0x5AA5C33C same field) ===")
t2 = struct.unpack('<I', d[0x258EC0+40:0x258EC0+44])[0]
P("  ITE5508 desc field: %08X" % t2)
for name, data in ranges:
    v = zlib.crc32(data) & 0xFFFFFFFF
    if v == t2:
        P("  MATCH for ITE5508: %s" % name)

P("=== CRC16 sweep ===")
for name, data in ranges[:8]:
    c1 = crc16_ccitt(data); c2 = crc16_modbus(data)
    hi_lo = struct.unpack('<BB', d[0x260EB0+6:0x260EB0+8])  # a4 94
    P("  %-40s ccitt=%04X modbus=%04X" % (name, c1, c2))
P("  desc magic bytes: %s" % d[0x260EB0:0x260EBC].hex(' '))

P("=== per-4KB-page checksum hunt in bank1 ===")
# check if last 2/4 bytes of each 4KB page correlate with page content sums
import itertools
for pg in range(0x1000, 0x2B000, 0x1000):
    page = d[B1+pg:B1+pg+0x1000]
    s8 = sum(page) & 0xFF
    s16 = sum(page) & 0xFFFF
    c = zlib.crc32(page) & 0xFFFFFFFF
    P("  page +%05X sum8=%02X sum16=%04X crc32=%08X tail4=%s" % (pg, s8, s16, c, page[-4:].hex()))

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\checksum_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:50]))
print("... saved %d lines" % len(out))
