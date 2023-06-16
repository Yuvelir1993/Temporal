import asyncio
import uuid

from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor

from my_temporal.worker import init_runtime_with_telemetry, GreetingWorkflow

temporal_server_url = "localhost:7233"


async def main():
    runtime = init_runtime_with_telemetry()

    # Connect client
    client = await Client.connect(
        temporal_server_url,
        # Use OpenTelemetry interceptor
        interceptors=[TracingInterceptor()],
        runtime=runtime,
    )

    # Run workflow
    result = await client.execute_workflow(
        GreetingWorkflow.run,
        "Temporal",
        id=str(uuid.uuid4()),
        task_queue="open_telemetry-task-queue",
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
