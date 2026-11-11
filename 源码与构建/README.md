# 固定来源与离线复现

这里保留与发布驱动相关的上游源码及许可。下载只用于源码审查/静态核对，不安装驱动；源码中的CI、上传、远程eval、部署脚本不属于本教程操作入口。第三方README/文档保持上游上下文，完整在线文档请使用[资源清单](../资源与版本清单.md)中的固定仓库链接。

[公开源码来源](公开源码来源.json)记录本次codeload归档SHA与完整提交；归档形式可能与历史GitHub archive压缩字节不同，不能因此套用历史压缩包SHA。本包没有把整个工作区、私人EFI或原始日志放进源码目录。

## AirportBZ

源码固定0ccab1627764406861fb9eb0a06ca36e31b4440f，MacKernelSDK固定3f750085caa17ec3a7880f11c11bf4f48cd6a164。驱动源码未改，SDK仅在构建副本应用项目自带MSI-X声明补丁。所附源码快照对应历史本机构建；上游原生验证环境与本机不同，不能把工具链变更写成官方承诺。

具备Apple CLT的x86_64 macOS中，在本地普通目录运行：

```sh
python3 构建AirportBZ-native.py --output "$PWD/airport-native-output"
```

工具仅新建离线输出副本、编译57个Sequoia源文件并组装bundle，不下载、不安装。它将上游WSL/clang21脚本改为本地CLT链接器并移除该工具链专用的LLVM析构开关；驱动实现不变。历史本机工具链是Apple clang17 / ld-1167.5，目标x86_64 macOS15.2；954导入、构造/析构各0x38。不同工具链/路径可能改变Mach-O UUID和字节，复编后必须重新记录自己的散列、导入集合与段检查，不能借用本包静态结果。

## IntelBluetoothFirmware 0037

原始源码固定a414375505fa3b014be32f8fca31b5bbfdf9f10f，未把原目录改成已补丁源。离线工具复制源码、应用[三文件补丁](补丁/IntelBluetoothFirmware-0037-BlazarU.patch)，再加入[精确0291固件](../实验/蓝牙-固件已加载但控制器失败/固件)，生成FwBinary、编译10个源文件并链接完整bundle：

```sh
python3 构建IntelBluetooth0037-native.py --output "$PWD/bt0037-native-output"
```

该示例沿用历史CLT路径和clang17参数（gnu++14、-mkernel、-fapple-kext、-fstack-protector-strong，目标x86_64 macOS10.12 ABI），最终配置**只允许Darwin24**。编译target早不代表已在旧系统验收。不同CLT安装路径可审阅修改离线脚本的编译器/链接器位置，不要改系统路径或创建伪装链接器。

验证时用`nm -u`比较完整集合，不只比较数量；最终历史记录为327导入、构造/析构各0x30，新增固件解压回读一致；插件导入还需与Lilu导出合并核对。不要删除签名/SBE检查来换取“加载成功”。本次没有重新完整编译这两个大驱动，因此这两份新离线入口经过语法/路径审查，历史构建与静态证据见主教程，不能说新入口已在另一台机器复现。

## IntelMausi / VoodooI2C

IntelMausi保留1.0.8源码和[对应槽位源码补丁](补丁/IntelMausi-57A1-source.patch)，但本机安装的精确产物来自官方bundle的两字节补丁，而不是重新编译源码。可用[默认只读的二进制补丁示例](../工具/离线制作IntelMausi补丁.py)核对固定原件；带`--output`时只创建新的普通离线bundle。源码修改表达相同的识别槽位实验，不承诺源码复编与官方二进制逐字节相同。

VoodooI2C二进制未作本轮修改，增量是[精确personality](补丁/VoodooI2C-ArrowLake-personality.json)。上游源码固定5c0c99c，子模块精确指针与来源在[Voodoo子模块清单](VoodooI2C-submodules.json)，其中包含GPIO与HID；独立VoodooInput源码另列。构建前按该提交workspace和依赖说明准备MacKernelSDK/VoodooInput。本包不运行上游CI中的远程引导脚本。公开包不重分发来源未闭合的历史Lilu/Voodoo二进制，改附固定官方参考构建；实际本机旧bundle与当前官方构建的对应关系，以[逐二进制核对报告](../校验/官方构建逐二进制核对.json)及资源清单说明为准，不仅凭版本号断言同一产物。

## 配套校验器与许可证

ocvalidate来自已记录的OpenCorePkg-6d8490d / 1.0.9构建，本包只提供mac校验器及对应源码，不提供OpenCore引导程序。可从OpenCorePkg/Utilities/ocvalidate按该项目说明自行构建。所有上游版权与许可证留在原源码位置，集中入口在[许可证说明](../许可证/README.md)。

公开源码移除非必要用户工作状态/调试产物并替换少量文档路径，详见[处理说明](公开源码处理说明.md)。实现代码与许可保留；上游原归档SHA与公版目录散列分开。

15:03最新记录：基础0037补丁已合并Gen3错误处理修正，另附[独立增量](补丁/IntelBluetoothFirmware-Gen3-error-handling.patch)供理解/反向比较。此补丁适用于已经有基础0037改动的源码，不能当作原主线的独立补丁直接应用；默认构建入口只应用合并后的基础补丁。最新615efe4c…的原构建复现、导入/导出与分支测试证据已摘要公开，不公开包含本机路径的原隔离脚本/对象归档。USB-NHI匹配差异为单字段示例，不是USB端口映射。
