# Get Started
[Send telemetry to an OpenTelemetry Collector](https://opentelemetry.io/docs/instrumentation/python/getting-started/#send-telemetry-to-an-opentelemetry-collector)

Please remember that OpenTelemetry doesn't store any data (traces, metrics, logs). It has concept of exporters, where data are exported to user selected data (trace, metric, log) storage (3rd party). 
OpenTelemetry is "middle layer", where you can switch to another storage easily.

## Run Collector + Jaeger docker container
Execute the command below using Ubuntu terminal from the 'otel-collector' folder.
`docker compose up`
http://localhost:16686/

### ZPages for quick collector overview
http://localhost:55679/debug/servicez

## Install Collector exporter
`pip install opentelemetry-exporter-otlp`