import sys
import time
from typing import Callable
from .thread_handler import ThreadHandler


class Mediator():
    def __init__(self, delayFunc : Callable, updateScreenFunc : Callable, threadHandler : ThreadHandler): 
        self.__delayFunc = delayFunc
        self.__updateScreenFunc = updateScreenFunc
        self.__threadHandler = threadHandler


    def getDelay(self) -> None: 
        return self.__delayFunc() 


    def updateScreen(self) -> None: 
        self.__updateScreenFunc() 


    def __pauseAlgorithm(self):
        # Attempts to acquire lock, pausing the thread
        self.__threadHandler.acquirePauseLock()
        # If the lock is not released then the GUI thread will freeze next time pause button is pressed
        self.__threadHandler.releasePauseLock()

    
    # Used to check is the algorithm needs to halt
    def __stopCheck(self): 
        # Checks if the algorithm needs to stop
        if(self.__threadHandler.hasAlgorithmStopped()): 
            # Output message confirming thread termination
            print("Algorithm Thread has terminated safely") 
            # Exit thread
            sys.exit(0) 


    def haltAlgorithm(self) -> None:  
        delay = self.getDelay() 
        interval = delay / 10
        i = 0 
        while(i < delay):
            self.__stopCheck() 
            # Checks if the GUI thread is holding the pause lock
            if(self.__threadHandler.isAlgorithmPaused()): self.__pauseAlgorithm()
            time.sleep(interval) 
            i += interval  


# Listen to Weak by Skunk Anansie
