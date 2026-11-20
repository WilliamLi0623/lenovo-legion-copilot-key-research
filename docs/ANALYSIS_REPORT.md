# Legion Pro 7 16AFR10H — Copilot 键固件级重映射：终版分析报告（R2 完成）

## 一、按键机制的完整结论（全链路已证实）

```
物理按下 Copilot 键
 ├─ [硬件层] EC 键盘矩阵处理 → PS/2 合成和弦 Win+Shift+F23
 │    (LL钩子实测3次一致：scan 0x5Bext/0x2A/0x6E，injected=0)
 └─ [ACPI层] EC 写 LSKV 寄存器 → SCI → DSDT _Qxx → LSKD=LSKV
      → Notify(WMIU, 0xD0) → _WED(0xD0)=LSKD → Windows WMI 事件
      → Lenovo 软件 (FnHotkeyUtility/LenovoSmartService) 启动 Copilot/小天
PowerToys KBM (91;160;134→163) 在硬件层和弦之后、消费级之前拦截 → 右Ctrl（现役方案）
```

## 二、DSDT/ACPI 层（本轮全破，iasl 20260930 反编译）

| 对象 | 位置/内容 |
|---|---|
| **WMIU 设备 (LSK20)** | DSDT L24143：`_HID PNP0C14, _UID "LSK20"`，`_WDG` 3 项 |
| LENOVO_UTILITY_DATA 方法 | `_WDG` ObjectId "SK" → `WMSK(Arg0,Arg1,Arg2)`：按 Arg2 查功能支持（0x02/0x03/0x07/0x08/0x0E/0x0F/0x13/0x15/0x16/0x17/0x26 → 0x03/0x02/0x15/0x1A/0x1B/0x24…），依赖 LTKB（键盘布局类型）/LTCC |
| AI 键事件 | EC 写 LSKV → SCI → AML（DSDT L13027）→ `LSKD=LSKV; Notify(WMIU,0xD0)` → `_WED(0xD0)=LSKD`；软件注入模拟：WMAE SFV0=0x000A0000+SFV1=1/2 → LSKD=0x31/0x32 |
| **LENOVO_OTHER_METHOD** | `_WDG` GUID `DC2A8805-3A8C-41BA-A6F7-092E0089CD3B` ObjectId "AE" → **WMAE(inst, cmd, buffer)**（LegionToolkit 同款 GUID） |
| WMAE 命令空间 | Arg1=0x11 读 / 0x12 写（推断）、0x33 等类；Arg2 4字节子命令（0x00010000、0x00030000=FnLock、0x000A0000=AI键、0x001A0000=AI键开关…）GFDI/SFV0/SFV1 字段解析 |
| **AI 键固件级开关** | `If (PANT & 0x02) { WECM(0x7F, x); M010(0x4A, x) }` —— WECM=写 IO 0x72/73（扩展CMOS bank 0x7F），M010=外部方法（定义表未在静态镜像内找到） |
| RECM/WECM 原语 | `OperationRegion (ECMS, SystemIO, 0x72, 0x02) { INDX, DATA }` —— 即扩展 CMOS 读写 |
| 能力描述符表 | WQA8（机型 switch）+ 按功能索引返回 12 字节描述符（0x08/0x09=AI能力 AISF 位、0x14=AI键→事件0x1A、能力位7） |
| EC0 关键 NVRAM 位段 | PANT(bit1=AI键存在)、AISF(AI支持)、LTKB、LTCC、GSKU、FNCE、FLBT、GFPB/GFPP |
| 27 项 _WDG | GameZone 全 GUID↔ObjectId 映射已解码（WMAA-WMAF/WQAA-WQAD…） |

## 三、EC 固件层（上轮已定位，本轮补充）

- bank1 = fd 0x260000（176KB）、bank2 = fd 0x299000（+256B 签名块@+0xA30）
- 键盘矩阵表 bank+0x28FE5（128 项）；字表 A/B（+0x27840/+0x278F0）；FF 配置表（bank+0x21100 区多份）；Fn 组合表（+0x2AD2 起多布局副本）
- **AI 键处理程序地址：字表 A 键 0x68 → 0xFF2A，B → 0xFF00**（差值 0x2A=LSHIFT 码；fd 0x26FF2A/0x26FF00 处有真实代码，两个状态处理器仅 0x2C/0x2D、0x89/0x75 等常数不同）
- **未破**：ITE 专有 8 位核指令集（RISC-V 假设已排除：capstone RISC-V 解码 0 条）；EC 代码窗口→flash 映射；EC 校验和（3CC3A55A 与 15 种范围 CRC32/CRC16/sum 均不匹配）

## 四、结论与可行路径

| 路径 | 状态 | 说明 |
|---|---|---|
| **A. PowerToys（现役）** | ✅ 已工作 | 硬件和弦被正确消费；唯一缺口=登录前/UEFI 内不生效 |
| **B. Lenovo 官方 CustomizeKey** | ✅ 可用 | FnHotkeyUtility 自带"自定义按键"（LaunchLeovoCustomizeKey）→ 软件级映射，开机自启即覆盖登录后全部场景 |
| **C. EC flash 补丁（原 C 路线）** | ⏳ 卡在 ITE 专有 ISA | 矩阵表/字表/FF配置表/双状态机制全已定位到地址；最后一公里=反汇编 bank+0xFF2A 和弦发射器 + 校验和算法 + 双 bank 刷写。需多轮会话 + 变砖风险（EC 刷坏=无法上电，需编程器救） |
| **D. AI 键固件级"禁用"** | ✅ 可达 | WMAE cmd 0x33 / SFV0=0x001A0000 → M010(0x4A,0)——但只会关掉和弦（键变死），不产生右Ctrl；且依赖缺失定义表的 M010 |

**给你的建议**：C（固件真重映射）在技术上完全可行但需要继续攻 ITE 专有 ISA（预计还要数轮，且刷写环节有一锤子买卖风险——EC 刷坏整机点不亮，只能拆机 CH341A 编程器救）。当前 PowerToys 方案已经是等效终态。如果你要继续攻 C，下一步是：把 WMAE 的完整 1607 行命令表整理成文档 + 用 Python 写 ITE 8 位核的推测式反汇编器（用已知行为的键做参照校准），这属于纯离线工作，零风险；刷写动作会单独再向你确认。
