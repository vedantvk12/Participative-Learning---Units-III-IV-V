"""
Build Dedicated Panel Discussion Role-Play Script PDF
Multi-Agent Enterprise AI Service Desk (Units III, IV & V)
Student: Vedant Sattejkumar Kirange | Roll: 55 | Enrollment: ADT23SOCB1294
"""

import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
OUTPUT_PDF = BASE_DIR / "Panel_Discussion_Role_Play_Script.pdf"

from panel_discussion.questions_data import PANEL_QUESTIONS


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Suppress header/footer on page 1 (cover)
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica", 8.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(54, 842 - 36, "Panel Discussion Role-Play Script | Building, Coordinating & Governing Agentic AI")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 842 - 42, 595 - 54, 842 - 42)

            # Footer
            self.line(54, 46, 595 - 54, 46)
            self.setFont("Helvetica", 8)
            self.drawString(54, 34, "Student: Vedant Sattejkumar Kirange | Roll: 55 | Enrollment: ADT23SOCB1294")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(595 - 54, 34, page_text)
        self.restoreState()


def build_panel_script():
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceAfter=20
    )
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0F172A")
    )
    h1_style = ParagraphStyle(
        'ScriptH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    q_title_style = ParagraphStyle(
        'QuestionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    mod_style = ParagraphStyle(
        'ModSpeech',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155")
    )
    speaker_label = ParagraphStyle(
        'SpeakerLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E3A8A")
    )
    body_style = ParagraphStyle(
        'SpeakerBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )
    disagree_style = ParagraphStyle(
        'DisagreeText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#991B1B")
    )
    decision_style = ParagraphStyle(
        'DecisionText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#065F46")
    )

    story = []

    # --- COVER PAGE ---
    story.append(Spacer(1, 40))
    story.append(Paragraph("PANEL DISCUSSION & ROLE-PLAY SCRIPT", title_style))
    story.append(Paragraph("Building, Coordinating, and Governing Real-World Agentic AI Systems", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor("#1E3A8A"), spaceAfter=25))

    overview_p = Paragraph(
        "<b>Activity Overview:</b> This structured classroom role-play script simulates a multi-stakeholder debate "
        "on the engineering, user experience, and governance challenges of deploying an autonomous Multi-Agent AI Service Desk. "
        "The debate features four distinct roles: <b>Moderator</b>, <b>Developer</b>, <b>End User</b>, and <b>Regulator</b>, "
        "addressing eight core questions concerning memory retention, tool authority, autonomous multi-agent consensus, liability, "
        "prompt injection, employee data privacy, conflict resolution, and deployment readiness gates.",
        ParagraphStyle('Overview', fontName='Helvetica', fontSize=10, leading=14.5, textColor=colors.HexColor("#334155"))
    )
    story.append(overview_p)
    story.append(Spacer(1, 25))

    # Identification Box
    id_data = [
        [Paragraph("<b>Student Name:</b>", meta_style), Paragraph("Vedant Sattejkumar Kirange", body_style)],
        [Paragraph("<b>Roll Number:</b>", meta_style), Paragraph("55", body_style)],
        [Paragraph("<b>Enrollment Number:</b>", meta_style), Paragraph("ADT23SOCB1294", body_style)],
        [Paragraph("<b>Curriculum Topics:</b>", meta_style), Paragraph("Units III, IV & V — Memory, Tools, Collaboration & Ethics", body_style)],
        [Paragraph("<b>Project Title:</b>", meta_style), Paragraph("Building and Governing a Multi-Agent Enterprise AI Service Desk", body_style)]
    ]
    id_table = Table(id_data, colWidths=[150, 337])
    id_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(id_table)
    story.append(Spacer(1, 30))

    # Role Definitions Table
    story.append(Paragraph("<b>Participating Stakeholder Roles:</b>", h1_style))
    roles_data = [
        [Paragraph("<b>Role</b>", meta_style), Paragraph("<b>Representative Focus & Mindset</b>", meta_style)],
        [Paragraph("<b>🎙️ Moderator</b>", speaker_label), Paragraph("Frames questions, balances speaking time, challenges complacency, and synthesizes consensus.", body_style)],
        [Paragraph("<b>👨‍💻 Developer</b>", speaker_label), Paragraph("Defends architecture, memory caching, tool automation, token efficiency, and operational speed.", body_style)],
        [Paragraph("<b>👤 End User</b>", speaker_label), Paragraph("Advocates for transparency, privacy, job security, accurate support, and effortless human escalation.", body_style)],
        [Paragraph("<b>⚖️ Regulator</b>", speaker_label), Paragraph("Enforces statutory compliance (GDPR, EU AI Act, NIST AI RMF), accountability, and human-in-the-loop controls.", body_style)]
    ]
    roles_table = Table(roles_data, colWidths=[120, 367])
    roles_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    # Fix header text color in table style
    roles_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0,0), (-1,0), colors.white)
    ]))
    story.append(roles_table)

    story.append(PageBreak())

    # --- SCRIPT BODY (8 QUESTIONS) ---
    story.append(Paragraph("Classroom Panel Discussion Script: 8 Deliberation Rounds", h1_style))
    story.append(Spacer(1, 10))

    for q in PANEL_QUESTIONS:
        q_elements = []
        q_elements.append(Paragraph(f"Round {q['q_id']}: {q['question']}", q_title_style))
        q_elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#93C5FD"), spaceAfter=8))

        # Moderator Opening
        mod_text = f"<b>Moderator:</b> Panelists, let us examine Question {q['q_id']}: <i>\"{q['question']}\"</i>. Developer, begin with the architectural design; User, give your reaction; and Regulator, outline legal boundaries."
        q_elements.append(Paragraph(mod_text, mod_style))
        q_elements.append(Spacer(1, 6))

        # Table of 3 views
        views_data = [
            [Paragraph("<b>👨‍💻 Developer:</b>", speaker_label), Paragraph(q['developer'], body_style)],
            [Paragraph("<b>👤 End User:</b>", speaker_label), Paragraph(q['end_user'], body_style)],
            [Paragraph("<b>⚖️ Regulator:</b>", speaker_label), Paragraph(q['regulator'], body_style)]
        ]
        views_table = Table(views_data, colWidths=[100, 387])
        views_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EFF6FF")),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F0FDF4")),
            ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#FEF2F2")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        q_elements.append(views_table)
        q_elements.append(Spacer(1, 6))

        # Disagreement & Decision Box
        summary_data = [
            [Paragraph("<b>⚡ Core Conflict:</b>", disagree_style), Paragraph(q['main_disagreement'], body_style)],
            [Paragraph("<b>🤝 Group Decision:</b>", decision_style), Paragraph(q['group_decision'], body_style)]
        ]
        sum_table = Table(summary_data, colWidths=[110, 377])
        sum_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#FFF1F2")),
            ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#ECFDF5")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        q_elements.append(sum_table)
        q_elements.append(Spacer(1, 14))

        story.append(KeepTogether(q_elements))

    # --- CONCLUSION & FINAL GOVERNANCE SYNTHESIS ---
    story.append(KeepTogether([
        Paragraph("Panel Summary: The 4-Pillar Enterprise Governance Charter", h1_style),
        Paragraph(
            "<b>Moderator's Closing Remarks:</b> Our panel discussion concludes that deploying autonomous Agentic AI "
            "in an enterprise service desk is viable only when speed and automation are bound to strict governance guardrails. "
            "The panel has reached consensus on four universal rules: "
            "(1) <b>Sanitized Persistent Memory</b> with explicit user consent and right-to-erasure; "
            "(2) <b>Tiered Least-Privilege Tools</b> requiring cryptographic Human-in-the-Loop gating for state mutations; "
            "(3) <b>Independent Security Guardrails</b> that intercept adversarial prompts prior to execution; and "
            "(4) <b>Hierarchical Conflict Precedence</b> ensuring safety and statutory compliance supersede system availability.",
            body_style
        ),
        Spacer(1, 10),
        Paragraph("<b>Final Group Decision:</b> ACCEPT SYSTEM FOR DEPLOYMENT SUBJECT TO GATED PHASED ROLLOUT AND SOC AUDITING.", meta_style)
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated: {OUTPUT_PDF}")


if __name__ == "__main__":
    build_panel_script()
