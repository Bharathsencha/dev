# DevOps Monitoring Stack Demo (Docker Compose)

A complete, production-ready DevOps monitoring and observability stack built with Docker Compose.

---

## 1. Stack Architecture

- **Prometheus** (`http://localhost:9090`): Time-series metrics scraper and query engine.
- **Grafana** (`http://localhost:3000`): Visual monitoring dashboards (pre-provisioned with Prometheus datasource and dashboard).
- **Node Exporter** (`http://localhost:9100`): Host system hardware and OS metrics (CPU, RAM, Disk).
- **Python Flask Application** (`http://localhost:5000`): Instrumented sample web application exposing `/metrics` via `prometheus_client`.

---

## 2. Repository Structure

```text
.
├── app/
│   ├── app.py                     # Flask application with Prometheus instrumentation
│   ├── Dockerfile                 # Container definition for Flask app
│   └── requirements.txt           # Python dependencies
├── grafana/
│   ├── dashboards/
│   │   └── dashboard.json         # Dashboard copy for automatic provisioning
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboards.yml     # Auto-loads dashboards into Grafana
│       └── datasources/
│           └── datasource.yml     # Pre-configures Prometheus as default datasource
├── dashboard.json                 # Standalone dashboard JSON for manual import/reference
├── docker-compose.yml             # Docker Compose orchestration
├── generate_traffic.sh            # Script to simulate load, latency, and errors
├── Makefile                       # Automation commands
├── prometheus.yml                 # Prometheus scrape target configuration
└── README.md                      # Documentation and quickstart guide
```

---

## 3. Quickstart Guide

### Option 1: Using Make (Recommended)

To start the entire monitoring stack:

```bash
make
```

To run the traffic simulator in another terminal:

```bash
make traffic
```

Other helpful commands:
- `make status` - Check container health
- `make logs`   - View live logs
- `make stop`   - Stop all services
- `make clean`  - Stop and remove all containers and data volumes

---

### Option 2: Using Docker Compose Directly

```bash
docker compose up --build -d
```

To view live container logs:

```bash
docker compose logs -f
```

---

## 4. Service Access and Credentials

| Service | URL | Credentials / Notes |
|---|---|---|
| **Grafana** | [http://localhost:3000](http://localhost:3000) | Username: `admin`<br>Password: `admin` |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | Targets: [http://localhost:9090/targets](http://localhost:9090/targets) |
| **Flask Web App** | [http://localhost:5000](http://localhost:5000) | JSON API endpoints |
| **Flask Metrics** | [http://localhost:5000/metrics](http://localhost:5000/metrics) | Raw Prometheus metrics format |
| **Node Exporter** | [http://localhost:9100/metrics](http://localhost:9100/metrics) | Host system raw metrics |

---

## 5. Viewing the Dashboard in Grafana

1. Open **[http://localhost:3000](http://localhost:3000)** in your web browser.
2. Log in with **`admin`** / **`admin`** (you can skip the password change prompt).
3. Navigate to **Dashboards** > **DevOps Monitoring Stack Demo**.
   - Note: The Prometheus datasource and dashboard are **automatically provisioned** on startup.
   - You can also manually import [`dashboard.json`](dashboard.json) via **Dashboards > New > Import** if desired.

### Dashboard Panels Included:
- **System CPU Usage (%)**: Real-time host CPU utilization via Node Exporter.
- **System Memory Usage (%)**: Memory utilization percentage.
- **Total Processed Requests**: Cumulative count of requests processed.
- **Current Request Rate (req/s)**: Per-second throughput.
- **Error Rate (%)**: Percentage of 4xx/5xx requests.
- **In-Flight Requests**: Active concurrent requests currently executing.
- **Request Rate by Endpoint and Status**: HTTP method, route, and status code breakdown.
- **Latency Percentiles (p95, p50, Average)**: Response time latency curves.
- **HTTP Error Rate over Time**: Visualizes 500/400 errors over time.
- **Target Health Status (UP/DOWN)**: Real-time scrape target status.

---

## 6. Generating Test Traffic

To populate the metrics and generate latency spikes and errors:

```bash
./generate_traffic.sh
```

Or test endpoints manually using `curl`:

- **Fast Success (200 OK):**
  ```bash
  curl http://localhost:5000/
  ```
- **Simulated Slow Response (Latency 0.5s - 2.0s):**
  ```bash
  curl http://localhost:5000/slow
  ```
- **Simulated Error (500 Internal Server Error):**
  ```bash
  curl http://localhost:5000/error
  ```
- **View Raw Metrics Output:**
  ```bash
  curl http://localhost:5000/metrics
  ```

---

## 7. Stopping the Stack

To stop and remove all containers while preserving data volumes:

```bash
make stop
# or: docker compose down
```

To stop containers and reset all Prometheus/Grafana stored metrics:

```bash
make clean
# or: docker compose down -v
```
