#!/usr/bin/env python3
"""Offline build example. Requires an explicit new local output directory; never installs."""
from pathlib import Path
import argparse,shutil,subprocess,os,plistlib
p=argparse.ArgumentParser(description='离线构建Sequoia AirportBZ，不下载、不安装。')
p.add_argument('--output',required=True,type=Path);a=p.parse_args();base=Path(__file__).resolve().parent;out=a.output.absolute()
if out.exists():raise SystemExit('输出必须是不存在的新目录')
if str(out).startswith(('/Volumes/','/Library/','/System/')) or 'EFI' in out.parts:raise SystemExit('请选本地普通构建目录，不是ESP或系统目录')
out.mkdir(parents=True);shutil.copytree(base/'AirportBZ',out/'src');shutil.copytree(base/'MacKernelSDK',out/'MacKernelSDK')
compiler=Path(subprocess.check_output(['xcrun','--find','clang++'],text=True).strip());linker=compiler.parent/'ld'
assert linker.exists()
s=(out/'src/scripts/build-sequoia-bz92.sh').read_text()
s=s.replace('  -mllvm -disable-atexit-based-global-dtor-lowering\n','')
s=s.replace('"$TOOLCHAIN/x86_64-apple-darwin-ld"','"'+str(linker)+'"')
script=out/'src/scripts/build-sequoia-native.sh';script.write_text(s)
env=dict(os.environ,MAC_KERNEL_SDK=str(out/'MacKernelSDK'),DARWIN_TOOLCHAIN=str(compiler.parent),BUILD_OUTPUT=str(out/'build'),PATH=str(compiler.parent)+os.pathsep+os.environ.get('PATH',''))
with (out/'build.log').open('w') as log:subprocess.run(['/bin/bash',str(script)],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
bundle=out/'AirportItlwm.kext';(bundle/'Contents/MacOS').mkdir(parents=True)
shutil.copyfile(out/'build/AirportItlwm',bundle/'Contents/MacOS/AirportItlwm')
# The release plist is already expanded and pinned; it contains no machine identity.
shutil.copyfile(base.parent/'驱动/部分通过/AirportItlwm.kext/Contents/Info.plist',bundle/'Contents/Info.plist')
print('仅生成离线bundle；请另做架构、ABI、固件和硬件验收。构建日志在输出目录。')
