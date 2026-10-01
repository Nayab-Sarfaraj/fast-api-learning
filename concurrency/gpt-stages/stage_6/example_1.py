import asyncio




async def long_job():
    print("Job started")

    try:
        await asyncio.sleep(10)
        print("Job finished")

    except asyncio.CancelledError:
        print("Job received cancellation")
        raise


async def main():
    task = asyncio.create_task(long_job())

    await asyncio.sleep(2)

    print("Task done?", task.done())
    print("Cancelling job...")

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Main caught cancellation")


asyncio.run(main())

# here so what is happening right we created a task called long_job and it is scheduled on the event loop and then when we  reached sleep(2) inside the main the main is suspeneded for 2 second now event loop pick up the long_job task and it is started and it is suspended for 10 seconds now after 2 seconds the main is resumed and we are cancelling the long_job task and then we are awaiting for the long_job task to finish but since it is cancelled it raises a CancelledError which we are catching in the main function.

# if we reduce the sleep time in the main function to 1 second then the long_job task will not be started yet and it will be cancelled before it is started and it will not raise a CancelledError because it was never started.