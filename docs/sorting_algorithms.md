## Sorting Algorithms:

This table below shows the searching algorithms visualised by AVA. <br>
For each algorithm, instructional steps are provided which can be followed to produce working implementations.

| Algorithm                                     |
| --------------------------------------------- |
| [Bogo Sort](#bogo-sort)                       |
| [Brick Sort](#brick-sort)                     | 
| [Bubble Sort](#bubble-sort)                   |
| [Cocktail Shaker Sort](#cocktail-shaker-sort) |
| [Gnome Sort](#gnome-sort)                     |
| [Insertion Sort](#insertion-sort)             |
| [Merge Sort](#merge-sort)                     |
| [Quick Sort](#quick-sort)                     |
| [Selection Sort](#selection-sort)             |
| [Tim Sort](#tim-sort)                         |

---
### Bogo Sort:

Algorithm Steps: 

1. While array is not sorted:
2. Randomly shuffle array 
3. If array is sorted: <br> 
    \- Stop Algorithm.
4. Go to Step one. 

#### Time-Space Complexities: 

Time Complexity: O((n + 1)!)<br>
Space Complexity: O(1)

---
### Brick Sort 

Algorithm steps:

1. Set a variable `swapped = True`  
2. While swapped is True: 
3. Set `swapped = False` 
4. for i in range(1, array.length() - 1, 2) 
5. If isSwapNeeded(array[i], array[i + 1]): <br>
    \- swap(array[i], array[i + 1]). <br>
    \- Set `swapped = True `
6.  for i in range(0, array.length() - 1, 2) 
7. If isSwapNeeded(array[i], array[i + 1]): swap(array[i], array[i + 1]). Set `swapped = True`
8. Go to Step 2.

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1) 

---
### Bubble Sort:

Algorithm steps: 

1. for i in range(0, array.length())
2. Set a variable `swapped = False`
3. for j in range(0, array.length() - i - 1) 
4. if isSwapNeeded(arrsy[j], array[j + 1]): <br>
    \- swap(array[j], array[j + 1]). <br> 
    \- Set `swapped = True`
6. if swapped == False: Array is sorted, return 0

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>) <br>
Space Complexity: O(1)

#### End of unsorted array formula: 

$$ index = n - i - 1$$

n -> length of the array <br>
i -> index of current element 

---
### Cocktail Shaker Sort 

Algorithm steps:

1. Set a variable `swapped = True` 
2. While swapped = True: 
3. Set `swapped = False`
4. for i in range(0, array.length() - 1)
5. If isSwapNeeded(array[i], array[i + 1]): <br>
    \- swap(array[i], array[i + 1]). <br> 
    \- Set `swapped = True`
6. If swapped = False. Array is sorted, return 0. 
7. for i in range(array.length() - 1, 1)
8. If isSwapNeeded(array[i], array[i - 1]): <br>
    \- swap(array[i], array[i - 1]). <br>
    \- Set `swapped = True`
9. If swapped = False. Array is sorted, return 0. 

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1) 

---
### Gnome Sort 

Algorithm steps:

1. Set a variable `pos = 0` 
2. While pos < array.length(): 
3. If pos = 0: `pos = pos + 1` 
4. If isSwapNeeded(array[pos], array[pos - 1]): <br>
    \- swap(array[pos], array[pos - 1]). <br>
    \- Set `pos = pos - 1`
5. Else: Set `pos = pos + 1` 

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1) 

---
### Insertion Sort:

Algorithm Steps: 

1. for i in range(1, array.length()):
2. Set variable `j = i`
3. while j > 0 AND isSwapNeeded(array[j - 1], array[j]): <br> 
    \- swap(array[j - 1], array[j]).<br> 
    \- Set `j = j - 1`
4. Go to Step 3.

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1)

---
### Merge Sort:

Algorithm Steps:

1. Repeatedly split the array into sub-arrays containing only one element 
2. Take pairs of sub-arrays
3. Merge both sub-arrays by comparing elements, creating a new larger sub-array.  
4. Repeat the merging process creating larger sorted sub-arrays 
5. Continue until only one sorted array remains 

#### Time-Space Complexities: 

Time Complexity: O(n log n) <br>
Space Complexity: O(n)


#### A note on the Space Complexity 

An O(1) space complexity can be achieved by merging the sub arrays in-place. 

---
### Quick Sort:

Algorithm Steps: 

1. Set a variable `low = 0`  
2. Set a variable `high = array.length() - 1`
3. Set a variable `pivot = medianOfThree(array, low, high)` [(See Median Of Three)](#median-of-three) 
4. for each element in the array:
5. If element < array[pivot]: Shift element to the left of the pivot
6. if element > array[pivot]: Shift element to the right of the pivot
7. Select two new pivots: <br>
    \- `Pivot One = medianOfThree(array, low, pivot - 1)` <br>
    \- `Pivot Two = medianOfThree(array, pivot + 1, high)`
8. If low > pivot - 1 AND pivot + 1 > high. Array is sorted, return 0 
9. Else: Go to Step 4. Using Pivot One and Pivot Two. 

#### Time-Space Complexities: 

Time Complexity: O(n log n) <br>
Space Complexity: O(1)  

#### A note on the Time Complexity 

If the pivot is not chosen efficiently, the worst case time complexity becomes O(n<sup>2</sup>)

#### Median of three

function medianOfThree(array, low, high): 
1. Set variable `mid = (low + high) // 2` 
2. Set variable `pivotValues = [array[low], array[mid], array[high]]` 
3. sort(pivotValues) 
4. Set variable `median = pivotValues[1]` 
5. return median

---
### Selection Sort:

Algorithm Steps: 

1. Iterate through the array
2. Set a variable called minIdx to the current index
3. In a nested loop from the current index plus one to the end of the array
4. Find the index of the smallest element and store it in minIdx 
5. Shift all elements between the current index and the smallest element index one place right 
6. Place the smallest element into the current index

#### Time-Space Complexities: 

Time Complexity: O(n<sup>2</sup>)<br>
Space Complexity: O(1)

---
### Tim Sort:

Algorithm Steps: 

1. Set variable `runSize = calculateRunSize()`  
2. Perform Insertion Sort on each run 
3. Perform Merge Sort (The starting sub-arrays are the sorted runs). 

#### Time-Space Complexities: 

Time Complexity: O(n log n)<br>
Space Complexity: O(n) 

#### A note on the Space Complexity 

An O(1) space complexity can be achieved by merging the sub arrays in-place. 

#### Calculating run size 

Tim sort calculated the run size between the rangge of 32 - 64 (inclusive). <br>
For arrays that are smaller than 64, the algorithm just performs an insersion sort on the whole array. <br>
The process Tim Sort uses to calculate the run size can be found [here.](https://en.wikipedia.org/wiki/Timsort)

--- 

Go to [README.md](../README.md)