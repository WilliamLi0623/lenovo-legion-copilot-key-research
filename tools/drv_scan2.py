#!/usr/bin/env python3
"""Fixed driver scan: IOCTL candidates + port IO across all sections."""
import re, struct, sys

def analyze(path, tag):
    b = open(path, 'rb').read()
    print('=' * 16, tag, 'len=%d' % len(b))
    e = struct.unpack('<I', b[0x3C:0x40])[0]
    nsec = struct.unpack('<H', b[e + 6:e + 8])[0]
    so = e + 24 + nsec * 40
    secs = []
    for i in range(nsec):
        s2 = so + i * 40
        nm = b[s2:s2 + 8].rstrip(b'\0').decode('latin-1')
        vs, va, rs, rw = struct.unpack('<IIII', b[s2 + 8:s2 + 24])
        if rs:
            secs.append((nm, rw, rs))
        print('  SEC %-9s va=%06X vs=%06X raw=%06X rs=%06X' % (nm, va, vs, rw, rs))
    seen = set()
    for nm, rw, rs in secs:
        for m in re.finditer(rb'\x81[\xf8\xf9\xfa\xfb]', b[rw:rw + rs]):
            o = m.start()
            imm = struct.unpack('<I', b[o + 2:o + 6])[0]
            if 0x20000 <= imm <= 0x7FFFFFFF and (imm & 0xFFFF) < 0x1000 and imm not in seen:
                seen.add(imm)
                print('  IOCTL? 0x%08X @%s+0x%X ctx %s' % (imm, nm, o, b[max(0, o - 20):o + 8].hex(' ')))
    for nm, rw, rs in secs:
        for m in re.finditer(rb'\xba([\x00-\xff]{4})\xe[ecd]', b[rw:rw + rs]):
            print('  portIO(mov edx,%s) @%s+0x%X' % (m.group(1).hex(), nm, m.start()))
    for nm, rw, rs in secs:
        for m in re.finditer(rb'[\xec\xed\xee]', b[rw:rw + rs]):
            o = m.start()
            print('  portIO @%s+0x%X ctx %s' % (nm, o, b[max(0, o - 12):o + 4].hex(' ')))

analyze(r"C:\Windows\system32\DriverStore\FileRepository\lnvprocessmanagement.inf_amd64_2b0415338bfdf876\LnvMSRIO.sys", "LnvMSRIO.sys")
analyze(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\H2OFFT64.sys", "H2OFFT64.sys")
