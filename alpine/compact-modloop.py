"""Store identical immutable firmware as hard links before streaming Squashfs."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import tarfile

project=Path(__file__).resolve().parent.parent
transfer=project/'transfer'
original=transfer/'alpine-modloop.tar'
compact=transfer/'alpine-modloop-compact.tar'
expected={}
seen={}
linked=0
saved=0
with tarfile.open(original) as source, tarfile.open(compact,'w') as dest:
    for member in source:
        info=copy.copy(member)
        if member.isfile():
            with source.extractfile(member) as data:
                digest=hashlib.file_digest(data,'sha256').hexdigest()
            key=(member.size,digest,member.mode,member.uid,member.gid,member.mtime)
            expected[member.name]=(key,member.linkname)
            if key in seen:
                info.type=tarfile.LNKTYPE
                info.linkname=seen[key]
                info.size=0
                dest.addfile(info)
                linked+=1
                saved+=member.size
            else:
                seen[key]=member.name
                dest.addfile(info,source.extractfile(member))
        else:
            expected[member.name]=(member.type,member.mode,member.uid,member.gid,member.mtime,member.linkname)
            dest.addfile(info)
with tarfile.open(compact) as archive:
    actual={}
    for member in archive:
        if member.isfile() or member.islnk():
            data=archive.extractfile(member)
            digest=hashlib.file_digest(data,'sha256').hexdigest()
            size=archive.getmember(member.linkname).size if member.islnk() else member.size
            actual[member.name]=((size,digest,member.mode,member.uid,member.gid,member.mtime),'')
        else:
            actual[member.name]=(member.type,member.mode,member.uid,member.gid,member.mtime,member.linkname)
assert actual==expected,'Compacted firmware contents or metadata differ'
print(f'Verified all {len(actual)} paths; {linked} hard links save {saved:,} bytes before compression',flush=True)
target=transfer/'alpine-modloop-cd.sfs'
with compact.open('rb') as source:
    subprocess.run([str(project/'tools/msys/usr/bin/mksquashfs.exe'),'-',str(target),'-tar','-numeric-owner','-default-uid','0','-default-gid','0','-comp','xz','-Xbcj','x86','-b','1M','-processors','6','-noappend','-no-progress'],stdin=source,check=True)
report=json.loads((transfer/'alpine-modloop-report.json').read_text())
with target.open('rb') as data: report['squashfs_sha256']=hashlib.file_digest(data,'sha256').hexdigest()
report.update(bytes=target.stat().st_size,hardlinked_files=linked,duplicate_bytes_saved=saved,all_file_contents_and_metadata_verified=True)
(transfer/'alpine-modloop-cd-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
