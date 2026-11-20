# EC Patch Data — Copilot Key → Right Ctrl

## Patched Bytes

### Matrix Table (EC bank1, fd offset 0x00288FE5)

The AI key is at row 4, position 7 in the 16×8 matrix table.
File offset of the AI key entry: `0x0028900C`

```
fd_offset  original  patched
0x0028900C   0x68     0x5A    # AI key → internal code 0x5A (Right Ctrl candidate)
0x002C200C   0x68     0x5A    # bank2 (backup) sync
```

### Word Table Key 0x68 Entries

Three copies in bank1 + one in bank2:

```
fd_offset    original  patched
0x00287876   0xFF      0x00    # Table A: chord handler flag
0x00287877   0x2A      0x00    # Table A: chord param (LSHIFT)
0x00287946   0xFF      0x00    # Table B: chord handler flag
0x00287947   0x00      0x00    # Table B: chord param (already 0)
0x002879F2   0xFF      0x00    # Table C: chord handler flag
0x002879F3   0x40      0x00    # Table C: chord param
0x002C0876   0xFF      0x00    # bank2 Table A sync
0x002C0877   0x2A      0x00    # bank2 Table A param sync
```

## How to Apply

1. Open `WinSMCN20WW.fd` in a hex editor
2. Apply the byte changes listed above
3. Flash using H2OFFT (requires bypassing Secure Flash — see docs)

## Alternative: Iterate

If `0x5A` does not produce Right Ctrl (E0-1D):
- Try `0x5B` → might be RAlt (E0-38) or another E0 key
- Try `0x5C` → might be End (E0-4F) or another E0 key
- Flash, test, adjust

## Risk Warning

⚠️ Flashing the EC during power loss = laptop won't boot.
⚠️ The ITE IT8380DX has internal flash — CH341A cannot be used directly.
⚠️ Secure Flash validation will reject any modified .fd without Lenovo's private key.
