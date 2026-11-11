# UTBDefault排除USB4 NHI：枚举修正通过，端口映射未完成

源机器旧IOPCIClassMatch为`0x0c030000&0xffff0000`，误命中class0c0340的8086:7EC3 NHI。最小修正把XHC1匹配收紧为：

```text
0x0c030000&0xffffff00 0x0c031000&0xffffff00 0x0c032000&0xffffff00 0x0c033000&0xffffff00
```

30台PCI静态对照保留两xHCI并排除NHI；18:45重启实际确认7EC3下不再有USBToolBox错绑，777D/7EC0保持14/5根端口。**这层枚举通过，不等于全机USB端口、USB4隧道或热插拔已通过。**

提供[单字段差异](../../源码与构建/补丁/UTBDefault-NHI-exclusion.json)和[匹配前后证据](匹配前后证据.json)。UTBDefault仍是通用配置，专用映射未完成；不能直接用别人UTBMap。USBToolBox/kext1.2.0快照未见明确再分发许可文件，所以本包只列官方来源和原创差异，不重分发整份源码、Info或USB驱动。

最近完整归档XhciPortLimit=false；不是本轮重新读取磁盘。扩展坞鼠标历史失灵与该NHI修正不能合并归因，本次鼠标正常也不能写成历史故障已修复。详见[19:44摘要](../../证据摘要/1944扩展坞鼠标.json)及主教程。

复用先核对自己的PCI class/绑定与现有端口方案，只在离线副本改变目标字段；回退只恢复自己修改前Info，保留最新主题及其他驱动。包内不会自动挂载或写ESP。
