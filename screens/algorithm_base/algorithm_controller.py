from __future__ import annotations

# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()
 
from typing import TYPE_CHECKING, TypeVar, Generic
from .thread_handler import ThreadHandler

if TYPE_CHECKING:
    from algorithm_base import AlgorithmScreen, AlgorithmModel, AlgorithmDataModel

S = TypeVar("S", bound="AlgorithmScreen")
M = TypeVar("M", bound="AlgorithmModel")
D = TypeVar("D", bound="AlgorithmDataModel")


class AlgorithmController(Generic[S, M, D]):  

    def __init__(self, screen : S, model : M, dataModel : D):
        self.__screen = screen
        self.__model = model
        self.__dataModel = dataModel
        self.__threadHandler = ThreadHandler()

    # TODO
    # Cancels any scheduled function calls left by a terminated thread
    def cancelScheduledProcesses(self):
        # If there are still processed scheduled from the terminated thread
            if(self.__screen.getWindow().getNumScheduledFunctions() > 0):  
                # Stop all processes 
                self.__screen.getWindow().cancelScheduledFunctions()   
    

    def startAlgorithmThread(self, algorithmChoice : str, algorithmType : str) -> None: 
        print("START ALgorithm")
        #self.__threadHandler.startAlgorithm(algorithmChoice, algorithmType)


    def stopAlgorithmThread(self) -> None: 
        self.__threadHandler.setAlgorithmStopFlag() 
        if self.__threadHandler.isAlgorithmPaused(): 
            self.__threadHandler.relasePauseLock() 
    

    def resumeAlgorithm(self) -> None: 
        self.__threadHandler.relasePauseLock() 


    def pauseAlgorithm(self) -> None: 
        self.__threadHandler.acquirePauseLock() 
    

    def isAlgorithmPaused(self) -> bool: 
        return self.__threadHandler.isAlgorithmPaused()
    
    
    def isAlgorithmRunning(self) -> bool: 
        return self.__threadHandler.isThreadAlive()

    
    # TODO 
    # Schedule function to redraw array after a certain amount of time 
    # Prevents the canvas flickering as updating is done by the main GUI thread
    def scheduleArrayUpdate(self):
        self.__screen.getWindow().scheduleFunctionExecution(self.displayArray, 0)
    