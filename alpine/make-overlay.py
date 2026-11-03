#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import shutil
import tarfile

base = Path('/home/aika/alpine-mini-build')
alpine = base/'chroot'
project = Path('/home/aika/aikaos-mini')
reference = project/'work/x86_64/airootfs'
output = alpine/'aika'
root = output/'overlay'
if root.exists():
    raise SystemExit('overlay already exists; preserve it before regenerating')
root.mkdir(parents=True)

def write(name, content, mode=0o644):
    path = root/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip()+'\n')
    path.chmod(mode)

def copy(source, name):
    path = root/name
    path.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,path)

def rc(service, level):
    path = root/f'etc/runlevels/{level}/{service}'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to('/etc/init.d/'+service)

with tarfile.open(base/'downloads/alpine-minirootfs-3.24.2-x86_64.tar.gz') as archive:
    def original(name):
        for item in (name, './'+name):
            try:
                return archive.extractfile(item).read().decode()
            except KeyError:
                pass
        raise RuntimeError(name)
    passwd = original('etc/passwd')
    groups = original('etc/group')
    shadow = original('etc/shadow')
    inittab = original('etc/inittab')
passwd = '\n'.join(line for line in passwd.splitlines() if not line.startswith('aika:'))
passwd += '\naika:x:1000:1000:AikaOS Mini:/home/aika:/bin/bash\n'
shadow = '\n'.join('root:!:20000:0:99999:7:::' if line.startswith('root:') else line for line in shadow.splitlines())
shadow += '\naika::20000:0:99999:7:::\n'
group_lines = [line.split(':') for line in groups.splitlines() if line]
for name in ('aika','wheel','audio','video','input','netdev','plugdev','autologin'):
    found = next((line for line in group_lines if line[0]==name),None)
    if not found:
        used = {int(line[2]) for line in group_lines}
        gid = 1000 if name=='aika' else next(i for i in range(1001,2000) if i not in used)
        found=[name,'x',str(gid),'']
        group_lines.append(found)
    members=set(filter(None,found[3].split(',')))
    members.add('aika')
    found[3]=','.join(sorted(members))
write('etc/passwd',passwd)
write('etc/group','\n'.join(':'.join(line) for line in group_lines))
write('etc/shadow',shadow,0o400)
write('etc/hostname','aika-mini')
write('etc/issue','AikaOS Mini 11.1 - Live CD')
write('etc/motd','Willkommen bei AikaOS Mini 11.1.\nDieses Live-System speichert Aenderungen im RAM.')
write('etc/hosts','127.0.0.1 localhost aika-mini\n::1 localhost')
write('etc/profile.d/aika-locale.sh','export LANG=de_DE.UTF-8\nexport LANGUAGE=de_DE:de\nexport TZ=Europe/Berlin')
(root/'etc/localtime').symlink_to('/usr/share/zoneinfo/Europe/Berlin')
write('etc/timezone','Europe/Berlin')
write('etc/conf.d/keymaps','keymap="de"\nwindowkeys="YES"')
write('etc/network/interfaces','auto lo\niface lo inet loopback')
write('etc/NetworkManager/conf.d/10-aika.conf','[main]\nplugins=keyfile\n[device]\nwifi.scan-rand-mac-address=yes')
write('etc/sudoers.d/10-aika-live','aika ALL=(ALL:ALL) NOPASSWD: ALL',0o440)
copy(project/'profile/airootfs/etc/polkit-1/rules.d/49-aika-live-network.rules','etc/polkit-1/rules.d/49-aika-live-network.rules')
copy(project/'profile/airootfs/etc/X11/xorg.conf.d/00-keyboard.conf','etc/X11/xorg.conf.d/00-keyboard.conf')
write('etc/lightdm/lightdm.conf','''
[LightDM]
run-directory=/run/lightdm
[Seat:*]
greeter-session=lightdm-gtk-greeter
autologin-user=aika
autologin-user-timeout=0
user-session=aika
''')
write('usr/share/xsessions/aika.desktop','[Desktop Entry]\nName=AikaOS Mini\nComment=AikaOS Mini IceWM Desktop\nExec=/usr/local/bin/aika-session\nType=Application\nDesktopNames=ICEWM')
write('usr/local/bin/aika-session','''
#!/bin/sh
export XDG_CURRENT_DESKTOP=ICEWM XDG_SESSION_DESKTOP=icewm XDG_SESSION_TYPE=x11 GTK_THEME=Adwaita:dark BROWSER=aika-browser
export LANG=de_DE.UTF-8 LANGUAGE=de_DE:de TZ=Europe/Berlin
export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/tmp/runtime-aika}
mkdir -p "$XDG_RUNTIME_DIR"
chmod 700 "$XDG_RUNTIME_DIR"
if [ -z "${DBUS_SESSION_BUS_ADDRESS:-}" ]; then
    exec dbus-run-session -- icewm-session
fi
exec icewm-session
''',0o755)
copy(reference/'usr/local/bin/aika-terminal','usr/local/bin/aika-terminal')
(root/'usr/local/bin/aika-terminal').chmod(0o755)
write('usr/local/bin/aika-browser','#!/bin/sh\nif command -v firefox >/dev/null; then exec firefox "$@"; fi\nexec firefox-esr "$@"',0o755)
write('usr/local/bin/aika-serial-login','#!/bin/sh\nexec /bin/login -f aika',0o755)
inittab += '\nttyS0::respawn:/sbin/getty -L -n -l /usr/local/bin/aika-serial-login 115200 ttyS0 vt100\n'
write('etc/inittab',inittab)
write('etc/local.d/aika-audio.start','#!/bin/sh\nalsactl init >/var/log/aika-alsa.log 2>&1 || true',0o755)
write('etc/local.d/aika-repositories.start','''
#!/bin/sh
cat > /etc/apk/repositories <<'EOF'
https://dl-cdn.alpinelinux.org/alpine/v3.24/main
https://dl-cdn.alpinelinux.org/alpine/v3.24/community
EOF
''',0o755)

