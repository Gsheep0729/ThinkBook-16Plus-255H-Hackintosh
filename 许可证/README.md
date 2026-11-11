# 许可与转载说明

上游软件、固件、SDK及其中各文件保留原版权、许可证及限制，本包没有将它们统一重新授权。源码各自原位置的许可与文件头是依据；集中副本便于阅读。版权作者、项目账户及标准协议常量属于上游署名/实现，不是本机隐私，予以保留。

| 材料 | 许可入口 |
|---|---|
| IntelMausi及本地识别补丁 | [GPLv2](IntelMausi-LICENSE.txt)，另保留源码中的APPLE_LICENSE等文件 |
| VoodooI2C、GPIO/HID | 原源码GPL及各文件许可，见[上游许可副本](VoodooI2C-LICENSE.txt)和子模块源码；上游根许可开头文字原样保留，完整GPLv3另见IntelBluetoothFirmware许可 |
| VoodooInput | [GPLv2](VoodooInput-LICENSE.txt) |
| AirportBZ | [GPLv2](AirportBZ-LICENSE)，另保留BSD/OpenBSD等源文件头与[Intel固件许可](AirportBZ-iwlwifi-firmware-license) |
| IntelBluetoothFirmware及0037增量 | [GPLv3](IntelBluetoothFirmware-LICENSE)，嵌入固件另循Intel固件许可 |
| BlueToolFixup / BrcmPatchRAM | [GPLv2](BrcmPatchRAM-LICENSE)及各源文件许可 |
| Lilu、AppleALC、BrightnessKeys | 各自BSD类许可，见[Lilu](Lilu-LICENSE.txt)、[AppleALC](AppleALC-LICENSE.txt)、[BrightnessKeys](BrightnessKeys-LICENSE) |
| OpenCorePkg / ocvalidate | [BSD类项目许可](OpenCorePkg-LICENSE.txt)与其第三方文件许可 |
| MacKernelSDK | [APSL 2.0](MacKernelSDK-LICENSE.txt)及各头文件/库附带声明；这是公开SDK源码，不是打包macOS系统框架 |
| 精确0291 SFI/DDC | [Intel固件许可](Intel-firmware-LICENCE.Intel)，固定linux-firmware快照中实际路径为LICENSES/LICENSE.intel |

本次新增的原创中文整理文字可公开转载，请保留标题、证据截止日期、项目来源及“待验收”边界，不将实验改称成功。本次新增Python操作示例及本地原创SSDT采用[MIT许可](原创代码-MIT.txt)；涉及上游源码的补丁随相应上游许可。不要删除固件许可或把其二进制内容当作普通源代码重新授权。

重分发时连同所需源码、补丁、构建说明及全部许可一起保留；不能只摘出GPL驱动二进制而丢弃对应材料。第三方NVIDIA安装包、macOS框架不在本包内，通过[资源清单](../资源与版本清单.md)的官方链接获取。

USBToolBox/kext 1.2.0快照未见明确再分发许可文件，因此本包只列固定官方来源与原创PCI匹配字段差异，不重分发它的源码、整份Info或驱动。没有提供本机端口映射。
