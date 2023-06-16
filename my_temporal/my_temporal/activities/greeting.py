from temporalio import activity


@activity.defn
async def greeting(name: str) -> str:
    return f"Hello, {name}!"


@activity.defn
async def phrase(word: str) -> str:
    return f"I am a phrase: {word}!"
