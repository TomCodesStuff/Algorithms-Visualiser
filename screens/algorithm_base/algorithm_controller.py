from __future__ import annotations
from typing import Callable

# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()
 
from typing import TYPE_CHECKING, TypeVar, Generic
from .mediator import Mediator
from .thread_handler import ThreadHandler 
from data_structures import DataStructure
from enums import AlgorithmType

# TODO -> make function to repeatedly check when algorithm done (done)
#      -> when done toggle widgets -> make cool animations clear variables (make abstract method) (do later)
#      -> add generic type hinting for DataStructure (done)
#      -> fix linear search and test running, pausing, stopping, adjusting delay (done)
#      -> fix other algorithms (in progress)

if TYPE_CHECKING:
    from algorithm_base import AlgorithmScreen, AlgorithmModel


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
    

    def startAlgorithmThread(self, algorithmType : AlgorithmType, algorithmName : str) -> None:    
        algorithmClass = self.getScreen().getWindow().getAlgorithmClass(algorithmType, algorithmName) 
        if algorithmClass is None: return 
        mediator = Mediator(self.getAlgorithmDelay, self.scheduleScreenUpdate, self.__threadHandler)
        
        try:
            algorithmObj = algorithmClass()
        except Exception as e: 
            print(f"ERROR: Unable to create algorithm object: {e}")
            self.getScreen().algorithmComplete()
            return
        
        try:
            algorithmObj.setDataStructure(self.getDataStructure())
            algorithmObj.setMediator(mediator)
        except Exception as e:
            self.getScreen().algorithmComplete()
            print(f"ERROR: {e}")
            return
        
        self.__threadHandler.startAlgorithm(algorithmObj)
        self.__handleAlgorithmExecution()


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


    def updateAlgorithmDelay(self, delay : float) -> None: 
        self.__threadHandler.acquireDelayLock() 
        self.__model.setDelay(delay)
        self.__threadHandler.releaseDelayLock() 


    def getAlgorithmDelay(self) -> float:
        self.__threadHandler.acquireDelayLock() 
        delay = self.__model.getDelay()
        self.__threadHandler.releaseDelayLock() 
        return delay


    def getScreen(self) -> S: return self.__screen 
    def getModel(self) -> M: return self.__model
    def getDataStructure(self) -> D: return self.__dataStructure


    def setUpdateFunction(self, updateFunc : Callable) -> None: 
        self.__updateFunc = updateFunc


    def setUpdateFunction(self, updateFunc : Callable) -> None: 
        self.__updateFunc = updateFunc


    def scheduleScreenUpdate(self) -> None:
        if self.__updateFunc is None: return
        self.__screen.getWindow().scheduleFunctionExecution(self.__updateFunc, EXECUTION_DELAY) 

    
    def __handleAlgorithmExecution(self) -> None: 
        if not self.__threadHandler.isThreadAlive(): 
            self.__updateFunc(refreshColours=False)
            self.getScreen().algorithmComplete()
        else: 
            self.__updateFunc(refreshColours=False)
            self.getScreen().getWindow().scheduleFunctionExecution(self.__handleAlgorithmExecution, EXECUTION_DELAY) 
       
    
    def isAlgorithmRunning(self) -> None: 
        return self.__threadHandler.isThreadAlive()

# Listen to Catch These Fists by Wet Leg     
