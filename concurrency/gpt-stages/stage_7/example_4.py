import asyncio

lock = asyncio.Lock()


async def worker(name):
    print(f"{name}: waiting for lock")

    async with lock:
        print(f"{name}: got lock")

        await asyncio.sleep(2)

        print(f"{name}: releasing lock")


async def main():
    await asyncio.gather(
        worker("A"),
        worker("B"),
        worker("C"),
    )


asyncio.run(main())