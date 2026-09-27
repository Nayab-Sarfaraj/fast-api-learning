import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = fetch_data(1)  # Could be awaited directly
    task2 = fetch_data(2)  # Could be awaited directly
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

# here even tho we are using the co routine this is takes same as the example 1 because when we run the co routine object it schedule it on event loop and it also runs it till completion so other operations are blocked till this coroutine completes

# Here, even though we are using coroutine objects, this takes the same amount of time as Example 1 because `task1` and `task2` are not scheduled independently. When we `await task1`, the event loop runs it to completion before moving on to `task2`. Therefore, the operations execute sequentially instead of concurrently.

