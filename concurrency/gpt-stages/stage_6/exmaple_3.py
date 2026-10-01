import asyncio

async def process_job(job):
    try:
        if job == "fail":
            raise ValueError("job failed")
    
        if job == "slow":
            await asyncio.sleep(10)
        if job == "worker-crash":
            raise RuntimeError("worker crashed")
        else:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        print(f"{job}: cancellation received")
        raise

async def worker(worker_id,queue):
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

        finally:
            queue.task_done()


async def main():
    queue = asyncio.Queue()

    # Create worker tasks
    workers = [
        asyncio.create_task(worker(i, queue))
        for i in range(2)
    ]

    # Enqueue jobs
    jobs = ["job-1", "worker-crash","slow", "job-2", "fail" , "slow", "job-3"]
    for job in jobs:
        await queue.put(job)

    # Wait until all jobs are processed
    await queue.join()

    # Cancel workers
    for w in workers:
        w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    for i, w in enumerate(workers):
        print(f"Worker {i}: done={w.done()}, cancelled={w.cancelled()}")

    for w in workers:
        if w.done() and not w.cancelled():
            print("exception:", w.exception())



asyncio.run(main())


