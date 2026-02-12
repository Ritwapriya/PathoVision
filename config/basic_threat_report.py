from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Symbola font for emojis
symbola_path = os.path.join(os.path.dirname(__file__), "Symbola.ttf")
if os.path.isfile(symbola_path):
    pdfmetrics.registerFont(TTFont('Symbola', symbola_path))
    default_font = 'Symbola'
else:
    print(f"Warning: Symbola.ttf not found at {symbola_path}, using default font.")
    default_font = 'Helvetica'

def create_threat_report(filename, model_name, gemini_text):
    """
    Generate a multi-page Gemini-style threat report PDF.

    Args:
        filename (str): Path to save PDF.
        model_name (str): Name of the model.
        gemini_text (str): AI-generated text (multiple items can be included).
    """
    styles = getSampleStyleSheet()

    # Box style for each detected item
    box_style = ParagraphStyle(
        'box',
        parent=styles['Normal'],
        fontName=default_font,
        fontSize=11,
        leading=16,
        spaceAfter=6,
        textColor=colors.black
    )

    # Title styles
    title_style = ParagraphStyle(
        'title',
        fontSize=36,
        alignment=1,
        spaceAfter=20
    )
    tagline_style = ParagraphStyle(
        'tagline',
        fontSize=16,
        alignment=1,
        spaceAfter=50
    )

    doc = SimpleDocTemplate(filename, pagesize=A4)
    story = []

    # --- Page 1: Title only ---
    story.append(Spacer(1, 40))

    # Optional logo
    logo_path = os.path.join(os.path.dirname(__file__), "logo.jpeg")
    if os.path.isfile(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 200  # adjust height
        logo.drawWidth = 200   # adjust width (keeps aspect ratio if square)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>{model_name}</b>", title_style))
    story.append(Spacer(1, 20))  # extra space below title
    story.append(Paragraph("Your Environmental & Public Health Sentinel", tagline_style))
    story.append(Spacer(1, 90))  # more space below tagline
    story.append(Paragraph("Detailed Threat Report",title_style))
    story.append(PageBreak())
     # --- Page 2+: Heading ---
    story.append(Paragraph("Detailed Description of Detected Items", 
                           ParagraphStyle('page2_title', 
                                          fontSize=20, 
                                          alignment=1,   # center
                                          spaceAfter=20,
                                          fontName=default_font)))
    # --- Page 2+: Split Gemini text per item ---
    # Split by "Detected Item :" assuming Gemini uses this for each entry
    items = gemini_text.split("Detected Item :")
    for item in items:
        item = item.strip()
        if not item:
            continue
        # Add back the prefix for clarity
        if not item.startswith("Detected Item :"):
            item = "Detected Item :" + item

        para = Paragraph(item.replace("\n", "<br/>"), box_style)
        box_table = Table([[para]], colWidths=[450])
        box_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.Color(0.97,0.98,1)),  # light blue
            ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#4B6584')),  # sober border
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),12),
            ('RIGHTPADDING',(0,0),(-1,-1),12),
            ('TOPPADDING',(0,0),(-1,-1),10),
            ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ]))
        story.append(box_table)
        story.append(Spacer(1, 15))

    doc.build(story)
