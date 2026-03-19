# Sorting Algorithms

Sorting is a fundamental operation in computer science. It involves arranging the elements of a list or array in a specific order, typically numerical or lexicographical (alphabetical). Efficient sorting is crucial for optimizing other algorithms, such as binary search, which require sorted input data.

Here we review several common sorting algorithms, ranging from simple but inefficient to more complex and highly efficient.

## 1. Bubble Sort

Bubble Sort is one of the simplest sorting algorithms. It works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they are in the wrong order. The pass through the list is repeated until no swaps are needed, indicating that the list is sorted.

The algorithm gets its name from the way smaller or larger elements "bubble" to the top of the list.

**Pseudocode:**
```text
procedure bubbleSort( A : list of sortable items )
    n = length(A)
    repeat
        swapped = false
        for i = 1 to n-1 inclusive do
            if A[i-1] > A[i] then
                swap(A[i-1], A[i])
                swapped = true
            end if
        end for
        n = n - 1
    until not swapped
end procedure
```
**Time Complexity:** Worst-case $O(n^2)$, Average-case $O(n^2)$, Best-case $O(n)$ (if already sorted).

## 2. Selection Sort

Selection Sort works by dividing the input list into two parts: a sorted sublist of items which is built up from left to right at the front (left) of the list, and a sublist of the remaining unsorted items that occupy the rest of the list. Initially, the sorted sublist is empty and the unsorted sublist is the entire input list.

The algorithm proceeds by finding the smallest (or largest, depending on sorting order) element in the unsorted sublist, exchanging (swapping) it with the leftmost unsorted element, and moving the sublist boundaries one element to the right.

**Pseudocode:**
```text
procedure selectionSort( A : list of sortable items )
    n = length(A)
    for i = 0 to n - 1 do
        minIndex = i
        for j = i + 1 to n do
            if A[j] < A[minIndex] then
                minIndex = j
            end if
        end for
        if minIndex != i then
            swap(A[i], A[minIndex])
        end if
    end for
end procedure
```
**Time Complexity:** Worst-case $O(n^2)$, Average-case $O(n^2)$, Best-case $O(n^2)$. It performs poorly on large lists.

## 3. Insertion Sort

Insertion sort is a simple sorting algorithm that builds the final sorted array (or list) one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort. However, it provides several advantages: simple implementation, efficient for small data sets, and adaptive (efficient for data sets that are already substantially sorted).

It works similar to the way you sort playing cards in your hands.

**Pseudocode:**
```text
procedure insertionSort( A : list of sortable items )
    n = length(A)
    for i = 1 to n - 1 do
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key do
            A[j+1] = A[j]
            j = j - 1
        end while
        A[j+1] = key
    end for
end procedure
```
**Time Complexity:** Worst-case $O(n^2)$, Average-case $O(n^2)$, Best-case $O(n)$.

## 4. Merge Sort

Merge Sort is an efficient, general-purpose, comparison-based sorting algorithm. Most implementations produce a stable sort. It is a divide and conquer algorithm.

Conceptually, a merge sort works as follows:
1.  Divide the unsorted list into $n$ sublists, each containing one element (a list of one element is considered sorted).
2.  Repeatedly merge sublists to produce new sorted sublists until there is only one sorted list remaining. This will be the sorted list.

**Pseudocode:**
```text
procedure mergeSort( A : list of sortable items )
    if length(A) <= 1 then
        return A
    end if
    mid = length(A) / 2
    left = mergeSort(A[0...mid-1])
    right = mergeSort(A[mid...length(A)])
    return merge(left, right)
end procedure

procedure merge( left, right )
    result = empty list
    while length(left) > 0 and length(right) > 0 do
        if left[0] <= right[0] then
            append left[0] to result
            remove left[0] from left
        else
            append right[0] to result
            remove right[0] from right
        end if
    end while
    append remaining elements of left and right to result
    return result
end procedure
```
**Time Complexity:** Worst-case $O(n \log n)$, Average-case $O(n \log n)$, Best-case $O(n \log n)$. Highly consistent performance. Space complexity is $O(n)$.

## 5. Quick Sort

Quicksort is an efficient, general-purpose sorting algorithm. It is also a divide-and-conquer algorithm.

It works by selecting a 'pivot' element from the array and partitioning the other elements into two sub-arrays, according to whether they are less than or greater than the pivot. The sub-arrays are then sorted recursively. This can be done in-place, requiring small additional amounts of memory to perform the sorting.

**Pseudocode:**
```text
procedure quickSort( A, low, high )
    if low < high then
        pi = partition(A, low, high)
        quickSort(A, low, pi - 1)
        quickSort(A, pi + 1, high)
    end if
end procedure

procedure partition( A, low, high )
    pivot = A[high]
    i = low - 1
    for j = low to high - 1 do
        if A[j] < pivot then
            i = i + 1
            swap(A[i], A[j])
        end if
    end for
    swap(A[i + 1], A[high])
    return i + 1
end procedure
```
**Time Complexity:** Worst-case $O(n^2)$ (rare, usually when list is already sorted and pivot choice is poor), Average-case $O(n \log n)$, Best-case $O(n \log n)$. Often faster in practice than other $O(n \log n)$ algorithms.
