#!/usr/bin/env python3
"""Static analysis of H2OFFT64.sys: strings, imports, IOCTL dispatch, port IO, MmMapIoSpace."""
import re, struct, os

P = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\H2OFFT64.sys"
b = open(P, 'rb').read()
out = []
def Pr(s=''):
    out.append(str(s))

Pr("size: %d" % len(b))

# --- strings ---
Pr("=== ASCII strings (>=6) ===")
for m in re.finditer(rb'[\x20-\x7e]{6,}', b):
    s = m.group().decode()
    if not re.match(r'^[A-Za-z$.]{0,3}[A-Z$@][\w$@]{2,}$', s) or len(s) > 8:
        Pr("  0x%04X %r" % (m.start(), s))

Pr("=== UTF16 strings (>=5) ===")
for m in re.finditer(rb'(?:[\x20-\x7e]\x00){5,}', b):
    Pr("  0x%04X %r" % (m.start(), m.group().decode('utf-16-le')))

# --- import table (parse PE) ---
e_lfanew = struct.unpack('<I', b[0x3C:0x40])[0]
machine = struct.unpack('<H', b[e_lfanew+4:e_lfanew+6])[0]
optoff = e_lfanew + 24
magic = struct.unpack('<H', b[optoff:optoff+2])[0]
ddoff = optoff + (240 if magic == 0x20b else 128)
imp_rva, imp_size = struct.unpack('<II', b[ddoff+8:ddoff+16])
sectoff = e_lfanew + 24 + struct.unpack('<H', b[e_lfanew+6:e_lfanew+8])[0]
numsec = struct.unpack('<H', b[e_lfanew+6:e_lfanew+8])[0]
sections = []
for i in range(numsec):
    so = sectoff + i*40
    name = b[so:so+8].rstrip(b'\0').decode()
    vsize, va, rsize, raw = struct.unpack('<IIII', b[so+8:so+24])
    sections.append((name, va, vsize, raw, rsize))
Pr("=== sections ===")
for s in sections:
    Pr("  %-8s va=%06X vs=%06X raw=%06X rs=%06X" % s)

def rva2off(rva):
    for name, va, vsize, raw, rsize in sections:
        if va <= rva < va + max(vsize, rsize):
            return raw + (rva - va)
    return None

if imp_rva:
    o = rva2off(imp_rva)
    Pr("=== imports ===")
    while True:
        try:
            ilt_rva, ts, fc, name_rva, iat_rva = struct.unpack('<IIIII', b[o:o+20])
        except Exception:
            break
        if name_rva == 0:
            break
        no = rva2off(name_rva)
        dllname = b[no:b.index(b'\0', no)].decode()
        funcs = []
        io = rva2off(ilt_rva)
        if io:
            j = io
            while True:
                try:
                    t = struct.unpack('<Q', b[j:j+8])[0]
                except Exception:
                    break
                if t == 0:
                    break
                if t & (1 << 63):
                    funcs.append('ord#%d' % (t & 0xFFFF))
                else:
                    fo = rva2off(t & 0xFFFFFFFF)
                    fn = b[fo+2:b.index(b'\0', fo+2)].decode()
                    funcs.append(fn)
                j += 8
        Pr("  %s: %s" % (dllname, ', '.join(funcs)))
        o += 20

# --- IOCTL pattern scan ---
Pr("=== candidate IOCTL compares ===")
code_ranges = [(raw, raw+rsize) for name, va, vsize, raw, rsize in sections if name in ('.text', 'CODE')]
hits = []
for lo, hi in code_ranges:
    for pat in (rb'\x81\xf8', rb'\x3d', rb'\x81\xf9', rb'\x3b\xca'):
        for m in re.finditer(pat, b[lo:hi]):
            o = m.start()
            if pat == rb'\x81\xf8':
                imm = struct.unpack('<I', b[o+2:o+6])[0]
            elif pat == rb'\x3d':
                imm = struct.unpack('<I', b[o+1:o+5])[0]
            elif pat == rb'\x81\xf9':
                imm = struct.unpack('<I', b[o+2:o+6])[0]
            else:
                continue
            if 0x20000 <= imm <= 0x7FFFFFFF and (imm & 0xFFFF) < 0x1000:
                hits.append((o, imm, pat.decode(errors='replace')))
seen = set()
for o, imm, p in hits:
    k = (imm, o)
    if k in seen:
        continue
    seen.add(k)
    Pr("  @0x%04X %s imm=0x%08X  ctx: %s" % (o, p, imm, b[max(0,o-16):o+12].hex(' ')))

# --- port IO / MmMap patterns ---
Pr("=== port IO instructions (in .text) ===")
for lo, hi in code_ranges:
    for pat, name in ((rb'\xee', 'OUT dx,al'), (rb'\xec', 'IN al,dx'), (rb'\x66\xef', 'OUT dx,ax'),
                      (rb'\x66\xed', 'IN ax,dx'), (rb'\xef', 'OUT dx,eax'), (rb'\xed', 'IN eax,dx')):
        for m in re.finditer(pat, b[lo:hi]):
            o = m.start()
            ctx = b[max(0, o-8):o+8]
            Pr("  %s @0x%04X ctx %s" % (name, o, ctx.hex(' ')))
    # mov edx, imm8/imm16/imm32 before EE/EC
    for m in re.finditer(rb'\xba([\x00-\xff]{1,4})\xee', b[lo:hi]):
        Pr("  OUT: mov edx,%s ; out @0x%04X" % (m.group(1).hex(), m.start()))
    for m in re.finditer(rb'\xba([\x00-\xff]{1,4})\xec', b[lo:hi]):
        Pr("  IN: mov edx,%s ; in @0x%04X" % (m.group(1).hex(), m.start()))

open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\drv_out.txt", 'w', encoding='utf-8').write('\n'.join(out))
print('\n'.join(out[:110]))
print("... saved %d lines" % len(out))
