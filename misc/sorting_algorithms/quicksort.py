import numpy as np

my_array = np.random.rand(100)
"""
implementation of quicksort. Select an element (pivot) of the array and put all smaller elements to the left and all bigger elements to the right.
This has O(n^2) worst-case complexity. Worst case happens when the selected pivot is the smallest or biggest element. 
The complexity equation becomes O(n) = O(n-1)+c(n) where c(n) has complexity O(n). If this happens recursively, we get a complexity of O(n^2) in the end.
Choosing the pivot at random minimizes the risk of encountering the worst-case scenario repeatedly. 
Therefor the complexity equation approches O(n) = 2*O(n/2)+c(n) where c(n) has comlpexity O(n). In the end, it approaches a complexity of O(n log(n))
"""

def partition(array, low, high):
    global counter

    pivot = np.random.randint(low, high) # Choosing the pivot at random minimizes chances of worst-case scenario

    # Need to place pivot at the end or problems when iterating over elements
    temp = array[high]
    array[high] = array[pivot]
    array[pivot] = temp
    pivot = high

    i = low

    for j in range(low, high):
        if array[j]<array[pivot]:
            temp = array[i]
            array[i] = array[j]
            array[j] = temp
            i += 1
    if i<pivot:
        temp = array[i]
        array[i] = array[pivot]
        array[pivot] = temp
    return i

def quicksort(array, low, high):

    index = partition(array, low, high)

    if low<index-1:
        quicksort(array, low, index-1)
    if index+1<high:
        quicksort(array, index+1, high)

quicksort(my_array, 0, len(my_array)-1)
print(my_array)
