import random
import time

from temporalio import activity
from opentelemetry import trace, baggage

tracer = trace.get_tracer(__name__)


@activity.defn
async def rich(rich_input: str) -> str:
    activity.logger.info("[1] Running rich activity with parameter %s" % rich_input)
    with tracer.start_as_current_span("rich_root") as root_span:
        parent_ctx = baggage.set_baggage("rich_root_context", "context value")
        root_span.set_attribute("rich.value", rich_input)
        root_span.add_event("Rich event.")
        activity.logger.info("[2] Running root part of rich activity with parameter %s" % rich_input)

        time.sleep(random.randint(0, 5))

        with tracer.start_as_current_span(
                name="rich_nested", context=parent_ctx
        ) as nested_span:
            activity.logger.info("[1.1] Running rich activity with parameter %s" % rich_input)
            nested_span.set_attribute("rich.nested.value", rich_input)
            nested_span.add_event("Rich nested event.")
            activity.logger.info("[2.1] Running nested part of rich activity with parameter %s" % rich_input)

    return f"Rich activity: {rich_input}!"
