#!/usr/bin/env python3
"""Next round: bank page headers, bank diff, strings, ITE magic in BIOS, Lenovo driver strings."""
import os, re, hashlib, zlib, lzma

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
out_lines = []
def P(s=''):
    out_lines.append(str(s))

BANK1, BANK1E = 0x260000, 0x28B000
BANK2, BANK2E = 0x299000, 0x2C4000
b1 = d[BANK1:BANK1E]; b2 = d[BANK2:BANK2E]

P("=== A: page heads (non-FF) bank1 ===")
for k in range(0, len(b1), 0x1000):
    h = b1[k:k+16]
    if h != b'\xFF'*16:
        P("  +0x%05X: %s" % (k, h.hex(' ')))
P("=== A2: page heads (non-FF) bank2 ===")
for k in range(0, len(b2), 0x1000):
    h = b2[k:k+16]
    if h != b'\xFF'*16:
        P("  +0x%05X: %s" % (k, h.hex(' ')))

P("=== B: bank1 vs bank2 diff ===")
diffs = [i for i in range(min(len(b1), len(b2))) if b1[i] != b2[i]]
P("  diff count: %d" % len(diffs))
if diffs:
    P("  first offsets: %s" % [hex(BANK1+o) for o in diffs[:40]])
    o = diffs[0]
    P("  ctx @first: b1 %s | b2 %s" % (b1[max(0,o-16):o+32].hex(' '), b2[max(0,o-16):o+32].hex(' ')))

P("=== C: strings in banks ===")
txt = d[BANK1:BANK2E]
strs = [m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{5,}', txt)]
P("  count: %d" % len(strs))
for s in strs[:60]:
    P("  %r" % s)
u16 = []
for m in re.finditer(rb'(?:[\x20-\x7e]\x00){4,}', txt):
    try:
        u16.append(m.group().decode('utf-16-le'))
    except Exception:
        pass
P("  utf16 count: %d %r" % (len(u16), u16[:15]))

P("=== D: crc/decompress (bank1) ===")
tests = [
    ('crc32 bank1', zlib.crc32(b1) & 0xFFFFFFFF),
    ('crc32 bank1[:0xEB0]', zlib.crc32(d[BANK1:0x260EB0]) & 0xFFFFFFFF),
    ('crc32 bank1[0xF40:]', zlib.crc32(d[0x260F40:BANK1E]) & 0xFFFFFFFF),
    ('crc32 bank2', zlib.crc32(b2) & 0xFFFFFFFF),
    ('sum8 bank1', sum(b1) & 0xFF),
]
desc_crc = int.from_bytes(d[0x260EE8:0x260EEC], 'little')
P("  desc field @0x260EE8: 0x%08X" % desc_crc)
for name, v in tests:
    P("  %-22s 0x%08X" % (name, v))
for off in (BANK1, BANK1+0x1000, 0x260F00):
    payload = d[off:BANK1E]
    for tag, fn in (('zlib', lambda p: zlib.decompressobj().decompress(p)),
                    ('rawdefl', lambda p: zlib.decompressobj(-15).decompress(p)),
                    ('lzma', lambda p: lzma.LZMADecompressor(format=lzma.FORMAT_ALONE).decompress(p))):
        try:
            o = fn(payload)
            if len(o) > 4096:
                P("  DECOMP HIT %s @0x%X -> %d" % (tag, off, len(o)))
        except Exception:
            pass

P("=== E: KB-table sequence hunt in banks ===")
for tag, pat in (('QWE', b'\x10\x11\x12'), ('ASD', b'\x1e\x1f\x20'), ('ZXC', b'\x2c\x2d\x2e'),
                 ('digits6', b'\x02\x03\x04\x05\x06\x07'),
                 ('esc01', b'\x01\x02\x03'), ('tab0F_Q10', b'\x0f\x10\x11\x12')):
    for name, buf, base in (('bank1', b1, BANK1), ('bank2', b2, BANK2)):
        hits = [m.start() for m in re.finditer(re.escape(pat), buf)]
        if hits:
            P("  %s in %s x%d %s" % (tag, name, len(hits), [hex(base+h) for h in hits[:6]]))

P("=== F: ITE magic in BIOS FV parts ===")
import glob
PARTS = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\analysis\parts"
pats = {'a5a5x6': b'\xa5\xa5\xa5\xa5\xa5\xa5', '5AA5C33C': b'\x3c\xc3\xa5\x5a', 'ITE8380': b'ITE8380', 'ITE5508': b'ITE5508'}
for fn in sorted(glob.glob(os.path.join(PARTS, '*.bin'))):
    try:
        buf = open(fn, 'rb').read()
    except OSError:
        continue
    for tag, pat in pats.items():
        j = buf.find(pat)
        if j != -1:
            P("  %s %s @part+0x%X" % (os.path.basename(fn)[:60], tag, j))

P("=== G: Lenovo driver/utility strings ===")
def fstrings(path, minlen=5):
    try:
        b = open(path, 'rb').read()
    except OSError:
        return [], []
    a = [m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, b)]
    u = []
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){%d,}' % minlen, b):
        try:
            u.append(m.group().decode('utf-16-le'))
        except Exception:
            pass
    return a, u

for path in (r'C:\Windows\system32\drivers\lenovoDriverBus.sys',
             r'C:\Windows\System32\DriverStore\FileRepository\lenovofnandfunctionkeys.inf_amd64_5e21bf389d23855a\FnHotkeyUtility.exe',
             r'C:\Windows\System32\DriverStore\FileRepository\lenovofnandfunctionkeys.inf_amd64_5e21bf389d23855a\FnHotkeyCapsLKNumLK.exe'):
    a, u = fstrings(path)
    P("  --- %s (ascii %d, u16 %d) ---" % (os.path.basename(path), len(a), len(u)))
    seen = set()
    for s in a + u:
        if re.search(r'(?i)copilot|f23|0x6e|hotkey|keycode|scan|chord|combo|ctrl|control|alt|shift|remap|custom', s) and s not in seen:
            seen.add(s)
            P("   %r" % s[:130])
            if len(seen) > 40:
                break

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\ec_next_out.txt", 'w', encoding='utf-8').write('\n'.join(out_lines))
print('\n'.join(out_lines[:55]))
print("... full output saved (%d lines)" % len(out_lines))
