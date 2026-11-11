# Lenovo ThinkBook 16+ · Ultra 7 255H · Hackintosh

ThinkBook 16+ / 21TL 的 macOS Sequoia 安装与排错实录：**Intel Core Ultra 7 255H、RTX 5060 Laptop 8 GB、BE201、OpenCore 1.0.9**。

本机已完成 macOS 15.8.2 安装；显卡、默认 200% HiDPI、背光和内置扬声器有通过记录，Wi-Fi 已联网但仍抖动。**蓝牙未修复，触控板仍漂移，整机睡眠未通过，摄像头和麦克风待验证。** 本仓库公开教程、踩坑、补丁、参考配置、对应源码与许可证，记录成功过程，也保留失败边界。

资料整理日期：**2026-11-11**。硬件结论截止 **2026-11-05**；最后身份加载验收启动为 **2026-11-05 20:20:42（北京时间）**，完整功能测试分别注明日期。本次公开整理没有重新启动硬件验收。

## 硬件与软件

| 项目 | 本机配置 |
|---|---|
| 笔记本 | Lenovo ThinkBook 16+，机器类型 **21TL** |
| CPU | Intel Core Ultra 7 **255H**（不是 255HX） |
| 内存 | 32 GB |
| 独立显卡 | NVIDIA GeForce RTX 5060 Laptop GPU，8 GB；本机独显模式 |
| 内屏 | 3200×2000 @ 165 Hz；逻辑 1600×1000、缩放 2 倍 |
| 存储 | KIOXIA 2 TB；利用已有 ESP 与专用 APFS 分区 |
| Wi-Fi / 蓝牙 | Intel BE201：PCI `8086:7740` / USB `8087:0037` |
| 内置有线 | Intel I219 系列，PCI `8086:57A1` |
| 音频 | ALC257 / `10EC:0257`，子系统 `17AA:3DD3`；HDA 控制器 `8086:7728` |
| 触控板 | GXTP5100 / `27C6:01E9`，I2C |
| 系统 | macOS Sequoia **15.8.2 / 24H232**，Darwin 24.6.0，x86_64 |
| OpenCore | **1.0.9 DEBUG**，固定源码与工具版本见资源清单 |
| SMBIOS | 当前 **MacPro7,1**；安装早期为 MacBookPro16,2；身份值不公开 |
| NVIDIA 驱动 | 第三方 NullMoth **2.6.6**，系统侧安装；2.7.1 仅准备，未证实升级 |

## 功能状态

| 功能 | 最后有证据的结论 |
|---|---|
| 系统安装 / 进入桌面 | ✅ 完成安装；不等于全功能正常 |
| RTX 5060 / Metal / HiDPI | ✅ Metal 3、8 GB、3200×2000 @ 165 Hz、默认 200% |
| 背光 / 内置扬声器 | ✅ 用户确认有效；不包含耳机与录音 |
| BE201 Wi-Fi | ⚠️ DHCP、DNS、公网 ICMP、HTTPS 通过；延迟抖动，长期稳定性待测 |
| 内置有线 | ⚠️ IntelMausi 已接管；未完成插线联网验收 |
| GXTP5100 | ⚠️ 接管与手势可用；离手及电池供电仍漂移 |
| G502 USB 鼠标 | ✅ 用户调整指针加速后恢复；具体数值未记录 |
| 蓝牙 `8087:0037` | ❌ 固件标记出现，但真实控制器仍失败，扫描配对未通过 |
| USB / 扩展坞 | ⚠️ NHI 误绑已排除；专用端口映射未完成，历史鼠标失灵未定因 |
| 摄像头 / 麦克风 / 耳机 | ❔ 摄像头、麦克风疑似不可用；耳机与输入功能待实测 |
| 整机睡眠 | ❌ 合盖仅记录灭屏/亮屏，Sleep Count 仍为 0 |
| AirDrop / 接力 / Apple 服务 | ❔ 无完整验收；本方案不提供 AWDL/AirDrop 能力承诺 |

