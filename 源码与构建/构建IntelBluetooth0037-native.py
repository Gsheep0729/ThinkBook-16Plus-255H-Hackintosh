#!/usr/bin/env python3
# coding: utf-8
from pathlib import Path
import concurrent.futures as cf
import importlib.util
import json
import plistlib
import shutil
import subprocess

BASE = Path(__file__).resolve().parent
import argparse
parser = argparse.ArgumentParser(description='离线构建蓝牙0037实验，不下载、不安装。')
parser.add_argument('--output', required=True, type=Path)
args = parser.parse_args()
WORK = args.output.absolute()
if WORK.exists(): raise SystemExit('输出必须是不存在的新目录')
if str(WORK).startswith(('/Volumes/', '/Library/', '/System/')) or 'EFI' in WORK.parts:
    raise SystemExit('请选择本地普通构建目录，不是ESP或系统目录')
WORK.mkdir(parents=True)
shutil.copytree(BASE/'IntelBluetoothFirmware', WORK/'src')
shutil.copytree(BASE/'MacKernelSDK', WORK/'MacKernelSDK')
subprocess.run(['/usr/bin/patch', '-p1', '-i', str(BASE/'补丁/IntelBluetoothFirmware-0037-BlazarU.patch')], cwd=WORK/'src', check=True)
SRC = WORK/'src/IntelBluetoothFirmware'
SDK = WORK/'MacKernelSDK'
OBJ = WORK/'objects'
OBJ.mkdir(exist_ok=True)
BUNDLE = WORK/'IntelBluetoothFirmware.kext'
(BUNDLE/'Contents/MacOS').mkdir(parents=True,exist_ok=True)
for ext in ('sfi','ddc'):
    shutil.copy2(BASE.parent/'实验/蓝牙-固件已加载但控制器失败/固件'/('ibt-0093-0291.'+ext), SRC/'fw')
module = WORK/'src/scripts/zlib_compress_fw.py'
spec = importlib.util.spec_from_file_location('fw_generator',module)
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
generator.process_files(str(SRC/'FwBinary.cpp'),str(SRC/'fw'))
info = plistlib.loads((SRC/'Info.plist').read_bytes())
for key,value in list(info.items()):
    if isinstance(value,str):
        info[key] = value.replace('$(EXECUTABLE_NAME)','IntelBluetoothFirmware').replace('$(MODULE_VERSION)','2.5.0').replace('$(PRODUCT_NAME)','IntelBluetoothFirmware').replace('$(PRODUCT_BUNDLE_IDENTIFIER)','com.zxystd.IntelBluetoothFirmware').replace('$(DEVELOPMENT_LANGUAGE)','en')
assert '$(' not in str(info)
(BUNDLE/'Contents/Info.plist').write_bytes(plistlib.dumps(info,sort_keys=False))
flags = ['-target','x86_64-apple-macos10.12','-mkernel','-fapple-kext',
         '-fno-exceptions','-fno-rtti','-fno-common','-mno-red-zone',
         '-fstack-protector-strong','-fno-builtin','-fno-threadsafe-statics',
         '-fno-use-cxa-atexit','-DKERNEL=1','-DKERNEL_PRIVATE=1',
         '-D__KERNEL__=1','-O2','-nostdinc',
         '-I'+str(SDK/'Headers'),'-I'+str(SDK/'Headers/i386'),
         '-I'+str(SDK/'Headers/libkern'),'-I'+str(SRC),
         '-Wno-deprecated-declarations','-Wno-c++11-narrowing']
sources = sorted(SRC.glob('*.cpp')) + [SRC/'zutil.c']
commands=[]
def compile_one(src):
    obj = OBJ/(src.stem+'.o')
    # The upstream zutil.c contains C++ linkage and is compiled as C++ by Xcode.
    compiler = '/usr/bin/clang++'
    args = [compiler,*flags,'-x','c++','-std=gnu++14']
    args+=['-c',str(src),'-o',str(obj)]
    p=subprocess.run(args,capture_output=True,text=True)
    (OBJ/(src.name+'.log')).write_text(p.stdout+p.stderr)
    return {'source':src.name,'argv':args,'code':p.returncode,'object':str(obj)}
with cf.ThreadPoolExecutor(max_workers=4) as pool:
    commands=list(pool.map(compile_one,sources))
(WORK/'编译命令.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2))
failed=[v for v in commands if v['code']]
if failed:
    for v in failed:
        print(v['source'],(OBJ/(v['source']+'.log')).read_text()[-2200:])
    raise SystemExit(1)
vers=WORK/'module.c'
vers.write_text('''#include <mach/kmod.h>
extern kern_return_t _start(kmod_info_t *, void *);
extern kern_return_t _stop(kmod_info_t *, void *);
KMOD_EXPLICIT_DECL(com.zxystd.IntelBluetoothFirmware, "2.5.0", _start, _stop)
__private_extern__ kmod_start_func_t *_realmain = 0;
__private_extern__ kmod_stop_func_t *_antimain = 0;
__private_extern__ int _kext_apple_cc = __APPLE_CC__;
''')
p=subprocess.run(['/usr/bin/clang',*flags,'-c',str(vers),'-o',str(OBJ/'module.o')],capture_output=True,text=True)
(OBJ/'module.log').write_text(p.stdout+p.stderr)
assert p.returncode==0,p.stdout+p.stderr
ld='/Library/Developer/CommandLineTools/usr/bin/ld'
args=[ld,'-kext','-arch','x86_64','-undefined','dynamic_lookup',
      '-o',str(BUNDLE/'Contents/MacOS/IntelBluetoothFirmware'),
      *[str(p) for p in sorted(OBJ.glob('*.o'))],
      str(SDK/'Library/x86_64/libkmod.a'),str(SDK/'Library/universal/libkmodc++.a')]
p=subprocess.run(args,capture_output=True,text=True)
(WORK/'链接.txt').write_text(p.stdout+p.stderr)
(WORK/'链接命令.json').write_text(json.dumps(args,indent=2))
assert p.returncode==0,p.stdout+p.stderr
print('Built',len(sources),'sources:',BUNDLE)
