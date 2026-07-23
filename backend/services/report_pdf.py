"""PDF rendering for the development report (Area 2 T14).

Round 6 (2026-07-21, user request): rebuilt to visually mirror the web laporan page
(frontend/src/pages/ReportPage.tsx + CvProfileSections/SkillGapSections/GapPanel) instead of the
original generic single-teal-panel layout — same color tokens (frontend/src/styles/tokens.css),
same section names/order (Ringkasan Analisis Keahlian -> Keahlian Eksplisit/Tersirat ->
Sesuai Kebutuhan/Kompetensi Belum Terpenuhi -> Kekuatan Utama -> Wawancara -> Estimasi Waktu
Upskilling), and a custom chip Flowable for the skill/competency badge lists since Platypus tables
are a fixed grid and can't flex-wrap on their own. Wawancara intentionally omits video (a static
PDF can't embed one) — question box + Aspek/Deskripsi/Skor rubric table + Transkrip Asli/Ringkasan
AI table only, per that request.
"""

import html
import io

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Same palette as frontend/src/styles/tokens.css — kept as (background, text) pairs matching each
# named "tone" the web app uses (GapPanel.tsx / .section-bar-header).
_INK = colors.HexColor("#1b1f1e")
_INK_2 = colors.HexColor("#3f4644")
_MUTED = colors.HexColor("#748580")
_BORDER = colors.HexColor("#dbe4e1")
_WHITE = colors.white

_TONES = {
    "info": (colors.HexColor("#e3efec"), colors.HexColor("#0f6b5c")),
    "success": (colors.HexColor("#e3f3ec"), colors.HexColor("#1c7a52")),
    "warning": (colors.HexColor("#faf1de"), colors.HexColor("#b5790a")),
    "gold": (colors.HexColor("#f7ecd8"), colors.HexColor("#c98a2c")),
    "danger": (colors.HexColor("#f7e8e6"), colors.HexColor("#a5352b")),
}

# Mirrors frontend/src/components/RubricDots.tsx's RUBRIC_LABELS — kept in sync manually since the
# PDF has no shared-schema import path to the frontend.
_RUBRIC_LABELS = {
    "clarity": "Kejelasan",
    "relevance": "Relevansi",
    "technical_depth": "Kedalaman Teknis",
}

# Round 8 (2026-07-21): upskilling_plan's effort-tier keys, mirrored to Indonesian display labels.
_TIER_LABELS = {
    "low_effort": "Effort Rendah (Jam/Hari)",
    "medium_effort": "Effort Sedang (Minggu)",
    "high_effort": "Effort Tinggi (Bulan)",
}


def _p(text: str, style) -> Paragraph:
    return Paragraph(html.escape(str(text)).replace("\n", "<br/>"), style)


class _ChipRow(Flowable):
    """Wrap-packed pill badges — the static-PDF equivalent of GapPanel.tsx's flex-wrap chip list.
    Platypus Tables are a fixed grid and can't wrap content across cells on their own, so this
    measures each label with reportlab's own metrics and greedily packs them into rows that fit
    `width`, drawing each as a rounded rect + centered text."""

    def __init__(self, items: list[str], width: float, bg: colors.Color, fg: colors.Color):
        super().__init__()
        self.items = items
        self.width = width
        self.bg = bg
        self.fg = fg
        self.font_name = "Helvetica-Bold"
        self.font_size = 8.3
        self._pad_x = 8
        self._gap = 6
        self._row_h = self.font_size + 11
        self._row_gap = 5
        self._rows: list[list[tuple[str, float]]] = []

    def wrap(self, avail_width, avail_height):
        self._rows = []
        current: list[tuple[str, float]] = []
        current_w = 0.0
        for item in self.items:
            w = stringWidth(item, self.font_name, self.font_size) + self._pad_x * 2
            added_w = w if not current else self._gap + w
            if current and current_w + added_w > self.width:
                self._rows.append(current)
                current = []
                current_w = 0.0
                added_w = w
            current.append((item, w))
            current_w += added_w
        if current:
            self._rows.append(current)
        # Must set self.height (not just return it) — draw() below reads self.height, and the
        # base Flowable class doesn't populate it from wrap()'s return value automatically. This
        # was the actual bug behind chips rendering near y=0 (bottom of/below the panel) instead
        # of top-anchored: self.height stayed at Flowable's default 0 the whole time.
        self.height = len(self._rows) * self._row_h + max(0, len(self._rows) - 1) * self._row_gap
        return self.width, self.height

    def draw(self):
        c = self.canv
        y = self.height - self._row_h
        for row in self._rows:
            x = 0.0
            for item, w in row:
                c.setFillColor(self.bg)
                c.roundRect(x, y, w, self._row_h - 3, 4, fill=1, stroke=0)
                c.setFillColor(self.fg)
                c.setFont(self.font_name, self.font_size)
                c.drawString(x + self._pad_x, y + (self._row_h - 3) / 2 - self.font_size / 2 + 2.2, item)
                x += w + self._gap
            y -= self._row_h + self._row_gap


