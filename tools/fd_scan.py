#!/usr/bin/env python3
"""Scan Insyde .fd BIOS image: walk FVs/FFS, decompress LZMA sections, dump leaf parts + strings. v2"""
import os, re, sys, json, struct, lzma, hashlib

FD  = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd"
OUT = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\analysis"
PARTS = os.path.join(OUT, "parts")
STRS  = os.path.join(OUT, "strings")
for d in (OUT, PARTS, STRS): os.makedirs(d, exist_ok=True)

GUID_LZMA  = bytes.fromhex('98584eee143959429d6e4221bffaff3a')  # EE4E5898-3914-4259-9D6E-4221BFFA3FFE
GUID_TIANO = bytes.fromhex('d66a12a31f62854f95583f4876896bf9')  # A3126AD6-621F-4F85-9558-3F4876896BF9
FS_VALID = {'8C8CE578-8A3D-4F1C-9935-896185C32DD3',  # FFS2
            '5473C07A-3DCB-4DCA-BD6F-1E9689E7349A',  # FFS3
            'FFF12B8D-7696-4C8B-A985-2747075B4F50'}  # NVRAM
seen_hash = set()
seq = [0]
index = []
comp_stats = {}

def guid_str(b):
    d1, d2, d3 = struct.unpack('<IHH', b[:8])
    d4 = b[8:16]
    return "%08X-%04X-%04X-%s-%s" % (d1, d2, d3, d4[:2].hex().upper(), d4[2:].hex().upper())

def safe_name(s):
    return re.sub(r'[^A-Za-z0-9._-]', '_', s)[:90]

def save_part(buf, hint, ctx):
    h = hashlib.sha1(buf).hexdigest()[:16]
    key = (h, len(buf))
    if key in seen_hash:
        return -1
    seen_hash.add(key)
    i = seq[0]; seq[0] += 1
    name = "p%05d_%s_%s.bin" % (i, safe_name(hint), h[:8])
    with open(os.path.join(PARTS, name), 'wb') as f:
        f.write(buf)
    m = dict(ctx); m.update({'idx': i, 'file': name, 'len': len(buf), 'sha1': h})
    index.append(m)
    out = []
    for mo in re.finditer(rb'[\x20-\x7e]{4,}', buf):
        out.append(mo.group().decode('ascii'))
    for mo in re.finditer(rb'(?:[\x20-\x7e]\x00){3,}', buf):
        try:
            out.append('U:' + mo.group().decode('utf-16-le'))
        except Exception:
            pass
    if out:
        with open(os.path.join(STRS, "p%05d.txt" % i), 'w', encoding='utf-8', errors='replace') as f:
            f.write('\n'.join(out))
    return i

def lzma_dec(payload):
    try:
        d = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        r = d.decompress(payload)
        return r if r else None
    except Exception:
        return None

def looks_like_fv(buf):
    return len(buf) >= 0x40 and buf[:16] == b'\x00'*16 and buf[0x28:0x2C] == b'_FVH'

FILE_TYPES = {0x01:'RAW',0x02:'FREEFORM',0x03:'SEC_CORE',0x04:'PEI_CORE',0x05:'DXE_CORE',
              0x06:'PEIM',0x07:'DRIVER',0x08:'COMBO_PEIM_DRV',0x09:'APPLICATION',0x0A:'SMM',
              0x0B:'FV_IMAGE',0x0C:'COMBO_SMM_DXE',0x0D:'SMM_CORE',0xF0:'PAD'}

def walk_fv(buf, base_name, depth=0):
    if not looks_like_fv(buf):
        return
    fs_guid = guid_str(buf[0x10:0x20])
    if fs_guid not in FS_VALID:
        return
    fv_len = struct.unpack('<Q', buf[0x20:0x28])[0]
    hdr_len = struct.unpack('<H', buf[0x30:0x32])[0]
    print('  '*depth + "FV %s len=%d fs=%s" % (base_name, min(fv_len, len(buf)), fs_guid))
    off = (hdr_len + 7) & ~7
    end = min(fv_len, len(buf))
    nfiles = 0
    while off + 24 <= end:
        if buf[off:off+24] == b'\xFF'*24:
            break
        size24 = buf[off+20] | (buf[off+21]<<8) | (buf[off+22]<<16)
        ftype = buf[off+18]
        if size24 == 0xFFFFFF:
            if off + 28 > end: break
            total = struct.unpack('<I', buf[off+24:off+28])[0]
            hdr = 32
        else:
            total = size24; hdr = 24
        if total < hdr or off + total > end:
            break
        fguid = guid_str(buf[off:off+16])
        if ftype != 0xF0:
            nfiles += 1
            ctx = {'fv': base_name, 'fs_guid': fs_guid, 'file_guid': fguid,
                   'file_type': '%02X' % ftype, 'file_tname': FILE_TYPES.get(ftype, '')}
            walk_sections(buf[off+hdr:off+total], 'F%s_T%s' % (fguid[:8], '%02X' % ftype), ctx, depth+1)
        off = (off + total + 7) & ~7
    print('  '*depth + "FV %s done, files=%d" % (base_name, nfiles))

