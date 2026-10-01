https://chatgpt.com/share/6abbd4c3-3dd4-83e8-8735-f4fca20a7eb4

## Stage 5 — Async Queue + Worker Pool

### What we learned

- **`asyncio.Queue`** is used to hold jobs waiting to be processed.
- **Workers** continuously take jobs from the queue and process them.
- We use **`asyncio.create_task()`** to start workers independently.
- `await queue.get()`:
  - gets a job if available
  - **pauses the worker** if the queue is empty

- `queue.task_done()` tells the queue that a job has finished.
- `await queue.join()` waits until **all jobs** have been completed.

### Worker Pool

Instead of:

```text
100 jobs → 100 tasks
```

we can do:

```text
100 jobs
   ↓
 Queue
   ↓
5 Workers
```

Only the workers actively process jobs, giving us **bounded concurrency**.

### Dynamic Distribution

Workers aren't assigned specific jobs.

```text
Worker 1 → job 1 → job 4 → job 7
Worker 2 → job 2 → job 5 → job 8
Worker 3 → job 3 → job 6 → job 9
```

When a worker finishes, it grabs the next available job.

### What we proved experimentally

With 100 jobs taking ~1 second each:

- 3 workers → ~34 sec
- 5 workers → ~20 sec
- 10 workers → ~10 sec
- 20 workers → ~5 sec

So **more workers = more concurrency = lower total time**, until some other bottleneck is reached.

### Most important takeaway

> **Stage 5 taught us how to process a large number of jobs using a fixed number of concurrent workers through `asyncio.Queue`.**

We also understood **why a worker pool is preferable to creating thousands of tasks at once** when the workload is large.
