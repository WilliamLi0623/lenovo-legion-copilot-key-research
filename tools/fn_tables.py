#!/usr/bin/env python3
"""Extract ALL Fn-combo table copies from bank1; parse 14-byte records fully."""
import re

FD = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
d = open(FD, 'rb').read()
B1 = 0x260000
b1 = d[B1:B1+0x2B000]

def parse_record(r):
    i, a, b_, c, z, p1, p2, d1, d2, d3, d4, d5, d6, d7 = list(r)
    parts = []
    def key(k):
        names = {0x02:'1',0x03:'2',0x04:'3',0x05:'4',0x06:'5',0x07:'6',0x08:'7',0x09:'8',0x0A:'9',0x0B:'0',
                 0x0F:'Tab',0x10:'Q',0x11:'W',0x12:'E',0x13:'R',0x14:'T',0x15:'Y',0x16:'U',0x17:'I',
                 0x18:'O',0x19:'P',0x1A:'[',0x1B:']',0x1D:'LCtrl',0x1E:'A',0x1F:'S',0x20:'D',0x21:'F',
                 0x22:'G',0x23:'H',0x24:'J',0x25:'K',0x26:'L',0x28:'\'',0x2A:'LShift',0x2C:'Z',0x2D:'X',
                 0x2E:'C',0x2F:'V',0x30:'B',0x31:'N',0x32:'M',0x33:',',0x34:'.',0x36:'RShift',0x37:'KP*',
                 0x38:'LAlt',0x39:'Space',0x3A:'Caps',0x3B:'F1',0x3C:'F2',0x3D:'F3',0x3E:'F4',0x3F:'F5',
                 0x40:'F6',0x41:'F7',0x42:'F8',0x43:'F9',0x44:'F10',0x45:'NumLk',0x46:'ScrLk',0x47:'KP7',
                 0x48:'KP8',0x49:'KP9',0x4A:'KP-',0x4B:'KP4',0x4C:'KP5',0x4D:'KP6',0x4E:'KP+',0x4F:'KP1',
                 0x50:'KP2',0x51:'KP3',0x52:'KP0',0x53:'KP.',0x57:'F11',0x58:'F12',0x01:'Esc',0x1C:'Enter',
                 0x0C:'-',0x0D:'=',0x0E:'BS',0x2B:'\\',0x35:'/',0x54:'SysGr'}
        return names.get(k, 'S%02X' % k)
    tri = key(a) + '+' + key(b_) + '+' + key(c) if c != 0x00 else key(a) + '+' + key(b_)
    outs = []
    for x in (d1, d2, d3, d4, d5, d6, d7):
        if x != 0x7F:
            outs.append(key(x))
    parts.append('%s [p=%02X%02X] -> %s' % (tri, p1, p2, '+'.join(outs) if outs else '(none)'))
    return ' | '.join(parts)

pat = re.compile(rb'[\x00-\x0A]([\x00-\x7F]{13})')
copies = []
for m in re.finditer(rb'\x01[\x10-\x13][\x10-\x1F]\x00\x05\x05\x41\x3e', b1):
    o = m.start() - 0
    copies.append(o)
# dedupe consecutive copies by start
starts = sorted(set(copies))
print('=== candidate table starts: %d ===' % len(starts))
seen = set()
for o in starts:
    if o in seen:
        continue
    # table = records 01..0A
    recs = []
    ok = True
    for idx in range(1, 11):
        # find record with id=idx within this copy
        base = o
        pos = base
        found = None
        for k in range(0, 160):
            p = base + k
            if p + 14 <= len(b1) and b1[p] == idx and b1[p+4] in (0x02, 0x05) and b1[p+5] == b1[p+4]:
                found = p
                break
        if not found:
            ok = False
            break
        recs.append(b1[found:found+14])
    if ok and len(recs) == 10:
        key = recs[0].hex()
        if key in seen:
            continue
        seen.add(key)
        print('--- copy @+%05X (fd 0x%08X) ---' % (o, B1+o))
        for r in recs:
            print('   ', parse_record(r))
