# Recursion

Recursion is a programming technique where a function calls itself to solve a problem. A recursive function breaks a problem down into smaller, similar subproblems until it reaches a simple case that can be solved directly.

## Base Case and Recursive Case

Every recursive function must have two components:

**Base case**: The condition under which the function stops calling itself and returns a value directly. Without a base case, the function would call itself infinitely, eventually causing a stack overflow error.

**Recursive case**: The part where the function calls itself with a modified argument, moving closer to the base case with each call.

Example — Factorial:
```python
def factorial(n):
    if n <= 1:          # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case
```

For `factorial(4)`:
- `factorial(4)` → returns `4 * factorial(3)`
- `factorial(3)` → returns `3 * factorial(2)`
- `factorial(2)` → returns `2 * factorial(1)`
- `factorial(1)` → returns `1` (base case hit)
- Then it unwinds: `2 * 1 = 2`, then `3 * 2 = 6`, then `4 * 6 = 24`

## The Call Stack

When a function calls itself, each call is added as a new **stack frame** on the call stack. Each frame holds its own copy of the function's local variables and parameters. The call stack grows with each recursive call and shrinks as each call returns.

For `factorial(4)`, the call stack looks like this at maximum depth:

```
| factorial(1)  |  ← top (most recent call)
| factorial(2)  |
| factorial(3)  |
| factorial(4)  |  ← bottom (original call)
```

When `factorial(1)` returns 1, its frame is popped off. Then `factorial(2)` can compute `2 * 1` and return, and so on. This unwinding process is how the final result is assembled.

**Stack overflow**: If recursion is too deep (too many nested calls), the call stack exceeds its memory limit and the program crashes. In Python, the default recursion limit is 1000. In Java, it depends on the thread stack size (typically a few thousand frames).

## Fibonacci — A Classic Example

```python
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
```

This works but is very inefficient — it has O(2^n) time complexity because it recalculates the same values many times. For example, `fibonacci(5)` calls `fibonacci(3)` twice and `fibonacci(2)` three times.

**Optimization with memoization**: Store previously computed results to avoid redundant calculations.

```python
def fibonacci_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    if n == 1:
        return 1
    memo[n] = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    return memo[n]
```

With memoization, the time complexity drops to O(n) because each value is computed only once.

## Tail Recursion

**Tail recursion** is a special form of recursion where the recursive call is the very last operation in the function — there is no additional computation after the recursive call returns. This matters because tail-recursive functions can be optimized by the compiler into a loop (called **tail call optimization** or TCO), eliminating the risk of stack overflow.

Regular recursion (NOT tail recursive):
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # multiplication happens AFTER the recursive call returns
```

Tail-recursive version:
```python
def factorial_tail(n, accumulator=1):
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)  # nothing happens after this call
```

In the tail-recursive version, the result is built up in the `accumulator` parameter. When the base case is reached, the accumulator already holds the final answer — no unwinding is needed.

**Important note**: Python does NOT optimize tail recursion. Java does not either (in most JVM implementations). Languages like Scheme, Haskell, and some C compilers do support tail call optimization. However, understanding tail recursion is important conceptually because it demonstrates how to convert recursive solutions into iterative ones.

## When to Use Recursion

Recursion is best suited for problems that have a naturally recursive structure: tree traversals, graph algorithms (DFS), divide-and-conquer algorithms (merge sort, quicksort), mathematical sequences, and problems involving nested or hierarchical data. For simple iteration, a loop is usually more efficient and readable.
