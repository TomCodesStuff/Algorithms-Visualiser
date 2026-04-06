## Searching Algorithms:  

This table below shows the searching algorithms visualised by AVA. <br>
For each algorithm, instructional steps are provided which can be followed to produce working implementations.


| Algorithm:                                    |
| --------------------------------------------- |
| [Binary Search](#binary-search)               | 
| [Exponential Search](#exponential-search)     | 
| [Fibonacci Search](#fibonacci-search)         | 
| [Interpolation Search](#interpolation-search) |
| [Jump Search](#jump-search)                   |
| [Linear Search](#linear-search)               | 
| [Tenary Search](#tenary-search)               |    

---
### Binary Search: 

#### Algorithm Steps:

1. Sort array.
2. Set variable `low = 0`
3. Set variable `high = array.length() - 1` 
4. While low <= high: 
5. Set variable `mid = (low + high) / 2`
6. If `array[mid] == target`. Target has been found, return 0
7. If array[mid] > target: `low = mid + 1` 
8. If array[mid] < target: `high = mid - 1` 
9. Go to Step 3.
10. If target is not in array, return 1 

#### Time-Space Complexities: 

Time complexity: O(log n)<br>
Space Complexity: O(1)

#### Midpoint Calcuation Formula: 

$$mid = {(low + high) \div 2}$$

---
### Exponential Search:

### Algorithm Steps:

1. If array[0] == target: Target has been found. Return 0. 
2. Set variable `i = 1` 
3. Set variable `n = array.length()` 
4. While i < n AND array[i] <= target:
5. `i = i * 2` 
6. Go to Step 4.
7. Perform a [binary search](#binary-search) where `low = i / 2` and `high = min(i, n - 1)`.

#### Time-Space Complexities:

Time Complexity: O(log n) <br>
Space Complexity: O(1) 

#### Binary Search Low:


$$low = {i \div 2}$$

#### Binary Search High:

$$high = {\min(i,\;n-1)}$$

---
### Fibonacci Search: 

#### Algorithm Steps: 

1. Set variable `fibN = First Fibonacci number >= array.length()`
2. Set variable `fibMin1 = Fibonnaci Number before FibN`
3. Set variable `fibMin2 = Fibonnaci Number before FibMin1`
4. Set variable `offset = -1` 
5. Set variable `n = array.length()` 
6. While fibN > 1: 
7. Set variable `index = min(offset + fibMin2, n - 1)`
8. If array[index] < target:  `offset = index`, `fibN = fibMin1`, `fibMin1 = fibMin2`, `fibMin2 = fibN - fibMin1`.   
9. If array[index] > target: `fibN = fibMin2`,  `fibMin1 = fibMin1 - fibMin2`, `fibMin2 = fibN - fibMin1`   
10. Else: Target has been found, return 0 
11. Gi to Step 6.
12. If fibMin1 > 0 AND array[array.length() -1] == target: Target found, return 0 
13. Return 1

#### Time-Space Complexities:

Time Complexity: O(log n) <br>
Space Complexity: O(1) 

#### Index Calculation Formula:

$$index = {\min(offset + fibMin2,\;n-1)}$$

---
### Interpolation Search: 

#### Algorithm Steps:

1. Set a variable `low = 0` 
2. Set a variable `high = array.length() - 1 ` 
3. While low <= to high AND target >= array[low] AND target <= array[high] 
4. Set variable `pos = (See Position Formula)` 
5. If array[pos] == target. Target is found, return 0 
6. If array[pos] > target: `high = pos - 1` 
7. If array[pos] < target: `low = pos + 1` 
8. Go to step 7. 
9. Target not found, return 1

#### Time-Space Complexities:

Time Complexity: O(log (log n)) <br>
Space Complexity: O(1) 

#### Position Formula:

$$pos = {low+{(target-array[low])\times(high - low)\over(array[high]-array[low])}}$$

---
### Jump Search: 

#### Algorithm Steps:

1. Set variable `step = sqrt(array.length())`
2. Set variable `prev = 0` 
3. While step < array.length() AND array[min(step, array.length()) -1] < target:  
4. `prev = step`, `step = step + sqrt(array.length())`. 
5. If prev >= array.length(): Target can not be found, return 1.  
6. Go to step 3. 
7. for each index `i` from `prev` to `prev + sqrt(array.length())` 
8. If array[i] == target: Target has been found, return 0
9. if array[i] > target: Target can not be found, return 1. 
10. Go to Step 7.

#### Time-Space Complexities:

Time Complexity: O($\sqrt{n}$)<br>
Space Complexity: O(1)

---
### Linear Search:

#### Algorithm Steps:<br>

1. For each index `i` in array.
2. If array[i] == target: Target has been found, return 0
3. Go to Step 1.
4. Target has not been found, return 1.

#### Time-Space Complexities:

Time Complexity: O(n)<br>
Space Complexity: O(1)

---
### Tenary Search:

#### Algorithm Steps: 

1. Set variable `left = 0`
2. Set variable `right = array.length() - 1` 
3. While left <= right: 
4. Set variable `mid1 = left + (right - left) / 3`
5. Set variable `mid2 = right - (right - left) / 3`
6. If array[mid1] == target OR array[mid2] == target: Target has been found, return 0 
7. If array[mid1] < target: `right = mid1 - 1` 
8. Else If array[mid2] > target: `left = mid2 + 1`
9. Else: `left = mid1 + 1`, `right = mid2 - 1` 
10. Go to Step 3.
11. Target can not be found, return 1 

#### Time-Space Complexities:

Time Complexity: O(log<sub>3</sub>n) <br>
Space Complexity: O(1) 

#### Mid Point #1 Formula:

$mid1 = {left + (right - left) \div 3}$

#### Mid Point #2 Formula: 

$mid2 = {right - (right - left) \div 3}$

---

Go to [README.md](../README.md)
