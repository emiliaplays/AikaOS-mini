from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pypdfium2 as pdfium
from pypdf import PdfReader

root=Path(__file__).resolve().parent.parent
out=root/'out'
target=out/'AikaOS-CD-Falthuelle-A4-Schwarzweiss-Aika.pdf'
pdfmetrics.registerFont(TTFont('AikaRegular','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('AikaBold','C:/Windows/Fonts/arialbd.ttf'))
c=canvas.Canvas(str(target),pagesize=(210*mm,297*mm),pageCompression=1)
c.setTitle('AikaOS Mini – Schwarz-Weiß-Falthülle auf A4')
c.setAuthor('AikaOS')
c.scale(mm,mm)
ink=0

def text(x,y,s,size=9,color=0,bold=False):
    c.setFillGray(0)
    c.setFont('AikaBold' if bold else 'AikaRegular',size/mm)
    c.drawString(x,y,s)
def line(x1,y1,x2,y2,color=0,width=.22,dash=None):
    c.setStrokeGray(0);c.setLineWidth(width);c.setDash(dash or [])
    c.line(x1,y1,x2,y2);c.setDash([])
def circle(x,y,r,width=.3):
    c.setStrokeGray(0);c.setLineWidth(width);c.circle(x,y,r,stroke=1,fill=0)
def centered(x,y,s,size=9,bold=False):
    width=pdfmetrics.stringWidth(s,'AikaBold' if bold else 'AikaRegular',size/mm)
    text(x-width/2,y,s,size,bold=bold)

# White paper, monochrome mascot and black text; no solid dark panels.
text(61,246,'AikaOS',25,bold=True)
text(61,238,'MINI  /  CD EDITION  /  11.1',8,bold=True)
line(61,231,149,231,width=.45)
text(61,221,'Dein Desktop zum Mitnehmen.',11,bold=True)
text(61,213,'Einlegen. Starten. Aika.',9)
for y,label,value in [(199,'IM GEPÄCK','Firefox ESR · Dateien · Terminal'),
                      (183,'LIVE VON CD','Aika-Desktop · Netzwerk · YouTube'),
                      (167,'ZUM STARTEN','64-Bit-PC · BIOS / UEFI')]:
    text(61,y,label,7.5,bold=True)
    text(61,y-5,value,8.5)
text(61,149,'4 GB RAM empfohlen · Secure Boot aus',7.2)
text(61,142,'Live-System: Änderungen bleiben nur bis zum Neustart.',6.8)
# These strips are OUTSIDE the pocket and disappear under the side tabs.
for x in (42,153):
    # Glue areas are labelled only: dashed lines must always mean folds.
    c.saveState();c.translate(x+8.5,164);c.rotate(90)
    text(0,0,'LASCHEN HIER AUSSEN AUFKLEBEN',6.7)
    c.restoreState()

# Front, upside down in the flat net; upright on the assembled sleeve.
c.saveState();c.translate(168,135);c.rotate(180)
centered(63,111,'MINI  /  CD EDITION',8.5,bold=True)
centered(63,96,'AikaOS',34,bold=True)
line(12,91,114,91,width=.25)
# Preserve the original 60 mm circular badge and insert Aika inside it.
c.saveState()
badge=c.beginPath();badge.circle(63,60,27.4)
c.clipPath(badge,stroke=0,fill=0)
c.drawImage(str(root/'assets/aika-logo-schwarzweiss.png'),36,35,
            width=54,height=50,preserveAspectRatio=True,anchor='c',mask='auto')
c.restoreState()
circle(63,60,28,.45);circle(63,60,30,.18)
centered(63,18,'KLEIN. LEICHT. AIKA.',13,bold=True)
centered(63,9,'11.1   /   LIVE SYSTEM   /   64-BIT',7.5)
# Tiny corner marks frame the design without filling the page with ink.
for x,y,sx,sy in [(6,6,1,1),(120,6,-1,1),(6,120,1,-1),(120,120,-1,-1)]:
    line(x,y,x+sx*7,y,width=.4);line(x,y,x,y+sy*7,width=.4)
c.restoreState()

# The tab backs receive glue; their visible faces stay mostly blank.
for x in (35,176):
    c.saveState();c.translate(x,40);c.rotate(90)
    text(0,0,'A I K A O S   /   M I N I',7,bold=True);c.restoreState()
c.saveState();c.translate(168,287);c.rotate(180)
centered(63,14,'A I K A O S',11,bold=True)
line(24,9,102,9,width=.22)
c.restoreState()

# Continuous outer cut outline, with a 20 mm finger notch on the front.
p=c.beginPath();p.moveTo(48,287);p.lineTo(162,287);p.lineTo(168,261)
p.lineTo(168,131);p.lineTo(183,126);p.lineTo(183,18);p.lineTo(168,13)
p.lineTo(168,9);p.lineTo(115,9)
p.curveTo(115,14.523,110.523,19,105,19)
p.curveTo(99.477,19,95,14.523,95,9)
p.lineTo(42,9);p.lineTo(42,13);p.lineTo(27,18);p.lineTo(27,126)
p.lineTo(42,131);p.lineTo(42,261);p.close()
c.setLineWidth(.22);c.setStrokeGray(0);c.drawPath(p,stroke=1,fill=0)
# White notch waste area makes the cut contour easy to see.
p=c.beginPath();p.moveTo(95,9);p.curveTo(95,14.523,99.477,19,105,19)
p.curveTo(110.523,19,115,14.523,115,9);p.close()
c.setFillGray(1);c.drawPath(p,stroke=1,fill=1)
for a in [(42,261,168,261),(42,135,168,135),(42,13,42,131),(168,13,168,131)]:
    line(*a,color='#12A3BB',width=.3,dash=[2,1.2])

# Instructions live entirely on the waste margin, not on the finished sleeve.
text(12,292,'A4 HOCHFORMAT  ·  EINSEITIG  ·  100 % / TATSÄCHLICHE GRÖSSE  ·  NICHT ANPASSEN',7.2,ink,True)
c.saveState();c.translate(10,35);c.rotate(90)
text(0,0,'1  Außenkontur ausschneiden. Gestrichelte Linien vorfalten. Druckseite nach unten legen.',8)
text(0,-4.5,'2  Vorderseite an der Mittellinie nach oben falten. Hülle wenden: Rückseite zeigt nach oben.',8)
text(0,-9,'3  Seitenlaschen außen auf die markierten Rückseitenstreifen kleben. Kleber nur auf die blanken Laschen!',8)
c.restoreState()
c.saveState();c.translate(194,45);c.rotate(90)
text(0,0,'4  Trocknen lassen, CD einschieben, Verschlussklappe nach vorn falten. Bei Bedarf mit Klebepunkt schließen.',7.6)
text(0,-4.5,'Durchgezogen = schneiden   /   Gestrichelt = falten   /   Fertig: ca. 126 × 126 mm für eine 120-mm-CD',7.6)
c.restoreState()
# A 50 mm physical calibration bar on the offcut.
line(190,215,190,265,ink,.35)
for yy in range(215,266,10):line(188.5,yy,191.5,yy,ink,.3)
c.saveState();c.translate(196,222);c.rotate(90);text(0,0,'KONTROLLE: 50 mm',7,ink,True);c.restoreState()
text(42,4,'Papier: 100–160 g/m² empfohlen · Schere + Papierkleber · Kein Kleber im CD-Fach',6.5)
c.showPage();c.save()

pdf=PdfReader(str(target));assert len(pdf.pages)==1
assert abs(float(pdf.pages[0].mediabox.width)-210*mm)<.01
assert abs(float(pdf.pages[0].mediabox.height)-297*mm)<.01
assert 126>120+4
doc=pdfium.PdfDocument(str(target))
page=doc[0];bitmap=page.render(scale=1.8)
bitmap.to_pil().save(out/'AikaOS-CD-Falthuelle-A4-Schwarzweiss-Aika-Vorschau.png')
print(target)
print('Verified: one A4 page, 126 mm pocket, outer glue tabs, 50 mm calibration bar.')
