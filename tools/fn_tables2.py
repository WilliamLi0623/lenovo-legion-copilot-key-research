#!/usr/bin/env python3
"""Decode ALL Fn-combo table copies as 15-byte records; diff them; identify the AI-key record."""
import re

b1 = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd", 'rb').read()[0x260000:0x260000+0x2B000]

KEYS = {0x01:'Esc',0x02:'1',0x03:'2',0x04:'3',0x05:'4',0x06:'5',0x07:'6',0x08:'7',0x09:'8',0x0A:'9',0x0B:'0',
        0x0C:'-',0x0D:'=',0x0E:'BS',0x0F:'Tab',0x10:'Q',0x11:'W',0x12:'E',0x13:'R',0x14:'T',0x15:'Y',
        0x16:'U',0x17:'I',0x18:'O',0x19:'P',0x1A:'[',0x1B:']',0x1C:'Enter',0x1D:'LCtrl',0x1E:'A',0x1F:'S',
        0x20:'D',0x21:'F',0x22:'G',0x23:'H',0x24:'J',0x25:'K',0x26:'L',0x27:';',0x28:"'",0x29:'`',
        0x2A:'LShift',0x2B:'\\',0x2C:'Z',0x2D:'X',0x2E:'C',0x2F:'V',0x30:'B',0x31:'N',0x32:'M',0x33:',',
        0x34:'.',0x35:'/',0x36:'RShift',0x37:'KP*',0x38:'LAlt',0x39:'Space',0x3A:'Caps',0x3B:'F1',
        0x3C:'F2',0x3D:'F3',0x3E:'F4',0x3F:'F5',0x40:'F6',0x41:'F7',0x42:'F8',0x43:'F9',0x44:'F10',
        0x45:'NumLk',0x46:'ScrLk',0x47:'KP7',0x48:'KP8',0x49:'KP9',0x4A:'KP-',0x4B:'KP4',0x4C:'KP5',
        0x4D:'KP6',0x4E:'KP+',0x4F:'KP1',0x50:'KP2',0x51:'KP3',0x52:'KP0',0x53:'KP.',0x54:'SysGr',
        0x57:'F11',0x58:'F12',0x59:'S59',0x5A:'S5A',0x5B:'S5B',0x5C:'S5C',0x5D:'S5D',0x5E:'S5E',
        0x63:'S63',0x64:'S64',0x6F:'S6F',0x70:'Fn?',0x74:'S74',0x76:'S76',0x7C:'S7C'}

def kn(k):
    return KEYS.get(k, 'S%02X' % k)

pat = re.compile(rb'\x01\x11\x11\x0f\x00')
starts = [m.start() for m in pat.finditer(b1)]
print('=== %d table copies ===' % len(starts))
tables = []
for o in starts:
    recs = []
    ok = True
    for idx in range(1, 11):
        p = o + (idx - 1) * 15
        r = b1[p:p+15]
        if len(r) < 15 or r[0] != idx:
            ok = False
            break
        recs.append(r)
    if not ok:
        continue
    tables.append((o, recs))

print('valid 15-byte tables:', len(tables))
# dedupe by content
uniq = {}
for o, recs in tables:
    key = b''.join(recs).hex()
    uniq.setdefault(key, []).append(o)
print('unique variants:', len(uniq))
for key, offs in uniq.items():
    recs = [key[i*30:(i+1)*30] for i in range(10)]
    print('--- variant (copies at %s) ---' % ['+%05X' % x for x in offs[:6]])
    for i, h in enumerate(recs):
        r = bytes.fromhex(h)
        tri = '+'.join(kn(x) for x in r[1:4] if x)
        p = '%02X%02X' % (r[5], r[6])
        outs = [kn(x) for x in r[7:14] if x != 0x7F]
        print('   %02d: %-22s p=%s -> %s' % (r[0], tri, p, '+'.join(outs) if outs else '-'))