详细时效和证据见[验收状态表](验收状态表.md)与[最后收尾状态](当前状态-20261105.md)。

## 阅读顺序

1. [安装实录](文档/安装实录.md)：安装前提、CPU 组合、Recovery、安装阶段重启与显卡收尾。
2. [踩坑与解决办法](文档/踩坑与解决办法.md)：每项按症状、依据、尝试、处理、验证、回退和来源整理。
3. [主教程](主教程.md)：驱动、ACPI、固件、ABI、最小变更和逐项验收的技术细节。
4. [日用设置与多系统回退](文档/日用设置与多系统回退.md)：使用习惯与失败案例，已撤回的四系统方案仅作历史记录。
5. [资源与版本清单](资源与版本清单.md)、[源码与构建](源码与构建/README.md)、[许可证](许可证/README.md)。

安装过程照片见[照片索引](照片/README.md)；仅发布经检查且去除 EXIF/GPS 元数据的副本。含序列号、BIOS 标识和账户细节的原图留在本地。

## 下载与 EFI 状态

- [资料与源码 ZIP](https://github.com/Gsheep0729/ThinkBook-16Plus-255H-Hackintosh/raw/refs/heads/main/下载/ThinkBook-16Plus-255H-资料与源码-20261111.zip)
- [安装过程照片 ZIP](https://github.com/Gsheep0729/ThinkBook-16Plus-255H-Hackintosh/raw/refs/heads/main/下载/ThinkBook-16Plus-255H-过程照片-20261111.zip)
- [ZIP SHA-256](https://github.com/Gsheep0729/ThinkBook-16Plus-255H-Hackintosh/raw/refs/heads/main/下载/SHA256SUMS.txt)
- [完整仓库 ZIP](https://github.com/Gsheep0729/ThinkBook-16Plus-255H-Hackintosh/archive/refs/heads/main.zip)

**本次没有发布可启动的完整 EFI。** [EFI参考](EFI参考/README.md)内是身份清空、注入默认禁用的字段模板，不能复制到 ESP 启动。完整 EFI 以最后启动验收对应的私有 `79665d05…` 归档为基线，待[依赖来源缺口](文档/EFI发布状态.md)补齐后再发布；不拿官方参考替换件继承原机启动结论。

即使今后发布 EFI，读者也必须核对自己硬件并填写独立身份；RTX 5060 的系统侧 NVIDIA 驱动与恢复机制不能仅靠 EFI 代替。第三方驱动从项目作者官方来源获取，具体链接见资源清单。

将资料与源码、过程照片两份ZIP解压到同一目录后，运行完整只读校验：

```sh
python3 工具/验证发布清单.py .
```

校验报告见[本次发布验证](校验/发布验证说明.md)。校验通过证明文件完整与静态结构，不证明另一台机器能启动。

## 致谢与许可

感谢 [Dortania](https://dortania.github.io/OpenCore-Install-Guide/)、[acidanthera](https://github.com/acidanthera)、[OpenIntelWireless](https://github.com/OpenIntelWireless)、[VoodooI2C](https://github.com/VoodooI2C)、[HuajiFruit/AirportBZ](https://github.com/HuajiFruit/AirportBZ)、[USBToolBox](https://github.com/USBToolBox/kext)、[NullMoth](https://github.com/nullmoth/nvidia-macos-driver)、linux-firmware 等项目。首页结构参考[社区 ThinkBook 仓库](https://github.com/aleixsr/ThinkBook-16-G6-ABP-Hackintosh)，其不同硬件的结论不用于本机验收。

原创整理可在保留标题、来源、证据日期和未解决边界的前提下转载；原创代码/SSDT 按随附 MIT 许可，上游软件、补丁及固件按各自许可证。见[许可入口](许可证/README.md)。macOS 镜像、系统框架、个人身份与私人备份不在发布范围内。
