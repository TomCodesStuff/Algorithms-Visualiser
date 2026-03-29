import random
from ..data_structure import DataStructure


class Array(DataStructure): 
    # Constructor
    def __init__(self):
        super().__init__()
        self.__array = []
        self.__barColours = []


    #TODO rename functions to not have Array in title user already knows it's an array

    # Returns the array
    def get(self) -> list: 
        return self.__array  
    
    
    # Appends passed value to the array
    def append(self, value : int) -> None: 
        self.__array.append(value)
        self.__barColours.append("black")
    

    # Removes last element from the array
    def pop(self) -> None: 
        self.__array.pop()
        self.__barColours.pop()


    # Sorts the array
    def sort(self) -> None:
        self.__array.sort()


    # Shuffles the array
    def shuffle(self) -> None:
        random.shuffle(self.__array)


    # TODO implement better checking
    # Swaps the elements at the specified indexed
    def swap(self, i : int, j : int) -> None: 
        if(i >= len(self.__array) or j >= self.size()): return  
        self.__array[i], self.__array[j] =\
            self.__array[i], self.__array[j]
    

    # TODO implement better checking
    # Swaps the colour values of the two indexes specified
    def swapColours(self, i : int, j : int) -> None: 
        if(i >= len(self.__barColours) or j >= self.size()): return  
        self.__barColours[i], self.__barColours[j] =\
            self.__barColours[i], self.__barColours[j]
    

    # Changes the element at the specified index to the passed value
    def setAt(self, index : int, value : int) -> None: 
        if(index >= self.getArraySize()): return
        self.__array[index] = value
    

    # Returns element at the specified index 
    def getAt(self, index : int) -> int:
        return self.__array[index]


    # Gets the colour of the bar the index passed
    def getColourAt(self, index : int) -> str:
        if(index >= len(self.__array)): return "" 
        else: return self.__barColours[index]
    

    # Sets the bar colour at the specified index to the specified colour
    def setColourAt(self, index : int, colour: str) -> None: 
        if(index >= len(self.__array)): return 
        else: self.__barColours[index] = colour


    # Resets all the bars colours to the default (black)
    def resetBarColours(self) -> None: 
        self.__barColours = ["black" for _ in range(len(self.__array))] 
    
    
    # Returns the size of the array
    def size(self) -> int:
        return len(self.__array)


    # Returns the smallest element in the array
    def getMin(self) -> int:
        return min(self.__array)


    # Returns the largest element in the array 
    def getMax(self) -> int:
        return max(self.__array)


    # Returns true if passed value is in the array, else false
    def isInArray(self, value : int) -> bool: 
        return value in self.__array


# Listen to Everlong By Foo Fighters
        