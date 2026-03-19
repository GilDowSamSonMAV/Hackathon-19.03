# Data Structures

A data structure is a way of organizing and storing data so that it can be accessed and modified efficiently. Choosing the right data structure is one of the most important decisions in software development, as it directly affects the performance of your program.

## Arrays

An **array** is a contiguous block of memory that stores elements of the same type. Each element is accessed by its index (position), starting from 0.

**Advantages**: Constant-time access to any element by index — O(1) lookup. Memory-efficient because elements are stored contiguously.

**Disadvantages**: Fixed size (in most languages). Inserting or deleting elements in the middle requires shifting all subsequent elements — O(n) time.

**Common operations:**
- Access by index: O(1)
- Search (unsorted): O(n)
- Insertion at end: O(1) amortized (for dynamic arrays)
- Insertion at position i: O(n)
- Deletion at position i: O(n)

## Linked Lists

A **linked list** is a sequence of nodes, where each node contains data and a reference (pointer) to the next node. Unlike arrays, linked list elements are not stored contiguously in memory.

**Singly linked list**: Each node points to the next node. The last node points to null.
**Doubly linked list**: Each node has pointers to both the next and previous nodes.
**Circular linked list**: The last node points back to the first node.

**Advantages**: Dynamic size — no need to declare size in advance. Efficient insertion and deletion at the head — O(1). No memory waste from pre-allocation.

**Disadvantages**: No random access — to reach the i-th element, you must traverse from the head — O(n). Extra memory for storing pointers. Poor cache locality compared to arrays.

**Common operations:**
- Access by index: O(n)
- Search: O(n)
- Insertion at head: O(1)
- Insertion at tail (with tail pointer): O(1)
- Insertion at position i: O(n) — need to traverse to position
- Deletion at head: O(1)
- Deletion at position i: O(n)

## Stacks

A **stack** is a Last-In-First-Out (LIFO) data structure. Think of it like a stack of plates — you can only add or remove from the top.

**Key operations:**
- **push(item)**: Add an item to the top — O(1)
- **pop()**: Remove and return the top item — O(1)
- **peek()**: View the top item without removing it — O(1)
- **isEmpty()**: Check if the stack is empty — O(1)

**Common uses**: Function call stack (tracks active function calls), undo/redo operations, expression evaluation (converting infix to postfix), backtracking algorithms (maze solving, DFS), and matching parentheses.

A stack can be implemented using an array (fixed size) or a linked list (dynamic size). The array implementation is more common due to cache efficiency.

## Queues

A **queue** is a First-In-First-Out (FIFO) data structure. Think of it like a line at a store — the first person in line is the first person served.

**Key operations:**
- **enqueue(item)**: Add an item to the back — O(1)
- **dequeue()**: Remove and return the front item — O(1)
- **front()**: View the front item without removing it — O(1)
- **isEmpty()**: Check if the queue is empty — O(1)

**Variations:**
- **Priority queue**: Elements are dequeued based on priority, not order of arrival. Often implemented with a heap.
- **Circular queue**: Uses a fixed-size array where the end wraps around to the beginning, avoiding wasted space.
- **Deque (double-ended queue)**: Allows insertion and deletion at both ends.

**Common uses**: Task scheduling (CPU scheduling, print queues), BFS (Breadth-First Search) in graphs, message buffers, and request handling in web servers.

## Trees

A **tree** is a hierarchical data structure consisting of nodes connected by edges. The topmost node is the **root**. Each node can have zero or more **children**. Nodes with no children are called **leaves**.

**Key terminology:**
- **Root**: The topmost node of the tree.
- **Parent**: A node that has children.
- **Child**: A node that has a parent.
- **Leaf**: A node with no children.
- **Depth**: The number of edges from the root to a node.
- **Height**: The number of edges on the longest path from a node to a leaf.

**Binary Tree**: A tree where each node has at most 2 children (left and right).

**Binary Search Tree (BST)**: A binary tree where for every node, all values in the left subtree are less than the node's value, and all values in the right subtree are greater. This property enables efficient searching.

**BST operations:**
- Search: O(log n) average, O(n) worst case (degenerate/unbalanced tree)
- Insertion: O(log n) average, O(n) worst case
- Deletion: O(log n) average, O(n) worst case
- In-order traversal yields sorted order

**Tree traversal methods:**
- **In-order** (Left, Root, Right): Visits nodes in sorted order for BST.
- **Pre-order** (Root, Left, Right): Useful for copying a tree.
- **Post-order** (Left, Right, Root): Useful for deleting a tree.
- **Level-order** (BFS): Visits nodes level by level, uses a queue.

## Hash Tables

A **hash table** (also called hash map or dictionary) stores key-value pairs and provides near-constant-time access. It uses a **hash function** to compute an index into an array of buckets, where the desired value is stored.

**How it works:**
1. Given a key, the hash function computes a hash code (an integer).
2. The hash code is mapped to a bucket index (usually via modulo: `index = hash(key) % array_size`).
3. The value is stored in (or retrieved from) that bucket.

**Collision handling**: When two different keys hash to the same index, a collision occurs. Two common strategies:
- **Chaining**: Each bucket contains a linked list of entries that hashed to that index.
- **Open addressing (Linear probing)**: If a bucket is occupied, check the next bucket sequentially until an empty one is found.

**Common operations:**
- Insert: O(1) average, O(n) worst case (all keys collide)
- Search: O(1) average, O(n) worst case
- Delete: O(1) average, O(n) worst case

**Load factor**: The ratio of stored entries to total buckets (`n / capacity`). When the load factor exceeds a threshold (commonly 0.75), the hash table resizes (typically doubles) and rehashes all entries. This keeps operations efficient.

**Common uses**: Dictionaries in Python (`dict`), caching, counting frequencies, indexing, and implementing sets.

## Complexity Comparison Table

| Data Structure | Access | Search | Insert | Delete | Space |
|----------------|--------|--------|--------|--------|-------|
| Array          | O(1)   | O(n)   | O(n)   | O(n)   | O(n)  |
| Linked List    | O(n)   | O(n)   | O(1)*  | O(1)*  | O(n)  |
| Stack          | O(n)   | O(n)   | O(1)   | O(1)   | O(n)  |
| Queue          | O(n)   | O(n)   | O(1)   | O(1)   | O(n)  |
| BST            | O(log n)| O(log n)| O(log n)| O(log n)| O(n) |
| Hash Table     | N/A    | O(1)   | O(1)   | O(1)   | O(n)  |

*At head/known position. At arbitrary position: O(n) to find, then O(1) to insert/delete.
