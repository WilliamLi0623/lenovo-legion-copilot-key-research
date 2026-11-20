#Requires AutoHotkey v2.0
#SingleInstance Force
; =====================================================================
; Legion Pro 7 (16AFR10H) Copilot 键 → 右Ctrl
; 原理: 键盘固件把 Copilot 键发成 Win + Shift + F23 (微软标准实现)
;       本脚本在 F23 到达时虚拟释放 Win/Shift、按下右Ctrl, 随物理释放
; 注意: 启用本脚本前, 先在 PowerToys → Keyboard Manager 里停用
;       "Win+Shift+F23 → 右Ctrl" 那条规则, 否则会双重转换
; =====================================================================
*F23:: {
    Send("{LWin up}{LShift up}{RCtrl down}")
    KeyWait("F23")
    Send("{RCtrl up}")
}
