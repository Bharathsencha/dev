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
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "DevOps Monitoring Stack — Complete Technical & Concepts Guide")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "DevOps Observability: Prometheus, PromQL, Grafana, Node Exporter, Flask")
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
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=12
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=2.5
    )

    table_header_style = ParagraphStyle(
        'TH_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TC_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("DevOps Monitoring Stack: Technical Guide", title_style))
    story.append(Paragraph("Full Architecture, File Breakdown, Grafana, PromQL vs SQL & Observability Concepts", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=10))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary & Purpose", h1_style))
    story.append(Paragraph(
        "This project implements an end-to-end <b>DevOps Observability and Monitoring Pipeline</b> using "
        "<b>Docker Compose</b>. It solves the critical problem of blind spots in production microservices by collecting, "
        "storing, querying, and visualizing real-time <b>infrastructure health</b> (CPU, Memory) and "
        "<b>application performance</b> (throughput, latency percentiles, and error rates) through "
        "<b>Prometheus</b> and <b>Grafana</b>.",
        body_style
    ))

    # 2. What Does What (Core Components)
    story.append(Paragraph("2. Stack Components: What Does What?", h1_style))
    comp_data = [
        [Paragraph("Component", table_header_style), Paragraph("Port", table_header_style), Paragraph("What It Is & Core Responsibility", table_header_style)],
        [Paragraph("<b>Flask Web App</b>", table_cell_style), Paragraph("5000", table_cell_style), Paragraph("Sample production microservice instrumented with <code>prometheus_client</code>. Exposes business routes and <code>/metrics</code>.", table_cell_style)],
        [Paragraph("<b>Prometheus</b>", table_cell_style), Paragraph("9090", table_cell_style), Paragraph("Time-Series Database (TSDB) & metrics scraper. Pulls metrics every 5s from Flask App and Node Exporter.", table_cell_style)],
        [Paragraph("<b>Grafana</b>", table_cell_style), Paragraph("3000", table_cell_style), Paragraph("Analytics & visualization UI. Queries Prometheus using PromQL and renders interactive graphs & gauges.", table_cell_style)],
        [Paragraph("<b>Node Exporter</b>", table_cell_style), Paragraph("9100", table_cell_style), Paragraph("Hardware/OS metrics agent. Gathers host CPU, RAM, and disk stats directly from Linux kernel files (<code>/proc</code>).", table_cell_style)],
        [Paragraph("<b>Docker Compose</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Multi-container orchestration tool. Connects all 4 services onto an isolated bridge network with volumes.", table_cell_style)],
        [Paragraph("<b>Makefile</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("CLI command automation. Allows 1-command startup (<code>make</code>), traffic simulation, and clean shutdown.", table_cell_style)]
    ]
    t_comp = Table(comp_data, colWidths=[100, 45, 359])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    # 3. What is Grafana & What is PromQL (That "SQL" of Metrics)
    story.append(Paragraph("3. Deep-Dive: What is Grafana & What is PromQL?", h1_style))
    story.append(Paragraph("<b>What is Grafana?</b>", h2_style))
    story.append(Paragraph(
        "Grafana is the industry-standard <b>data visualization and dashboarding platform</b>. "
        "It does not store data itself; instead, it connects to data sources (like Prometheus, Elasticsearch, or MySQL) "
        "and executes queries to transform raw metrics into real-time graphs, heatmaps, gauges, and alerts.",
        body_style
    ))
    
    story.append(Paragraph("<b>What is PromQL? (Prometheus Query Language vs SQL)</b>", h2_style))
    story.append(Paragraph(
        "PromQL is the query language designed specifically for <b>Time-Series Data</b>. Unlike standard <b>SQL</b> "
        "(which queries relational rows and tables), PromQL queries timestamped numerical data points over time windows.",
        body_style
    ))

    sql_vs_promql = [
        [Paragraph("Feature", table_header_style), Paragraph("Traditional SQL (e.g., PostgreSQL, MySQL)", table_header_style), Paragraph("PromQL (Prometheus Query Language)", table_header_style)],
        [Paragraph("<b>Data Model</b>", table_cell_style), Paragraph("Relational tables (Rows, Columns, Foreign Keys)", table_cell_style), Paragraph("Time-Series streams (Metric Name + Labels + Timestamp + Value)", table_cell_style)],
        [Paragraph("<b>Primary Use Case</b>", table_cell_style), Paragraph("Transactional business records (Users, Orders, Payments)", table_cell_style), Paragraph("Real-time system telemetry, rate of change, durations, CPU%", table_cell_style)],
        [Paragraph("<b>Time Functions</b>", table_cell_style), Paragraph("Complex <code>GROUP BY date_trunc(...)</code> queries", table_cell_style), Paragraph("Built-in instant time-window operators like <code>[1m]</code>, <code>[5m]</code>, <code>rate()</code>", table_cell_style)],
        [Paragraph("<b>Example Query</b>", table_cell_style), Paragraph("<code>SELECT count(*) FROM requests WHERE status=500;</code>", table_cell_style), Paragraph("<code>sum(rate(http_requests_total{http_status=\"500\"}[1m]))</code>", table_cell_style)]
    ]
    t_sql = Table(sql_vs_promql, colWidths=[85, 205, 214])
    t_sql.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_sql)
    story.append(Spacer(1, 6))

    # PromQL Queries Used in This Project
    story.append(Paragraph("<b>Exact PromQL Queries Used in Our Project:</b>", h2_style))
    story.append(Paragraph("• <b>Host CPU %:</b> <code>100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[1m])) * 100)</code> (Calculates non-idle CPU time)", bullet_style))
    story.append(Paragraph("• <b>Host Memory %:</b> <code>(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100</code> (Percentage of RAM in use)", bullet_style))
    story.append(Paragraph("• <b>Throughput (req/s):</b> <code>sum(rate(http_requests_total[1m])) by (endpoint, http_status)</code> (Per-second request rate by route)", bullet_style))
    story.append(Paragraph("• <b>p95 Latency:</b> <code>histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le, endpoint))</code>", bullet_style))
    story.append(Paragraph("• <b>Error Rate %:</b> <code>(sum(rate(http_request_errors_total[1m])) / sum(rate(http_requests_total[1m]))) * 100</code>", bullet_style))

    story.append(PageBreak())

    # 4. Flask Application Endpoints
    story.append(Paragraph("4. The Flask Application: Endpoints & Instrumentation", h1_style))
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
    t_flask = Table(flask_endpoints, colWidths=[85, 75, 344])
    t_flask.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_flask)
    story.append(Spacer(1, 6))

    # Metric Types
    story.append(Paragraph("<b>The 3 Metric Types Implemented in Our Flask App:</b>", h2_style))
    story.append(Paragraph("1. <b>Counter (<code>http_requests_total</code>):</b> Cumulative integer that only increases. Used to measure total traffic and error counts.", bullet_style))
    story.append(Paragraph("2. <b>Histogram (<code>http_request_duration_seconds</code>):</b> Samples response times into configurable duration buckets to calculate percentiles (p50, p95, p99).", bullet_style))
    story.append(Paragraph("3. <b>Gauge (<code>http_requests_in_progress</code>):</b> Numerical value that goes up and down. Tracks real-time active concurrency.", bullet_style))

    # 5. File Structure Map
    story.append(Paragraph("5. Project File Structure: Where is What?", h1_style))
    file_map_data = [
        [Paragraph("File / Folder", table_header_style), Paragraph("Purpose & What It Contains", table_header_style)],
        [Paragraph("<code>app/app.py</code>", table_cell_style), Paragraph("Flask web server code with Prometheus instrumentation middleware.", table_cell_style)],
        [Paragraph("<code>app/Dockerfile</code>", table_cell_style), Paragraph("Instructions to build the lightweight Python 3.11 container image.", table_cell_style)],
        [Paragraph("<code>app/requirements.txt</code>", table_cell_style), Paragraph("Python library dependencies (<code>Flask</code>, <code>prometheus_client</code>).", table_cell_style)],
        [Paragraph("<code>docker-compose.yml</code>", table_cell_style), Paragraph("Docker Compose blueprint: wires all 4 containers, ports, network, and storage.", table_cell_style)],
        [Paragraph("<code>prometheus.yml</code>", table_cell_style), Paragraph("Prometheus scrape configuration (defines 5s scrape jobs for Flask & Node Exporter).", table_cell_style)],
        [Paragraph("<code>dashboard.json</code>", table_cell_style), Paragraph("Complete Grafana dashboard JSON definition with all CPU, RAM, Latency, and Error panels.", table_cell_style)],
        [Paragraph("<code>grafana/provisioning/</code>", table_cell_style), Paragraph("Zero-config files: automatically connects Prometheus datasource & loads dashboard.", table_cell_style)],
        [Paragraph("<code>generate_traffic.sh</code>", table_cell_style), Paragraph("Bash load generator script simulating fast, slow, and error requests.", table_cell_style)],
        [Paragraph("<code>Makefile</code>", table_cell_style), Paragraph("Automation CLI interface: <code>make</code>, <code>make traffic</code>, <code>make stop</code>, <code>make pdf</code>.", table_cell_style)]
    ]
    t_files = Table(file_map_data, colWidths=[140, 364])
    t_files.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_files)
    story.append(Spacer(1, 6))

    # 6. Step by Step Guide
    story.append(Paragraph("6. Simple Step-by-Step Execution Guide", h1_style))
    steps_data = [
        [Paragraph("Step", table_header_style), Paragraph("Command / Action", table_header_style), Paragraph("Expected Result", table_header_style)],
        [Paragraph("<b>1. Start Stack</b>", table_cell_style), Paragraph("<code>make</code>", table_cell_style), Paragraph("Builds and starts all 4 services in the background.", table_cell_style)],
        [Paragraph("<b>2. Open Grafana</b>", table_cell_style), Paragraph("<code>http://localhost:3000</code><br/>(User: <code>admin</code> / <code>admin</code>)", table_cell_style), Paragraph("Pre-provisioned dashboard displays live real-time metrics.", table_cell_style)],
        [Paragraph("<b>3. Generate Load</b>", table_cell_style), Paragraph("<code>make traffic</code>", table_cell_style), Paragraph("Sends continuous traffic with latency & error spikes.", table_cell_style)],
        [Paragraph("<b>4. Check Status</b>", table_cell_style), Paragraph("<code>make status</code>", table_cell_style), Paragraph("Displays container health and port bindings.", table_cell_style)],
        [Paragraph("<b>5. Stop Stack</b>", table_cell_style), Paragraph("<code>make stop</code>", table_cell_style), Paragraph("Stops and removes all containers cleanly.", table_cell_style)]
    ]
    t_steps = Table(steps_data, colWidths=[70, 160, 274])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_steps)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {PDF_OUTPUT_PATH}")

if __name__ == '__main__':
    build_pdf()
