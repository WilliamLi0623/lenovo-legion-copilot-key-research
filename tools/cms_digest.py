import struct, hashlib, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd", "rb").read()

# FOUND the messageDigest in the CMS signature!
# messageDigest OID at file offset 0x021F6519
# The value: 24 7c cc 4f f3 6a 83 d4 13 05 67 a0 0d f6 a0 b5 e7 b2 42 f2 db 61 8e d3 4a bc 8c 91 7d b4 a0 d2
# This is the SHA-256 hash of the SIGNED CONTENT

# The signed content: what is it?
# In a detached CMS signature, the signed content is the data that the signature covers
# For the Insyde Secure Flash: the content = the firmware data (the .reloc section?)

# Let me verify: compute SHA-256 of the firmware data and compare with the messageDigest
expected_digest = bytes.fromhex("247ccc4ff36a83d4130567a00df6a0b5e7b242f2db618ed34abc8c917db4a0d2")
print("Expected messageDigest: %s" % expected_digest.hex())

# Candidate content ranges to hash:
# 1. The entire .fd file (0x0000 to 0x021F60C0 = before overlay)
# 2. The .reloc section (0x59E0 to 0x21F60C0)
# 3. The firmware data from some offset

candidates = [
    ("full file minus overlay", d[:0x021F60C0]),
    (".reloc section", d[0x59E0:0x021F60C0]),
    (".reloc minus reloc table", d[0x5A40:0x021F60C0]),
    ("full file", d[:0x021F6660]),
]

for name, data in candidates:
    h = hashlib.sha256(data).digest()
    match = " <<< MATCH!" if h == expected_digest else ""
    print("  %s: %s%s" % (name, h.hex(), match))

# If none match, let me try other ranges
if not any(hashlib.sha256(data).digest() == expected_digest for _, data in candidates):
    print()
    print("No direct match. Let me try other ranges...")
    # The CMS might have a different content range
    # Let me look at the CMS structure more carefully
    # The overlay header: a0 05 00 00 00 02 02 00
    # Maybe: a0 = tag, 05 00 00 00 = offset (little-endian) = 5?
    # Or: the signed content starts at a specific offset in the file
    
    # Let me try: the signed content starts from the beginning of the firmware data
    # But the "beginning" might be after the PE header
    
    for start_off in (0, 0x59E0, 0x5A40, 0x59E0, 0x280, 0x400):
        for end_off in (0x021F60C0, 0x021F5B00, 0x021F6660, 0x021F6000):
            if end_off <= start_off:
                continue
            h = hashlib.sha256(d[start_off:end_off]).digest()
            if h == expected_digest:
                print("MATCH! Range 0x%08X - 0x%08X" % (start_off, end_off))
                break
        else:
            continue
        break

    # Also try: the content might be the PFAT-capsule data
    # Let me look at the _BIOSCR2 structure more carefully
    print()
    print("=== _BIOSCR2 structure area ===")
    for i in range(0x021F5AF0, 0x021F5B20, 16):
        row = d[i:i+16]
        print("  %08X: %s  %s" % (i, row.hex(" "), "".join(chr(c) if 32 <= c < 127 else "." for c in row)))
