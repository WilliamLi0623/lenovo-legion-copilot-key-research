#!/usr/bin/env python3
"""Scan for IoControlCode access [reg+0xB8] and following cmp; dump dispatch code."""
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
    hits = []
    for nm, rw, rs in secs:
        if nm not in ('.text', 'PAGE', 'INIT'):
            continue
        for m in re.finditer(rb'(?:[\x40-\x4f])?\x8b[\x80-\xbf]\xb8\x00\x00\x00', b[rw:rw + rs]):
            o = m.start()
            # following 24 bytes contain the compare
            window = b[rw + o:rw + o + 40]
            hits.append((nm, o, window.hex(' ')))
        # also 0xB8 disp32 with 44 8b prefix variants handled above; and movzx path
        for m in re.finditer(rb'\x8b[\x80-\xbf]\xb8\x00\x00\x00', b[rw:rw + rs]):
            pass
    for nm, o, wx in hits:
        print('  IoCtlCode read @%s+0x%X: %s' % (nm, o, wx))
    if not hits:
        print('  (no [reg+0xB8] pattern found)')

scan(r"C:\Windows\system32\DriverStore\FileRepository\lnvprocessmanagement.inf_amd64_2b0415338bfdf876\LnvMSRIO.sys", "LnvMSRIO.sys")
scan(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\H2OFFT64.sys", "H2OFFT64.sys")

# dump LnvMSRIO .text fully (5KB) to file for manual reading
b = open(r"C:\Windows\system32\DriverStore\FileRepository\lnvprocessmanagement.inf_amd64_2b0415338bfdf876\LnvMSRIO.sys", 'rb').read()
secs = rva_tables(b)
for nm, rw, rs in secs:
    if nm == '.text':
        open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\lnvmsrio_text.bin", 'wb').write(b[rw:rw + rs])
        print('dumped LnvMSRIO .text %d bytes' % rs)
h = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\H2OFFT64.sys", 'rb').read()
for nm, rw, rs in rva_tables(h):
    if nm == '.text':
        open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\h2offt_text.bin", 'wb').write(h[rw:rw + rs])
        print('dumped H2OFFT .text %d bytes' % rs)
