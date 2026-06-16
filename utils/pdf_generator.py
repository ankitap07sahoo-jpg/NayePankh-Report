from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
from sqlalchemy.sql import func
from database.connection import get_session
from database.models import Volunteer, Donation, Program, Beneficiary
import datetime

def generate_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    
    elements = []
    
    # Title
    title = Paragraph("<b>NayePankh Foundation</b>", styles['Title'])
    elements.append(title)
    
    subtitle = Paragraph("<b>Summary Report</b>", styles['Heading2'])
    elements.append(subtitle)
    
    date_str = Paragraph(f"<i>Generated on: {datetime.date.today().strftime('%d %b, %Y')}</i>", styles['Normal'])
    elements.append(date_str)
    elements.append(Spacer(1, 0.25*inch))
    
    session = get_session()
    
    # Volunteers Stats
    v_count = session.query(Volunteer).filter_by(is_active=True).count()
    elements.append(Paragraph("<b>1. Volunteer Statistics</b>", styles['Heading3']))
    elements.append(Paragraph(f"Active Volunteers: {v_count}", styles['Normal']))
    elements.append(Spacer(1, 0.15*inch))
    
    # Donations Stats
    elements.append(Paragraph("<b>2. Donation Statistics</b>", styles['Heading3']))
    d_total = session.query(func.sum(Donation.amount)).scalar() or 0.0
    elements.append(Paragraph(f"Total Funds Raised: INR {d_total:,.2f}", styles['Normal']))
    
    d_purpose = session.query(Donation.purpose, func.sum(Donation.amount)).group_by(Donation.purpose).all()
    if d_purpose:
        data = [["Purpose", "Amount (INR)"]]
        for p, amt in d_purpose:
            data.append([p if p else "General", f"{amt:,.2f}"])
            
        t = Table(data, colWidths=[2.5*inch, 2.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4361ee')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f4f6f9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(t)
        
    elements.append(Spacer(1, 0.25*inch))
    
    # Programs Stats
    elements.append(Paragraph("<b>3. Programs Overview</b>", styles['Heading3']))
    p_count = session.query(Program).count()
    elements.append(Paragraph(f"Total Programs: {p_count}", styles['Normal']))
    
    # Beneficiaries Stats
    b_count = session.query(Beneficiary).count()
    elements.append(Paragraph(f"Total Beneficiaries Impacted: {b_count}", styles['Normal']))
    
    session.close()
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
