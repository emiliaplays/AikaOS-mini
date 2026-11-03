# AikaOS Mini 💿

**AikaOS auf einer 700-MB-CD – mit Aika-Desktop und Firefox ESR.**

Die CD Edition 11.1 ist ein schlankes Live-System für x86_64-PCs. Für die kleine CD verwendet sie Alpine Linux 3.24 und IceWM. Das Aika-Design und die grundlegenden Desktop-Funktionen bleiben erhalten; die [große AikaOS-Edition](https://github.com/emiliaplays/AikaOS) wird separat entwickelt.

![AikaOS Mini Desktop](verification/AikaOS-Mini-Desktop.png)

## Download

**[ISO und Zubehör herunterladen](https://github.com/emiliaplays/AikaOS-mini/releases/tag/v11.1-cd)**

| Ausgabe | Wert |
| --- | --- |
| ISO | `aikaos-mini-11.1-cd-x86_64.iso` |
| Größe | **684.285.952 Byte / 684,3 MB** |
| CD-Grenze | 700.000.000 Byte |
| Architektur | x86_64, BIOS und UEFI |
| Arbeitsspeicher | 4 GB empfohlen und in QEMU getestet |
| Desktop / Browser | IceWM / Firefox ESR |

SHA-256:

```text
2543c5b506a70abf17657a314b39be8cd1bce069c2ba76baf2e2f3beb3392baf
```

Die Release-Dateien enthalten die ISO, ihre Prüfsumme, Buildquellen, Dokumentation und eine druckbare CD-Hülle.

## Brennen und starten

1. Die ISO herunterladen. Unter PowerShell lässt sich die Prüfsumme mit `Get-FileHash .\aikaos-mini-11.1-cd-x86_64.iso -Algorithm SHA256` prüfen.
2. Im Brennprogramm **ISO / Datenträgerabbild brennen** wählen. Einen 700-MB-CD-R-Rohling verwenden, Medium abschließen und anschließend überprüfen lassen. Ein geeigneter „Audio CD-R“-Rohling wird hier als bootfähiges Datenabbild beschrieben.
3. Im PC-Bootmenü das CD/DVD-Laufwerk auswählen. Secure Boot muss für diese Ausgabe ausgeschaltet sein.
4. Der Aika-Desktop startet automatisch. Von einer echten CD kann der erste Start etwas dauern.

## Enthalten

- Aika-Hintergrund, Startmenü, Logo und Fastfetch-Porträt
- Firefox ESR mit HTML5-Video; YouTube benötigt Internet
- PCManFM, Mousepad und Terminal
- Netzwerk-/WLAN-Applet und Lautstärkeregler
- Deutsches Tastaturlayout und Zeitzone Europe/Berlin
- Tastenkürzel: **Super+Enter** Terminal, **Super+E** Dateien, **Super+B** Browser

Dies ist eine experimentelle **Live-CD ohne Installer und ohne dauerhafte Speicherung**. Änderungen liegen im RAM und gehen beim Neustart verloren. Dateien zum Behalten auf einem anderen Datenträger speichern. Der Live-Benutzer `aika` meldet sich automatisch an und kann `sudo` ohne Passwort verwenden. Die Paketverwaltung ist `apk`.

## Papier-CD-Hülle

[Schwarz-Weiß-Falthülle mit Aika im Kreis (PDF)](print/AikaOS-CD-Falthuelle-A4-Schwarzweiss-Aika.pdf): einseitig auf A4 mit **100 % / tatsächlicher Größe** drucken. Ausschneiden, an den gestrichelten Linien falten und die seitlichen Laschen außen ankleben. Die fertige Tasche ist ungefähr 126 × 126 mm groß. Eine 50-mm-Kontrolllinie hilft beim Prüfen des Ausdrucks.

## Tests und Grenzen

Die finale ISO wurde in QEMU mit 4 GB RAM unter BIOS und UEFI von einem nur lesbaren virtuellen CD-Laufwerk gestartet. Desktop, Netzwerk, HTTPS und Modloop-Signatur wurden geprüft. Der YouTube-Test zeigte Videowiedergabe und einen aktiven Firefox-Audiostream. Er erfolgte vor dem letzten OpenSSL-Zusatz; die bestehenden Browser- und Desktop-Pakete wurden danach byteweise mit der finalen ISO abgeglichen.

Details stehen in [ABNAHME.txt](verification/ABNAHME.txt). Die technische Abnahme umfasst keine physische Hardwareprüfung und keine Zusage für eine bestimmte Videoauflösung. Der Ersteller berichtet zusätzlich vom erfolgreichen Betrieb auf einer 700-MB-CD.

## Quellen und Build

Dieses Repository enthält CD-Konfiguration, Build- und Testskripte, das fertige Konfigurations-Overlay, Assets und Prüfberichte. Die ISO liegt im GitHub-Release.

[BUILD-HINWEISE.txt](BUILD-HINWEISE.txt) beschreibt den ursprünglichen Build. Die Skripte dokumentieren eine vorbereitete lokale Buildumgebung; sie sind **kein fertiger Ein-Befehl-Builder**. Teile verwenden lokale Referenzverzeichnisse und Host-Werkzeuge. Das fertige Overlay liegt deshalb unter `prepared/`. Neue Alpine-Paketstände können Größe und Prüfsumme verändern.

Die [Paketliste](verification/cd-packages.txt) und das [Manifest](verification/cd-build-manifest.json) beschreiben diese konkrete ISO. Eigene Software steht unter GPL-3.0-or-later; Drittanbieter-Komponenten behalten ihre jeweiligen Lizenzen. Siehe [LICENSE](LICENSE), [THIRD_PARTY.md](THIRD_PARTY.md) und [ARTWORK.md](ARTWORK.md).
