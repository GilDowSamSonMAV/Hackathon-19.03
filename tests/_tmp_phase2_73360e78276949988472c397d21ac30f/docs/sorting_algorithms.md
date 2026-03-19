# Sorting Algorithms

## Why Sorting Matters

Sorting is one of the most fundamental operations in computer science. A sorted dataset enables binary search (O(log n) instead of O(n)), simplifies finding duplicates, and is required by many algorithms as a preprocessing step. Understanding sorting algorithms teaches core concepts: time/space tradeoffs, divide-and-conquer, stability, and in-place vs. extra-space approaches.

## Bubble Sort

Bubble sort repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The largest unsorted element "bubbles up" to its correct position after each pass.

```
Pseudocode:
for i = 0 to n-1:
    for j = 0 to n-i-2:
        if arr[j] > arr[j+1]:
            swap(arr[j], arr[j+1])
```

**Time complexity:** O(n²) average and worst case. O(n) best case (already sorted, with early termination optimization).
**Space complexity:** O(1) — in-place.
**Stable:** Yes — equal elements maintain their relative order.

Bubble sort is simple to understand but impractical for large datasets. It is primarily used for educational purposes.

## Selection Sort

Selection sort divides the array into a sorted portion (left) and an unsorted portion (right). It repeatedly finds the minimum element in the unsorted portion and swaps it with the first unsorted element.

```
Pseudocode:
for i = 0 to n-1:
    minIndex = i
    for j = i+1 to n-1:
        if arr[j] < arr[minIndex]:
            minIndex = j
    swap(arr[i], arr[minIndex])
```

**Time complexity:** O(n²) in all cases — always scans the entire unsorted portion.
**Space complexity:** O(1) — in-place.
**Stable:** No — the swap can change the relative order of equal elements.

Selection sort performs fewer swaps than bubble sort (at most n swaps total), which can be advantageous when write operations are expensive.

## Insertion Sort

Insertion sort builds the sorted array one element at a time. It picks the next unsorted element and inserts it into its correct position within the sorted portion by shifting larger elements to the right.

```
Pseudocode:
for i = 1 to n-1:
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j = j - 1
    arr[j+1] = key
```

**Time complexity:** O(n²) average and worst case. O(n) best case (already sorted).
**Space complexity:** O(1) — in-place.
**Stable:** Yes.

Insertion sort is efficient for small datasets (n < 20-50) and nearly sorted data. Many optimized sorting implementations use insertion sort as a subroutine for small partitions.

## Merge Sort

Merge sort is a divide-and-conquer algorithm. It divides the array into two halves, recursively sorts each half, and then merges the two sorted halves back together.

```
Pseudocode:
mergeSort(arr, left, right):
    if left < right:
        mid = (left + right) / 2
        mergeSort(arr, left, mid)       // sort left half
        mergeSort(arr, mid+1, right)    // sort right half
        merge(arr, left, mid, right)    // merge both halves

merge(arr, left, mid, right):
    Create temp arrays L and R
    Copy data to L and R
    Merge L and R back into arr by comparing elements one by one
```

**Time complexity:** O(n log n) in ALL cases — always divides and merges.
**Space complexity:** O(n) — requires auxiliary array for merging.
**Stable:** Yes.

Merge sort guarantees O(n log n) performance regardless of input. This makes it predictable and reliable. The tradeoff is the extra O(n) space. Merge sort is the algorithm of choice when stability is required and extra space is available.

## Quick Sort

Quick sort is also divide-and-conquer. It selects a **pivot** element, partitions the array so that all elements smaller than the pivot are on the left and all larger elements are on the right, then recursively sorts the two partitions.

```
Pseudocode:
quickSort(arr, low, high):
    if low < high:
        pivotIndex = partition(arr, low, high)
        quickSort(arr, low, pivotIndex - 1)    // sort left partition
        quickSort(arr, pivotIndex + 1, high)    // sort right partition

partition(arr, low, high):
    pivot = arr[high]      // choose last element as pivot
    i = low - 1
    for j = low to high-1:
        if arr[j] <= pivot:
            i++
            swap(arr[i], arr[j])
    swap(arr[i+1], arr[high])
    return i + 1
```

**Time complexity:** O(n log n) average case. O(n²) worst case (already sorted array with bad pivot choice).
**Space complexity:** O(log n) for the recursive call stack.
**Stable:** No — the partitioning swaps can change relative order of equal elements.

Quick sort is faster in practice than merge sort for most inputs despite having a worse worst case. This is because it has better cache locality (works in-place, no auxiliary arrays) and lower constant factors. The worst case can be mitigated by choosing the pivot wisely — common strategies include median-of-three and random pivot selection.

## Comparison Summary

| Algorithm | Best | Average | Worst | Space | Stable |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |

## Choosing the Right Algorithm

For small arrays (n < 50): insertion sort is fastest due to low overhead. For general-purpose sorting: quick sort is the default choice in most standard libraries. When guaranteed O(n log n) is needed: use merge sort. When stability matters: merge sort or insertion sort. Java's `Arrays.sort()` uses a dual-pivot quicksort for primitives and TimSort (a hybrid merge sort + insertion sort) for objects.