def _section_bar(title: str, tone: str, styles: dict, content_width: float) -> Table:
    """One-row colored header bar on its own — used for full-width section titles (Wawancara,
    Ringkasan Analisis Keahlian) that don't need a bordered body wrapper of their own."""
    bg, fg = _TONES[tone]
    style = ParagraphStyle(
        "SectionBar", parent=styles["heading"], textColor=fg, fontSize=10.5,
    )
    table = Table([[Paragraph(html.escape(title.upper()), style)]], colWidths=[content_width])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def _panel(title: str, body_flowables: list, tone: str, styles: dict, content_width: float) -> Table:
    """Colored header row + white body — same nested-table technique as before, now parameterized
    by tone so it can render any of the app's accent colors, not just teal."""
    bg, fg = _TONES[tone]
    if not body_flowables:
        body_flowables = [_p("Tidak ada data.", styles["body"])]

    header_style = ParagraphStyle("PanelHeading", parent=styles["heading"], textColor=fg)
    rows = [[Paragraph(html.escape(title), header_style)]]
    for flow in body_flowables:
        rows.append([flow])

    table = Table(rows, colWidths=[content_width], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), bg),
                ("BACKGROUND", (0, 1), (-1, -1), _WHITE),
                ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _gap_panel(title: str, items: list[str], empty_label: str, tone: str, styles: dict, width: float) -> Table:
    """Direct PDF counterpart of GapPanel.tsx — colored header + chip-row body, one column wide."""
    inner_width = width - 24  # panel's own left+right padding
    body = [_ChipRow(items, inner_width, *_TONES[tone])] if items else [_p(empty_label, styles["hint"])]
    return _panel(title, body, tone, styles, width)


def _strength_card(title: str, description: str, styles: dict, width: float) -> Table:
    """Bordered mini-card (title + description) — mirrors SkillGapSections.tsx's Kekuatan Utama
    .profile-list-item rows, stacked inside the "Kekuatan Utama" panel body."""
    table = Table(
        [[_p(title, styles["subheading"])], [_p(description, styles["body_small"])]],
        colWidths=[width],
    )
    table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (0, 0), 8),
                ("BOTTOMPADDING", (0, 0), (0, 0), 2),
                # Row/col were swapped here — (1, 0) addresses a nonexistent second column on this
                # 1-column table, so it silently no-ops and row 1 (the description) fell back to
                # ReportLab's default 6pt top padding stacked on top of the title's own 2pt bottom
                # padding, which is what produced the oversized gap inside each card.
                ("TOPPADDING", (0, 1), (0, 1), 0),
                ("BOTTOMPADDING", (-1, -1), (-1, -1), 8),
            ]
        )
    )
    return table


def _question_box(index: int, question_text: str, styles: dict, width: float) -> Table:
    """Direct counterpart of ReportPage.css's .report-question-box — teal-soft callout with a small
    "PERTANYAAN N" label above the bolded question text."""
    bg, fg = _TONES["info"]
    label_style = ParagraphStyle(
        "QuestionLabel", parent=styles["hint"], textColor=fg, fontName="Helvetica-Bold", fontSize=8,
    )
    table = Table(
        [[_p(f"PERTANYAAN {index}", label_style)], [_p(question_text, styles["subheading"])]],
        colWidths=[width],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (0, 0), 10),
                ("BOTTOMPADDING", (0, 0), (0, 0), 4),
                ("TOPPADDING", (1, 0), (1, 0), 0),
                ("BOTTOMPADDING", (-1, -1), (-1, -1), 10),
            ]
        )
    )
    return table


