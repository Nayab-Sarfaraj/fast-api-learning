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
# so here we have created a task why because if we create a couroutine object instead we will not be able to add the items in the queue because worker will run infinitely while main remains suspended and it will not be able to add the items in the queue so we need to create a task for the worker so that it can run in the background and main can add the items in the queue.

# when we create a task as a worker it is schedule on the event loop and main continues to run as soon as reach the await queue.put the main will be suspened and event loop will pick the woorker task and that willl be get suspended for next 1 second and then main will be resumed and it will add the next item in the queue and then main will be suspened again and event loop will pick the worker task and that will be get suspended for next 1 second and then main will be resumed and it will add the next item in the queue and this process will continue until all the items are added in the queue.

# what will happen if the queue is empty . -> here is the intresting part when in the worker we will do get on the queue and if the queue is empty then the worker will be suspended until the next item is added in the queue and then it will be resumed and it will process the item and then it will be suspended again until the next item is added in the queue.