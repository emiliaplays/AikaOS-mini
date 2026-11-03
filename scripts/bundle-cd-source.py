"""Bundle the public repository without ISO files or local build state."""
from pathlib import Path
import hashlib
import subprocess
import tarfile

root=Path(__file__).resolve().parent.parent
out=root/'out'
out.mkdir(exist_ok=True)
target=out/'aikaos-mini-11.1-cd-buildquellen.tar.gz'
names=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
with tarfile.open(target,'w:gz') as archive:
    for name in sorted(filter(None,names)):
        path=root/name
        assert path.is_file() and path.suffix!='.iso'
        info=archive.gettarinfo(str(path),'AikaOS-mini-CD/'+name)
        info.uid=info.gid=0
        info.uname=info.gname='root'
        info.mode=0o755 if path.suffix in ('.sh','.py') else 0o644
        with path.open('rb') as content: archive.addfile(info,content)
with target.open('rb') as content: digest=hashlib.file_digest(content,'sha256').hexdigest()
Path(str(target)+'.sha256').write_text(f'{digest}  {target.name}\n')
print(f'{target.name}: {target.stat().st_size} bytes; SHA256 {digest}')
