import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
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


# This takes approximately 3 seconds because `time.sleep()` is a synchronous, blocking operation. Unlike `asyncio.sleep()`, it is not awaitable and blocks the entire event loop while it sleeps. Therefore, `task1` blocks the event loop for 1 second, and only after it finishes can `task2` run and block it for another 2 seconds, resulting in a total of approximately 3 seconds.

# If we want to achieve concurrency with `asyncio`, we should avoid blocking operations inside async functions. Instead, we should use their asynchronous/awaitable alternatives, such as `asyncio.sleep()` instead of `time.sleep()`, so the event loop can switch to other scheduled tasks while the operation is waiting.

