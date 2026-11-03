"""Verify that the final packaging change only added OpenSSL."""
from pathlib import Path
import hashlib
import json
import tarfile

base=Path('/home/aika/alpine-mini-build')
old=base/'final-stage-without-openssl'
new=base/'final-stage'

def same(left,right):
    if left.stat().st_size!=right.stat().st_size: return False
    with left.open('rb') as a,right.open('rb') as b:
        while True:
            x,y=a.read(1024*1024),b.read(1024*1024)
            if x!=y: return False
            if not x: return True

a={p.name:p for p in old.rglob('*.apk')}
b={p.name:p for p in new.rglob('*.apk')}
added=sorted(b.keys()-a.keys())
assert added==['openssl-3.5.9-r0.apk'],added
assert not a.keys()-b.keys()
assert all(same(path,b[name]) for name,path in a.items())
kernel_files=('boot/modloop-lts','boot/vmlinuz-lts','boot/initramfs-lts')
assert all(same(old/name,new/name) for name in kernel_files)

def overlay(path):
    result={}
    with tarfile.open(path/'aika-mini.apkovl.tar.gz') as archive:
        for member in archive:
            payload=hashlib.sha256(archive.extractfile(member).read()).hexdigest() if member.isfile() else None
            result[member.name]=(member.type.decode(),member.mode,member.uid,member.gid,member.linkname,payload)
    return result
x,y=overlay(old),overlay(new)
changed=sorted(name for name in x.keys()|y.keys() if x.get(name)!=y.get(name))
assert changed==['etc/apk/world'],changed
result={'previous_iso_sha256':'4a34f6f9c96a812fc7e91cee82c7c9cbfb887ede0730775961ecc3c4a2fbc4ba',
        'added_packages':added,'existing_packages_byte_identical':len(a),
        'kernel_files_byte_identical':list(kernel_files),'overlay_changed_files':changed,
        'browser_and_desktop_configuration_unchanged':True,'verified':True}
(base/'out/media-equivalence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
