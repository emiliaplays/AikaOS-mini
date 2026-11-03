#!/bin/bash
set -euo pipefail
base=/home/aika/alpine-mini-build
root="$base/chroot"
[[ -s "$root/aika/aika-mini.apkovl.tar.gz" ]] || python3 "$base/make-overlay.py"
mount --bind "$root" "$root"
trap 'umount "$root" 2>/dev/null || true' EXIT
arch-chroot "$root" /usr/bin/env PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin HOME=/root /bin/sh -c '
set -e
test -f /root/.abuild/abuild.conf || abuild-keygen -an
mkdir -p /aika/work /aika/out /aika/tmp
export TMPDIR=/aika/tmp
cd /aports/scripts
sh mkimage.sh --tag 11.1 --arch x86_64 --profile aika --hostkeys --outdir /aika/out --workdir /aika/work --repository https://dl-cdn.alpinelinux.org/alpine/v3.24/main --repository https://dl-cdn.alpinelinux.org/alpine/v3.24/community
'
