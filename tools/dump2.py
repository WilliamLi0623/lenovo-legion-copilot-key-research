#!/usr/bin/env python3
"""Dump the suspicious keyboard-table RAW part, list SMM modules, strings of Lenovo driver."""
import os, json, re, glob

BASE = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot"
PARTS = os.path.join(BASE, "analysis", "parts")
idx = json.load(open(os.path.join(BASE, "analysis", "index.json")))

print("=== SMM files (type 0C) ===")
for m in idx:
    if m.get('file_type') == '0C':
        print("%s  ui=%-12s %s len=%d" % (m['file_guid'], m.get('ui', ''), m.get('file', ''), m.get('len')))

print("=== F2132D258 index entries ===")
for m in idx:
    if 'F2132D258' in json.dumps(m):
        print(m)

cands = glob.glob(os.path.join(PARTS, 'p00247_RAW_F2132D258*'))
if not cands:
    cands = glob.glob(os.path.join(PARTS, '*F2132D258*'))
d = open(cands[0], 'rb').read()
print("FILE: %s size=%d" % (os.path.basename(cands[0]), len(d)))

def hx(b, base=0):
    out = []
    for i in range(0, len(b), 16):
        row = b[i:i+16]
        out.append('%08X  %s  %s' % (base+i, row.hex(' '), ''.join(chr(c) if 32 <= c < 127 else '.' for c in row)))
    return '\n'.join(out)

print("=== head 320 ===")
print(hx(d[:320]))
print("=== around 0x2D78 ===")
print(hx(d[0x2B00:0x3100], 0x2B00))

sp = os.path.join(BASE, 'analysis', 'strings')
pats = ['SmmKbd', 'SpecialKey', 'SendKey', 'KbdSmm', 'EcKbd', 'KbcSmm', 'HotkeySmm',
        'HotKeySmm', 'LenovoHotkey', 'IhisiHotkey', 'LnvHotkey', 'CHotkey', 'KeyBoard']
print("=== BIOS string grep ===")
found = {}
for f in glob.glob(os.path.join(sp, '*.txt')):
    t = open(f, encoding='utf-8', errors='replace').read()
    for p in pats:
        if p in t:
            found.setdefault(p, []).append(os.path.basename(f))
for p, fs in found.items():
    print("%s -> %s" % (p, ', '.join(fs[:8])))

def fstrings(path, minlen=5):
    try:
        d = open(path, 'rb').read()
    except OSError as e:
        return [], []
    a = [m.group().decode() for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, d)]
    u = []
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){%d,}' % minlen, d):
        try:
            u.append(m.group().decode('utf-16-le'))
        except Exception:
            pass
    return a, u

print("=== lenovoDriverBus.sys interesting strings ===")
a, u = fstrings(r'C:\Windows\system32\drivers\lenovoDriverBus.sys')
seen = set()
for s in a + u:
    if re.search(r'(?i)copilot|ctrl|control|alt|hotkey|keyboard|key', s) and s not in seen:
        seen.add(s)
        print(repr(s[:140]))
        if len(seen) > 60:
            break

print("=== FnHotkeyUtility dir ===")
d1 = r'C:\Windows\System32\DriverStore\FileRepository\lenovofnandfunctionkeys.inf_amd64_5e21bf389d23855a'
for fn in os.listdir(d1):
    print(" ", fn, os.path.getsize(os.path.join(d1, fn)))
cfgs = [os.path.join(d1, fn) for fn in os.listdir(d1) if fn.lower().endswith(('.xml', '.json', '.ini', '.config', '.cfg', '.exe.config'))]
for c in cfgs:
    print("--- config %s ---" % c)
    print(open(c, encoding='utf-8', errors='replace').read()[:3000])
