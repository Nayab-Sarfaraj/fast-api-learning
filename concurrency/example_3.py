import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    print("Task 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")


# Here, both coroutines are explicitly scheduled as Tasks using `asyncio.create_task()`. This allows the event loop to run them concurrently. When `task1` reaches `await asyncio.sleep(1)`, the event loop can switch to `task2` instead of waiting for `task1` to finish. Therefore, both operations overlap and the total execution time is approximately 2 seconds rather than 3 seconds.
