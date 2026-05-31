from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

seats = [
    ("Oskar",     "Chris"),
    ("Andreas",   "Anja"),
    ("Concordia", "Ronnie"),
    ("Sophie",    "Melissa"),
    ("Eleonora",  "Antje"),
    ("Jan",       "Lucia"),
    ("Isabel",    "Amaryllis"),
    ("Manu",      "Symeon"),
    ("Timo",      "Jennifer"),
    ("Kevin",     "Lilian"),
    ("Felix",     "Amelie"),
    ("Miriam",    "Christian"),
    ("Christina", "Michelle"),
    ("Enya",      "Jana"),
    ("Toni",      "Frederik"),
    ("Boris",     "Taro"),
    ("Chrystal",  "Marie"),
    ("Antonia",   "Martin"),
    ("Aila",      "Andrea"),
    ("Christine", "Detti"),
    ("Susanne",   "Wolfgang"),
    ("Klaus",     "Bettina"),
    ("Laurence",  "Larissa"),
    ("Claudia",   "Maysa"),
    ("Peneolope", "Latif"),
    ("Phileas",   "Ayla"),
    ("Philomela", "Derya"),
    ("Markus",    "Sezer"),
    ("Leyan",     "Sami"),
]

doc = SimpleDocTemplate(
    "static/Sitzordnung.pdf",
    pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2.5*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("title", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=22, leading=30,
    alignment=TA_CENTER, spaceAfter=4)
sub_style = ParagraphStyle("sub", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=11, leading=16,
    alignment=TA_CENTER, spaceAfter=2, textColor=colors.HexColor("#555555"))
label_style = ParagraphStyle("label", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=9, leading=12,
    alignment=TA_CENTER, textColor=colors.HexColor("#777777"))

header = ["Linke Seite", "Nr.", "Rechte Seite"]
data = [header] + [[left, str(i+1), right] for i, (left, right) in enumerate(seats)]

col_widths = [6.5*cm, 1.8*cm, 6.5*cm]

table = Table(data, colWidths=col_widths, repeatRows=1)
table.setStyle(TableStyle([
    ("FONTNAME",      (0,0), (-1,0),  "Times-Bold"),
    ("FONTSIZE",      (0,0), (-1,0),  9),
    ("FONTNAME",      (0,1), (-1,-1), "Times-Roman"),
    ("FONTSIZE",      (0,1), (-1,-1), 11),
    ("LEADING",       (0,0), (-1,-1), 15),
    ("ALIGN",         (0,0), (0,-1),  "RIGHT"),
    ("ALIGN",         (1,0), (1,-1),  "CENTER"),
    ("ALIGN",         (2,0), (2,-1),  "LEFT"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("LINEBELOW",     (0,0), (-1,0),  1, colors.black),
    ("LINEBELOW",     (0,1), (-1,-1), 0.3, colors.HexColor("#dddddd")),
    ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
    ("TEXTCOLOR",     (1,1), (1,-1),  colors.HexColor("#555555")),
]))

story = [
    Paragraph("Jana &amp; Frederik", title_style),
    Paragraph("20. Juni 2026 · Florenz", sub_style),
    Spacer(1, 0.3*cm),
    Paragraph("S I T Z O R D N U N G", label_style),
    Spacer(1, 0.6*cm),
    table,
]

doc.build(story)
print("PDF erstellt: static/Sitzordnung.pdf")
