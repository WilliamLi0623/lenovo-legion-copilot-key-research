import struct, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d = open(r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\extract\WinSMCN20WW.fd", "rb").read()

# Found RSA public keys embedded in the BIOS at:
# 0x011E7F8E: modulus starts with e1 ec 19 1d f8 2e 40 a9...
# 0x011E83F3: modulus starts with c4 e8 b5 8a bf ad 57 26...
# 0x011E89B7: modulus starts with e3 5e 88 8b 73 2c c3 0a...
# These are RSA-2048 public keys (modulus = 0x101 = 257 bytes with leading 00)

# These are likely the Intel Boot Guard OEM keys and the Insyde Secure Flash key
# Let me extract the full modulus from each

for key_off in (0x011E7F8E, 0x011E83F3, 0x011E89B7):
    # After the RSA OID (11 bytes) + 05 00 (2 bytes) + 03 82 01 0F 00 (5 bytes)
    # = 18 bytes after OID start, the modulus begins
    # Structure: OID(11) + 05 00(2) + BIT STRING header(5) + 30(1) + 82(2) + 01 0A(2) + 02 82(2) + 01 01(2) + 00(1)
    # The modulus data starts at key_off + 11 + 2 + 5 + 1 + 2 + 2 + 2 + 2 + 1 = key_off + 28
    mod_start = key_off + 28
    mod_len = 0x101  # 257 bytes (leading 00 + 256 bytes modulus)
    modulus = d[mod_start:mod_start + mod_len]
    # Skip leading 00
    actual_mod = modulus[1:]
    print("=== RSA Key @0x%08X ===" % key_off)
    print("  Modulus length: %d bits" % (len(actual_mod) * 8))
    print("  First 16 bytes: %s" % actual_mod[:16].hex(" "))
    print("  Last 4 bytes: %s" % actual_mod[-4:].hex(" "))
    print()

# Now let me search for the HASH of the firmware that the BIOS compares
# The BIOS would compute SHA-256 of the firmware data and compare
# with the value in the signed attributes (messageDigest)
# The SHA-256 constant in the certificate area

# Let me look at the certificate area to find the messageDigest
# The CMS structure at 0x021F60C8:
# SEQUENCE (1423 bytes)
#   OID 1.2.840.113549.1.7.2 (signedData)
#   [0] { SEQUENCE (1408 bytes)
#     INTEGER 1
#     SET { SHA-256 OID }
#     EncapContentInfo
#     [0] { certificates }
#     SET { SignerInfo {
#       INTEGER 1
#       IssuerAndSerialNumber
#       SHA-256 OID
#       [0] { signed attributes:
#         contentType
#         messageDigest (SHA-256 of the signed content)
#       }
#       RSA OID
#       OCTET STRING signature
#     }}
#   }

# The signed attributes contain the messageDigest = SHA-256 of the content
# The RSA signature covers the DER-encoded signed attributes
# To change the content, we need to:
# 1. Recompute SHA-256 of the new content
# 2. Update the messageDigest in the signed attributes
# 3. Re-sign the signed attributes with RSA-2048 (needs private key)

# BUT: What if the BIOS doesn't verify the RSA signature at all?
# What if it only checks the SHA-256 messageDigest?
# In that case:
# 1. Recompute SHA-256 of the new content
# 2. Update the messageDigest
# 3. The RSA signature would be "invalid" but not checked!

# Let me test this theory: patch the .fd with EC changes AND update
# the messageDigest in the CMS. If the flash succeeds, the BIOS only checks SHA-256!