def _rubric_table(rubric_scores: list[dict], styles: dict, width: float) -> Table:
    """Direct counterpart of ReportPage.tsx's .rubric-table — Aspek | Deskripsi | Skor, teal-soft
    header row. Skor is rendered as "N/5" text rather than the web's dot indicator — the base-14
    PDF fonts don't reliably carry the filled/outline circle glyphs the dots use."""
    bg, fg = _TONES["info"]
    header_style = ParagraphStyle("RubricHeader", parent=styles["hint"], textColor=fg, fontName="Helvetica-Bold")
    aspek_w = width * 0.22
    skor_w = width * 0.12
    desk_w = width - aspek_w - skor_w

    rows = [[_p("ASPEK", header_style), _p("DESKRIPSI", header_style), _p("SKOR", header_style)]]
    for r in rubric_scores:
        label = _RUBRIC_LABELS.get(r["criterion_name"], r["criterion_name"])
        rows.append([_p(label, styles["subheading"]), _p(r["rationale"], styles["body_small"]), _p(f"{r['score']}/5", styles["body_small"])])

    table = Table(rows, colWidths=[aspek_w, desk_w, skor_w], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), bg),
                ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _ats_table(items: list[dict], styles: dict, width: float) -> Table:
    """Direct counterpart of ReportPage.css's .ats-table — Kalimat Asli di CV | Saran Perbaikan
    Kalimat, gold header row, 50/50 columns."""
    bg, fg = _TONES["gold"]
    header_style = ParagraphStyle("AtsHeader", parent=styles["hint"], textColor=fg, fontName="Helvetica-Bold")
    col_w = width / 2

    rows = [[_p("KALIMAT ASLI DI CV", header_style), _p("SARAN PERBAIKAN KALIMAT", header_style)]]
    for item in items:
        rows.append([_p(item["original"], styles["body_small"]), _p(item["improved"], styles["body_small"])])

    table = Table(rows, colWidths=[col_w, col_w], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), bg),
                ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, _BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _transcript_table(summary_text: str | None, styles: dict, width: float) -> Table | None:
    """Direct counterpart of ReportPage.tsx's .answer-summary-table, minus the Transkrip Asli row
    (PDF-only, user request 2026-07-21) — the raw transcript is the longest text block per answer
    and kept forcing this table to split awkwardly mid-row across a page break; Ringkasan AI alone
    is short enough to consistently stay on one page. The web page still shows both."""
    if not summary_text:
        return None
    rows_data = [("RINGKASAN AI", summary_text)]

    bg, fg = _TONES["info"]
    label_style = ParagraphStyle("AnswerLabel", parent=styles["hint"], textColor=fg, fontName="Helvetica-Bold")
    label_w = width * 0.22
    value_w = width - label_w

    rows = [[_p(label, label_style), _p(value, styles["body_small"])] for label, value in rows_data]
    table = Table(rows, colWidths=[label_w, value_w])
    style = [
        ("BACKGROUND", (0, 0), (0, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.9, _BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, _BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    table.setStyle(TableStyle(style))
    return table


def render_report_pdf(report: dict, interview_answers: list[dict] | None = None) -> bytes:
    """report: the dict returned by services.report.build_report().
    interview_answers: the list returned by services.report.build_interview_answers() (optional —
    omitted/empty simply skips the Wawancara section, same as the web page does)."""
    base_styles = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "Title", parent=base_styles["Title"], fontSize=20, alignment=TA_CENTER,
            textColor=_INK, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base_styles["BodyText"], fontSize=11, alignment=TA_CENTER,
            textColor=_INK_2, spaceAfter=16,
        ),
        "heading": ParagraphStyle(
            "Heading", parent=base_styles["Heading3"], fontSize=10.5, fontName="Helvetica-Bold",
        ),
        "subheading": ParagraphStyle(
            "SubHeading", parent=base_styles["BodyText"], fontSize=10.5, fontName="Helvetica-Bold",
            textColor=_INK, spaceAfter=2,
        ),
        "body": ParagraphStyle(
            "Body", parent=base_styles["BodyText"], fontSize=10.2, leading=14.5,
            alignment=TA_JUSTIFY, textColor=_INK_2, spaceAfter=4,
        ),
        "body_small": ParagraphStyle(
            "BodySmall", parent=base_styles["BodyText"], fontSize=9.3, leading=13.5,
            alignment=TA_JUSTIFY, textColor=_INK_2,
        ),
        "hint": ParagraphStyle(
            "Hint", parent=base_styles["BodyText"], fontSize=8.5, textColor=_MUTED,
        ),
    }

    buffer = io.BytesIO()
    pdf_title = f"Laporan {report['candidate_alias']} - {report['job_title']}"
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, topMargin=36, bottomMargin=36, leftMargin=32, rightMargin=32,
        title=pdf_title, author="GaskeunKerja for Business",
    )
    content_width = A4[0] - 64

    story = []
    story.append(_p("Laporan Feedback CV dan Wawancara", styles["title"]))
    story.append(_p(f"{report['candidate_alias']} · {report['job_title']}", styles["subtitle"]))

    # Ringkasan Analisis Keahlian
    story.append(_panel("Ringkasan Analisis Keahlian", [_p(report["gap_summary"], styles["body"])], "info", styles, content_width))
    story.append(Spacer(1, 14))

    # Keahlian Eksplisit / Keahlian Tersirat — stacked full-width (not side-by-side like the web
    # page) so a long chip list gets the whole row's width to wrap into instead of being squeezed
    # into half of it, per user request (2026-07-21, PDF-only change).
    story.append(_gap_panel("Keahlian Eksplisit", report.get("skills", []), "Tidak ada.", "info", styles, content_width))
    story.append(Spacer(1, 10))
    story.append(_gap_panel("Keahlian Tersirat", report.get("skills_implicit", []), "Tidak ada.", "success", styles, content_width))
    story.append(Spacer(1, 14))

    # Sesuai Kebutuhan / Kompetensi Belum Terpenuhi — same stacked full-width treatment.
    story.append(
        _gap_panel(
            "Sesuai Kebutuhan", report["matched_competencies"], "Belum ada kompetensi yang sesuai.",
            "success", styles, content_width,
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        _gap_panel(
            "Kompetensi Belum Terpenuhi", report["missing_competencies"], "Tidak ada kesenjangan kompetensi.",
            "warning", styles, content_width,
        )
    )
    story.append(Spacer(1, 14))

    # Kekuatan Utama — no Spacer between cards: each card is its own row in the outer _panel
    # table, which already applies 8pt top/bottom padding per row, so an extra Spacer row (itself
    # also padded 8pt top/bottom by that same rule) was double-counting whitespace and produced the
    # oversized gap between cards.
    key_strengths = report.get("key_strengths", [])
    if key_strengths:
        cards = [_strength_card(s["title"], s["description"], styles, content_width - 24) for s in key_strengths]
        story.append(_panel("Kekuatan Utama", cards, "gold", styles, content_width))
        story.append(Spacer(1, 14))

    # Saran Perbaikan CV (ATS) — same position as the web laporan page (after Kekuatan Utama,
    # before Wawancara).
    resume_action_items = report.get("resume_action_items", [])
    if resume_action_items:
        story.append(_section_bar("Saran Perbaikan CV (ATS)", "gold", styles, content_width))
        story.append(Spacer(1, 10))
        story.append(_ats_table(resume_action_items, styles, content_width))
        story.append(Spacer(1, 14))

    # Wawancara — question box + rubric table + transkrip/ringkasan table, no video.
    if interview_answers:
        story.append(_section_bar("Wawancara", "info", styles, content_width))
        story.append(Spacer(1, 10))
        for i, answer in enumerate(interview_answers, start=1):
            story.append(_question_box(i, answer["question_text"], styles, content_width))
            story.append(Spacer(1, 8))
            if answer["rubric_scores"]:
                story.append(_rubric_table(answer["rubric_scores"], styles, content_width))
                story.append(Spacer(1, 8))
            transcript_table = _transcript_table(answer["summary_text"], styles, content_width)
            if transcript_table:
                story.append(transcript_table)
            story.append(Spacer(1, 18))

    # Kekuatan Utama Wawancara / Feedback Wawancara — the web page shows these two side-by-side
    # (profile-grid-2), but the PDF's content_width is too narrow for a readable 2-column split, so
    # both render as a single stacked column of long cards instead, same treatment as Kekuatan
    # Utama above.
    interview_key_strengths = report.get("interview_key_strengths", [])
    if interview_key_strengths:
        cards = [_strength_card(s["title"], s["description"], styles, content_width - 24) for s in interview_key_strengths]
        story.append(_panel("Kekuatan Utama Wawancara", cards, "info", styles, content_width))
        story.append(Spacer(1, 14))

    interview_feedback = report.get("interview_feedback", [])
    if interview_feedback:
        cards = [_strength_card(s["title"], s["description"], styles, content_width - 24) for s in interview_feedback]
        story.append(_panel("Feedback Wawancara", cards, "danger", styles, content_width))
        story.append(Spacer(1, 14))

    # Estimasi Waktu Upskilling — Round 8 (2026-07-21): report["upskilling_plan"] is now
    # {"kompetensi_belum_terpenuhi": {name: {tier: [...]}}, "area_pengembangan_wawancara": {name:
    # {tier: [...]}}}, fully LLM-generated (services/skillgap.py::generate_upskilling_plan) — same
    # shape rendered on the web laporan page. Two groups, same panel style, distinguished by tone
    # (teal = CV skill gap, red = interview weakness, matching Wawancara's own accent elsewhere).
    upskilling_plan = report.get("upskilling_plan") or {}
    for group_key, group_tone in (("kompetensi_belum_terpenuhi", "info"), ("area_pengembangan_wawancara", "danger")):
        for name, tiers in (upskilling_plan.get(group_key) or {}).items():
            flows = []
            for tier_key, tier_label in _TIER_LABELS.items():
                items = (tiers or {}).get(tier_key, [])
                if not items:
                    continue
                flows.append(_p(tier_label, styles["subheading"]))
                for it in items:
                    flows.append(_strength_card(it["title"], it["description"], styles, content_width - 24))
            if flows:
                story.append(_panel(name, flows, group_tone, styles, content_width))
                story.append(Spacer(1, 14))

    doc.build(story)
    return buffer.getvalue()
