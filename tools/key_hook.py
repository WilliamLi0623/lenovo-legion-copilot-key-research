import ctypes, ctypes.wintypes as wt, time, sys, datetime

LOG = r"C:\Users\William Li\Documents\deepseek-harness\default-workspace\bios_copilot\copilot_press.log"
OUT = open(LOG, 'w', encoding='utf-8')
user32 = ctypes.WinDLL('user32', use_last_error=True)
LRESULT = ctypes.c_ssize_t
WH_KEYBOARD_LL = 13
HC_ACTION = 0
PM_REMOVE = 1

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [('vkCode', wt.DWORD), ('scanCode', wt.DWORD), ('flags', wt.DWORD),
                ('time', wt.DWORD), ('dwExtraInfo', ctypes.POINTER(wt.ULONG))]

HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wt.WPARAM, ctypes.POINTER(KBDLLHOOKSTRUCT))

EV = {0x0100: 'DOWN', 0x0101: 'UP', 0x0104: 'SYSDOWN', 0x0105: 'SYSUP'}
VN = {0x5B: 'LWIN', 0x5C: 'RWIN', 0xA0: 'LSHIFT', 0xA1: 'RSHIFT', 0xA2: 'LCTRL', 0xA3: 'RCTRL',
      0x86: 'F23', 0x87: 'F24', 0x2C: 'VK_PRINT', 0xC0: 'VK_0xC0', 0xC1: 'VK_0xC1',
      0x70: 'VK_F1_0x70', 0x278: 'VK_278', 0x279: 'VK_279'}

def proc(nCode, wParam, lParam):
    if nCode == HC_ACTION:
        k = lParam.contents
        name = VN.get(k.vkCode, '')
        line = "%s %s vk=0x%02X scan=0x%03X ext=%d injected=%d %s" % (
            datetime.datetime.now().isoformat(timespec='milliseconds'),
            EV.get(wParam, hex(wParam)), k.vkCode, k.scanCode,
            k.flags & 1, (k.flags >> 4) & 1, name)
        print(line, file=OUT, flush=True)
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

cb = HOOKPROC(proc)
hhk = user32.SetWindowsHookExW(WH_KEYBOARD_LL, cb, None, 0)
if not hhk:
    print("HOOK FAILED err=%d" % ctypes.get_last_error(), file=OUT, flush=True)
    sys.exit(1)
print("HOOK ACTIVE, capturing for %s s" % (sys.argv[1] if len(sys.argv) > 1 else 90), file=OUT, flush=True)
msg = wt.MSG()
end = time.time() + float(sys.argv[1] if len(sys.argv) > 1 else 90)
while time.time() < end:
    while user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, PM_REMOVE):
        user32.TranslateMessage(ctypes.byref(msg))
        user32.DispatchMessageW(ctypes.byref(msg))
    time.sleep(0.02)
user32.UnhookWindowsHookEx(hhk)
print("DONE", file=OUT, flush=True)
