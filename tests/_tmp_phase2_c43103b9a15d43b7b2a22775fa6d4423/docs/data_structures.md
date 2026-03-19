# Data Structures

## Overview

A data structure is a way of organizing and storing data so that it can be accessed and modified efficiently. The choice of data structure depends on the type of operations you need to perform and how frequently you perform them.

## Arrays

An array is a contiguous block of memory that stores elements of the same type. Each element is accessed by its index (position), starting from 0.

**Strengths:** O(1) random access by index. Memory-efficient — no overhead per element.
**Weaknesses:** Fixed size (in most languages). Inserting or deleting elements in the middle requires shifting all subsequent elements — O(n).

```java
int[] grades = new int[5];
grades[0] = 95;  // O(1) access
```

Arrays are the foundation of many other data structures. When you need fast access by position and the size is known in advance, arrays are the best choice.

## Linked Lists

A linked list is a sequence of nodes where each node contains data and a reference (pointer) to the next node. Unlike arrays, linked list elements are not stored in contiguous memory.

**Singly linked list:** Each node points to the next node. The last node points to null.
**Doubly linked list:** Each node points to both the next and previous nodes, allowing traversal in both directions.

**Strengths:** O(1) insertion/deletion at the head (and tail for doubly linked). Dynamic size — grows and shrinks as needed.
**Weaknesses:** O(n) access by index — must traverse from the head. Extra memory for pointers. Poor cache locality.

```
Head → [10 | →] → [20 | →] → [30 | null]
```

Use linked lists when you frequently insert/delete at the beginning or when you don't know the size in advance.

## Stacks

A stack is a Last-In-First-Out (LIFO) data structure. Think of a stack of plates — you add and remove from the top only.

**Operations:**
- `push(item)` — add item to the top. O(1)
- `pop()` — remove and return the top item. O(1)
- `peek()` — view the top item without removing. O(1)
- `isEmpty()` — check if stack is empty. O(1)

**Use cases:** Function call stack (tracking method calls and local variables), undo functionality, expression evaluation (converting infix to postfix), backtracking algorithms (maze solving, DFS).

A stack can be implemented using an array or a linked list. The array implementation is typically more efficient due to better cache locality.

## Queues

A queue is a First-In-First-Out (FIFO) data structure. Think of a line at a store — first person in line is first to be served.

**Operations:**
- `enqueue(item)` — add item to the back. O(1)
- `dequeue()` — remove and return the front item. O(1)
- `peek()` — view the front item. O(1)

**Variants:**
- **Priority Queue:** Elements are dequeued based on priority, not insertion order. Typically implemented with a heap. O(log n) enqueue/dequeue.
- **Circular Queue:** The back wraps around to the front, making efficient use of fixed-size arrays.
- **Deque (Double-ended queue):** Supports insertion and deletion at both ends.

**Use cases:** BFS (Breadth-First Search), task scheduling, print job management, message buffers.

## Trees

A tree is a hierarchical data structure consisting of nodes connected by edges. The topmost node is called the root. Each node can have zero or more child nodes.

**Terminology:**
- **Root:** The topmost node (no parent)
- **Leaf:** A node with no children
- **Height:** The longest path from root to a leaf
- **Depth:** The distance from the root to a node

### Binary Tree
Each node has at most two children (left and right).

### Binary Search Tree (BST)
A binary tree where for every node, all values in the left subtree are smaller and all values in the right subtree are larger.

**Operations on BST:**
- Search: O(log n) average, O(n) worst case (degenerate/unbalanced tree)
- Insert: O(log n) average, O(n) worst
- Delete: O(log n) average, O(n) worst

**Balanced BSTs** (AVL trees, Red-Black trees) guarantee O(log n) for all operations by maintaining balance after every insertion and deletion.

```
        8
       / \
      3   10
     / \    \
    1   6    14
```

In the BST above, searching for 6: start at 8 (go left), then at 3 (go right), found 6. That's 3 comparisons instead of scanning all elements.

## Hash Tables

A hash table (also called hash map) stores key-value pairs. It uses a **hash function** to compute an index (bucket) where the value should be stored.

**How it works:**
1. Take the key (e.g., "alice")
2. Pass it through a hash function: `hash("alice") = 4`
3. Store the value at index 4 in the underlying array

**Operations:** Insert, search, and delete are all O(1) on average.

**The collision problem:** Two different keys may hash to the same index. Common resolution strategies:
- **Chaining:** Each bucket holds a linked list of entries. Multiple key-value pairs can live in the same bucket.
- **Open addressing (linear probing):** If the bucket is occupied, check the next bucket sequentially until an empty one is found.

**Load factor** = number of entries / number of buckets. When the load factor exceeds a threshold (commonly 0.75), the hash table **resizes** — typically doubling the array and rehashing all entries. This is an O(n) operation but happens infrequently, so amortized insert is still O(1).

**Worst case:** If all keys hash to the same bucket, operations degrade to O(n). A good hash function distributes keys uniformly to avoid this.

## Complexity Comparison Table

| Data Structure | Access | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1)* | O(1)* |
| Stack | O(n) | O(n) | O(1) | O(1) |
| Queue | O(n) | O(n) | O(1) | O(1) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Hash Table | N/A | O(1) avg | O(1) avg | O(1) avg |

*For linked list: O(1) insertion/deletion assumes you already have a reference to the node. Finding the node is O(n).

The right data structure choice can make the difference between an algorithm that runs in milliseconds and one that takes hours. Always analyze what operations your program performs most frequently and choose accordingly.
