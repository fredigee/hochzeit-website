from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

rooms = [
    ("1",   "Villa Merlo Nero", "Fairy",      "1. OG",  "Jana, Frederik, Taro"),
    ("2",   "Villa Merlo Nero", "Sevilliana", "1. OG",  "Andrea"),
    ("3",   "Villa Merlo Nero", "Eden Rose",  "1. OG",  "Christina, Susanne"),
    ("4",   "Villa Merlo Nero", "Gardenia",   "1. OG A","Michelle, Christian"),
    ("5",   "Villa Merlo Nero", "Peonia",     "1. OG A","Sophie, Charlotte"),
    ("6",   "Villa Merlo Nero", "Iris",       "1. OG A","Kevin, Timo"),
    ("7",   "Villa Merlo Nero", "Magnolia",   "1. OG A","Wolfgang, Bernadette"),
    ("8",   "Villa Antica",     "Sofonisba",  "1. OG",  "Larissa, Latif, Maysa"),
    ("9",   "Villa Antica",     "Putti",      "1. OG",  "Marie, Martin"),
    ("10",  "Villa Antica",     "Patrick",    "1. OG",  "Bettina, Christina"),
    ("11",  "Villa Antica",     "Helen",      "1. OG",  "Lilian, Jennifer"),
    ("12",  "Villa Antica",     "Tinaia",     "EG",     "Klaus, Laurance"),
    ("13a", "Cottage",          "—",          "—",      "Boris, Chrystal"),
    ("13b", "Cottage",          "—",          "—",      "Aila, Antonia"),
]

doc = SimpleDocTemplate(
    "static/Zimmerliste.pdf",
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle("title", parent=styles["Normal"],
    fontName="Times-Roman", fontSize=20, leading=28,
    alignment=TA_CENTER, spaceAfter=6)
sub_style = ParagraphStyle("sub", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=11, leading=16,
    alignment=TA_CENTER, spaceAfter=4, textColor=colors.HexColor("#555555"))
note_style = ParagraphStyle("note", parent=styles["Normal"],
    fontName="Times-Italic", fontSize=10, leading=14,
    alignment=TA_CENTER, textColor=colors.HexColor("#555555"))

header = ["#", "Gebäude", "Zimmer", "Stockwerk", "Gäste"]
data = [header] + [list(r) for r in rooms]

col_widths = [1.2*cm, 4.8*cm, 3.2*cm, 2.4*cm, 5.4*cm]

table = Table(data, colWidths=col_widths, repeatRows=1)
table.setStyle(TableStyle([
    ("FONTNAME",      (0,0), (-1,0),  "Times-Bold"),
    ("FONTSIZE",      (0,0), (-1,0),  10),
    ("FONTNAME",      (0,1), (-1,-1), "Times-Roman"),
    ("FONTSIZE",      (0,1), (-1,-1), 10),
    ("LEADING",       (0,0), (-1,-1), 14),
    ("ALIGN",         (0,0), (-1,-1), "LEFT"),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [colors.white, colors.HexColor("#f5f5f5")]),
    ("LINEBELOW",     (0,0), (-1,0),  1, colors.black),
    ("LINEBELOW",     (0,1), (-1,-1), 0.3, colors.HexColor("#dddddd")),
    ("BOX",           (0,0), (-1,-1), 0.5, colors.HexColor("#cccccc")),
]))

story = [
    Paragraph("Jana &amp; Frederik — Juni 2026", title_style),
    Paragraph("Zimmereinteilung", sub_style),
    Spacer(1, 0.5*cm),
    table,
    Spacer(1, 0.4*cm),
    Paragraph("Check-out: Montag, 22. Juni 2026 — 10:00 Uhr", note_style),
]

doc.build(story)
print("PDF erstellt: static/Zimmerliste.pdf")
