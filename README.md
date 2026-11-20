# Lenovo Legion Pro 7 Copilot Key EC Firmware Research

Reverse engineering and patching research for remapping the Copilot (AI) key to Right Ctrl on the **Lenovo Legion Pro 7 16AFR10H** (BIOS: SMCN20WW, EC: ITE IT8380DX V1.43).

## Summary

The Copilot key on this laptop is **not** a software-triggered key. It is the **ITE IT8380DX embedded controller's hardware keyboard matrix** that directly emits the `Win+Shift+F23` PS/2 chord. No Windows-level software hook (including PowerToys) sees an "injected" flag — the chord comes from below kbdclass.

This research mapped the complete data path:

```
Copilot key press
  → ITE EC keyboard matrix (internal code 0x68)
    → EC word table handler (word = FF 2A = special chord)
      → EC emits PS/2 chord: 0x5B(ext) + 0x2A + 0x6E
        → i8042 → kbdclass → Windows sees Win+Shift+F23
```

## Key Findings

### EC Keyboard Matrix Table
- Location: `bank1+0x28FE5` (fd offset `0x00288FE5`), 128 entries (16 rows × 8)
- AI key = row 4, position 7, internal code `0x68`
- Word table (3 copies): `bank1+0x277C0/0x278E4/0x27994`
- Key 0x68 entries: `(FF,2A)` / `(FF,00)` / `(FF,40)` = chord handlers

### Proposed EC Patch (10 bytes)
| Location | Original | Patched | Meaning |
|----------|----------|---------|---------|
| Matrix fd 0x0028900C | 0x68 | 0x5A | AI key → Right Ctrl candidate |
| Matrix fd 0x002C200C | 0x68 | 0x5A | bank2 sync |
| Word table 0x00287876-77 | FF 2A | 00 00 | Disable chord handler |
| Word table 0x00287946-47 | FF 00 | 00 00 | Layout 2 |
| Word table 0x002879F2-F3 | FF 40 | 00 00 | Layout 3 |
| Word table 0x002C0876-77 | FF 2A | 00 00 | bank2 sync |

### ACPI/WMI Data Path
```
EC → SCI → DSDT _Qxx → LSKV → LSKD → Notify(WMIU, 0xD0) → _WED(0xD0)
  → LENOVO_UTILITY_DATA (CE6C0974-0407-4F50-88BA-4FC3B6559AD8)
    → FnHotkeyUtility.exe
```

### H2OFFT64.sys Driver IOCTLs (Fully Reversed)

| IOCTL | Function | Handler VA |
|-------|----------|-----------|
| 0x222280 | CMOS read (port 0x70/0x71) | 0x21F0 |
| 0x222284 | CMOS write | 0x2B0C |
| 0x222288 | Extended CMOS read (port 0x72/0x73) | 0x2278 |
| 0x22228C | Extended CMOS write | 0x2B98 |
| 0x222290 | PCI config space read | 0x23BC |
| 0x222298 | **Physical memory read/write** (>= 0xFE000000) | 0x2300 |
| 0x22229C | Extended CMOS read | 0x2278 |

### IHISI SMI Protocol

```
Context struct (via IOCTL 0x222298):
  [0x00] = EAX (IHISI function)
  [0x04] = EBX (parameter)
  [0x08] = ECX (function number)
  [0x0C] = EDX (SMI port = 0xB2)
  [0x10] = ESI
  [0x14] = EDI
Trigger: OUT DX, AL (SMI)
Buffer: Physical address 0xFE000000 (via MmMapIoSpace)
UEFI variable: IhisiParamBuffer = 0xB8D81000 (GUID: 92E59835-5F42-4E0B-9A84-47C7810EA806)
```

### Secure Flash (PFAT) Protection

**Fully broken** the Authenticode hash algorithm:
- SPC_INDIRECT_DATA digest = `SHA-256(PE file minus CheckSum field minus Certificate Directory)` 
- Verified: `633d25d1affa88d439f78e24b6dff177b89c1a1354217ce9be974d86eac41de3` ✓

