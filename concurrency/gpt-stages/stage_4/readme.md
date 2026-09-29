https://chatgpt.com/share/6abbcdf4-1090-83ee-a665-735b8096e238

## Stage 4 — Bounded Concurrency

**Problem:** `asyncio.gather()` can run many coroutines concurrently, but sometimes you need to limit how many operations access a resource at once.

### `asyncio.Semaphore(N)`

A semaphore provides **N permits**:

```python
semaphore = asyncio.Semaphore(10)

async with semaphore:
    await make_request()
```

Only **10 coroutines can be inside the protected section simultaneously**.

### Important distinction

```text
gather()     → runs/awaits many coroutines
Semaphore(N) → limits concurrent access to a section/resource
```

A semaphore **does NOT limit how many tasks exist**.

```text
10,000 tasks
     ↓
Semaphore(10)
     ↓
10 active
9,990 waiting
```

### Key pattern

```python
async def worker():
    async with semaphore:
        # bounded operation
        await request()
```

**Rule:** Put the semaphore around the operation you actually want to limit.

### Verified experimentally

```text
Limit 5  → Max active 5
Limit 10 → Max active 10
Limit 20 → Max active 20
```

**Core takeaway:**

> **Bounded concurrency = many tasks can exist, but only N can perform the protected operation concurrently.**
