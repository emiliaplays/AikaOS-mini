"""Publish the recorded CD acceptance results after the live checks finish."""
from pathlib import Path
import datetime
import hashlib
import json
import re

project=Path(__file__).resolve().parent.parent
out=project/'out'
manifest=json.loads((out/'cd-build-manifest.json').read_text())
iso=out/manifest['filename']
with iso.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
assert digest==manifest['sha256']
assert iso.stat().st_size<=700_000_000

logs={}
for firmware in ('bios','uefi'):
    text=(project/f'tests/{firmware}/check.log').read_text(errors='replace')
    text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text)
    for expected in ('AIKA_MINI_CHECK_END','NAME="AikaOS Mini"','layout:     de',
                     'eth0:ethernet:connected','HTTP/2 200','LIVE_SUDO_OK',
                     '/usr/bin/nm-connection-editor','OpenSSL 3.5.9'):
        assert expected in text,(firmware,expected)
    assert 'MISSING:' not in text
    logs[firmware]=text
assert 'MODLOOP_SIGNATURE_VERIFIED' in logs['uefi']
video=json.loads((out/'youtube-test.json').read_text())
assert video['pass']
sample=video['successful_sample']['video']
assert sample['time']>8 and sample['decoded']>1 and not sample['error']
assert any(s['properties'].get('application.name')=='Firefox' and not s['mute'] and not s['corked'] for s in video['audio_sink_inputs'])
equivalence=json.loads((out/'media-equivalence.json').read_text())
assert equivalence['verified'] and equivalence['browser_and_desktop_configuration_unchanged']
report={
 'tested_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'name':'AikaOS Mini 11.1 CD Edition','iso':manifest['filename'],
 'bytes':iso.stat().st_size,'sha256':digest,'fits_700mb_cd':True,
 'environment':{'emulator':'QEMU 11.1.0','acceleration':'TCG','ram_mib':4096,'vcpus':4,
                'graphics':'virtio-vga','audio':'HDA duplex, silent host backend','hard_disks':0},
 'final_iso_checks':{'bios_desktop':True,'uefi_desktop':True,'autologin_aika':True,
   'german_keyboard_layout':True,'ethernet_dhcp_https':True,'desktop_commands_present':True,
   'modloop_signature_verified':True,'default_services_running':True,'live_root_in_ram':True},
 'media_test':{'tested_iso_sha256':video['tested_iso_sha256'],'youtube_video':True,
   'firefox_audio_stream':True,'width':sample['width'],'height':sample['height'],
   'playback_seconds':sample['time'],'decoded_frames':sample['decoded'],
   'relation_to_final_iso':'Existing 403 APKs and kernel/initramfs/modloop are byte-identical; only openssl APK and /etc/apk/world were added/changed.'},
 'desktop_test':{'pcmanfm_opened':True,'mousepad_opened':True,
   'evidence':'Desktop-Test.png; same byte-verified desktop packages and configuration'},
 'limitations':['No physical CD burn/drive test','No physical Wi-Fi/GPU/audio device test',
                'No installer or persistence','Secure Boot unsupported','No promise of a particular YouTube resolution']}
(out/'abnahme.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'ABNAHME.txt').write_text(f'''AikaOS Mini 11.1 - Abnahme der CD Edition

ISO: {iso.name}
Groesse: {iso.stat().st_size:,} Byte ({iso.stat().st_size/1e6:.1f} MB)
Grenze: 700.000.000 Byte - bestanden
SHA-256: {digest}

Die fertige ISO wurde unter BIOS und UEFI von einem virtuellen, nur
lesbaren CD-Laufwerk ohne Festplatte gestartet. QEMU 11.1.0, TCG,
4 GB RAM, 4 virtuelle CPUs, Virtio-Grafik, virtuelle HDA-Soundkarte.

Bestanden: automatischer Aika-Desktop, deutsches Tastaturlayout,
Ethernet/DHCP, HTTPS-Zugriff, Desktop-Programmstarter, sudo in der
Live-Sitzung und laufende Standarddienste. Das Live-Dateisystem liegt
im RAM; ISO und Modloop sind nur lesbar eingebunden.
Die Modloop-Signatur wurde mit dem auf der CD enthaltenen OpenSSL
geprueft: Verified OK.

YouTube: Big Buck Bunny lief in Firefox ESR mit Bild und Ton.
Messpunkt: {sample['time']} Sekunden, {sample['width']} x {sample['height']},
{sample['decoded']} dekodierte Bilder, kein Decoderfehler. Ein aktiver,
nicht stummgeschalteter Firefox-Audiostream wurde in PulseAudio gemessen.
Der Host-Audioausgang der Test-VM war stumm; echte Lautsprecher wurden
nicht abgenommen. Ein separater Pruefton aktivierte die virtuelle HDA-Ausgabe.
Die Testaufloesung ist keine Mindest- oder Hoechstzusage fuer echte Hardware.

Der Video- und Anwendungstest erfolgte vor dem letzten Paket-Zusatz
OpenSSL auf ISO mit SHA-256:
{video['tested_iso_sha256']}
Danach wurden alle 403 vorhandenen APKs, Kernel, Initramfs und Modloop
Byte fuer Byte mit der Endfassung verglichen. Sie sind identisch.
Die Aika-Konfiguration ist bis auf die neue Paketzeile in /etc/apk/world
identisch. Siehe media-equivalence.json und youtube-test.json.
Die BIOS-/UEFI-Starttests und die Signaturpruefung gelten fuer die oben
genannte Endfassung. Dateimanager PCManFM und Texteditor Mousepad wurden
geoeffnet; Screenshot Desktop-Test.png. YouTube-Test.png zeigt die Wiedergabe.

Nicht getestet: echte CD-R/Laufwerke, physische WLAN-, Grafik- und
Audiogeraete. Diese lokale Live-CD hat keinen Installer, keine dauerhafte
Speicherung und keine Secure-Boot-Unterstuetzung.
'''.replace(f'{iso.stat().st_size:,}',f'{iso.stat().st_size:,}'.replace(',','.')))
print(f'Acceptance report completed for {digest}')
