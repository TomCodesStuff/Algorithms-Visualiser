import random
from ..algorithm_base import DataStructure


class Array(DataStructure): 
    # Constructor
    def __init__(self):
        super().__init__()
        self.__array = []
        self.__barColours = []


    #TODO rename functions to not have Array in title user already knows it's an array

    # Returns the array
    def getArray(self) -> list: 
        return self.__array  
    
    
    # Appends passed value to the array
    def appendArray(self, value : int) -> None: 
        self.__array.append(value)
        self.__barColours.append("black")
    

    # Removes last element from the array
    def popArray(self) -> None: 
        self.__array.pop()
        self.__barColours.pop()


    # Sorts the array
    def sortArray(self) -> None:
        self.__array.sort()


    # Shuffles the array
    def shuffleArray(self) -> None:
        random.shuffle(self.__array)


    # Swaps the elements at the specified indexed
    def swapElements(self, sourceIndex : int, destinationIndex : int) -> None: 
        if(sourceIndex >= len(self.__array) or destinationIndex >= self.getArraySize()): 
            return  
        self.__array[sourceIndex], self.__array[destinationIndex] =\
            self.__array[destinationIndex], self.__array[sourceIndex]
    

    # Swaps the colour values of the two indexes specified
    def swapBarColours(self, sourceIndex : int, destinationIndex : int) -> None: 
        if(sourceIndex >= len(self.__barColours) or destinationIndex >= self.getArraySize()): 
            return  
        self.__barColours[sourceIndex], self.__barColours[destinationIndex] =\
            self.__barColours[destinationIndex], self.__barColours[sourceIndex]
    

    # Changes the element at the specified index to the passed value
    def changeElement(self, index : int, value : int) -> None: 
        if(index >= self.getArraySize()): return
        self.__array[index] = value
    

    # Returns element at the specified index 
    def getElementAtIndex(self, index : int) -> int:
        return self.__array[index]


    # Gets the colour of the bar the index passed
    def getBarColour(self, index : int) -> str:
        if(index >= len(self.__array)): return "" 
        else: return self.__barColours[index]
    

    # Sets the bar colour at the specified index to the specified colour
    def setBarColour(self, index : int, colour: str) -> None: 
        if(index >= len(self.__array)): return 
        else: self.__barColours[index] = colour


    # Resets all the bars colours to the default (black)
    def resetBarColours(self) -> None: 
        self.__barColours = ["black" for _ in range(len(self.__array))] 
    
    
    # Returns the size of the array
    def getArraySize(self) -> int:
        return len(self.__array)


    # Returns the smallest element in the array
    def getSmallestElement(self) -> int:
        return min(self.__array)


    # Returns the largest element in the array 
    def getLargestElement(self) -> int:
        return max(self.__array)


    # Returns true if passed value is in the array, else false
    def isElementInArray(self, value : int) -> bool: 
        return value in self.__array


# Listen to Everlong By Foo Fighters
        