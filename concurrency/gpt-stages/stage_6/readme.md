https://chatgpt.com/share/6abe3031-2918-83ee-a41d-6b73a67028b0

# Stage 6 — Failures, Timeouts & Cancellation

## 1. Task Cancellation

A task can be cancelled using:

```python
task.cancel()
```

`cancel()` does not instantly kill the task. It requests cancellation.

If the coroutine is still running/suspended at an `await`, Python raises:

```python
asyncio.CancelledError
```

inside that coroutine.

```python
async def job():
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("cancelled")
        raise
```

### Important

After handling cancellation, normally re-raise it:

```python
except asyncio.CancelledError:
    cleanup()
    raise
```

This allows the cancellation signal to propagate to the caller.

---

## 2. `asyncio.timeout()`

Used to limit how long an operation can run:

```python
async with asyncio.timeout(3):
    await process_job(job)
```

If the operation exceeds 3 seconds:

```text
timeout
   ↓
coroutine gets CancelledError
   ↓
cleanup
   ↓
CancelledError is re-raised
   ↓
timeout context converts it to TimeoutError
```

So:

- Inside the cancelled coroutine → `CancelledError`
- Outside the timeout context → `TimeoutError`

Example:

```python
try:
    async with asyncio.timeout(3):
        await process_job(job)

except TimeoutError:
    print("job timed out")
```

---

## 3. `asyncio.wait_for()`

Another way to apply a timeout:

```python
await asyncio.wait_for(process_job(job), timeout=3)
```

Main difference:

```python
asyncio.timeout()
```

is a context manager:

```python
async with asyncio.timeout(3):
    await job()
```

while:

```python
asyncio.wait_for()
```

wraps a specific awaitable:

```python
await asyncio.wait_for(job(), 3)
```

---

## 4. Job Failure vs Worker Failure

### Job failure

A job can raise an exception:

```python
if job == "fail":
    raise ValueError("job failed")
```

The worker catches it:

```python
except ValueError as e:
    print(f"job failed: {e}")
```

The worker continues processing other jobs.

```text
job A → success
job B → failure
           ↓
       catch error
           ↓
job C → success
```

### Worker failure

If an exception escapes the worker itself:

```python
raise RuntimeError("worker crashed")
```

the worker task terminates.

```text
worker
   ↓
uncaught exception
   ↓
worker task dies
```

Other worker tasks are **not automatically cancelled**.

This is important:

> asyncio tasks are independent unless you explicitly coordinate their cancellation.

---

## 5. `queue.task_done()`

Every job retrieved with:

```python
job = await queue.get()
```

must eventually call:

```python
queue.task_done()
```

Usually use:

```python
try:
    ...
finally:
    queue.task_done()
```

This ensures the queue is marked complete even when the job:

- succeeds
- fails
- times out

---

## 6. `queue.join()`

```python
await queue.join()
```

waits until every queued item has had:

```python
queue.task_done()
```

called for it.

This is useful for graceful shutdown:

```text
stop producer
     ↓
no new jobs
     ↓
queue.join()
     ↓
all accepted jobs finish
```

---

## 7. Cancelling Workers

Workers usually run forever:

```python
while True:
    job = await queue.get()
```

After all jobs are complete, workers may still be waiting for new jobs.

Cancel them:

```python
for worker in workers:
    worker.cancel()
```

Then wait for them:

```python
await asyncio.gather(
    *workers,
    return_exceptions=True
)
```

This ensures the workers actually terminate before the program exits.

---

## 8. `gather(..., return_exceptions=True)`

Normally:

```python
await asyncio.gather(*workers)
```

can propagate an exception from a task.

With:

```python
await asyncio.gather(
    *workers,
    return_exceptions=True
)
```

exceptions/cancellations are returned as results instead of immediately propagating.

Useful when shutting down multiple tasks.

---

# 9. Graceful Shutdown

Graceful shutdown means:

> Stop accepting new work, but allow already accepted work to finish.

Pattern:

```python
producer_task.cancel()

try:
    await producer_task
except asyncio.CancelledError:
    pass

await queue.join()

for worker in workers:
    worker.cancel()

await asyncio.gather(
    *workers,
    return_exceptions=True
)
```

Flow:

```text
shutdown signal
       ↓
stop producer
       ↓
no new jobs
       ↓
queue.join()
       ↓
existing jobs finish
       ↓
workers become idle
       ↓
cancel workers
       ↓
await workers
       ↓
clean exit
```

---

# 10. Immediate Shutdown vs Graceful Shutdown

### Graceful

```text
stop producer
      ↓
finish queued/running work
      ↓
cancel idle workers
      ↓
exit
```

### Immediate

```text
stop producer
      ↓
cancel workers immediately
      ↓
running jobs receive CancelledError
      ↓
cleanup
      ↓
exit
```

Graceful shutdown prioritizes completing accepted work.

Immediate shutdown prioritizes stopping quickly.

---

# Final Mental Model

```text
                 PRODUCER
                    │
                    ▼
                  QUEUE
                    │
             ┌──────┴──────┐
             ▼             ▼
          Worker 1      Worker 2
             │             │
             ▼             ▼
           Job A         Job B
             │             │
       ┌─────┼─────┐       │
       ▼     ▼     ▼       ▼
    success fail timeout  success
                │
                ▼
          CancelledError
                │
                ▼
             cleanup
                │
                ▼
           TimeoutError
```

### Most important rules

```text
1. cancel() requests cancellation.
2. CancelledError is the mechanism used to deliver cancellation.
3. Clean up, then usually re-raise CancelledError.
4. timeout converts cancellation into TimeoutError for the caller.
5. Catch job exceptions so one bad job doesn't kill the worker.
6. An uncaught worker exception kills that worker task.
7. queue.task_done() must correspond to every queue.get().
8. queue.join() waits for all accepted jobs to finish.
9. Cancel and await workers during shutdown.
10. Graceful shutdown = stop intake → drain queue → stop workers.
```
