import random
import time

from temporalio import activity

from commons import python_greeting_activity


@activity.defn(name=python_greeting_activity)
async def greeting(name: str) -> str:
    time.sleep(random.randint(0, 3))
    return f"Hello, {name}!"


@activity.defn
async def phrase(word: str) -> str:
    time.sleep(random.randint(0, 2))
    return f"I am a phrase: {word}!"


@activity.defn
async def error_activity(word: str):
    time.sleep(random.randint(0, 5))
    raise EnvironmentError("Environment error raised from error_activity with given input " + word)
