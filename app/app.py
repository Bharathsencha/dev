import time
import random
from flask import Flask, Response, request, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Prometheus Metrics Definitions
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests processed by the application',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration/latency in seconds',
    ['method', 'endpoint', 'http_status'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0]
)

REQUEST_ERRORS = Counter(
    'http_request_errors_total',
    'Total number of HTTP error responses (status >= 400)',
    ['method', 'endpoint', 'http_status']
)

IN_PROGRESS_REQUESTS = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests currently being processed',
    ['endpoint']
)

@app.before_request
def before_request():
    request._prometheus_start_time = time.time()
    IN_PROGRESS_REQUESTS.labels(endpoint=request.path).inc()

@app.after_request
def after_request(response):
    if hasattr(request, '_prometheus_start_time'):
        latency = time.time() - request._prometheus_start_time
        status = str(response.status_code)
        endpoint = request.path
        method = request.method

        REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint, http_status=status).observe(latency)
        
        if response.status_code >= 400:
            REQUEST_ERRORS.labels(method=method, endpoint=endpoint, http_status=status).inc()
            
        IN_PROGRESS_REQUESTS.labels(endpoint=endpoint).dec()
    return response

@app.route('/')
def index():
    return jsonify({
        "status": "success",
        "message": "DevOps Monitoring Stack Demo Flask App is running!",
        "endpoints": {
            "/": "Healthy endpoint (fast 200 OK)",
            "/slow": "Simulated slow endpoint (0.5s - 2.0s latency)",
            "/error": "Simulated 500 Internal Server Error",
            "/metrics": "Prometheus metrics endpoint"
        }
    })

@app.route('/slow')
def slow():
    # Simulate a slow request with a delay between 0.5 and 2.0 seconds
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
    return jsonify({
        "status": "success",
        "message": f"Slow response completed after {delay:.2f} seconds",
        "delay_seconds": round(delay, 2)
    })

@app.route('/error')
def error():
    # Simulate an internal server error (500)
    return jsonify({
        "status": "error",
        "error": "InternalServerError",
        "message": "Simulated 500 Internal Server Error for monitoring demonstration"
    }), 500

@app.route('/metrics')
def metrics():
    # Prometheus scrape endpoint
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
