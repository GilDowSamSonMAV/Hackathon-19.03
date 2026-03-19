# Data Structures

A data structure is a specialized format for organizing, processing, retrieving and storing data. There are several basic and advanced types of data structures, designed to arrange data to suit a specific purpose. Data structures make it easy for users to access and work with the data they need in appropriate ways.

Choosing the right data structure can drastically improve the performance of an algorithm. We generally classify data structures into linear and non-linear types.

## Linear Data Structures

In linear data structures, the elements are arranged in a sequence one after the other. Since elements are arranged in a particular order, they are easy to implement.

### 1. Arrays

An array is a collection of items stored at contiguous memory locations. The idea is to store multiple items of the same type together. This makes it easier to calculate the position of each element by simply adding an offset to a base value, i.e., the memory location of the first element of the array (generally denoted by the name of the array).

*   **Advantages:** Random access of elements (using index) is very fast O(1).
*   **Disadvantages:** Fixed size (in most traditional implementations), insertion and deletion can be slow O(n) as elements need to be shifted.

### 2. Linked Lists

A linked list is a linear data structure, in which the elements are not stored at contiguous memory locations. The elements in a linked list are linked using pointers.

In simple words, a linked list consists of nodes where each node contains a data field and a reference(link) to the next node in the list.

*   **Singly Linked List:** Each node points to the next node.
*   **Doubly Linked List:** Each node points to both the next and the previous node.
*   **Advantages:** Dynamic size, easy insertion/deletion O(1) if the node pointer is given.
*   **Disadvantages:** Sequential access only; no random access. Extra memory is required for pointers.

### 3. Stacks

A stack is a linear data structure that follows a particular order in which the operations are performed. The order may be LIFO (Last In First Out) or FILO (First In Last Out). Primarily, the following three basic operations are performed in the stack:
*   `Push`: Adds an item in the stack. If the stack is full, then it is said to be an Overflow condition.
*   `Pop`: Removes an item from the stack. The items are popped in the reversed order in which they are pushed. If the stack is empty, then it is said to be an Underflow condition.
*   `Peek` or `Top`: Returns top element of stack.

Think of a stack of plates; you can only add or remove a plate from the top.

### 4. Queues

A queue is a linear structure which follows a particular order in which the operations are performed. The order is First In First Out (FIFO). A good example of a queue is any queue of consumers for a resource where the consumer that came first is served first.

Operations:
*   `Enqueue`: Adds an item to the queue.
*   `Dequeue`: Removes an item from the queue.

## Non-Linear Data Structures

In non-linear data structures, elements are not arranged sequentially.

### 5. Trees

A tree is a hierarchical data structure defined as a collection of nodes. Nodes represent value and nodes are connected by edges. A tree has the following properties:
*   The tree has one node called root.
*   Every node (excluding a root) is connected by a directed edge from exactly one other node; this node is called a parent.

**Binary Tree:** A tree whose elements have at most 2 children is called a binary tree. Since each element in a binary tree can have only 2 children, we typically name them the left and right child.

**Binary Search Tree (BST):** A binary tree with the additional property that for every node, all nodes in its left subtree have a smaller value, and all nodes in its right subtree have a larger value. This property makes searching very efficient.

### 6. Hash Tables

A hash table is a data structure that implements an associative array abstract data type, a structure that can map keys to values. A hash table uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.

Ideally, the hash function will assign each key to a unique bucket, but most hash table designs employ an imperfect hash function, which might cause hash collisions where the hash function generates the same index for more than one key. Such collisions are typically accommodated in some way (e.g., chaining or open addressing).

*   **Advantages:** Extremely fast average-case lookup, insertion, and deletion O(1).
*   **Disadvantages:** Worst-case performance can be O(n) if many collisions occur. Unordered iteration.

## Time Complexity Table

Here is a summary of the average time complexities for basic operations on these data structures:

| Data Structure | Access | Search | Insertion | Deletion |
| :--- | :---: | :---: | :---: | :---: |
| **Array** | O(1) | O(n) | O(n) | O(n) |
| **Linked List** | O(n) | O(n) | O(1) | O(1) |
| **Stack** | O(n) | O(n) | O(1) | O(1) |
| **Queue** | O(n) | O(n) | O(1) | O(1) |
| **Binary Search Tree** | O(log n) | O(log n) | O(log n) | O(log n) |
| **Hash Table** | N/A | O(1) | O(1) | O(1) |

*Note: The time complexities for BST are average cases assuming the tree is balanced. In the worst case (a heavily skewed tree), operations can degrade to O(n).*
