import ctypes, ctypes.wintypes as wt

def try_open(path, tag):
    k32 = ctypes.WinDLL('kernel32', use_last_error=True)
    GENERIC_READ = 0x80000000
    GENERIC_WRITE = 0x40000000
    h = k32.CreateFileW(path, GENERIC_READ | GENERIC_WRITE, 0, None, 3, 0, None)
    err = ctypes.get_last_error()
    if h != ctypes.c_void_p(-1).value and h != -1:
        print("%s: OPENED handle=%s" % (tag, h))
        k32.CloseHandle(h)
    else:
        print("%s: FAILED err=%d (5=access denied, 2=not found)" % (tag, err))

try_open(r'\\.\WinMsrDev', 'WinMsrDev')
try_open(r'\\.\{EC96C944-9351-4768-B44D-6720A449F849}', 'H2OFFT-guid')
try_open(r'\\.\LnvMiniFilterDriverPort', 'LnvMiniFilter')
try_open(r'\\.\PhysicalDrive0', 'PhysicalDrive0(non-admin expect deny)')