**But**: RSA-2048 signature covers the signedAttributes (including messageDigest).
Without the Lenovo private key, the signature cannot be forged.

### Flashing Attempts (11 experiments)

| # | Method | Result |
|---|--------|--------|
| 1 | Patched .fd + intact signature | ❌ Checksum incorrect! |
| 2 | Patched .fd + erased signature | ❌ Invalid Firmware (BIOS) |
| 3 | + SkipSecureBootProtectionCheck | ❌ Invalid Firmware |
| 4 | + SkipBootGuardVersionVerification | ❌ Invalid Firmware |
| 5 | + -mfg (manufacture mode) | ❌ Invalid Firmware |
| 6 | + Embedded platform.ini modified | ❌ Invalid Firmware |
| 7 | -ecupdate:FILE | ❌ Invalid parameters |
| 8 | -ec | ❌ Invalid parameters |
| 9 | -ecp | ❌ No effect |
| 10 | IHISI direct via IOCTL | ⚠️ SMI triggered, format wrong |
| 11 | Original .fd (reference) | ✅ **Flash succeeded** |

### Why EC Update is Blocked

The H2OFFT.log reveals:
```
Platform [Secure]
BIOS Guard (PFAT) [NOT Support]
[UpdateEC] Flag=1 does not valid in secure flash mode, revised to 0
```

Even though PFAT is **NOT** supported, the BIOS still validates the firmware image. The `UpdateEC` flag is **forcefully overridden to 0** in Secure mode by H2OFFT-W.exe itself (hard-coded logic, not ini-controlled).

## Working Solution

**PowerToys Keyboard Manager** remaps Copilot key → Right Ctrl perfectly for all Windows use. This is the **terminal solution** for this problem under Lenovo Secure Flash protection.

## Repository Structure

```
├── docs/
│   ├── FINAL_REPORT.md          # Complete research report
│   ├── IHISI_ATTACK_REPORT.md   # IHISI SMI protocol details
│   └── ANALYSIS_REPORT.md       # Initial analysis findings
├── tools/                       # Python analysis scripts
│   ├── fd_scan.py              # FV/FFS scanner for the .fd image
│   ├── fn_tables.py            # Fn-combo table parser
│   ├── key_hook.py             # LL keyboard hook (scancode capture)
│   ├── checksum_hunt.py        # EC checksum algorithm search
│   ├── template_hunt.py        # EC code template finder
│   └── ...
├── analysis/                    # Extracted data from the .fd
│   ├── parts/                  # 763 extracted FFS sections
│   ├── strings/                # String tables
│   └── index.json              # Section index
├── patches/                     # EC patch files (offsets + data)
└── README.md
```

## Hardware Details

| Component | Detail |
|-----------|--------|
| Laptop | Lenovo Legion Pro 7 16AFR10H (83RU) |
| BIOS | Insyde H2O SMCN20WW (2026-03-26) |
| EC | ITE IT8380DX V1.43 (internal flash, dual-bank) |
| EC bank1 | fd 0x260000–0x28B000 (176KB) |
| EC bank2 | fd 0x299000–0x2C4000 (176KB, backup) |
| EC descriptor | bank1+0xEB0: `A5A5A5A5A5A5 A494 8512 5A5A AA00 5555` + "ITE8380-EC-V1.43" |
| BIOS FV main | fd 0x1328E30 (10MB) |
| ACPI DSDT | INSYDE, 112KB decompiled |

## Tools Used

- Python 3.12 + capstone 5.0.7
- iasl (ACPICA 20260930) via WSL
- 7-Zip
- ctypes (Windows API: LL hooks, UEFI variables, DeviceIoControl)
- H2OFFT-W.exe v6.7.3.0 (Insyde flash tool)

## Disclaimer

This research is for **educational purposes** on **your own hardware**. Flashing EC firmware carries brick risk. Always have a recovery plan (CH341A + ITE adapter, or a second laptop with a CH341A to reprogram).

## License

MIT
