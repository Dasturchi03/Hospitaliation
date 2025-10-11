from redis import asyncio as redis


_client: redis.Redis | None = None


def get_client():
    global _client

    _client = redis.Redis(host='localhost', port=6379, db=0, protocol=3)

    return _client


async def aclose_client():
    global _client
    if _client is not None:
        await _client.aclose()
