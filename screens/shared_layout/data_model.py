import random
import threading

# This class contains solely the data and functions algorithms need to run 
# This is kept seperate from the SearchModel class to add more abstraction
class SharedDataModel():
    # Constructor
    def __init__(self):
        self.__controller = None
        self.__array = []
        self.__barColours = []
        self.__target = None
        self.__targetSetting = 0
        self.__isAscending = True
        self.__delay = None 
        self.__delayLock = threading.Lock()

    # Sets controller attribute to value passed
    def addController(self, controller):
        if(self.__controller is None):
            self.__controller = controller
    
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


    # Updates the screen so changes to the array are shown
    def updateArrayOnScreen(self) -> None:
        self.__controller.scheduleArrayUpdate() 


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
    
    # Gets the delay (time algorithm is paused for)
    def getDelay(self) -> int:
        self.__delayLock.acquire()  
        delay = self.__delay
        self.__delayLock.release()
        return delay
    
    # Sets the delay to the passed integer
    def setDelay(self, value : int) -> None:
        self.__delayLock.acquire()
        self.__delay = value  
        self.__delayLock.release()
    
    # Returns the target (the element being looked for)
    def getTarget(self) -> int: 
        return self.__target
    
    # Sets the element being looked for to the passed value
    def setTarget(self, value : int) -> None:
        self.__target = value   


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
    
    # Updates the target setting to the passed value
    def setTargetSetting(self, value : int) -> None:
        self.__targetSetting = value
    
    # Returns the current value of the target setting 
    def getTargetSetting(self) -> int:
        return self.__targetSetting
    
    # Toggles the sort setting between and ascending and descending
    def toggleSortDirection(self):
        self.__isAscending = not self.__isAscending
    
    # Returns if the sorting direction is ascending or descending
    def isAscending(self) -> bool: return self.__isAscending 

# Listen to Everlong By Foo Fighters