#!/usr/bin/env python3
"""Comprehensive EC checksum search: try CRC32/sum/other over various ranges of bank1+bank2."""
import struct, zlib

d = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd", 'rb').read()
B1 = 0x260000; B2 = 0x299000
bank1 = d[B1:B1+0x2B000]
bank2 = d[B2:B2+0x2B000]
TARGET = 0x5AA5C33C  # bytes 3c c3 a5 5a LE = 0x5AA5C33C

print("Target value: 0x%08X (from ITE descriptor)" % TARGET)
print("Bank1 size: 0x%X, Bank2 size: 0x%X" % (len(bank1), len(bank2)))
print()

def crc32_variants(data, label):
    """Try multiple CRC32 variants."""
    results = {}
    # Standard CRC32 (zlib)
    results['zlib'] = zlib.crc32(data) & 0xFFFFFFFF
    # CRC32/BZIP2 (non-reflected, poly 0x04C11DB7, init 0xFFFFFFFF)
    # Implement manually
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            if crc & 0x80000000:
                crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFF
    results['bzip2'] = crc
    # CRC32/MPEG-2 (non-reflected, init 0xFFFFFFFF, no final xor)
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            if crc & 0x80000000:
                crc = ((crc << 1) ^ 0x04C11DB7) & 0xFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFF
    results['mpeg2'] = crc & 0xFFFFFFFF
    # CRC32/POSIX (reflected, init 0, final xor 0xFFFFFFFF)
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
    results['posix'] = crc ^ 0xFFFFFFFF
    # CRC32/JAMCRC (reflected, init 0xFFFFFFFF, no final xor)
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
    results['jam'] = crc
    return results

def sum_variants(data, label):
    results = {}
    results['sum8'] = sum(data) & 0xFF
    results['sum16'] = sum(data) & 0xFFFF
    results['sum32'] = sum(data) & 0xFFFFFFFF
    # Two's complement of sum
    results['neg_sum8'] = (-sum(data)) & 0xFF
    results['neg_sum16'] = (-sum(data)) & 0xFFFF
    results['neg_sum32'] = (-sum(data)) & 0xFFFFFFFF
    # XOR
    x = 0
    for byte in data:
        x ^= byte
    results['xor8'] = x
    return results

# Try various ranges
ranges = [
    ('bank1 all', bank1),
    ('bank1 [0x1000:]', bank1[0x1000:]),
    ('bank1 [0x1000:0x2B000-excl-desc]', bank1[0x1000:0xEB0] + bank1[0xF40:]),
    ('bank1 excl-desc-page', bank1[:0xEB0] + bank1[0xF40:]),
    ('bank2 all', bank2),
    ('bank1+bank2', bank1 + bank2),
    ('bank1[0:0x2B000-2]', bank1[:0x2AFFE]),  # exclude last 2 bytes
    ('bank1 excl first-4KB', bank1[0x1000:]),
]

print("=== CRC32 variants ===")
for name, data in ranges:
    if len(data) > 0x100000:
        print("  %s: too large for brute CRC, trying standard only" % name)
        v = zlib.crc32(data) & 0xFFFFFFFF
        match = " <<< MATCH!" if v == TARGET else ""
        print("    zlib: 0x%08X%s" % (v, match))
    else:
        results = crc32_variants(data, name)
        for alg, v in results.items():
            match = " <<< MATCH!" if v == TARGET else ""
            print("  %s/%s: 0x%08X%s" % (name, alg, v, match))

print()
print("=== Sum variants ===")
for name, data in ranges[:5]:
    results = sum_variants(data, name)
    for alg, v in results.items():
        match = " <<< MATCH!" if v == TARGET else ""
        print("  %s/%s: 0x%08X%s" % (name, alg, v, match))

# Also try: maybe the checksum is over a SPECIFIC portion like the code area only
print()
print("=== CRC32 over code areas only ===")
code_areas = [
    ('bank1[0x5000:0x28000]', bank1[0x5000:0x28000]),
    ('bank1[0x1000:0x28000]', bank1[0x1000:0x28000]),
    ('bank1[0x0:0x27000]', bank1[:0x27000]),
]
for name, data in code_areas:
    v = zlib.crc32(data) & 0xFFFFFFFF
    match = " <<< MATCH!" if v == TARGET else ""
    print("  %s: zlib=0x%08X%s" % (name, v, match))

# Try: maybe the target is stored differently (byte-swapped)
target_swapped = struct.unpack('<I', struct.pack('>I', TARGET))[0]
print()
print("Byte-swapped target: 0x%08X" % target_swapped)
for name, data in ranges[:5]:
    v = zlib.crc32(data) & 0xFFFFFFFF
    match = " <<< MATCH!" if v == target_swapped else ""
    print("  %s: zlib=0x%08X%s" % (name, v, match))
