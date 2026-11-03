# Third-party components — CD Edition

AikaOS Mini 11.1 CD Edition uses Alpine Linux 3.24, Linux, IceWM, Firefox ESR, GNU GRUB, Fastfetch, PCManFM, Mousepad, NetworkManager and PulseAudio. It is an independent experimental live image, not an official Alpine Linux release. The large Arch/KDE edition is a separate project.

The exact package inventory is in `verification/cd-packages.txt`; the release manifest is `verification/cd-build-manifest.json`. Packages, firmware, fonts and libraries retain their individual licenses. The repository's GPL-3.0-or-later license covers AikaOS-specific software, not every ISO component or artwork.

`alpine/upstream/` contains the Alpine mkimage scripts used from the `3.24-stable` aports branch. Existing upstream notices are retained. The local mkimage change removes `--no-chown` during APK initialization for this root/APK 3 build.

Upstream build recipes and source references:

- Alpine package metadata: https://pkgs.alpinelinux.org/packages?branch=v3.24&arch=x86_64
- Alpine aports, including source URLs, patches and licenses: https://gitlab.alpinelinux.org/alpine/aports/-/tree/3.24-stable
- Alpine source archive: https://distfiles.alpinelinux.org/distfiles/
- Alpine mkimage scripts: https://gitlab.alpinelinux.org/alpine/aports/-/tree/3.24-stable/scripts
- Linux: https://www.kernel.org/
- IceWM: https://github.com/ice-wm/icewm
- Firefox source: https://archive.mozilla.org/pub/firefox/releases/
- GNU GRUB: https://www.gnu.org/software/grub/
- Fastfetch: https://github.com/fastfetch-cli/fastfetch

Use the exact package versions in the inventory when locating sources. This repository and its build-source archive contain the AikaOS recipe and prepared configuration; they are not a complete source mirror of all bundled packages. Native build-tool provenance is recorded under `verification/`.

Artwork originates from the main AikaOS project. See `ARTWORK.md` for provenance and exclusions.
