#!/usr/bin/env python3
"""Build cv.pdf from site.json.

Two deliberate omissions, because this file is downloadable from a public page
and git keeps every version forever:
  * no home address, phone numbers, date of birth or gender
  * no papers under review, matching what the website shows

Keep the FlowCV version for sending directly to named people.
"""

import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, CondPageBreak)

D = json.load(open('site.json'))
V = D.get('visiting') or {}

PLUM, INK, SOFT, RULE = HexColor("#8f2555"), HexColor("#231c21"), HexColor("#6a6169"), HexColor("#d3d8da")

GF = "/usr/share/fonts/truetype/google-fonts/"
CE = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("Lora", GF + "Lora-Variable.ttf"))
pdfmetrics.registerFont(TTFont("Lora-I", GF + "Lora-Italic-Variable.ttf"))
pdfmetrics.registerFont(TTFont("Body", CE + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Body-B", CE + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body-I", CE + "Carlito-Italic.ttf"))

S = {
 "name":    ParagraphStyle("name", fontName="Lora", fontSize=23, leading=26,
                           textColor=PLUM, spaceAfter=3),
 "role":    ParagraphStyle("role", fontName="Lora-I", fontSize=10.5, leading=14,
                           textColor=INK, spaceAfter=2),
 "meta":    ParagraphStyle("meta", fontName="Body", fontSize=8.6, leading=12,
                           textColor=SOFT, spaceAfter=0),
 "h2":      ParagraphStyle("h2", fontName="Lora", fontSize=11.5, leading=13,
                           textColor=PLUM, spaceBefore=13, spaceAfter=5),
 "title":   ParagraphStyle("title", fontName="Body-B", fontSize=9.4, leading=12.4,
                           textColor=INK, spaceAfter=0.6),
 "venue":   ParagraphStyle("venue", fontName="Body-I", fontSize=8.6, leading=11,
                           textColor=SOFT, spaceAfter=0),
 "body":    ParagraphStyle("body", fontName="Body", fontSize=8.8, leading=11.8,
                           textColor=SOFT, alignment=TA_LEFT, spaceAfter=0),
 "when":    ParagraphStyle("when", fontName="Body", fontSize=8.4, leading=11,
                           textColor=SOFT),
}

story = []


def rule(space_before=3, space_after=6):
    t = Table([[""]], colWidths=[168 * mm], rowHeights=[0.4])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    story.extend([Spacer(1, space_before), t, Spacer(1, space_after)])


def section(label):
    # keep a heading from stranding itself at the foot of a page
    story.append(CondPageBreak(34 * mm))
    story.append(Paragraph(label, S["h2"]))
    rule(1, 5)


def two_col(left, blocks, gutter=26 * mm):
    """Date gutter on the left, content on the right."""
    t = Table([[Paragraph(left, S["when"]), blocks]],
              colWidths=[gutter, 168 * mm - gutter])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (0, 0), 6),
                           ("RIGHTPADDING", (1, 0), (1, 0), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    story.append(t)


# ---------------------------------------------------------------- header
story.append(Paragraph(D["name"], S["name"]))
story.append(Paragraph(f'{D["role"]}, {D["affiliation"]}', S["role"]))
if V:
    sup = f' with {V["supervisor"]}' if V.get("supervisor") else ""
    story.append(Paragraph(
        f'{V["role"]} at {V["orgFull"]} ({V["org"]}), {V["host"]}{sup} '
        f'&mdash; {V.get("period","")}', S["role"]))
story.append(Spacer(1, 5))
story.append(Paragraph(
    f'{D["email"]} &nbsp;&middot;&nbsp; merybria99.github.io'
    f' &nbsp;&middot;&nbsp; {D["location"]}', S["meta"]))
rule(7, 2)

# ---------------------------------------------------------------- research
section("Research")
for t in D["research"]:
    story.append(KeepTogether([
        Paragraph(t["title"], S["title"]),
        Paragraph(t["body"], S["body"]),
        Spacer(1, 6)]))

# ---------------------------------------------------------------- publications
VIS = [p for p in D["publications"] if not p.get("hidden")]
section("Publications")
for p in VIS:
    venue = p["venue"]
    if p.get("highlight"):
        venue += f' &mdash; {p["highlight"]}'
    two_col(p["year"], [Paragraph(p["title"], S["title"]),
                        Paragraph(venue, S["venue"])])

# ---------------------------------------------------------------- service
if D.get("service"):
    section("Service")
    for sv in D["service"]:
        two_col(sv["year"], [Paragraph(sv["text"], S["body"])])

# ---------------------------------------------------------------- education
section("Education and positions")
for b in D["background"]:
    blocks = [Paragraph(b["title"], S["title"]), Paragraph(b["org"], S["venue"])]
    if b.get("note"):
        blocks += [Spacer(1, 2), Paragraph(b["note"], S["body"])]
    two_col(b["period"], blocks)

# ---------------------------------------------------------------- schools
section("Summer schools")
for s in D["schools"]:
    two_col(s["year"], [Paragraph(f'{s["name"]}, {s["where"]}', S["title"])])

# ---------------------------------------------------------------- awards
section("Awards")
for yr, txt in (("2023", "Recognition for an outstanding academic career, University of Salerno "
                         "&mdash; for completing the B.Sc. with highest honours in the shortest time possible."),
                ("2023", "Selected for courses reserved for excellent students, University of Salerno "
                         "&mdash; open only to students averaging at least 28.")):
    two_col(yr, [Paragraph(txt, S["body"])])

# ---------------------------------------------------------------- skills
section("Technical")
story.append(Paragraph(
    "Python, C, Java, R, Matlab &nbsp;&middot;&nbsp; PyTorch, TensorFlow "
    "&nbsp;&middot;&nbsp; ROS Noetic, Django &nbsp;&middot;&nbsp; Linux",
    S["body"]))
story.append(Spacer(1, 3))
story.append(Paragraph(
    "Italian (native) &nbsp;&middot;&nbsp; English (C1, Cambridge Advanced) "
    "&nbsp;&middot;&nbsp; French (beginner)", S["body"]))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Body", 7.6)
    canvas.setFillColor(SOFT)
    canvas.drawString(21 * mm, 12 * mm, D["name"])
    canvas.drawRightString(A4[0] - 21 * mm, 12 * mm, f"Page {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    "/mnt/user-data/outputs/cv.pdf", pagesize=A4,
    leftMargin=21 * mm, rightMargin=21 * mm,
    topMargin=18 * mm, bottomMargin=20 * mm,
    title=f'{D["name"]} \u2014 Curriculum Vitae',
    author=D["name"], subject="Curriculum Vitae")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("built cv.pdf |", len(VIS), "publications,", len(D["background"]), "positions")
