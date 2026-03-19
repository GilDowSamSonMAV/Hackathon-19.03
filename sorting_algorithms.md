# Sorting Algorithms

Sorting is the process of arranging elements in a specific order (usually ascending or descending). Sorting is one of the most fundamental operations in computer science — it makes searching, merging, and analyzing data much more efficient. There are many sorting algorithms, each with different performance characteristics and use cases.

## Bubble Sort

Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. Larger elements "bubble" to the end with each pass.

```
Pseudocode:
for i from 0 to n-1:
    for j from 0 to n-i-2:
        if arr[j] > arr[j+1]:
            swap(arr[j], arr[j+1])
```

**Time complexity**: O(n²) average and worst case. O(n) best case (already sorted, with optimization flag).
**Space complexity**: O(1) — in-place.
**Stable**: Yes — equal elements maintain their relative order.

Bubble sort is simple to understand and implement but extremely inefficient for large datasets. It is primarily used for educational purposes.

## Selection Sort

Selection sort divides the array into a sorted portion (left) and an unsorted portion (right). In each iteration, it finds the minimum element from the unsorted portion and swaps it with the first unsorted element.

```
Pseudocode:
for i from 0 to n-1:
    min_index = i
    for j from i+1 to n-1:
        if arr[j] < arr[min_index]:
            min_index = j
    swap(arr[i], arr[min_index])
```

**Time complexity**: O(n²) in all cases (always scans the entire unsorted portion).
**Space complexity**: O(1) — in-place.
**Stable**: No — swapping can change the relative order of equal elements.

Selection sort performs fewer swaps than bubble sort (at most n-1 swaps), which can be advantageous when swap operations are expensive.

## Insertion Sort

Insertion sort builds the sorted array one element at a time. It takes each element from the unsorted portion and inserts it into its correct position in the sorted portion, shifting larger elements to the right.

```
Pseudocode:
for i from 1 to n-1:
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j = j - 1
    arr[j+1] = key
```

**Time complexity**: O(n²) average and worst case. O(n) best case (already sorted).
**Space complexity**: O(1) — in-place.
**Stable**: Yes.

Insertion sort is efficient for small datasets and nearly-sorted data. It is often used as the base case in hybrid sorting algorithms (like Timsort, which Python uses internally).

## Merge Sort

Merge sort is a divide-and-conquer algorithm. It divides the array into two halves, recursively sorts each half, and then merges the two sorted halves into a single sorted array.

```
Pseudocode:
function merge_sort(arr):
    if length(arr) <= 1:
        return arr
    mid = length(arr) / 2
    left = merge_sort(arr[0..mid])
    right = merge_sort(arr[mid..end])
    return merge(left, right)

function merge(left, right):
    result = []
    while left and right are not empty:
        if left[0] <= right[0]:
            append left[0] to result
        else:
            append right[0] to result
    append remaining elements
    return result
```

**Time complexity**: O(n log n) in all cases — always divides in half, always merges linearly.
**Space complexity**: O(n) — requires additional space for the merged subarrays.
**Stable**: Yes.

Merge sort guarantees O(n log n) performance regardless of input. Its main disadvantage is the O(n) extra space required. It is well-suited for sorting linked lists (where the space overhead is minimal) and for external sorting (sorting data that doesn't fit in memory).

## Quick Sort

Quick sort is also a divide-and-conquer algorithm. It selects a **pivot** element, partitions the array so that elements less than the pivot go to the left and elements greater go to the right, and then recursively sorts the two partitions.

```
Pseudocode:
function quick_sort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

function partition(arr, low, high):
    pivot = arr[high]  // choose last element as pivot
    i = low - 1
    for j from low to high - 1:
        if arr[j] < pivot:
            i = i + 1
            swap(arr[i], arr[j])
    swap(arr[i+1], arr[high])
    return i + 1
```

**Time complexity**: O(n log n) average case. O(n²) worst case (when pivot is always the smallest or largest element — e.g., already sorted input with last-element pivot).
**Space complexity**: O(log n) average (for the recursion stack). O(n) worst case.
**Stable**: No — partitioning can change the relative order of equal elements.

Quick sort is generally the fastest in practice for random data due to good cache locality and low constant factors. The worst case can be avoided by using **randomized pivot selection** or the **median-of-three** strategy.

## Comparison Table

| Algorithm      | Best Case  | Average    | Worst Case | Space  | Stable |
|---------------|------------|------------|------------|--------|--------|
| Bubble Sort   | O(n)       | O(n²)     | O(n²)     | O(1)   | Yes    |
| Selection Sort| O(n²)      | O(n²)     | O(n²)     | O(1)   | No     |
| Insertion Sort| O(n)       | O(n²)     | O(n²)     | O(1)   | Yes    |
| Merge Sort    | O(n log n) | O(n log n)| O(n log n)| O(n)   | Yes    |
| Quick Sort    | O(n log n) | O(n log n)| O(n²)     | O(log n)| No    |

## Choosing a Sorting Algorithm

For small arrays (n < 50): Insertion sort is fast and simple. For general-purpose sorting: Merge sort if stability matters, quick sort if average-case speed matters most. For nearly sorted data: Insertion sort is optimal. For guaranteed worst-case performance: Merge sort. Most production languages use hybrid algorithms — Python's Timsort combines merge sort and insertion sort, and Java's Arrays.sort uses dual-pivot quicksort for primitives and Timsort for objects.