home = root/'home/aika'
home.mkdir(parents=True)
for name in ('.icewm','.config'):
    shutil.copytree(reference/'etc/skel'/name,home/name,symlinks=True)
copy(reference/'etc/skel/.bashrc','home/aika/.bashrc')
write('home/aika/.bash_profile','[[ -f ~/.bashrc ]] && . ~/.bashrc')
write('home/aika/.icewm/startup','''
#!/bin/sh
xdg-user-dirs-update
nm-applet &
pulseaudio --start --exit-idle-time=-1 > "$HOME/.pulse-start.log" 2>&1
xset s off
xset -dpms
if [ ! -e "$HOME/.aika-welcome-shown" ]; then
    touch "$HOME/.aika-welcome-shown"
    aika-terminal -geometry 100x34 -e env AIKA_MINI_WELCOME=1 bash &
fi
''',0o755)
menu=(home/'.icewm/menu').read_text().replace('NetSurf · Browser','Firefox · Browser').replace(' web-browser ',' firefox ')
menu=menu.replace('separator\nprog "Neustarten"','prog "Lautstärke" multimedia-volume-control pavucontrol\nseparator\nprog "Neustarten"')
menu=menu.replace('sudo systemctl reboot','sudo /sbin/reboot').replace('sudo systemctl poweroff','sudo /sbin/poweroff')
(home/'.icewm/menu').write_text(menu)
(home/'.icewm/preferences').write_text((home/'.icewm/preferences').read_text().replace('sudo systemctl reboot','sudo /sbin/reboot').replace('sudo systemctl poweroff','sudo /sbin/poweroff'))
(home/'.icewm/toolbar').write_text((home/'.icewm/toolbar').read_text().replace('NetSurf','Firefox').replace(' web-browser ',' firefox '))
copy(project/'assets/desktop.png','usr/share/backgrounds/aikaos/desktop.png')
copy(project/'assets/aikaos-logo.png','usr/share/pixmaps/aikaos-logo.png')
copy(project/'assets/fastfetch.jsonc','etc/xdg/fastfetch/config.jsonc')
welcome=(reference/'usr/share/aikaos-mini/welcome.html').read_text().replace('NetSurf','Firefox ESR')
welcome=welcome.replace('https://www.netsurf-browser.org/','https://www.mozilla.org/firefox/')
welcome=welcome.replace('https://archlinux.org/','https://alpinelinux.org/').replace('>Arch Linux<','>Alpine Linux<')
welcome=welcome.replace(' Ein CD-Laufwerk allein sagt nichts über die Kompatibilität des Prozessors aus.','')
welcome=welcome.replace('Firefox ESR spart viel Platz und eignet sich für einfache Webseiten. Moderne Web-Apps mit umfangreichem JavaScript werden nicht vollständig unterstützt.','Firefox ESR unterstützt moderne Webseiten und HTML5-Video, etwa YouTube. Videoleistung und Auflösung hängen von der Hardware ab.')
write('usr/share/aikaos-mini/welcome.html',welcome)
policy={'policies':{'DontCheckDefaultBrowser':True,'OverrideFirstRunPage':'file:///usr/share/aikaos-mini/welcome.html','OverridePostUpdatePage':'','Homepage':{'URL':'file:///usr/share/aikaos-mini/welcome.html','StartPage':'homepage'}}}
for name in ('firefox','firefox-esr'):
    write(f'usr/lib/{name}/distribution/policies.json',json.dumps(policy))
write('etc/os-release','''
NAME="AikaOS Mini"
PRETTY_NAME="AikaOS Mini 11.1"
ID=aikaos
ID_LIKE=alpine
VERSION_ID=11.1
BUILD_ID=mini-cd-firefox
ANSI_COLOR="38;2;83;213;247"
LOGO=aikaos-logo
''')
write('etc/apk/world',(output/'world').read_text())
for service in ('devfs','dmesg','udev','udev-trigger','udev-settle','hwdrivers','modloop'):
    rc(service,'sysinit')
for service in ('hwclock','modules','sysctl','hostname','bootmisc','syslog','networking','keymaps','dbus','elogind'):
    rc(service,'boot')
# polkit is activated by D-Bus. Starting it here races that activation.
for service in ('networkmanager','local','lightdm'):
    rc(service,'default')
for service in ('mount-ro','killprocs','savecache'):
    rc(service,'shutdown')
archive = output/'aika-mini.apkovl.tar.gz'
with tarfile.open(archive,'w:gz') as tar:
    for path in sorted(root.rglob('*')):
        relative=path.relative_to(root).as_posix()
        info=tar.gettarinfo(str(path),relative)
        info.uid=info.gid=1000 if relative.startswith('home/aika') else 0
        info.uname=info.gname='aika' if info.uid==1000 else 'root'
        if relative=='home/aika': info.mode=0o700
        if info.isfile():
            with path.open('rb') as content: tar.addfile(info,content)
        else:
            tar.addfile(info)
digest=hashlib.sha256(archive.read_bytes()).hexdigest()
wrapper=alpine/'aports/scripts/genapkovl-aika.sh'
wrapper.write_text(f'#!/bin/sh\nset -e\n# Overlay SHA256 {digest}\ncp /aika/aika-mini.apkovl.tar.gz "$1.apkovl.tar.gz"\n')
wrapper.chmod(0o755)
print(f'Prepared {archive}, {archive.stat().st_size} bytes, SHA256 {digest}')
