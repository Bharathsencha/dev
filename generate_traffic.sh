#!/bin/bash
# Traffic generation script to test the DevOps Monitoring Stack

URL="http://localhost:5000"

echo "=========================================================="
echo " Starting traffic generator against $URL"
echo " Press Ctrl+C to stop"
echo "=========================================================="

while true; do
  # Send 5 requests to healthy endpoint
  for i in {1..5}; do
    curl -s "$URL/" > /dev/null
    echo -n "."
  done

  # Send 2 requests to slow endpoint
  for i in {1..2}; do
    curl -s "$URL/slow" > /dev/null
    echo -n "S"
  done

  # Send 1 request to error endpoint
  curl -s "$URL/error" > /dev/null
  echo -n "E"

  sleep 1
done
