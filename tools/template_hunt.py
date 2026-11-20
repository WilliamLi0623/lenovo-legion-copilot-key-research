#!/usr/bin/env python3
"""Find all instances of the key-event handler template; extract per-instance constants."""
import re, struct

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
B1 = 0x260000
b1 = d[B1:B1+0x2B000]

# template: 46 00 01 00 00 10 02 00 5a 18 10 XX 20 YY 05 00 4e ZZ 00 WW ... fc 00 84 KK ... 49 ff d2 VV
pat = re.compile(rb'\x46\x00\x01\x00\x00\x10\x02\x00\x5a\x18\x10(.)\x20(.)\x05\x00\x4e(..)\xfc\x00\x84(..)')
print('=== template instances in bank1 ===')
n = 0
for m in pat.finditer(b1):
    o = m.start()
    a1 = m.group(1)[0]; a2 = m.group(2)[0]
    zzww = m.group(3); kk = m.group(4)
    # find the following 49 ff d2 VV within 24 bytes
    tail = b1[o+24:o+48]
    mv = re.search(rb'\x49\xff\xd2(..)', tail)
    vv = mv.group(1).hex() if mv else '????'
    n += 1
    print('  @bank+%05X: 5a-arg=%02X 20-arg=%02X 4e-args=%s 84-K=%02X 49ff-d2=%s' % (
        o, a1, a2, zzww.hex(), kk[0], vv))
print('  total:', n)

# also looser: any '46 00 01 00 00 10 02 00 5a 18 10'
pat2 = re.compile(rb'\x46\x00\x01\x00\x00\x10\x02\x00\x5a\x18\x10')
print('=== loose 5a-18-10 prefix count ===', len(pat2.findall(b1)))

# and the [key][10 03 08] arrays context dump
print('=== +0x13990..+0x13C00 hexdump ===')
for i in range(0x13990, 0x13C00, 16):
    row = b1[i:i+16]
    print('  %04X  %s  %s' % (i, row.hex(' '), ''.join(chr(c) if 32 <= c < 127 else '.' for c in row)))
