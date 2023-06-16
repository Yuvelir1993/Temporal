import asyncio
from datetime import timedelta
from typing import List

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from temporalio import workflow
from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor
from temporalio.runtime import OpenTelemetryConfig, Runtime, TelemetryConfig
from temporalio.worker import Worker

from activities.greeting import greeting, phrase
from activities.rich import rich
from commons import otel_collector_url, temporal_server_url, task_queue


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> List[str]:
        results = await asyncio.gather(
            workflow.execute_activity(
                greeting, name, start_to_close_timeout=timedelta(seconds=10)
            ),
            workflow.execute_activity(
                phrase, name, start_to_close_timeout=timedelta(seconds=5)
            )
        )

        await workflow.execute_activity(
            phrase, "Second phrase", start_to_close_timeout=timedelta(seconds=10)
        )

        await workflow.execute_activity(
            rich, "Rich phrase", start_to_close_timeout=timedelta(seconds=10)
        )

        return list(sorted(results))


interrupt_event = asyncio.Event()


def init_runtime_with_telemetry() -> Runtime:
    # Setup global tracer for workflow traces
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "python-worker-service"}))
    exporter = OTLPSpanExporter(endpoint=otel_collector_url, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    # Setup SDK metrics to OTel endpoint
    return Runtime(
        telemetry=TelemetryConfig(
            metrics=OpenTelemetryConfig(url=otel_collector_url)
        )
    )


async def main():
    runtime = init_runtime_with_telemetry()

    # Connect client
    client = await Client.connect(
        temporal_server_url,
        # Use OpenTelemetry interceptor
        interceptors=[TracingInterceptor()],
        runtime=runtime,
    )

    # Run a worker for the workflow
    async with Worker(
            client,
            task_queue=task_queue,
            workflows=[GreetingWorkflow],
            activities=[greeting, phrase, rich],
    ):
        # Wait until interrupted
        print("Worker started, ctrl+c to exit")
        await interrupt_event.wait()
        print("Shutting down")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)
    try:
        asyncio.set_event_loop(loop)
        loop.set_debug(True)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        queue.task_done()
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        try:
            queue.task_done()
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            asyncio.set_event_loop(None)
            loop.close()
