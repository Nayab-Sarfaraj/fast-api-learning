### Asyncio

- `asyncio` provides and manages the **event loop**, which executes and coordinates asynchronous tasks.

### Awaitables

An **awaitable** is an object that can be used with the `await` keyword.

For example:

```python
result = await something
```

For this to work, `something` must be awaitable.

Python has three main types of awaitables:

1. **Coroutine**
2. **Task**
3. **Future**

### Coroutine Function

A **coroutine function** is a function defined using the `async` keyword:

```python
async def fetch_data():
    ...
```

### Coroutine Object

When we call a coroutine function:

```python
coro = fetch_data()
```

it returns a **coroutine object**.

The coroutine object is awaitable.

When we do:

```python
await coro
```

the current coroutine waits for `coro` to complete. The coroutine is executed by the event loop, and when it reaches an `await` point, the event loop can run other **already-scheduled** tasks.

### Tasks

A **Task** is a wrapper around a coroutine that schedules that coroutine to run on the event loop.

```python
task = asyncio.create_task(fetch_data())
```

Unlike a plain coroutine object, a Task is scheduled independently.

The Task can be placed on the event loop and remain there until the event loop gets control and executes it. This allows us to **schedule work now and await it later**, enabling multiple coroutines to make progress concurrently.

For example:

```python
task1 = asyncio.create_task(fetch_data(1))
task2 = asyncio.create_task(fetch_data(2))

result1 = await task1
result2 = await task2
```

Here, both tasks are scheduled before we await either one, so while `task1` is suspended at an `await`, the event loop can run `task2`.

### `asyncio.gather()` with Coroutines

```python
coroutines = [fetch_data(i) for i in range(1, 3)]
results = await asyncio.gather(*coroutines, return_exceptions=True)
```

`gather()` accepts awaitables such as coroutine objects, schedules them as Tasks, and waits for all of them to complete. The results are returned in the **same order as the input awaitables**, regardless of which coroutine finishes first.

With `return_exceptions=True`, an exception raised by one coroutine is **returned as an exception object in the results list** instead of being propagated to the caller. The other coroutines are allowed to continue running.

---

### `asyncio.gather()` with Tasks

```python
tasks = [asyncio.create_task(fetch_data(i)) for i in range(1, 3)]
results = await asyncio.gather(*tasks)
```

Here, the coroutines are explicitly converted into Tasks and scheduled before being passed to `gather()`. `gather()` then waits for all of the Tasks and returns their results in the **same order as the input Tasks**.

By default, `return_exceptions=False`, so if one Task raises an exception, `gather()` propagates that exception to the caller. It does **not automatically cancel the other Tasks**; they may continue running in the background.

If we use:

```python
await asyncio.gather(*tasks, return_exceptions=True)
```

then exceptions are returned as values in the results list instead of being raised.

---

### `asyncio.TaskGroup`

```python
async with asyncio.TaskGroup() as tg:
    results = [tg.create_task(fetch_data(i)) for i in range(1, 3)]
```

`TaskGroup` provides structured concurrency. All tasks created inside the group are automatically awaited when the `async with` block exits, so we don't need to explicitly await each Task.

Unlike `gather()`, `TaskGroup` has stronger failure handling: if one task raises an exception, the **remaining tasks in the group are automatically cancelled**, and the exception is propagated when leaving the `TaskGroup` context. Multiple exceptions can be collected into an `ExceptionGroup`.

After the context exits successfully, the Tasks are complete, so we can retrieve their results using:

```python
[result.result() for result in results]
```
