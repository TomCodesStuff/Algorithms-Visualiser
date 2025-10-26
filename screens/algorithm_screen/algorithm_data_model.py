import threading

class AlgorithmDataModel(): 
    def __init__(self):
        self.__delay = 0 
        self.__algorithmRunning = threading.Event()
        self.__algorithmPauseLock = threading.Lock()
        self.__delayLock = threading.Lock()
    

    def setDelay(self, val : int) -> None:
        if val > 0: self.__delay = val 
    

    def getDelay(self) -> int: return self.__delay