import asyncio

counter = 0


async def increment():
    global counter

    for _ in range(1000):
        current = counter
        await asyncio.sleep(0)
        counter = current + 1


async def main():
    tasks = [increment() for _ in range(100)]

    await asyncio.gather(*tasks)

    print("Expected:", 100_000)
    print("Actual:", counter)


asyncio.run(main())
