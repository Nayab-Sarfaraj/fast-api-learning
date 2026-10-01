import asyncio
import random


async def worker(queue, worker_id):
    while True:
        job = await queue.get()

        print(f"Worker {worker_id} processing {job}")

        # await asyncio.sleep(1)
        await asyncio.sleep(random.uniform(0.1, 2))

        print(f"Worker {worker_id} finished {job}")

        queue.task_done()

async def main():
    queue = asyncio.Queue()

    start = asyncio.get_running_loop().time()

    worker_tasks = [
        asyncio.create_task(worker(queue, i))
        for i in range(5)
    ]

    for i in range(100):
        await queue.put(f"job-{i}")

    await queue.join()

    elapsed = asyncio.get_running_loop().time() - start
    print(f"Total time: {elapsed:.2f}s")

    for task in worker_tasks:
        task.cancel()


asyncio.run(main())