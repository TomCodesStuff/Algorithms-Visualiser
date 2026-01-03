import threading


class ThreadHandler():
    def __init__(self):
        self.__algorithmThread = None 
        self.__algorithmStopped = threading.Event()
        self.__algorithmPauseLock = threading.Lock()
        self.__delayLock = threading.Lock() 
    

    def isThreadAlive(self) -> bool:
        return self.__algorithmThread and self.__algorithmThread.is_alive()


    def setAlgorithmStopFlag(self) -> None:
        self.__algorithmStopped.set() 
    

    def clearAlgorithmStopFlag(self) -> None:
        self.__algorithmStopped.clear() 
    

    def hasAlgorithmStopped(self) -> bool: 
        return self.__algorithmStopped.is_set() 


    def acquirePauseLock(self) -> None:
        self.__algorithmPauseLock.acquire()
    

    def relasePauseLock(self) -> None: 
        self.__algorithmPauseLock.release()  
    

    def isAlgorithmPaused(self) -> bool:
        return self.__algorithmPauseLock.locked() 


    def acquireDelayLock(self) -> None: 
        self.__delayLock.acquire() 
    

    def releaseDelayLock(self) -> None: 
        self.__delayLock.release()
    
    def startAlgorithm(self, algorithmChoice : str, algorithmType : str) -> None: 
        # Sets flag indicating the algorithm needs to halt to false
        if(self.hasAlgorithmStopped()): self.clearAlgorithmStopFlag()  
        # Call algorithm -> so this program actually has a use
        self.__algorithmThread = threading.Thread(target=callAlgorithm, 
                                                    args=(self.__dataModel, self.__mediator, 
                                                          algorithmChoice, algorithmType))
        # Start Thread
        self.__algorithmThread.start() 

    

