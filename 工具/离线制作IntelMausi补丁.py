#!/usr/bin/env python3
"""Default is read-only; --output explicitly creates a new offline bundle, never ESP."""
from pathlib import Path
import argparse,plistlib,hashlib,shutil
p=argparse.ArgumentParser(description='检查固定IntelMausi 1.0.8输入；--output仅生成新的离线bundle。')
p.add_argument('input',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
base=a.input.resolve();binary=base/'Contents/MacOS/IntelMausi';info=base/'Contents/Info.plist'
# Exact known input hash is filled from the official rollback bundle in this release.
expected='dc49b4f6281347044503bd59acd195ead8f0949c84fc4e5add700b5bf1b76200'
data=binary.read_bytes();assert hashlib.sha256(data).hexdigest()==expected,'输入不是精确官方构建，停止'
assert len(data)==168888 and data[78944:78946]==bytes.fromhex('0a55')
d=plistlib.loads(info.read_bytes());matches=[v for v in d['IOKitPersonalities'].values() if 'IOPCIMatch' in v];assert len(matches)==1
assert '0x57A18086' not in matches[0]['IOPCIMatch']
print('精确输入与偏移通过；默认没有写入。')
if a.output:
 out=a.output.absolute()
 if any(part in ('EFI','OC','Kexts') for part in out.parts) or str(out).startswith(('/Volumes/','/Library/','/System/')):raise SystemExit('拒绝系统/外置卷/EFI目标，请在本地普通工作目录生成后人工审阅')
 if out.exists():raise SystemExit('输出已存在，停止')
 shutil.copytree(base,out)
 changed=bytearray(data);changed[78944:78946]=bytes.fromhex('a157')
 (out/'Contents/MacOS/IntelMausi').write_bytes(changed)
 matches[0]['IOPCIMatch']+=' 0x57A18086'
 (out/'Contents/Info.plist').write_bytes(plistlib.dumps(d,sort_keys=False))
 print('已生成离线副本；二进制SHA-256',hashlib.sha256(changed).hexdigest())
 print('plist序列化格式可能不同；语义与本机补丁相同，不套用另一文件的plist散列。')
