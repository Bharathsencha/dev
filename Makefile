.DEFAULT_GOAL := up

.PHONY: up start stop down restart logs status traffic clean help

## Start the entire monitoring stack (Default)
up: start

start:
	@echo "Starting DevOps Monitoring Stack..."
	docker compose up --build -d
	@echo "\nAll services started successfully!"
	@echo "--------------------------------------------------------"
	@echo "Grafana:       http://localhost:3000 (admin / admin)"
	@echo "Prometheus:    http://localhost:9090/targets"
	@echo "Flask App:     http://localhost:5000"
	@echo "Metrics:       http://localhost:5000/metrics"
	@echo "Node Exporter: http://localhost:9100/metrics"
	@echo "--------------------------------------------------------"
	@echo "Tip: Run 'make traffic' in another terminal to generate live data!"

## Generate live simulated traffic
traffic:
	@echo "Running traffic generator..."
	@./generate_traffic.sh

## Generate PDF report in Downloads
pdf:
	@python3 generate_pdf_report.py

## View running container status
status:
	docker compose ps

## View live logs
logs:
	docker compose logs -f

## Stop the monitoring stack
stop: down

down:
	@echo "Stopping DevOps Monitoring Stack..."
	docker compose down

## Restart the stack
restart: down up

## Stop and clean all containers and volumes
clean:
	@echo "Cleaning up all containers and persistent volumes..."
	docker compose down -v --remove-orphans

## Show available Makefile commands
help:
	@echo "Available commands:"
	@echo "  make         - Build and start all services in the background"
	@echo "  make traffic - Run simulated traffic to populate dashboard"
	@echo "  make status  - Check status of all containers"
	@echo "  make logs    - Tail live logs from all containers"
	@echo "  make stop    - Stop all services"
	@echo "  make restart - Restart all services"
	@echo "  make clean   - Stop and wipe volumes/data"
