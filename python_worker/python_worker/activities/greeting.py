from temporalio import activity

from commons import python_greeting_activity


@activity.defn(name=python_greeting_activity)
async def greeting(name: str) -> str:
    return f"Hello, {name}!"


@activity.defn
async def phrase(word: str) -> str:
    return f"I am a phrase: {word}!"
