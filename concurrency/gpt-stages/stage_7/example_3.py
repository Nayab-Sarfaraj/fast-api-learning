import asyncio

balance = 100
lock = asyncio.Lock()

#  gets lock
#    ↓
# checks balance
#    ↓
# await
#    ↓
# another coroutine gets scheduled
#    ↓
# BUT it tries to acquire the same lock
#    ↓
# it has to wait
#    ↓
# A resumes
#    ↓
# withdraws
#    ↓
# releases lock


async def withdraw(amount):
    global balance

    async with lock:
        if balance >= amount:
            print(f"Enough balance for {amount}")

            await asyncio.sleep(0)

            balance -= amount
            print(f"Withdrew {amount}")
        else:
            print(f"Not enough balance for {amount}")


async def main():
    await asyncio.gather(
        withdraw(80),
        withdraw(80),
    )

    print("Final balance:", balance)


asyncio.run(main())