# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from abc import ABC, abstractmethod
import time
import sys

# Abstract class - every algorithm must implement the getName() method
class Algorithm(ABC):     

    def __init__(self, dataModel) -> None:
        self.__dataModel = dataModel


    @abstractmethod
    def getName(self): pass 


    def __haltAlgorithm(self, delay, interval):
        i = 0 
        while(i < delay):
            self.__stopCheck() 
            # Checks if the GUI thread is holding the pause lock
            if(self.__dataModel.isPaused()): self.__pauseAlgorithm()
            time.sleep(interval) 
            i += interval  


    def delay(self):
        delay = self.__dataModel.getDelay()
        self.__haltAlgorithm(delay, delay / 10)


    # Used to check is the algorithm needs to halt
    def __stopCheck(self): 

        # Checks if the algorithm needs to stop
        if(self.__dataModel.isStopped()): 
            # Output message confirming thread termination
            print("Algorithm Thread has terminated safely") 
            # Exit thread
            sys.exit() 


    def __pauseAlgorithm(self):
        # Attempts to acquire lock, pausing the thread
        self.__dataModel.acquireLock()
        # If the lock is not released then the GUI thread will freeze next time pause button is pressed
        self.__dataModel.releaseLock()


    # Sort and display array on screen
    def sortArray(self, delay:bool=True):
        self.__dataModel.sortArray()
        self.__dataModel.updateArrayOnScreen()
        if(delay):
            # Pauses algorithm for short amount of time 
            self.__haltAlgorithm(0.5, 0.1)


    # Shuffle and display array on screen
    def shuffleArray(self, delay:bool=True):
        self.__dataModel.shuffleArray()
        self.__dataModel.updateArrayOnScreen()  
        if(delay):
            # Pauses algorithm for short amount of time 
            self.__haltAlgorithm(0.5, 0.1)


    # Refreshes screen to display any changes to the array
    def updateArrayOnScreen(self):
        self.__dataModel.updateArrayOnScreen() 


    # Returns array
    def getArray(self):
        return self.__dataModel.getArray()


    # Returns the target
    def getTarget(self):
        return self.__dataModel.getTarget() 


    # Change colour of bar at specified index to colour given
    def changeBarColour(self, index : int, colour : str):
        self.__dataModel.setBarColour(index, colour)


    # Swaps elements at the specified index 
    def swapElements(self, sourceIdx, destIdx):
        self.__dataModel.swapElements(sourceIdx, destIdx)


    # Swaps the bar colours at the specified indexes
    def swapBarColours(self, sourceIdx, destIdx): 
        self.__dataModel.swapBarColours(sourceIdx, destIdx) 


    # Returns the element at the specified index
    def getElement(self, index : int) -> int:
        return self.__dataModel.getElementAtIndex(index) 


    # Changes the element at the specified index to the specified value 
    def changeElement(self, index : int, value : int) -> None:
        self.__dataModel.changeElement(index, value)


    # Checks if elements need to be swapped 
    def isSwapNeeded(self, sourceIdx : int, destIdx : int) -> bool: 
        # If the sorting is in ascending order
        if(self.__dataModel.isAscending()):
            return self.getElement(sourceIdx) > self.getElement(destIdx) 
        # If sorting is in descending order 
        else: return self.getElement(sourceIdx) < self.getElement(destIdx) 


    # Checks if elements at the specified indexes are equal
    def areElementsEqual(self, sourceIdx : int, destIdx : int) -> bool: 
        return self.getElement(sourceIdx) == self.getElement(destIdx)


    # Plays a cool animation when the array is sorted
    # It alternates between colouring the bars green and black
    def coolEndingAnimation(self):
        for _ in range(3):
            self.updateArrayOnScreen() 
            self.__haltAlgorithm(0.5, 0.5) 
            self.__setAllBarColoursGreen() 
            self.updateArrayOnScreen() 
            self.__haltAlgorithm(0.5, 0.5)


    # Changes the colour of each bar to green 
    def __setAllBarColoursGreen(self): 
        for i in range(len(self.getArray())):
            self.changeBarColour(i, "green")


    # Used to check constructor implementation
    def getDataModel(self):
        return self.__dataModel
    
# Listen to American Idiot by Green Day