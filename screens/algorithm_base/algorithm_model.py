class AlgorithmModel(): 
    def __init__(self):
        self.__delay = 0
        self.__minimumDelay = 0 
        self.__maximumDelay = 0  
        self.__resolution = 0 
        self.__isDelayMilliseconds = False 

    def setDelay(self, val : int) -> None:
        if val > 0: self.__delay = val 

    def setMaxDelay(self, val : int) -> None:
        if val > 0 and val > self.__minimumDelay: 
            self.__maximumDelay = val
    
    def setMinDelay(self, val : int) -> None:
        if val > 0 and val < self.__maximumDelay: 
            self.__minimumDelay = val

    def setResolution(self, val : int) -> None:
        if val > 0: self.__resolution = val  
    
    def setDelayToMilliseconds(self) -> None:
        self.__isDelayMilliseconds = True

    def setDelayToSeconds(self) -> None:
        self.__isDelayMilliseconds = False


    def getDelay(self) -> int: return self.__delay
    def getMaxDelay(self) -> int: return self.__maximumDelay
    def getMinDelay(self) -> int: return self.__minimumDelay 
    def getResolution(self) -> int: return self.__resolution 
    def isDelayMilliSeconds(self) -> bool: return self.__isDelayMilliseconds
