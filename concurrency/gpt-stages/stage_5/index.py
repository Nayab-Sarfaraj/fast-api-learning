import asyncio


async def main():
    queue = asyncio.Queue()

    await queue.put("job-1")
    await queue.put("job-2")
    await queue.put("job-3")

    print("Queue size:", queue.qsize())

    job = await queue.get()
    print("Got:", job)

    queue.task_done()

    job = await queue.get()
    print("Got:", job)

    queue.task_done()

    job = await queue.get()
   
    print("Got:", job)

    queue.task_done()

    await queue.join()

    print("All jobs completed")


asyncio.run(main())