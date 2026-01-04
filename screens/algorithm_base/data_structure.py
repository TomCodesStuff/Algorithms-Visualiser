class DataStructure(): 
    def __init__(self):
        self.__delay = 0 


    def setDelay(self, val : int) -> None:
        self.__delayLock.acquire()  
        if val > 0: self.__delay = val 
        self.__delayLock.release()

    
    def getDelay(self) -> int: 
        self.__delayLock.acquire()  
        delay = self.__delay
        self.__delayLock.release()
        return delay
    
    
    # Updates the screen so changes to the array are shown
    def updateArrayOnScreen(self) -> None:
        self.__controller.scheduleArrayUpdate() 