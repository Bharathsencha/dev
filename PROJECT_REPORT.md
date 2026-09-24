# Project Report: Full-Stack DevOps Observability & Monitoring Pipeline

---

## 1. Executive Summary

In modern cloud computing and distributed microservices architectures, ensuring application reliability, uptime, and performance requires real-time observability. Traditional log-based debugging is reactive and insufficient for high-scale systems. 

This project implements an end-to-end, containerized **DevOps Monitoring and Observability Pipeline** using **Docker Compose**, **Prometheus**, **Grafana**, **Node Exporter**, and a custom-instrumented **Python Flask application**. The system collects, stores, visualizes, and analyzes both **system-level infrastructure metrics** (CPU, RAM) and **application-level performance metrics** (request rate, latency percentiles, and error rates) in real-time.

---

## 2. Project Objectives

1. **Infrastructure Observability**: Collect low-level host metrics (CPU utilization, Memory consumption, Disk I/O) without modifying the host OS.
2. **Application Performance Monitoring (APM)**: Instrument a Python web microservice using the `prometheus_client` SDK to track Google's **Four Golden Signals of Monitoring** (Latency, Traffic, Errors, and Saturation).
3. **Automated Provisioning**: Implement zero-configuration Grafana datasources and pre-loaded interactive dashboards on startup.
4. **Reproducible Orchestration**: Package the entire multi-service ecosystem into isolated Docker containers orchestrated via Docker Compose and an automated `Makefile`.
5. **Dynamic Traffic Simulation**: Build an automated stress and traffic simulation generator to validate real-time latency distributions and error thresholds.

---

## 3. System Architecture & Component Workflow

### Architecture Diagram

```
                     +-----------------------------------+
                     |      Host Machine (Linux Mint)    |
                     +-----------------+-----------------+
                                       |
                   Reads /proc, /sys   |
                                       v
                     +-----------------------------------+
                     |  Node Exporter (Port 9100)        |
                     |  - Host CPU Usage (%)             |
                     |  - Host Memory Usage (%)          |
                     +-----------------+-----------------+
                                       |
                                       | (HTTP Scrape every 5s)
                                       v
+------------------------+   HTTP Scrape   +-----------------------------------+
| Python Flask App       | <============== | Prometheus TSDB (Port 9090)       |
| (Port 5000)            |   (every 5s)    | - Time-Series Storage             |
| - Custom /metrics      |                 | - PromQL Engine                   |
| - /, /slow, /error     |                 +-----------------+-----------------+
+------------------------+                                   |
           ▲                                                 | (PromQL Queries)
           |                                                 v
           | (Simulated Traffic)           +-----------------------------------+
+------------------------+                 | Grafana Dashboard (Port 3000)     |
| generate_traffic.sh    |                 | - System CPU & RAM Panels         |
| (Traffic Generator)    |                 | - Request Rate & Latency (p95)    |
+------------------------+                 | - Real-time Error Rate (%)        |
                                           +-----------------------------------+
```

### Component Interaction Steps:
1. **Metric Emission**: The Flask application intercepts every incoming HTTP request, measures execution duration, and increments counters/histograms.
2. **Infrastructure Metric Gathering**: Node Exporter reads host kernel metrics from `/proc` and `/sys` volumes mounted into the container.
3. **Metric Scraping & Storage**: Prometheus acts as a central collector, polling (`pull` model) all targets every 5 seconds and persisting timestamped series in its internal TSDB.
4. **Visualization & Analytics**: Grafana queries Prometheus via PromQL and presents interactive graphs and gauges.
5. **Traffic Testing**: The bash test script sends periodic traffic across healthy, slow, and error routes to generate dynamic monitoring data.

---

## 4. Comprehensive File-by-File Breakdown

### 4.1. `docker-compose.yml` (Service Orchestration)
- **Role**: Defines the deployment specification for all 4 microservices.
- **Key Configurations**:
  - **Networks**: Creates a dedicated bridge network (`monitoring`) allowing DNS resolution between containers (e.g. `http://prometheus:9090`).
  - **Volumes**: Persistent storage for Prometheus (`prometheus_data`) and Grafana (`grafana_data`), preventing data loss across restarts.
  - **Volume Mounts**: Mounts `/proc` and `/sys` read-only to Node Exporter for system-level host visibility.
  - **Auto-restart**: `restart: unless-stopped` ensures container self-healing upon process crashes.

### 4.2. `prometheus.yml` (Metrics Scraper Configuration)
- **Role**: Instructs Prometheus which targets to monitor and the polling frequency.
- **Key Configurations**:
  - `scrape_interval: 5s` - Fast polling interval suitable for development and real-time monitoring demos.
  - `job_name: 'flask_app'` - Scrapes `flask-app:5000` at `metrics_path: '/metrics'`.
  - `job_name: 'node_exporter'` - Scrapes `node-exporter:9100`.
  - `job_name: 'prometheus'` - Scrapes Prometheus's own internal health metrics.

### 4.3. `app/app.py` (Instrumented Web Application)
- **Role**: Core application exposing business endpoints and instrumented metrics.
- **Prometheus Metrics Defined**:
  1. `http_requests_total` (`Counter`): Dimensions: `[method, endpoint, http_status]`.
  2. `http_request_duration_seconds` (`Histogram`): Buckets: `[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]`. Tracks latency percentiles.
  3. `http_request_errors_total` (`Counter`): Tracks 4xx and 5xx failure counts.
  4. `http_requests_in_progress` (`Gauge`): Tracks active concurrent requests.
