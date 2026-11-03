#!/bin/bash
set -u
pid=$(pgrep -u 1000 -x icewm | head -1)
if [[ -n $pid ]]; then
    for name in DISPLAY XAUTHORITY XDG_RUNTIME_DIR DBUS_SESSION_BUS_ADDRESS; do
        value=$(tr '\0' '\n' < "/proc/$pid/environ" | sed -n "s/^$name=//p")
        [[ -z $value ]] || export "$name=$value"
    done
fi
export DISPLAY=${DISPLAY:-:0}
export XAUTHORITY=${XAUTHORITY:-/home/aika/.Xauthority}
printf '\nAIKA_MINI_CHECK_BEGIN\n'
id
cat /etc/os-release
printf '\n--- session ---\n'
pgrep -a -x icewm
pgrep -a -x Xorg || pgrep -a -x X
pgrep -a -x nm-applet
printf '\n--- keyboard ---\n'
setxkbmap -query
printf '\n--- network ---\n'
nmcli -t -f STATE general
nmcli -t -f DEVICE,TYPE,STATE device
curl --max-time 30 -I https://www.mozilla.org/
printf '\n--- audio ---\n'
pactl info
pactl list short sinks
printf '\n--- media ---\n'
mount | grep -E 'tmpfs|squashfs|iso9660'
printf '\n--- memory ---\n'
free -m
printf '\n--- packages ---\n'
apk info -v firefox-esr icewm pcmanfm mousepad
printf '\n--- desktop launchers ---\n'
for app in aika-browser aika-terminal firefox-esr pcmanfm mousepad nm-connection-editor pavucontrol /sbin/reboot /sbin/poweroff; do
    command -v "$app" || printf 'MISSING: %s\n' "$app"
done
pgrep -a polkitd
printf '\n--- live sudo ---\n'
sudo -n true && echo LIVE_SUDO_OK
printf '\n--- modloop verification tool ---\n'
openssl version
if [[ ${1:-} == --verify ]]; then
    found=0
    for key in /etc/apk/keys/*.pub; do
        signature=/var/cache/misc/modloop-lts.SIGN.RSA.${key##*/}
        if [[ -f $signature ]]; then
            found=1
            openssl dgst -sha1 -verify "$key" -signature "$signature" /media/sr0/boot/modloop-lts && echo MODLOOP_SIGNATURE_VERIFIED
        fi
    done
    [[ $found == 1 ]] || echo MISSING_MODLOOP_SIGNATURE
fi
printf '\n--- services ---\n'
sudo rc-status default
printf '\nAIKA_MINI_CHECK_END\n'
