# Algorithm Visualiser

Written in python by Thomas Gibson.

---
| Table of contents                                                      | 
| ---------------------------------------------------------------------- |
|   [1. Searching Algorithms](#searching-algorithms)                     |  
|   [2. Sorting Algorithms](#sorting-algorithms)                         |
|   [3. Adding a new Search Algorithm](#adding-a-new-search-algorithm)   |
|   [4. Adding a new Sorting Algorithm](#adding-a-new-sorting-algorithm) |
|   [5. The Algorithm class](#algorithm-class)                           |
|   [6. The DataModel class](#datamodel-class)                           |


## Searching Algorithms 

A full list of implmeneted Searching algorithms can be found [here](./algorithms/SEARCHING.md)

## Sorting Algorithms


A full list of implmeneted Sorting algorithms can be found [here](./algorithms/SORTING.md)

## Adding a new Search Algorithm
New search algorithms can be added if they meet these requirements:

| Requirement: | Description: |
| ------------ | ------------ | 
| Location     | New algorithm files must be found in the <b>algorithms/searching</b> directory | 
| File Name    | New files must be named in the following format: <b>algorithm_name_search.py.</b> <br> e.g. binary_search.py, linear_search.py |
| Class Implementation        | The algorithm must be implemented as a class. | 
| Class Name   | An algorithm class must be named in the following format: <b>AlgorithmNameSearch.</b> <br> e.g BinarySearch, LinearSearch | 
| Inheritance  | Each algorithm class must be a child of the [Algorithm class](#algorithm-class). <br> The Algorithm class must be imported (See [imports](#imports).) | 
| Constructor | Each new class must implement a constructor. (See [Constructor](#constructor)) |
| DataModel helper functions   | The DataModel class contains useful functions that will be needed (See [DataModel](#datamodel-class)) | 
| Function Naming | The function which implements the algorithm must be named in the following format: <b>algorithmNameSearch</b> <br> e.g. binarySearch and linearSearch |
| Function Implementation | Each new algorithm class must provide an implementation for the <b>getName()</b> method. (See [Algorithm class](#algorithm-class))  |
| Return value/s          | Each algorithm doesn't strictly need to return anything. <br> As a convention, 1 for success or -1 for failure should be returned | 

--- 

## Adding a new Sorting Algorithm 

New sorting algorithms can be added if they meet these requirements:

| Requirement: | Description: |
| ------------ | ------------ | 
| Location     | New algorithm files must be found in the <b>algorithms/sorting</b> directory | 
| File Name    | New files must be named in the following format: <b>algorithm_name_sort.py.</b> <br> e.g. bubble_sort.py, merge_sort.py |
| Class Implementation        | The algorithm must be implemented as a class. | 
| Class Name   | An algorithm class must be named in the following format: <b>AlgorithmNameSort.</b> <br> e.g BubbleSort, MergeSort | 
| Inheritance  | Each algorithm class must be a child of the [Algorithm class](#algorithm-class). <br> The Algorithm class must be imported (See [imports](#imports).) | 
| Constructor | Each new class must implement a constructor. (See [Constructor](#constructor)) |
| DataModel helper functions   | The DataModel class contains useful functions that will be needed (See [DataModel](#datamodel-class)) | 
| Function Naming | The function which implements the algorithm must be named in the following format: <b>algorithmNameSort</b> <br> e.g. bubbleSort and mergeSort |
| Function Implementation | Each new algorithm class must provide an implementation for the <b>getName()</b> method. (See [Algorithm class](#algorithm-class))  |
| Return value/s          | Each algorithm doesn't strictly need to return anything. <br> As a convention, 1 for success or -1 for failure should be returned | 
| Sorting in Ascending and Descending order | Code does not need to be written in an algorithms implementation to sort in ascending and descending order. A helper function in the [Algorithm class](#algorithm-class) returns True or False if two elements need to be swapped, another helper function can then be called to make this swap. |  

--- 

### Imports:

```python 
from algorithms import Algorithm 
```
<i> Import statement needed to import Algorithm parent class </i>

--- 

### Constructor 

```python 
def __init__(self, dataModel):
        super().__init__(dataModel)
```
<i> Constructor required (See [DataModel](#datamodel-class)) </i>

---

## Algorithm class: 

The algorithm class is a wrapper for some of the [DataModel](#datamodel-class) class functions. <br>
These functions are needed to interact with the visualizer properly. <br>
The methods in DataModel can still be called directly (not recommended).

| Function | Parameters | Returns  | Description: |
| -------- | ---------- | -------- | ------------ |
| getName()| None       | A String, contains the name of the algorithm being implemented | An abstract method. Every subclass must provide an implementation. | 
| getArray() | None     | The array to be processed | Returns the array to be iterated over. (See [DataModel](#datamodel-class)). |
| getElement()     | index (int) : index of the element to be retieved | The value at the specified index, or -1 if the index is out of bounds | Gets the value of the element at the specified index (See [DataModel](#datamodel-class)) | 
| changeElement()  | index (int) : index of the element to be changed <br> value (int): The new value that the element is being replaced with| None | Changes the value at the specified index to the value passed (See [DataModel](#datamodel-class)) | 
| swapElements() | sourceIdx (int) : index of an element to be swapped destIdx (int): index of an element to be swapped | none | Swaps the elements at the specified indexes. (See [DataModel](#datamodel-class))|
| sortArray() | None    | delay (bool): By default there is a small delay when the array is sorted. Setting this parameter to False removed this delay | Sorts the array and refreshes the screen to display it. (See [DataModel](#datamodel-class)).| 
| shuffleArray() | None | delay (bool): By default there is a small delay when the array is shuffled. Setting this parameter to False removed this delay | Randomly shuffles the array and refreshes the screen to display it. (See [DataModel](#datamodel-class)). | 
| changeBarColour() | index (int) : Position to have the colour changed. <br> colour (str) : The new colour | None | Changes the colour of the bar at the specified index. (See [DataModel](#datamodel-class)). | 
| swapbarColours() | sourceIdx (int) : index of a bar colour to be swapped destIdx (int): index of a bar colour to be swapped | none | Swaps the bar colours at the specified indexes. (See [DataModel](#datamodel-class))|
| isSwapNeeded()   | sourceIdx (int) : index of an element to be checked. destIdx (int): index of an element to be checked | A boolean value, True if the elements need to be swapped otherwise False is returned | Checks if the elements at the passed indexes need to be swapped. (Works for both sorting in descending and ascending order) | 
| areElementsEqual() | sourceIdx (int) : index of an element to be checked. destIdx (int): index of an element to be checked | A boolean value, True if the elements at the specified index are true, else false | Compared the elements at the specified indexes and returns True if they are equal | 
| getTarget() | None    | The target to be searched for | Returns the target to be searched for. (See [DataModel](#datamodel-class)). |
| updateArrayOnScreen() | None     | None | Refreshes the screen to display any changes to the array. (See [DataModel](#datamodel-class)). |  
| delay() | None        | None     | Pauses the execution of the program using <b> time.sleep().</b> |


## DataModel class:

Useful functions, most are wrapped by the [Algorithm](#algorithm-class) class. <br>
The functions can still be called directly, if an attribute containing the DataModel class is created (not recommended). 

| Function | Parameters | Returns  | Description: |
| -------- | ---------- | -------- | ------------ |
| getArray() | None     | The array to be processed | Returns the array to be iterated over |
| getElementAtIndex()     | index (int) : index of the element to be retieved | The value at the specified index, or -1 if the index is out of bounds | Gets the value of the element at the specified index | 
| changeElement()  | index (int) : index of the element to be changed <br> value (int): The new value that the element is being replaced with| None | Changes the value at the specified index to the value passed | 
| swapElements() | sourceIndex (int) : index of an element to be swapped destinationIndex (int): index of an element to be swapped | none | Swaps the elements at the specified indexes. |
| updateArrayOnScreen() | None | None | Redraws the array on screen | 
| sortArray()    | None | None | Sorts the array and refreshes the screen to display it. |
| shuffleArray() | None | None | Randomly shuffles the array and refreshes the screen to display it. | 
| setBarColour() | index (int) : Position to have the colour changed. <br> colour (str) : The new colour | None | Changes the colour of the bar at the specified index | 
| swapbarColours() | sourceIndex (int) : index of a bar colour to be swapped destinationIndex (int): index of a bar colour to be swapped | none | Swaps the bar colours at the specified indexes. |
| isAscending()    | None | Returns True if the sorting direction is in ascending order. <br> Returns False if the sorting direction is in descending order | Returns the boolean value corresponding to the direction of the sort | 
| getTarget() | None    | The target to be searched for | Returns the target to be searched for |

---

