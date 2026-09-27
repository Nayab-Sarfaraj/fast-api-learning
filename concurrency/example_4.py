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
    result2 = await task2
    print("Task 2 fully completed")
    result1 = await task1
    print("Task 1 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")

# Here, both coroutines are scheduled as Tasks before we await either one. Even though we `await task2` first, `task1` is already running concurrently in the event loop. While `task2` is sleeping, `task1` can complete independently. Therefore, when we eventually `await task1`, it may already be finished, and the total execution time is still approximately 2 seconds.


# Even though `task1` finishes first (after 1 second), `"Task 1 fully completed"` is not printed immediately because `main()` is currently waiting at `await task2`. The event loop allows `task1` to finish in the background, but execution of `main()` remains suspended until `task2` completes. After 2 seconds, `await task2` returns, so `"Task 2 fully completed"` is printed first. Then `await task1` returns immediately because task1 has already finished, and `"Task 1 fully completed"` is printed afterward.
