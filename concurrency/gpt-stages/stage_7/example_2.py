import asyncio

balance = 100


async def withdraw(amount):
    global balance

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

# here the see the output as -60 but ideally we should see withdraw 80 and Not enough balance for 80 so what happened two co routine were schedules first one executted then it reached the await statement and it got suspened then second one was pick and it see balance as 100 so it executed the if block but then it is suspened since it encountered the await statement then control switeched back to the first one which did the minus operation then control came to second co routine which also did minus 

