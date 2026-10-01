import asyncio



# 2 seconds elapsed
#        ↓
# timeout triggers cancellation
#        ↓
# long_job receives CancelledError
#        ↓
# long_job is stopped
#        ↓
# timeout context manager catches that cancellation
#        ↓
# converts it to TimeoutError
#        ↓
# your except TimeoutError runs

async def long_job():
    try:
        print("Job started")

        await asyncio.sleep(10)

        print("Job finished")
    except asyncio.CancelledError:
        print("Job cancelled")
        print("Cleaning up...")
        raise





async def main():
    try:
        async with asyncio.timeout(2):
            await long_job()

    except asyncio.TimeoutError:
        print("Job timed out")


asyncio.run(main())