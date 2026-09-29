import asyncio
import random
import time

active = 0
max_active = 0


async def worker(i, semaphore):
    global active, max_active

    async with semaphore:
        active += 1
        max_active = max(max_active, active)

        duration = random.uniform(0.5, 1.5)
        await asyncio.sleep(duration)

        active -= 1


async def run(limit):
    global active, max_active

    active = 0
    max_active = 0

    semaphore = asyncio.Semaphore(limit)

    start = time.perf_counter()

    await asyncio.gather(
        *(worker(i, semaphore) for i in range(100))
    )

    elapsed = time.perf_counter() - start

    print(
        f"Limit={limit} | "
        f"Time={elapsed:.2f}s | "
        f"Max active={max_active}"
    )


async def main():
    await run(5)
    await run(10)
    await run(20)


asyncio.run(main())