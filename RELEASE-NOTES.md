# AikaOS Mini 11.1 — CD Edition 💿

AikaOS as a bootable live CD for a 700 MB disc: **684.3 MB**, with the Aika desktop, IceWM and Firefox ESR. Built on Alpine Linux 3.24.

**[AikaOS full version →](https://github.com/emiliaplays/AikaOS)** — visit the main project for the regular AikaOS edition.

## Download and boot

- `aikaos-mini-11.1-cd-x86_64.iso`: bootable image for x86_64, BIOS and UEFI
- `.iso.sha256`: SHA-256 checksum
- `aikaos-mini-11.1-cd-buildquellen.tar.gz`: build scripts, prepared overlay, documentation and verification reports; not a complete source archive of all third-party packages
- `AikaOS-CD-Falthuelle-A4-Schwarzweiss-Aika.pdf`: paper CD sleeve; print single-sided on A4 at 100% scale (German instructions)

Choose **Burn ISO / disc image** in your burning software and verify the disc afterward. 4 GB RAM is recommended. Secure Boot is not supported.

## What's included

Firefox ESR with HTML5 video, PCManFM, Mousepad, a terminal, a network/Wi-Fi applet, volume controls, a German keyboard layout and Aika artwork. YouTube requires internet access; suitable playback resolution depends on your hardware.

## Release status

Experimental live CD **without an installer or persistent storage**. The user `aika` logs in automatically and can use `sudo` without a password. Changes in RAM are lost on reboot.

The final ISO was tested in QEMU under BIOS and UEFI. The documented video/audio-stream test took place before the final OpenSSL addition; the existing browser and desktop packages are byte-identical in the final image. See `ABNAHME.txt` (German) and the repository for details and hardware limitations. The maintainer additionally reports successful operation from a 700 MB CD.

ISO SHA-256:

```text
2543c5b506a70abf17657a314b39be8cd1bce069c2ba76baf2e2f3beb3392baf
```