SEC_NAMES = {0x01:'COMPRESSION',0x02:'GUID_DEFINED',0x03:'DISPOSABLE',0x10:'PE32',0x11:'PIC',
             0x12:'TE',0x13:'DXE_DEPEX',0x14:'VERSION',0x15:'UI',0x16:'COMPAT16',
             0x17:'FV_IMAGE',0x18:'FREEFORM_SUBTYPE',0x19:'RAW',0x1B:'PEI_DEPEX',0x1C:'SMM_DEPEX'}

def walk_sections(buf, label, ctx, depth):
    off = 0; end = len(buf)
    while off + 4 <= end:
        size24 = buf[off] | (buf[off+1]<<8) | (buf[off+2]<<16)
        stype = buf[off+3]
        if size24 == 0xFFFFFF:
            if off + 8 > end: break
            total = struct.unpack('<I', buf[off+4:off+8])[0]; hdr = 8
        else:
            if size24 < 4 or off + size24 > end: break
            total = size24; hdr = 4
        s = buf[off:off+total]
        body = s[hdr:]
        m = dict(ctx); m['section'] = '%02X' % stype; m['sname'] = SEC_NAMES.get(stype, '')
        if stype == 0x15:  # UI
            try:
                ctx['ui'] = body.decode('utf-16-le').rstrip('\x00')
                label = 'UI_%s' % safe_name(ctx['ui'])
            except Exception:
                pass
        elif stype == 0x01:  # compression
            if len(body) >= 5:
                ctype = body[4]; comp = body[5:]
                comp_stats['comp_type%d' % ctype] = comp_stats.get('comp_type%d' % ctype, 0) + 1
                if ctype == 0:
                    walk_sections(comp, label, m, depth)
                elif ctype == 2:
                    d = lzma_dec(comp)
                    if d is not None:
                        if looks_like_fv(d): walk_fv(d, 'LZMAFV_' + label, depth)
                        else: walk_sections(d, label, m, depth)
                    else:
                        save_part(s, 'LZMAFAIL_' + label, m)
                elif ctype == 1:
                    save_part(s, 'TIANOSEC_' + label, m)
                else:
                    save_part(s, 'COMP%d_' % ctype + label, m)
        elif stype == 0x02:  # GUID defined
            if len(body) >= 20:
                g = body[0:16]
                dataoff = struct.unpack('<H', body[16:18])[0]
                gs = guid_str(g)
                comp_stats['guid_' + gs[:8]] = comp_stats.get('guid_' + gs[:8], 0) + 1
                if dataoff >= hdr + 20 and dataoff <= len(s):
                    payload = s[dataoff:]
                    if g == GUID_LZMA:
                        d = lzma_dec(payload)
                        if d is not None:
                            if looks_like_fv(d): walk_fv(d, 'LZMAFV_' + label, depth)
                            else: walk_sections(d, label, m, depth)
                        else:
                            save_part(s, 'LZMAFAIL_' + label, m)
                    elif g == GUID_TIANO:
                        save_part(s, 'TIANOGUID_' + label, m)
                    else:
                        d = lzma_dec(payload)
                        if d is not None:
                            if looks_like_fv(d): walk_fv(d, 'LZMAFV2_%s_%s' % (gs[:8], label), depth)
                            else: walk_sections(d, 'UNKGUID_%s_%s' % (gs[:8], label), m, depth)
                        else:
                            save_part(payload, 'GUID%s_%s' % (gs[:8], label), m)
                else:
                    save_part(s, 'GUIDHDR_' + label, m)
        elif stype in (0x17, 0x0B):  # FV image
            if looks_like_fv(body):
                walk_fv(body, 'FVSEC_' + label, depth+1)
            else:
                save_part(body, 'FVIMG_' + label, m)
        elif stype == 0x03:  # disposable
            walk_sections(body, label, m, depth)
        else:
            save_part(body, '%s_%s' % (SEC_NAMES.get(stype, 'S%02X' % stype), label), m)
        off = (off + total + 3) & ~3

def main():
    data = open(FD, 'rb').read()
    print("FD size:", len(data))
    tops = []
    i = data.find(b'_FVH')
    while i != -1:
        tops.append(i - 0x28)
        i = data.find(b'_FVH', i + 1)
    print("_FVH offsets:", tops)
    seen = set()
    for b in tops:
        if b in seen: continue
        seen.add(b)
        if data[b:b+16] == b'\x00'*16:
            walk_fv(data[b:], "top@0x%X" % b)
    with open(os.path.join(OUT, "index.json"), 'w') as f:
        json.dump(index, f, indent=1)
    print("parts:", seq[0])
    print("comp stats:", json.dumps(comp_stats, indent=1))

if __name__ == '__main__':
    main()
