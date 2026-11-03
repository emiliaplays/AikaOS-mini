# AikaOS Mini 11.1 — CD Edition 💿

AikaOS als bootfähige Live-CD für einen 700-MB-Rohling: **684,3 MB**, mit Aika-Desktop, IceWM und Firefox ESR. Alpine Linux 3.24 bildet die kompakte Basis.

## Download und Start

- `aikaos-mini-11.1-cd-x86_64.iso`: bootfähiges Abbild für x86_64, BIOS und UEFI
- `.iso.sha256`: SHA-256-Prüfsumme
- `aikaos-mini-11.1-cd-buildquellen.tar.gz`: Buildskripte, vorbereitetes Overlay, Dokumentation und Prüfberichte; kein vollständiges Quellarchiv aller Drittanbieter-Pakete
- `AikaOS-CD-Falthuelle-A4-Schwarzweiss-Aika.pdf`: Papier-CD-Hülle, auf A4 einseitig bei 100 % drucken

Im Brennprogramm **ISO / Datenträgerabbild brennen** wählen und danach prüfen lassen. 4 GB RAM werden empfohlen. Secure Boot wird nicht unterstützt.

## Enthalten

Firefox ESR mit HTML5-Video, PCManFM, Mousepad, Terminal, Netzwerk-/WLAN-Applet, Lautstärkeregler, deutsches Tastaturlayout und Aika-Gestaltung. YouTube benötigt Internet; die geeignete Auflösung hängt von der Hardware ab.

## Stand der Ausgabe

Experimentelle Live-CD **ohne Installer und ohne dauerhafte Speicherung**. Der Benutzer `aika` startet automatisch und verwendet `sudo` ohne Passwort. Änderungen im RAM gehen beim Neustart verloren.

Die finale ISO wurde in QEMU unter BIOS und UEFI getestet. Der dokumentierte Video-/Audiostream-Test fand vor dem letzten OpenSSL-Zusatz statt; die vorhandenen Browser- und Desktop-Pakete sind in der Endfassung bytegleich. Einzelheiten und Hardwaregrenzen stehen in `ABNAHME.txt` und im Repository. Der Ersteller berichtet zusätzlich vom erfolgreichen Betrieb auf einer 700-MB-CD.

SHA-256 der ISO:

```text
2543c5b506a70abf17657a314b39be8cd1bce069c2ba76baf2e2f3beb3392baf
```
