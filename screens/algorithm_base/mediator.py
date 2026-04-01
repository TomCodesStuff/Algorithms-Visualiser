import sys
import time
from typing import Callable
from .thread_handler import ThreadHandler


class Mediator():
    def __init__(self, delayFunc : Callable, updateScreenFunc : Callable, threadHandler : ThreadHandler): 
        self.__delayFunc = delayFunc
        self.__updateScreenFunc = updateScreenFunc
        self.__threadHandler = threadHandler
        

    def getDelay(self) -> float:  
        print(self.__delayFunc())
        return self.__delayFunc() 


    def refreshScreen(self) -> None: 
        self.__updateScreenFunc() 


    def __pauseAlgorithm(self):
        # Attempts to acquire lock, pausing the thread
        self.__threadHandler.acquirePauseLock()
        # If the lock is not released then the GUI thread will freeze next time pause button is pressed
        self.__threadHandler.releasePauseLock()

    
    # Used to check is the algorithm needs to halt
    def __hasAlgorithmStopped(self): 
        # Checks if the algorithm needs to stop
        if(self.__threadHandler.hasAlgorithmStopped()): 
            # Output message confirming thread termination
            print("Algorithm Thread has terminated safely") 
            # Exit thread
            sys.exit(0) 


    def __delayAlgorithm(self, delay : float) -> None:
        interval = delay / 10
        i = 0 
        while(i < delay):
            self.__hasAlgorithmStopped() 
            # Checks if the GUI thread is holding the pause lock
            if(self.__threadHandler.isAlgorithmPaused()): self.__pauseAlgorithm()
            time.sleep(interval) 
            i += interval  


    def briefDelay(self) -> None: 
        self.__delayAlgorithm(0.5)


    def delay(self) -> None:  
        self.__delayAlgorithm(self.getDelay())


# Listen to Weak by Skunk Anansie