- **Application Endpoints**:
  - `GET /`: Fast 200 OK root endpoint.
  - `GET /slow`: Injects a non-blocking random sleep (`0.5s - 2.0s`) to simulate database or downstream I/O latency.
  - `GET /error`: Returns HTTP 500 status to simulate unhandled server exceptions.
  - `GET /metrics`: Standard Prometheus-formatted text exposition endpoint.

### 4.4. `app/Dockerfile` & `app/requirements.txt`
- **Role**: Container build blueprint for the Flask app.
- **Design Choices**:
  - Uses `python:3.11-slim` base image for minimal attack surface and lightweight image size (~150MB).
  - Configures `PYTHONUNBUFFERED=1` to ensure application logs flush directly to stdout/docker logs.

### 4.5. `dashboard.json` & Grafana Provisioning (`grafana/provisioning/`)
- **Role**: Implements "Infrastructure as Code" (IaC) for monitoring dashboards.
- **Datasource Provisioning (`datasource.yml`)**: Automatically connects Grafana to `http://prometheus:9090` without manual UI configuration.
- **Dashboard Provisioning (`dashboards.yml`)**: Pre-loads `dashboard.json` into Grafana's default folder on container startup.
- **Panels Configured**:
  1. **CPU Usage (%)**: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)`
  2. **Memory Usage (%)**: `(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100`
  3. **Request Throughput (req/s)**: `sum(rate(http_requests_total[1m])) by (endpoint, http_status)`
  4. **95th Percentile Latency (p95)**: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le, endpoint))`
  5. **50th Percentile Latency (Median)**: `histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[1m])) by (le, endpoint))`
  6. **Error Rate (%)**: `(sum(rate(http_request_errors_total[1m])) / sum(rate(http_requests_total[1m]))) * 100`
  7. **Active In-Flight Requests**: `sum(http_requests_in_progress)`
  8. **Scrape Target Health (UP/DOWN)**: `up`

### 4.6. `generate_traffic.sh` (Traffic Generator)
- **Role**: Test harness to simulate live production traffic.
- **Traffic Pattern**: Loops indefinitely, issuing 5 fast `/` requests, 2 slow `/slow` requests, and 1 failing `/error` request every second to generate varied data in Prometheus.

### 4.7. `Makefile` (Developer Automation)
- **Role**: Unified CLI interface for project lifecycle management.
- **Commands**:
  - `make` / `make up`: Builds and launches all containers in detached mode.
  - `make traffic`: Starts the traffic generator.
  - `make status`: Checks container health and port mappings.
  - `make logs`: Follows aggregate log streams.
  - `make stop`: Stops all running services.
  - `make clean`: Tears down containers and purges storage volumes.

---

## 5. Key DevOps Concepts Demonstrated

### 1. The Four Golden Signals
- **Latency**: Time taken to service a request. Differentiated into p50 (median), average, and p95 (tail latency).
- **Traffic**: A measure of demand on the system (HTTP requests per second).
- **Errors**: The rate of requests that fail explicitly (HTTP 500).
- **Saturation**: How "full" the service and host resources are (Host CPU % and Memory %).

### 2. Pull vs. Push Architecture
Prometheus operates on a **Pull** model:
- The monitoring system maintains control over scrape frequency and network load.
- If a client experiences a traffic spike, it does not overload the monitoring backend with pushed metrics.
- Centralized target health detection: If a target cannot be scraped, Prometheus immediately marks `up == 0`.

### 3. Histogram Quantiles (p95 & p99)
Averages can hide severe performance degradation (e.g., 99 fast requests at 1ms + 1 slow request at 10s gives an average of 100ms, hiding the outage). **Histograms** group requests into buckets, allowing exact calculation of the **95th percentile (p95)** latency.

---

## 6. How to Run & Verify

1. **Start the pipeline:**
   ```bash
   make
   ```
2. **Verify endpoints:**
   - Grafana: `http://localhost:3000` (User: `admin`, Pass: `admin`)
   - Prometheus Targets: `http://localhost:9090/targets`
   - Flask API: `http://localhost:5000`
   - Metrics Endpoint: `http://localhost:5000/metrics`
3. **Simulate live traffic:**
   ```bash
   make traffic
   ```
4. **Shutdown:**
   ```bash
   make stop
   ```

---

## 7. Future Scope: Transition to Kubernetes (K8s)

For multi-node, large-scale enterprise deployments, this stack translates directly into Kubernetes:
1. **Flask Microservice**: Deployed as a Kubernetes `Deployment` with 3+ replicas and a `HorizontalPodAutoscaler (HPA)` scaling pods dynamically on CPU or request rate.
2. **Node Exporter**: Deployed as a Kubernetes `DaemonSet` ensuring 1 exporter pod per physical/virtual worker node.
3. **Prometheus & Grafana**: Deployed using the standard **`kube-prometheus-stack`** Helm Chart, utilizing `ServiceMonitor` Custom Resource Definitions (CRDs) for dynamic auto-discovery of microservices.

---

## 8. Conclusion

This project successfully demonstrates a production-standard observability architecture. By combining system metrics from Node Exporter with custom application metrics from a Flask service into Prometheus and Grafana, it provides 360-degree visibility into application health, performance, and resource utilization.
