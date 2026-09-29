import asyncio
import random

semaphore = asyncio.Semaphore(3)


# async def worker(i):
#     async with semaphore:
#         n=random.randint(1,4)
#         print(f"Task {i} START WILL TAKE {n} SEC")
#         await asyncio.sleep(n)
#         print(f"Task {i} END")

active = 0

async def worker(i):
    global active

    async with semaphore:
        active += 1
        print(f"Task {i} START | Active: {active}")

        n = random.randint(1, 4)
        await asyncio.sleep(n)

        active -= 1
        print(f"Task {i} END | Active: {active}")


async def main():
    await asyncio.gather(
        *(worker(i) for i in range(10))
    )


asyncio.run(main())