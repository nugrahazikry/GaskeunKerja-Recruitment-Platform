"""PDF rendering for the development report (Area 2 T14).

Adapts the ReportLab styling technique (panels, chip-style lists) from the Tahap 2
`_build_report_pdf()` reference (backend/app.py) — same visual approach, but built fresh
against this project's actual report schema (competency_framework + resource_library
development plan), which is structurally different from Tahap 2's career-gap report shape.
"""

import html
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

_HEADER_BG = colors.HexColor("#0f6b5c")  # Enterprise Trust teal (Area 1's locked palette)
_BORDER = colors.HexColor("#d1dce8")
_WHITE = colors.white


def _p(text: str, style) -> Paragraph:
    return Paragraph(html.escape(str(text)).replace("\n", "<br/>"), style)


def _panel(title: str, body_flowables: list, styles: dict, content_width: float) -> Table:
    if not body_flowables:
        body_flowables = [_p("Tidak ada data.", styles["body"])]

    rows = [[Paragraph(html.escape(title), styles["heading"])]]
    for flow in body_flowables:
        rows.append([flow])

    table = Table(rows, colWidths=[content_width], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _HEADER_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), _WHITE),
                ("BACKGROUND", (0, 1), (-1, -1), _WHITE),
                ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def render_report_pdf(report: dict) -> bytes:
    """report: the dict returned by services.report.build_report()."""
    base_styles = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title", parent=base_styles["Title"], fontSize=20, alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"), spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base_styles["BodyText"], fontSize=11, alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"), spaceAfter=16,
        ),
        "heading": ParagraphStyle(
            "Heading", parent=base_styles["Heading3"], fontSize=12.5, fontName="Helvetica-Bold",
        ),
        "subheading": ParagraphStyle(
            "SubHeading", parent=base_styles["BodyText"], fontSize=11, fontName="Helvetica-Bold",
            textColor=colors.HexColor("#0f172a"), spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "Body", parent=base_styles["BodyText"], fontSize=10.2, leading=14.5,
            alignment=TA_JUSTIFY, spaceAfter=4,
        ),
    }

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=36, bottomMargin=36, leftMargin=32, rightMargin=32
    )
    content_width = A4[0] - 64

    story = []
    story.append(_p("Laporan Pengembangan Kandidat", styles["title"]))
    story.append(_p(report["candidate_alias"], styles["subtitle"]))

    story.append(_panel("Ringkasan Kesenjangan Keterampilan", [_p(report["gap_summary"], styles["body"])], styles, content_width))
    story.append(Spacer(1, 14))

    if report.get("development_priority"):
        story.append(
            _panel(
                "Prioritas Pengembangan",
                [_p(report["development_priority"], styles["body"])],
                styles,
                content_width,
            )
        )
        story.append(Spacer(1, 14))

    for item in report.get("development_plan", []):
        flows = [
            _p(f"Level saat ini → target: {item['level_description']}", styles["body"]),
            _p("Sumber belajar yang direkomendasikan:", styles["subheading"]),
        ]
        for r in item["resources"]:
            flows.append(_p(f"• {r['title']} ({r['duration']}) — {r['milestone']}", styles["body"]))
        story.append(_panel(item["competency_name"], flows, styles, content_width))
        story.append(Spacer(1, 14))

    if report.get("interview_overall_score") is not None:
        story.append(
            _panel(
                "Skor Wawancara Keseluruhan",
                [_p(f"{report['interview_overall_score']:.1f} / 5.0", styles["body"])],
                styles,
                content_width,
            )
        )

    doc.build(story)
    return buffer.getvalue()
