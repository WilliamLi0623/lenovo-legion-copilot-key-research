#!/usr/bin/env python3
"""Find EC-firmware-sized RAW files in index.json and chord-search them + micro patterns."""
import os, json, glob

BASE = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot"
idx = json.load(open(os.path.join(BASE, "analysis", "index.json")))

print("=== RAW/FREEFORM parts sized 64KB..3MB ===")
cands = []
for m in idx:
    ln = m.get('len', 0)
    if m.get('file_type') in ('01', '02') and 0x10000 <= ln <= 0x300000:
        cands.append(m)
        print(m['file'], ln, m.get('sname'), m.get('fv', '')[:40])

PATS = {
    'E05B_2A':      b'\xe0\x5b\x2a',
    '2A_6E':        b'\x2a\x6e',
    '5B_2A_6E':     b'\x5b\x2a\x6e',
    '5B_A0_86':     b'\x5b\xa0\x86',
    'seq_5B2A6E16': b'\x5b\x00\x2a\x00\x6e\x00',
}
for m in cands:
    p = os.path.join(BASE, 'analysis', 'parts', m['file'])
    try:
        d = open(p, 'rb').read()
    except OSError:
        continue
    hits = []
    for tag, pat in PATS.items():
        j = d.find(pat)
        while j != -1 and len(hits) < 10:
            hits.append((tag, j, d[max(0, j-16):j+len(pat)+16].hex()))
            j = d.find(pat, j + 1)
    if hits:
        print("### %s (len=%d)" % (m['file'], m['len']))
        for tag, off, hx in hits:
            print("   %-12s @0x%06X %s" % (tag, off, hx))
    # ITE signature hints
    for sig in (b'ITE', b'iTE', b'ECFW', b'E8987', b'IT8987', b'IT5570'):
        j = d.find(sig)
        if j != -1:
            print("   SIG %s @0x%X ctx %s" % (sig, j, d[max(0, j-8):j+24].hex()))
print("scan done")
