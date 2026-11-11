#!/usr/bin/env python3
"""Verify public payload bytes and sanitized template; never installs or executes a binary."""
import argparse
import hashlib
import json
import plistlib
from pathlib import Path

EXCLUDED = {'.git', '下载'}
MANIFEST = '校验/发布文件清单.json'
SUMS = '校验/SHA256SUMS.txt'

def payload_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and p.relative_to(root).parts[0] not in EXCLUDED
                  and not p.name.startswith('._') and p.name != '.DS_Store')

def verify(root):
    rows = json.loads((root / MANIFEST).read_text())
    expected = {r['path']: r for r in rows}
    assert len(expected) == len(rows), 'Duplicate manifest paths'
    for rel in expected:
        p = Path(rel)
        assert not p.is_absolute() and '..' not in p.parts, 'Unsafe manifest path'
    actual = {p.relative_to(root).as_posix() for p in payload_files(root)}
    assert actual == set(expected) | {MANIFEST, SUMS}, 'Payload file set differs'
    plist_count = aml_count = 0
    for rel, row in expected.items():
        p = root / rel
        assert not p.is_symlink(), 'Symlink: ' + rel
        data = p.read_bytes()
        assert len(data) == row['bytes'], 'Size: ' + rel
        assert hashlib.sha256(data).hexdigest() == row['sha256'], 'SHA256: ' + rel
        if p.suffix == '.plist' and not rel.startswith('源码与构建/'):
            plistlib.loads(data)
            plist_count += 1
        if p.suffix == '.aml' and not rel.startswith('源码与构建/'):
            assert len(data) >= 36 and sum(data) % 256 == 0, 'AML: ' + rel
            aml_count += 1
    assert (root / SUMS).read_text().splitlines() == [r['sha256'] + '  ' + r['path'] for r in rows]
    config = plistlib.loads((root / 'EFI参考/OC/config-参考-全部禁用.plist').read_bytes())
    generic = config['PlatformInfo']['Generic']
    assert generic['SystemSerialNumber'] == generic['MLB'] == generic['SystemUUID'] == ''
    assert generic['ROM'] == bytes(6) and generic['SystemProductName'] == 'MacPro7,1'
    for section, array in [('ACPI', 'Add'), ('Kernel', 'Add'), ('UEFI', 'Drivers'), ('Misc', 'Tools')]:
        assert all(not row['Enabled'] for row in config[section][array])
    return {'verifiedFiles': len(rows), 'manifestMatches': True, 'parsedPublicPlists': plist_count,
            'validPublicAMLs': aml_count, 'templateIdentityEmptyAndEntriesDisabled': True,
            'upstreamFixturesParsedAsProductionConfig': False, 'hardwareBootRetested': False}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.root.resolve()), ensure_ascii=False))
