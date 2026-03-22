from __future__ import annotations

# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()
 
from typing import TYPE_CHECKING, TypeVar, Generic
from .mediator import Mediator
from .thread_handler import ThreadHandler

if TYPE_CHECKING:
    from algorithm_base import AlgorithmScreen, AlgorithmModel, DataStructure


S = TypeVar("S", bound="AlgorithmScreen")
M = TypeVar("M", bound="AlgorithmModel")
D = TypeVar("D", bound="DataStructure")

EXECUTION_DELAY = 0

class AlgorithmController(Generic[S, M, D]):  

    def __init__(self, screen : S, model : M, dataStructure : D):
        self.__screen = screen
        self.__model = model
        self.__dataStructure = dataStructure
        self.__threadHandler = ThreadHandler() 

        # TODO create some abstract methods to make sure these are defined
        self.__updateFunc = None


    # Cancels any scheduled function calls left by a terminated thread
    def cancelScheduledProcesses(self):
        # If there are still processed scheduled from the terminated thread
            if(self.__screen.getWindow().getNumScheduledFunctions() > 0):  
                # Stop all processes 
                self.__screen.getWindow().cancelScheduledFunctions()   
    

    def startAlgorithmThread(self, algorithmChoice : str, algorithmType : str) -> None:  
        mediator = Mediator(self.getAlgorithmDelay, self.scheduleScreenUpdate, self.__threadHandler)
        self.__threadHandler.startAlgorithm(algorithmChoice, algorithmType)


    def stopAlgorithmThread(self) -> None: 
        self.cancelScheduledProcesses()
        self.__threadHandler.stopAlgorithm()

        self.__threadHandler.setAlgorithmStopFlag() 
        if self.__threadHandler.isAlgorithmPaused(): 
            self.__threadHandler.releasePauseLock() 
    

    def resumeAlgorithm(self) -> None: 
        self.__threadHandler.releasePauseLock() 


    def pauseAlgorithm(self) -> None: 
        self.__threadHandler.acquirePauseLock() 
    

    def isAlgorithmPaused(self) -> bool: 
        return self.__threadHandler.isAlgorithmPaused()
    
    
    def isAlgorithmRunning(self) -> bool: 
        return self.__threadHandler.isThreadAlive()


    def updateAlgorithmDelay(self, value : float) -> None: 
        self.__threadHandler.acquireDelayLock() 
        self.__model.setDelay(value)
        self.__threadHandler.releaseDelayLock() 


    def getAlgorithmDelay(self) -> float:
        self.__threadHandler.acquireDelayLock() 
        delay = self.__model.getDelay()
        self.__threadHandler.releaseDelayLock() 
        return delay


    def getScreen(self) -> S: return self.__screen 
    def getModel(self) -> M: return self.__model
    def getDataStructure(self) -> D: return self.__dataStructure


    def scheduleScreenUpdate(self) -> None:
        self.__screen.getWindow().scheduleFunctionExecution(self.__updateFunc, EXECUTION_DELAY)
    
    