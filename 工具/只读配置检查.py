#!/usr/bin/env python3
"""Only reads user-selected ordinary files/directories. Never mounts or modifies anything."""
import argparse,hashlib,json,plistlib
from pathlib import Path
p=argparse.ArgumentParser(description='只读比较plist语义或目录文件清单；不自动挂载、不写文件。')
p.add_argument('input',type=Path);p.add_argument('--compare',type=Path);a=p.parse_args()
def digest(b):return hashlib.sha256(b).hexdigest()
def tree(root):
 out={}
 for p in sorted(root.rglob('*')):
  if p.is_symlink():raise SystemExit('拒绝符号链接，改用普通目录副本')
  if p.is_file():out[p.relative_to(root).as_posix()]={'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())}
 return out
def flat(v,path=''):
 if isinstance(v,dict):
  out={}
  for k,x in v.items():out.update(flat(x,path+'/'+k))
  return out
 if isinstance(v,list):
  out={}
  for i,x in enumerate(v):out.update(flat(x,path+'/'+str(i)))
  return out
 # Values are intentionally not displayed, including identity fields.
 return {path:{'type':type(v).__name__,'valueDigest':digest(repr(v).encode())}}
def load(p):return tree(p) if p.is_dir() else flat(plistlib.loads(p.read_bytes()))
x=load(a.input)
if a.compare:
 y=load(a.compare);print(json.dumps([{'path':k,'before':x.get(k),'after':y.get(k)} for k in sorted(x.keys()|y.keys()) if x.get(k)!=y.get(k)],ensure_ascii=False,indent=2))
else:print(json.dumps(x,ensure_ascii=False,indent=2))
