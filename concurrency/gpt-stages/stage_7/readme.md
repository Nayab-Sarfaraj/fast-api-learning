https://chatgpt.com/share/6abe4aa3-4790-83ee-a4b4-35b1cbf25b1f

Here’s a **short revision note for Stage 7**.

## Stage 7 — Race Conditions & Locks

### 1. Shared State

Data that multiple coroutines can access or modify.

```python
counter = 0
```

If multiple coroutines modify `counter`, it becomes shared mutable state.

---

### 2. Why the first counter example was safe

```python
async def increment():
    global counter

    for _ in range(1000):
        counter += 1
```

There was **no `await` inside the loop**.

Therefore, once a coroutine started executing `increment()`, it kept running until it finished. The event loop couldn't switch to another coroutine in the middle.

So:

```text
A → completes → B → completes → C
```

instead of:

```text
A → B → A → C → B
```

---

### 3. Race Condition

A race condition happens when multiple coroutines access shared state and the result depends on **how their execution gets interleaved**.

Example:

```python
current = counter

await asyncio.sleep(0)

counter = current + 1
```

Possible execution:

```text
counter = 0

A: current = 0
A: await

B: current = 0
B: await

A: counter = 1
B: counter = 1
```

Two increments happened, but the counter only increased by 1.

---

### 4. `await` creates the opportunity for interleaving

`await` gives the event loop an opportunity to run another coroutine.

So this:

```python
read shared state
await
modify shared state
```

can be dangerous.

But remember:

> **`await` doesn't automatically cause a race condition.**

You need **shared mutable state + unsafe interleaving**.

---

### 5. Critical Section

The part of an operation that must be protected from concurrent access.

Our bank example:

```python
if balance >= amount:
    await asyncio.sleep(0)
    balance -= amount
```

The **check and modification together** form the critical section.

Why?

Because this is logically one operation:

```text
check balance → withdraw money
```

You don't want another coroutine changing the balance between those two steps.

---

### 6. `asyncio.Lock`

A lock allows only one coroutine at a time to enter a protected section.

```python
lock = asyncio.Lock()

async with lock:
    if balance >= amount:
        balance -= amount
```

Execution:

```text
A gets lock
   ↓
A checks balance
   ↓
A awaits
   ↓
B tries to get lock
   ↓
B waits
   ↓
A resumes
   ↓
A modifies balance
   ↓
A releases lock
   ↓
B gets lock
```

So even though A can `await` while holding the lock, B **cannot enter the same locked section**.

---

### 7. Locks don't protect everything automatically

This:

```python
async with lock:
    balance -= 10
```

only protects code that uses **that same lock**.

If another coroutine does:

```python
balance -= 10
```

without using the lock, it can still interfere.

---

### 8. Keep the critical section small

Good:

```python
async with lock:
    balance -= amount
```

Avoid unnecessarily doing expensive work inside:

```python
async with lock:
    # network request
    # expensive computation
    # unrelated work
```

The longer you hold the lock, the more other coroutines have to wait.

---

## The mental model to remember

```text
Shared state
     ↓
Multiple coroutines access it
     ↓
Can they interleave during the operation?
     ↓
YES → possible race condition
     ↓
Identify critical section
     ↓
Protect it with asyncio.Lock
```

### One-liner for revision

> **A race condition occurs when coroutines can interleave while manipulating shared mutable state; `asyncio.Lock` makes the critical section exclusive so only one coroutine can execute it at a time.**
