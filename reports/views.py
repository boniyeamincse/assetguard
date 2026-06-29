from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from assets.models import Asset
from vulnerabilities.models import Vulnerability
from django.utils import timezone
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

@login_required
def reports_index(request):
    return render(request, 'reports/reports_index.html')

@login_required
def asset_report(request):
    assets = Asset.objects.all()
    context = {'assets': assets}
    return render(request, 'reports/asset_report.html', context)

@login_required
def vulnerability_report(request):
    vulnerabilities = Vulnerability.objects.all()
    context = {'vulnerabilities': vulnerabilities}
    return render(request, 'reports/vulnerability_report.html', context)

@login_required
def team_report(request):
    from teams.models import Team
    teams = Team.objects.all()
    context = {'teams': teams}
    return render(request, 'reports/team_report.html', context)

@login_required
def overdue_report(request):
    overdue_vulnerabilities = Vulnerability.objects.filter(
        due_date__lt=timezone.now(),
        status__in=['new', 'triaged', 'assigned', 'in_progress', 'reopened']
    )
    context = {'vulnerabilities': overdue_vulnerabilities}
    return render(request, 'reports/overdue_report.html', context)

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vulnerabilities.csv"'

    writer = csv.writer(response)
    writer.writerow(['Code', 'Title', 'Asset', 'Severity', 'Status', 'Assigned To', 'Created At'])

    vulnerabilities = Vulnerability.objects.all()
    for vuln in vulnerabilities:
        writer.writerow([
            vuln.vulnerability_code,
            vuln.title,
            vuln.asset.asset_name,
            vuln.severity,
            vuln.status,
            vuln.assigned_to.get_full_name() if vuln.assigned_to else '',
            vuln.created_at
        ])

    return response

@login_required
def export_reports(request):
    from django.utils import timezone
    assets = Asset.objects.all()
    vulnerabilities = Vulnerability.objects.all()
    context = {
        'assets': assets,
        'total_vulnerabilities': vulnerabilities.count(),
        'now': timezone.now(),
    }
    return render(request, 'reports/export_reports.html', context)

@login_required
def export_asset_report_pdf(request):
    asset_id = request.GET.get('asset_id')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="asset_report_{datetime.now().strftime("%Y%m%d")}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )

    # Title
    elements.append(Paragraph('Asset Report', title_style))
    elements.append(Paragraph(f'Generated on {datetime.now().strftime("%B %d, %Y")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    # Assets Section
    if asset_id:
        assets = Asset.objects.filter(pk=asset_id)
    else:
        assets = Asset.objects.all()

    elements.append(Paragraph(f'Assets: {assets.count()}', heading_style))

    asset_data = [['Code', 'Name', 'Type', 'Criticality', 'Vulnerabilities']]
    for asset in assets:
        asset_data.append([
            asset.asset_code,
            asset.asset_name,
            asset.get_asset_type_display(),
            asset.get_criticality_display(),
            str(asset.vulnerabilities.count())
        ])

    asset_table = Table(asset_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    asset_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f5f9')]),
    ]))
    elements.append(asset_table)
    elements.append(Spacer(1, 0.3*inch))

    # Vulnerabilities Section
    if asset_id:
        vulns = Vulnerability.objects.filter(asset_id=asset_id)
    else:
        vulns = Vulnerability.objects.all()

    elements.append(PageBreak())
    elements.append(Paragraph(f'Vulnerabilities: {vulns.count()}', heading_style))

    vuln_data = [['Code', 'Title', 'Severity', 'Status', 'Assigned To']]
    for vuln in vulns:
        vuln_data.append([
            vuln.vulnerability_code,
            vuln.title[:30],
            vuln.get_severity_display(),
            vuln.get_status_display(),
            vuln.assigned_to.get_full_name() if vuln.assigned_to else 'Unassigned'
        ])

    vuln_table = Table(vuln_data, colWidths=[1*inch, 2.5*inch, 1*inch, 1.2*inch, 1.3*inch])
    vuln_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fee2e2')]),
    ]))
    elements.append(vuln_table)

    doc.build(elements)
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response

@login_required
def export_vulnerability_report_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vulnerability_report_{datetime.now().strftime("%Y%m%d")}.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=30,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#ef4444'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )

    # Title
    elements.append(Paragraph('Vulnerability Report', title_style))
    elements.append(Paragraph(f'Generated on {datetime.now().strftime("%B %d, %Y")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))

    vulns = Vulnerability.objects.all()
    elements.append(Paragraph(f'Total Vulnerabilities: {vulns.count()}', heading_style))

    vuln_data = [['Code', 'Title', 'Asset', 'Severity', 'Status', 'Assigned']]
    for vuln in vulns:
        vuln_data.append([
            vuln.vulnerability_code,
            vuln.title[:25],
            vuln.asset.asset_code,
            vuln.get_severity_display(),
            vuln.get_status_display(),
            vuln.assigned_to.get_full_name()[:15] if vuln.assigned_to else 'No'
        ])

    vuln_table = Table(vuln_data, colWidths=[0.9*inch, 2.2*inch, 0.9*inch, 0.9*inch, 1*inch, 1.1*inch])
    vuln_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fee2e2')]),
    ]))
    elements.append(vuln_table)

    doc.build(elements)
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
