import threading
from typing import Callable
from algorithms import Algorithm


THREAD_TIMEOUT = 1


class ThreadHandler():
    def __init__(self):
        self.__algorithmThread = None 
        self.__algorithmStarted = threading.Event()
        self.__algorithmStopped = threading.Event()
        self.__algorithmPauseLock = threading.Lock()
        self.__delayLock = threading.Lock() 

        self.__algorithmSuccess = False 


    def runAlgorithm(self, algorithm : Algorithm): 
        self.__algorithmSuccess = False
        self.__algorithmStarted.set() 
        try:
            algorithm.run()   
            self.__algorithmSuccess = True 
        except Exception as e:
            print(f"ERROR: Algorithm broke at some point :(.\nException: {e}") 
            self.__algorithmSuccess = False
            

    def isThreadAlive(self) -> bool:
        if self.__algorithmThread is None: return False 
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


    def wasAlgorithmSuccessful(self) -> bool:
        return self.__algorithmSuccess 
    

    def stopAlgorithm(self) -> None: 
        if(self.isAlgorithmPaused()): self.releasePauseLock() 
        if(self.__delayLock.locked()): self.releaseDelayLock()
        self.setAlgorithmStopFlag() 

        if self.__algorithmThread is None: return
        if self.isThreadAlive(): self.__algorithmThread.join(timeout=THREAD_TIMEOUT)
        if self.isThreadAlive(): print("ERROR: Thread did not terminate in time.")        
        print("Thread Terminated :)")
        self.__algorithmThread = None
        return 


    def startAlgorithm(self, algorithm : Algorithm) -> None:  
        if self.__algorithmThread is not None: self.stopAlgorithm() 
        if algorithm is None: return 
        
        # Ensure various locks are released 
        if(self.hasAlgorithmStopped()): self.clearAlgorithmStopFlag()  
        if(self.isAlgorithmPaused()): self.releasePauseLock() 
        if(self.__delayLock.locked()): self.releaseDelayLock()
        self.__algorithmStarted.clear()

        print("Starting Thread")
        # Call algorithm -> so this program actually has a use
        self.__algorithmThread = threading.Thread(target=self.runAlgorithm, args=(algorithm,))
        # Start Thread
        self.__algorithmThread.start() 
        # Wait until thread has started
        self.__algorithmStarted.wait(timeout=THREAD_TIMEOUT)

    
# Listen to Disarm by The Smashing Pumpkins
