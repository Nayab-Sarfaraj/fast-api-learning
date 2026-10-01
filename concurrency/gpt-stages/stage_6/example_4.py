import asyncio


async def process_job(job):
    try:
        if job == "fail":
            raise ValueError("job failed")

        if job == "slow":
            await asyncio.sleep(10)

        if job == "worker-crash":
            raise RuntimeError("worker crashed")
        if job == "job-5":
            raise RuntimeError("job-5 crashed")

        await asyncio.sleep(1)

    except asyncio.CancelledError:
        print(f"{job}: cancellation received")
        raise


async def worker(worker_id, queue):
    while True:
        job = await queue.get()

        try:
            async with asyncio.timeout(3):
                await process_job(job)
                print(f"Worker {worker_id}: {job} completed")

        except asyncio.TimeoutError:
            print(f"Worker {worker_id}: {job} timed out")
        except ValueError as e:
            print(f"Worker {worker_id}: {job} failed with error: {e}")
        except RuntimeError as e:
            print(f"Worker {worker_id}: {job} crashed with error: {e}")

        finally:
            queue.task_done()


async def producer(queue):
    try:
        for i in range(20):
            await queue.put(f"job-{i}")
            print(f"Added job-{i}")
            await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        print("Producer cancelled")
        raise


async def main():
    queue = asyncio.Queue()

    workers = [
        asyncio.create_task(worker(i, queue))
        for i in range(2)
    ]

    producer_task = asyncio.create_task(producer(queue))

    await asyncio.sleep(2)

    print("SHUTDOWN SIGNAL")

    producer_task.cancel()

    try:
        await producer_task
    except asyncio.CancelledError:
        pass

    await queue.join()

    for w in workers:
        w.cancel()

    await asyncio.gather(*workers, return_exceptions=True)

    print("Shutdown complete")
    for i, w in enumerate(workers):
        print(f"Worker {i}: done={w.done()}, cancelled={w.cancelled()}")

    for w in workers:
        if w.done() and not w.cancelled():
            print("exception:", w.exception())


asyncio.run(main())



# here we demonstrater graceful shutdown of the producer and workers. The producer is cancelled after 2 seconds, and the workers continue to process any remaining jobs in the queue before shutting down.