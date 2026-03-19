# Recursion

## What is Recursion?

Recursion is a programming technique where a method calls itself to solve a problem. A recursive solution breaks a problem into smaller instances of the same problem until it reaches a case simple enough to solve directly.

Every recursive method must have two components:
1. **Base case** — the condition that stops the recursion. Without it, the method calls itself infinitely and causes a StackOverflowError.
2. **Recursive case** — the part where the method calls itself with a smaller or simpler input, making progress toward the base case.

## The Call Stack

When a method is called, the JVM pushes a new **stack frame** onto the call stack. This frame contains the method's local variables, parameters, and the return address. When the method returns, its frame is popped off the stack.

For recursive methods, each call adds a new frame. If the recursion is too deep (too many nested calls), the stack runs out of space — this is a **stack overflow**.

Example — tracing `factorial(4)`:

```
factorial(4) → calls factorial(3)
  factorial(3) → calls factorial(2)
    factorial(2) → calls factorial(1)
      factorial(1) → base case, returns 1
    factorial(2) → returns 2 * 1 = 2
  factorial(3) → returns 3 * 2 = 6
factorial(4) → returns 4 * 6 = 24
```

The stack grows to depth 4 before unwinding. Each frame waits for the frame above it to return before computing its own result.

## Classic Examples

### Factorial

```java
int factorial(int n) {
    if (n <= 1) return 1;           // base case
    return n * factorial(n - 1);    // recursive case
}
```

Time complexity: O(n) — n recursive calls.
Space complexity: O(n) — n frames on the call stack.

### Fibonacci

```java
int fibonacci(int n) {
    if (n <= 1) return n;                              // base case
    return fibonacci(n - 1) + fibonacci(n - 2);        // two recursive calls
}
```

Time complexity: O(2^n) — exponential! Each call branches into two more calls. This is extremely inefficient for large n. The solution: **memoization** — store previously computed values to avoid redundant calculations, reducing time to O(n).

### Binary Search (Recursive)

```java
int binarySearch(int[] arr, int target, int low, int high) {
    if (low > high) return -1;                          // base case: not found
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;                 // base case: found
    if (arr[mid] < target)
        return binarySearch(arr, target, mid + 1, high);  // search right half
    else
        return binarySearch(arr, target, low, mid - 1);   // search left half
}
```

Time complexity: O(log n) — halves the search space each call.

## Tail Recursion

A recursive call is in **tail position** if it is the very last operation the method performs — meaning the method does nothing after the recursive call returns except pass the result up.

```java
// NOT tail recursive — multiplication happens AFTER the recursive call returns
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Tail recursive — the recursive call is the last operation
int factorialTail(int n, int accumulator) {
    if (n <= 1) return accumulator;
    return factorialTail(n - 1, n * accumulator);
}
```

In languages that support **tail call optimization** (TCO), tail recursive functions are converted into loops by the compiler, using O(1) stack space instead of O(n). Java does NOT support TCO, but languages like Scala, Scheme, and Kotlin do.

## When to Use Recursion

Recursion is natural for problems with recursive structure: tree traversal, divide-and-conquer algorithms (merge sort, quick sort), graph traversal (DFS), parsing nested expressions, and problems defined by mathematical recurrence relations.

However, recursion uses extra stack space and has function call overhead. For simple loops, iteration is usually more efficient. The rule of thumb: if the problem has a natural recursive structure and the depth is bounded, use recursion. Otherwise, prefer iteration or convert to tail recursion.
