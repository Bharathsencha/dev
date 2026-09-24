import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = "/home/bharath/Downloads/DevOps_Monitoring_Stack_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "DevOps Monitoring Stack — Technical Project Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "DevOps Observability Pipeline (Prometheus, Grafana, Docker Compose)")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    table_header_style = ParagraphStyle(
        'TH_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TC_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("DevOps Monitoring Stack Demo", title_style))
    story.append(Paragraph("Complete Technical Project Guide & Architecture Explanation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=12))

    # 1. Project Summary
    story.append(Paragraph("1. Project Summary & Objectives", h1_style))
    story.append(Paragraph(
        "This project implements an end-to-end <b>DevOps Observability and Monitoring Pipeline</b> built with "
        "<b>Docker Compose</b>. It solves the critical problem of microservice blind spots in production by providing "
        "real-time monitoring of both <b>infrastructure health</b> (CPU, Memory) and <b>application performance</b> "
        "(request rates, latency percentiles, and error rates) through <b>Prometheus</b> and <b>Grafana</b>.",
        body_style
    ))

    # 2. What Does What
    story.append(Paragraph("2. Stack Components: What Does What?", h1_style))
    
    comp_data = [
        [Paragraph("Component", table_header_style), Paragraph("Port / URL", table_header_style), Paragraph("Role & Core Responsibility", table_header_style)],
        [Paragraph("<b>Flask Web App</b>", table_cell_style), Paragraph("5000", table_cell_style), Paragraph("Sample production microservice instrumented with <code>prometheus_client</code>. Exposes business routes and <code>/metrics</code>.", table_cell_style)],
        [Paragraph("<b>Prometheus</b>", table_cell_style), Paragraph("9090", table_cell_style), Paragraph("Time-Series Database (TSDB) and scraper. Pulls metrics every 5 seconds from Flask App and Node Exporter.", table_cell_style)],
        [Paragraph("<b>Grafana</b>", table_cell_style), Paragraph("3000", table_cell_style), Paragraph("Visualization engine. Queries Prometheus using PromQL and renders real-time interactive dashboards.", table_cell_style)],
        [Paragraph("<b>Node Exporter</b>", table_cell_style), Paragraph("9100", table_cell_style), Paragraph("Hardware/OS metrics agent. Gathers host CPU, Memory, and Disk stats directly from Linux kernel files.", table_cell_style)],
        [Paragraph("<b>Docker Compose</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Multi-container orchestration tool. Connects all 4 services onto an isolated bridge network with volumes.", table_cell_style)],
        [Paragraph("<b>Makefile</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("CLI command automation. Allows 1-command startup (<code>make</code>), traffic simulation, and shutdown.", table_cell_style)]
    ]
    
    t_comp = Table(comp_data, colWidths=[110, 65, 329])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # 3. What Our Flask App Does
    story.append(Paragraph("3. The Flask Application: Detailed Workflow", h1_style))
    story.append(Paragraph(
        "The Python web service (<code>app/app.py</code>) represents a live backend API. Every incoming request "
        "is intercepted before execution and upon response to compute metrics:",
        body_style
    ))
    
    flask_endpoints = [
        [Paragraph("Endpoint", table_header_style), Paragraph("HTTP Status", table_header_style), Paragraph("Behavior & DevOps Testing Purpose", table_header_style)],
        [Paragraph("<b>GET /</b>", table_cell_style), Paragraph("200 OK", table_cell_style), Paragraph("Fast healthy response. Represents normal user baseline traffic.", table_cell_style)],
        [Paragraph("<b>GET /slow</b>", table_cell_style), Paragraph("200 OK", table_cell_style), Paragraph("Injects random delay (0.5s–2.0s). Simulates slow database queries or API latency.", table_cell_style)],
        [Paragraph("<b>GET /error</b>", table_cell_style), Paragraph("500 Error", table_cell_style), Paragraph("Returns internal server error. Simulates unhandled code crashes or failed DB connections.", table_cell_style)],
        [Paragraph("<b>GET /metrics</b>", table_cell_style), Paragraph("200 OK", table_cell_style), Paragraph("Raw Prometheus-formatted metric dump scraped every 5s by the Prometheus engine.", table_cell_style)]
    ]
    t_flask = Table(flask_endpoints, colWidths=[90, 75, 339])
    t_flask.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_flask)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Flask Metrics Instrumentation:</b>", h2_style))
    story.append(Paragraph("• <b>http_requests_total (Counter):</b> Cumulative count of requests labeled by method, path, and HTTP status code.", bullet_style))
    story.append(Paragraph("• <b>http_request_duration_seconds (Histogram):</b> Execution duration grouped into exponential buckets to calculate percentiles (p50, p95).", bullet_style))
    story.append(Paragraph("• <b>http_request_errors_total (Counter):</b> Count of all 4xx and 5xx client/server errors.", bullet_style))
    story.append(Paragraph("• <b>http_requests_in_progress (Gauge):</b> Real-time concurrency tracking active concurrent requests in flight.", bullet_style))

    story.append(PageBreak())

    # 4. The Four Golden Signals
    story.append(Paragraph("4. The Four Golden Signals of Monitoring", h1_style))
    story.append(Paragraph(
        "The project tracks Google's industry-standard <b>Four Golden Signals</b> to achieve full observability:",
        body_style
    ))
    
    signals_data = [
        [Paragraph("Signal", table_header_style), Paragraph("Description", table_header_style), Paragraph("Project Implementation & PromQL", table_header_style)],
        [Paragraph("<b>Latency</b>", table_cell_style), Paragraph("Time taken to service requests.", table_cell_style), Paragraph("Measured via histogram: <code>histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))</code>", table_cell_style)],
        [Paragraph("<b>Traffic</b>", table_cell_style), Paragraph("Demand placed on the service.", table_cell_style), Paragraph("Request throughput: <code>sum(rate(http_requests_total[1m])) by (endpoint, http_status)</code>", table_cell_style)],
        [Paragraph("<b>Errors</b>", table_cell_style), Paragraph("Rate of requests that fail.", table_cell_style), Paragraph("Error percentage: <code>(sum(rate(http_request_errors_total[1m])) / sum(rate(http_requests_total[1m]))) * 100</code>", table_cell_style)],
        [Paragraph("<b>Saturation</b>", table_cell_style), Paragraph("How full the resources are.", table_cell_style), Paragraph("Host CPU & RAM utilization tracked via Node Exporter kernel metrics.", table_cell_style)]
    ]
    t_signals = Table(signals_data, colWidths=[80, 140, 284])
    t_signals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_signals)
    story.append(Spacer(1, 10))

    # 5. Grafana Dashboard Panels
    story.append(Paragraph("5. Grafana Dashboard Panels Explained", h1_style))
    story.append(Paragraph("• <b>CPU Usage (%):</b> Shows host processor utilization over time with warning (75%) and critical (90%) thresholds.", bullet_style))
    story.append(Paragraph("• <b>Memory Usage (%):</b> Shows host RAM utilization percentage and total used memory.", bullet_style))
    story.append(Paragraph("• <b>Total Processed Requests:</b> Stat card showing cumulative HTTP requests handled by the Flask web server.", bullet_style))
    story.append(Paragraph("• <b>Current Request Rate:</b> Live requests per second (req/s) throughput.", bullet_style))
    story.append(Paragraph("• <b>Error Rate (%):</b> Real-time failure percentage card; turns red when 500 errors occur.", bullet_style))
    story.append(Paragraph("• <b>Active In-Flight Requests:</b> Real-time concurrency indicator showing requests currently executing.", bullet_style))
    story.append(Paragraph("• <b>Request Rate by Endpoint:</b> Breakdown graph colored by route (<code>/</code>, <code>/slow</code>, <code>/error</code>).", bullet_style))
    story.append(Paragraph("• <b>Request Latency (p95, p50, Avg):</b> Visual curves comparing median response times against 95th percentile spikes.", bullet_style))
    story.append(Spacer(1, 6))

    # 6. Simple Step-by-Step Instructions
    story.append(Paragraph("6. Step-by-Step Execution Guide", h1_style))
    
    steps_data = [
        [Paragraph("Step", table_header_style), Paragraph("Command / Action", table_header_style), Paragraph("Expected Result", table_header_style)],
        [Paragraph("<b>1. Start</b>", table_cell_style), Paragraph("<code>make</code>", table_cell_style), Paragraph("Builds images & launches all 4 containers in the background.", table_cell_style)],
        [Paragraph("<b>2. View</b>", table_cell_style), Paragraph("Open <code>http://localhost:3000</code><br/>(User: <code>admin</code> / <code>admin</code>)", table_cell_style), Paragraph("Opens pre-provisioned Grafana dashboard automatically.", table_cell_style)],
        [Paragraph("<b>3. Traffic</b>", table_cell_style), Paragraph("<code>make traffic</code>", table_cell_style), Paragraph("Simulates continuous live traffic with latency & error spikes.", table_cell_style)],
        [Paragraph("<b>4. Status</b>", table_cell_style), Paragraph("<code>make status</code>", table_cell_style), Paragraph("Lists all container health statuses and exposed ports.", table_cell_style)],
        [Paragraph("<b>5. Stop</b>", table_cell_style), Paragraph("<code>make stop</code>", table_cell_style), Paragraph("Stops and removes all containers cleanly.", table_cell_style)]
    ]
    t_steps = Table(steps_data, colWidths=[65, 170, 269])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 10))

    # 7. Transition to Kubernetes
    story.append(Paragraph("7. Upgrading to Kubernetes (Production Scale)", h1_style))
    story.append(Paragraph(
        "For multi-node, large-scale enterprise deployments, this stack translates directly into Kubernetes objects:",
        body_style
    ))
    story.append(Paragraph("• <b>Flask App &rarr; Deployment + HPA:</b> Replicated across multiple pods and auto-scaled dynamically based on CPU/traffic load.", bullet_style))
    story.append(Paragraph("• <b>Node Exporter &rarr; DaemonSet:</b> Runs 1 pod per physical worker node to collect cluster-wide hardware metrics.", bullet_style))
    story.append(Paragraph("• <b>Prometheus &rarr; Prometheus Operator:</b> Uses <code>ServiceMonitor</code> CRDs to automatically discover new microservices without manual configuration.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_OUTPUT_PATH}")

if __name__ == '__main__':
    build_pdf()
