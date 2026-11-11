# EFI 字段参考：不能直接启动

[配置模板](OC/config-参考-全部禁用.plist)从11月5日MacPro7,1写后基线`79665d05…`派生。本轮核对模板实际型号为MacPro7,1；MacBookPro16,2是早期安装历史。

- SystemSerialNumber、MLB、SystemUUID为空，ROM为六个零；没有可用个人身份。
- ACPI/Add、Kernel/Add、UEFI/Drivers、Misc/Tools全部默认禁用；仅保留排错相关条目。
- 不包含固件DSDT、完整基础驱动、OpenCore.efi、BOOTX64.EFI、UEFI驱动和USB映射。
- ProvideCustomSlide、EnableWriteUnprotector、AllowRelocationBlock、EnableSafeModeSlide及RequestBootVarRouting设为false，是为禁用OpenRuntime的参考模板作结构处理，不是对实际机器的修复建议。
- 模板使用Builtin/Auto，不复刻原机主题；不能作为原机回退整包。

使用自己的有效EFI作起点，核对硬件与路径后只合并所需字段；保留自己的身份、驱动与完整备份。三张公开SSDT分别对应背光、触控板接管和音频，是否复用须逐项核对。

公版模板的配套静态检查见[验证说明](../校验/发布验证说明.md)。完整EFI发布条件及来源缺口见[EFI发布状态](../文档/EFI发布状态.md)。本仓库不通过替换来源不明的依赖来虚构原机启动验收。
