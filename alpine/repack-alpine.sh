#!/bin/bash
set -euo pipefail
base=/home/aika/alpine-mini-build
project=/home/aika/aikaos-mini
input="$base/chroot/aika/out/aikaos-mini-11.1-x86_64.iso"
stage="$base/final-stage"
out="$base/out"
[[ -s "$input" && ! -e "$stage" ]]
mkdir -p "$stage" "$out" "$base/original-boot"
xorriso -osirrox on -indev "$input" -extract / "$stage"
cp "$base/chroot/aika/aika-mini.apkovl.tar.gz" "$stage/aika-mini.apkovl.tar.gz"
for item in efi EFI boot/grub boot/syslinux; do
    if [[ -e "$stage/$item" || -L "$stage/$item" ]]; then
        mv "$stage/$item" "$base/original-boot/${item//\//-}"
    fi
done
theme="$stage/boot/grub/themes/aikaos"
mkdir -p "$theme" "$stage/boot/grub/fonts"
cp "$project/assets/background.png" "$project/assets/theme.txt" "$theme/"
grub-mkfont -s 18 -o "$theme/aika18.pf2" /usr/share/fonts/TTF/DejaVuSans.ttf
grub-mkfont -s 24 -o "$theme/aika24.pf2" /usr/share/fonts/TTF/DejaVuSans.ttf
cp /usr/share/grub/unicode.pf2 "$stage/boot/grub/fonts/"
cp "$base/grub.cfg" "$stage/boot/grub/grub.cfg"
grub-script-check "$stage/boot/grub/grub.cfg"
iso="$out/aikaos-mini-11.1-cd-x86_64.iso"
grub-mkrescue --locales=de --themes= --compress=xz -o "$iso" "$stage" -volid AIKA_MINI
(cd "$out" && sha256sum "$(basename "$iso")" > "$(basename "$iso").sha256")
xorriso -indev "$iso" -report_el_torito plain -report_system_area plain > "$out/cd-boot-report.txt" 2>&1
find "$stage/apks" -name '*.apk' -printf '%f\n' | sort > "$out/cd-packages.txt"
python3 - "$iso" <<'PY'
import datetime,json,pathlib,sys
iso=pathlib.Path(sys.argv[1])
size=iso.stat().st_size
manifest={'name':'AikaOS Mini','version':'11.1','architecture':'x86_64','base_distribution':'Alpine Linux 3.24',
 'desktop':'IceWM','browser':'Firefox ESR','filename':iso.name,'bytes':size,'limit_bytes':700000000,'fits_700mb_cd':size<=700000000,
 'sha256':pathlib.Path(str(iso)+'.sha256').read_text().split()[0],
 'built_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'experimental-local-build',
 'installer_included':False,'secure_boot_supported':False}
(iso.parent/'cd-build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
if size>700000000: raise SystemExit('700 MB CD size limit exceeded')
PY
for name in aikaos-mini-11.1-cd-x86_64.iso aikaos-mini-11.1-cd-x86_64.iso.sha256 cd-build-manifest.json cd-boot-report.txt cd-packages.txt; do
    curl -fsS -T "$out/$name" "http://10.0.2.2:18087/$name"
done
curl -fsS -T "$base/chroot/aika/aika-mini.apkovl.tar.gz" http://10.0.2.2:18087/aika-mini.apkovl.tar.gz
echo FIREFOX_CD_EXPORTED
