import asyncio


async def worker(queue):
    while True:
        job = await queue.get()

        print(f"Worker started {job}")

        await asyncio.sleep(1)

        print(f"Worker finished {job}")

        queue.task_done()


async def main():
    queue = asyncio.Queue()

    worker_task = asyncio.create_task(worker(queue))

    for i in range(5):
        await queue.put(f"job-{i}")

    await queue.join()

    worker_task.cancel()


asyncio.run(main())