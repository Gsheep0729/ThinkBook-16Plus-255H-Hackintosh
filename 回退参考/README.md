# 按目标字段回退，不发布机器绑定的一键安装器


本页驱动事务主要对应11月4日过程；11月5日最后私有基线已是79665d05…/MacPro7,1，见[当前状态](../当前状态-20261105.md)。历史回退字段不授权恢复旧整包。

原维护脚本绑定本机路径、ESP标识、完整清单与多次提权事务，不适合别人运行，因此没有收入公开包。下面是对**自己最新离线config副本**的操作示例；不是本次已执行的系统变更，也不是把整个参考模板写入ESP的说明。

共同步骤：确认当前实际引导源 → 完整备份 → 在离线副本只改下表目标 → 比较语义与文件清单 → 配套ocvalidate → 人工写入最小集合并回读 → 卸载 → 用户保存工作后手动重启。没有后续变更才允许恢复自己那次的整份config；否则必须重新基于最新配置撤差异。

| 目标 | 只撤销这些配置/文件 | 保留什么 |
|---|---|---|
| 最新HDA0 | 从ACPI/Add停用或移除SSDT-HDA0，确认无引用后移走AML | 蓝牙、原设备属性、AppleALC、GPU与其他ACPI；早期HDA设备属性实验另行撤 |
| 最新蓝牙 | 停用/移除IntelBluetoothFirmware、IntelBTPatcher、BlueToolFixup三项；移走对应完整bundle | HDA0、Wi-Fi、触控板、NVIDIA、Lilu |
| Wi-Fi | 撤AirportItlwm项/bundle；恢复自己改前CNVW表Enabled值 | 后续音频/蓝牙及现有出网兜底 |
| 背光开关 | 只从boot-args移除新增nvrmacpibl=1 | 所有原NVIDIA参数、Block与工具；PNLF若另撤只撤该表 |
| TPI0/本机I2C人格 | 撤TPI0条目/表，恢复自己改前I2C Info；换过完整bundle则恢复完整bundle | 其他输入驱动、GPU、CPU、SMBIOS；不要盲删全部ACPI |
| 有线 | 撤本轮IntelMausi条目/bundle；原先已有则恢复完整原bundle | 其他驱动与最新显卡配置 |

[原版IntelMausi 1.0.8](IntelMausi-1.0.8-original.kext)仅供精确输入核对和还原原文件；它不识别57A1，不是联网已通过的备选包。[修改前I2C Info](VoodooI2C-Info-before-ArrowLake.plist)来自加入ArrowLake人格之前，只适合作字段对比；另一台机器应使用自己的备份。

macOS不能启动时：进入原Windows Boot Manager，依据自己记录的物理盘、分区标识、偏移、大小和卷对应关系确认正确ESP，先备份现状，再将已审阅的回退副本写入目标。不要猜盘符，不用mountvol /S自动选择另一块盘的ESP，不删Windows/Linux原引导。无需为了撤这些驱动执行Remove NVIDIA driver、Reset NVRAM或恢复显卡安装前config。

公版模板故意默认禁用，不能作为源机器实际的可启动回退config。私人整份回退文件从未随包发布。

15:03新增量回退：Gen3错误处理单项撤回仅恢复自己保存的4b955161…旧可执行文件，保留0037/0291匹配；更稳妥的故障隔离是直接从最新config停用整组三个蓝牙条目。原本机蓝牙事务会校验旧二进制，最新版会使其停止，不能强行跳过，须按本机最新单文件回退顺序或手工从最新配置撤项。USB只恢复改前UTBDefault Info，不动config及其他驱动。本包不包含机器绑定事务脚本。

当前已完成18:45重启：声卡扬声器通过、NHI错绑消失；蓝牙控制器失败、触控板跳动。16:05后已有主题事务，不能用旧f3140c7c…整份config回灌撤驱动。任何回退应重新读取当时实际EFI，只撤指定驱动/字段并保留PickerMode/Variant、OpenCanopy和主题资源；菜单逻辑还可能有后续维护。最近归档9d31f082…仅是历史来源，不保证仍匹配现场。
