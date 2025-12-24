"""
report_generator.py - Generate PDF test reports using ReportLab
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_test_report_pdf(output_path: str, lab_name: str, sample, test_name: str, raw_values: str, result: str, technician: str = '', date: datetime = None):
    if date is None:
        date = datetime.utcnow()
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"<b>{lab_name}</b>", styles['Title']))
    story.append(Spacer(1, 12))
    data = [
        ['Sample ID', getattr(sample, 'sample_id', '')],
        ['Sample Type', getattr(sample, 'sample_type', '')],
        ['Project', getattr(sample, 'project_name', '')],
        ['Client', getattr(sample, 'client_name', '')],
        ['Date Collected', getattr(sample, 'date_collected', '')],
        ['Test Name', test_name],
        ['Date Tested', date.strftime('%Y-%m-%d %H:%M')],
        ['Technician', technician]
    ]
    t = Table(data, hAlign='LEFT', colWidths=[120, 360])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0),(1,0), colors.whitesmoke),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))
    story.append(Paragraph('<b>Raw Values</b>', styles['Heading3']))
    story.append(Paragraph(str(raw_values).replace('\n','<br/>'), styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph('<b>Calculated Result</b>', styles['Heading3']))
    story.append(Paragraph(str(result), styles['Normal']))
    story.append(Spacer(1, 36))
    sig_data = [['Prepared by:', '', 'Checked by:', ''], ['', 'Signature: ____________________', '', 'Signature: ____________________']]
    sig_table = Table(sig_data, colWidths=[80, 180, 80, 180])
    sig_table.setStyle(TableStyle([('SPAN', (0,1),(1,1)), ('SPAN',(2,1),(3,1))]))
    story.append(sig_table)
    doc.build(story)
