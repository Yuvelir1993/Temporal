import asyncio
import uuid

from temporalio.client import Client
from temporalio.contrib.opentelemetry import TracingInterceptor

from commons import temporal_server_url, task_queue
from worker import init_runtime_with_telemetry, GreetingWorkflow


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
        id="python-" + str(uuid.uuid4()),
        task_queue=task_queue,
    )
    print(f"Workflow result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
