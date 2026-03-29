import threading


class ThreadHandler():
    def __init__(self):
        self.__algorithmThread = None 
        self.__algorithmStopped = threading.Event()
        self.__algorithmPauseLock = threading.Lock()
        self.__delayLock = threading.Lock() 


    def runAlgorithm(self): 
        # Has algorithm already -> run it via algorithm.run
        
        
        running = True
        while(running):
            print("I am Running") 
            if self.hasAlgorithmStopped(): running = False
            self.acquirePauseLock()
            self.releasePauseLock()

        print("I have stoppped")

    def isThreadAlive(self) -> bool:
        if self.__algorithmThread is None: return True 
        return self.__algorithmThread and self.__algorithmThread.is_alive()


    def setAlgorithmStopFlag(self) -> None:
        self.__algorithmStopped.set() 
    

    def clearAlgorithmStopFlag(self) -> None:
        self.__algorithmStopped.clear() 
    

    def hasAlgorithmStopped(self) -> bool: 
        return self.__algorithmStopped.is_set() 


    def acquirePauseLock(self) -> None:
        self.__algorithmPauseLock.acquire()
    

    def releasePauseLock(self) -> None: 
        self.__algorithmPauseLock.release()  
    

    def isAlgorithmPaused(self) -> bool:
        return self.__algorithmPauseLock.locked() 


    def acquireDelayLock(self) -> None: 
        self.__delayLock.acquire() 
    

    def releaseDelayLock(self) -> None: 
        self.__delayLock.release()


    def stopAlgorithm(self) -> None: 
        if(self.isAlgorithmPaused()): self.releasePauseLock() 
        if(self.__delayLock.locked()): self.releaseDelayLock()
        self.setAlgorithmStopFlag() 

        if self.__algorithmThread is None: return
        while(self.isThreadAlive()): 
            print("Waiting for Thread to halt")
        
        print("Thread Terminated :)")
        self.__algorithmThread = None
        return 


    def startAlgorithm(self, algorithmChoice : str, algorithmType : str) -> None:  
        if self.__algorithmThread is not None: self.stopAlgorithm() 

        # Ensure various locks are released 
        if(self.hasAlgorithmStopped()): self.clearAlgorithmStopFlag()  
        if(self.isAlgorithmPaused()): self.releasePauseLock() 
        if(self.__delayLock.locked()): self.releaseDelayLock()

        print("Starting Thread")
        # Call algorithm -> so this program actually has a use
        self.__algorithmThread = threading.Thread(target=self.runAlgorithm)
        # Start Thread
        self.__algorithmThread.start() 

    
# Listen to Disarm by The Smashing Pumpkins
