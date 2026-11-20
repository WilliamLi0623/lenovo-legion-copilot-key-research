# EC 固件级攻击：IHISI 直接调用技术报告

## 攻击面概述

Lenovo Legion Pro 7 16AFR10H 使用 Insyde H2O BIOS + Lenovo Secure Flash (PFAT)。
我们完全逆向了以下组件：

### 1. H2OFFT64.sys 驱动（Insyde Flash Utility Driver）
- 设备：`\\.\{EC96C944-9351-4768-B44D-6720A449F849}`
- 类型：KMDF (WDF Insyde IO Device Driver)
- 状态：仅在 H2OFFT-W.exe 运行期间加载

### IOCTL 接口完整列表

| IOCTL | Handler VA | 功能 | 输入格式 |
|-------|-----------|------|----------|
| 0x222280 | 0x21F0 | CMOS 读 | [0]=offset, [1]=0 |
| 0x222284 | 0x2B0C | CMOS 写 | [0]=offset, [1]=value |
| 0x222288 | 0x2278 | 扩展 CMOS 读 (0x72/0x73) | [0]=offset, [1]=0 |
| 0x22228C | 0x2B98 | 扩展 CMOS 写 (0x72/0x73) | [0]=offset, [1]=value |
| 0x222290 | 0x23BC | PCI 配置空间读 | 4字节 PCI 地址编码 |
| 0x222298 | 0x2300 | **物理内存读写 (>= 0xFE000000)** | [0]=地址, [4]=大小, [8:]=数据 |
| 0x22229C | 0x2278 | 同 0x222288 | |
| 0x2222E4 | 0x2878 | 其他 | |
| 0x2222E8 | 0x2B0C | 其他 | |
| 0x2222F0 | 0x2B98 | 其他 | |

### 2. IHISI SMI 通信协议

SMI 触发函数 (VA 0x1000)：
```
输入: RCX = context struct
  [0x00] = EAX (函数码, 结果返回)
  [0x04] = EBX (参数)
  [0x08] = ECX (IHISI 函数号)
  [0x0C] = EDX (SMI 端口 = 0xB2)
  [0x10] = ESI
  [0x14] = EDI
执行: OUT DX, AL (触发 SMI)
结果: 寄存器值写回 context struct
```

IHISI 缓冲区（物理地址 0xFE000000）：
- Handler (VA 0x2300) 用 MmMapIoSpace 映射并读写
- 数据写入后由 BIOS SMM handler 读取处理

### 3. IHISI 缓冲区地址
- UEFI 变量 `IhisiParamBuffer` (GUID: {92E59835-5F42-4E0B-9A84-47C7810EA806})
- 值: 0xB8D81000 (SMM scratch 区域)
- Driver 检查: command >= 0xFE000000 (只接受 0xFE000000+)

### 4. Secure Flash (PFAT) 验证

签名算法完全破解：
- CMS/PKCS#7 携带 RSA-2048 签名
- SPC_INDIRECT_DATA digest = Authenticode 哈希 (SHA-256 of PE minus CheckSum + CertDir)
- messageDigest = SHA-256 of DER(signedAttributes)
- RSA 签名覆盖 DER(signedAttributes) — 需要 Lenovo 私钥

**已验证: 修改 Authenticode 哈希后 RSA 签名失效 → BIOS 拒绝**

### 5. 攻击路径评估

| 路径 | 状态 | 阻断点 |
|------|------|--------|
| H2OFFT 直接刷补丁 .fd | ❌ | PFAT RSA 签名 |
| IHISI 0x222298 直接写 EC | ⚠️ 理论可行 | 需要正确的 IHISI 命令格式 |
| \Device\PhysicalMemory 映射 | ❌ | 需要 SYSTEM 权限 |
| 内核驱动直接调用 IHISI | ⚠️ 理论可行 | 需要自定义驱动开发 |
| ITE EC 寄存器直接编程 | ⚠️ 理论可行 | 需要知道 ITE 编程协议 |
| CH341A SPI 编程器 | ❌ 不适用 | IT8380DX flash 在芯片内部 |

### 6. EC 键盘矩阵补丁（已准备好）

```
地址: bank1 fd 0x0028900C (0x68 → 0x5A)
       bank2 fd 0x002C200C (0x68 → 0x5A)
       字表 bank1 0x27876/77, 0x27946/47, 0x279F2/F3 (FF 2A → 00 00)
       字表 bank2 0x27876/77 (FF 2A → 00 00)
```

## 下一步建议

1. **调试 H2OFFT-W.exe 刷写过程**：用 x64dbg 或 WinDbg 附加到 H2OFFT-W.exe
   捕获它发送的确切 IOCTL 调用和参数
2. **内核调试**：用 WinDbg + 串口调试查看 SMM handler 执行流程
3. **自定义内核驱动**：加载 H2OFFT64.sys（已加载），通过 IOCTL 0x222298
   以正确的 IHISI 格式发送 EC Update 命令
4. **替代方案**：使用外部 ITE EC 编程器（需要拆机）
