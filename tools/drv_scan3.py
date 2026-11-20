#!/usr/bin/env python3
"""Robust scan: sections, cmp-imm IOCTL candidates, port IO, for both drivers."""
import re, struct

def rva_tables(b):
    e = struct.unpack('<I', b[0x3C:0x40])[0]
    nsec = struct.unpack('<H', b[e + 6:e + 8])[0]
    optsz = struct.unpack('<H', b[e + 20:e + 22])[0]
    so = e + 24 + optsz
    secs = []
    for i in range(nsec):
        s2 = so + i * 40
        nm = b[s2:s2 + 8].rstrip(b'\0').decode('latin-1')
        vs, va, rs, rw = struct.unpack('<IIII', b[s2 + 8:s2 + 24])
        if rw and rs:
            secs.append((nm, rw, rs))
    return secs

def scan(path, tag):
    b = open(path, 'rb').read()
    print('=' * 16, tag)
    secs = rva_tables(b)
    print('  sections:', [(nm, rs) for nm, rw, rs in secs])
    # IOCTL candidates: cmp dword [reg+disp32], imm32  (81 /3x disp32 imm32) and 44 39 variants
    pats = []
    for modrm in b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7':
        pats.append(bytes([0x81, modrm]))
    for modrm in b'\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf':
        pats.append(bytes([0x44, 0x39, modrm]))
        pats.append(bytes([0x44, 0x3b, modrm]))
    seen = {}
    for nm, rw, rs in secs:
        for p in pats:
            plen = len(p)
            for m in re.finditer(re.escape(p), b[rw:rw + rs]):
                o = m.start()
                if plen == 2:
                    disp = struct.unpack('<i', b[rw + o + 2:rw + o + 6])[0]
                    imm = struct.unpack('<I', b[rw + o + 6:rw + o + 10])[0]
                else:
                    disp = struct.unpack('<i', b[rw + o + 3:rw + o + 7])[0]
                    imm = struct.unpack('<I', b[rw + o + 7:rw + o + 11])[0]
                if 0x20000 <= imm <= 0x7FFFFFFF and (imm & 0xFFFF) < 0x1000 and (imm & 3) != 0:
                    key = imm
                    if key not in seen:
                        seen[key] = (nm, o, disp)
                        print('  IOCTL? 0x%08X @%s+0x%X disp=%d' % (imm, nm, o, disp))
    # port IO
    for nm, rw, rs in secs:
        for m in re.finditer(rb'\xba([\x00-\xff]{4})[\xec\xed\xee]', b[rw:rw + rs]):
            print('  portIO(mov edx,0x%s) @%s+0x%X' % (m.group(1).hex(), nm, m.start()))
        for m in re.finditer(rb'[\xec\xed\xee]', b[rw:rw + rs]):
            o = m.start()
            print('  portIO @%s+0x%X ctx %s' % (nm, o, b[rw + max(0, o - 10):rw + o + 4].hex(' ')))

scan(r"C:\Windows\system32\DriverStore\FileRepository\lnvprocessmanagement.inf_amd64_2b0415338bfdf876\LnvMSRIO.sys", "LnvMSRIO.sys")
scan(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\H2OFFT64.sys", "H2OFFT64.sys")
