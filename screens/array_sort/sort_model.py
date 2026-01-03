class SortModel(): 
    def __init__(self) -> None: 
        self.__interval = 1 
        self.__sliderStart = 1000 
        self.__sliderEnd = 1 
        self.__buttonWidth = 16

    # Returns the interval for the slider bar
    def getSlidernterval(self) -> int: return self.__interval 
    # Returns the starting value of the slider bar
    def getSliderStart(self) -> int: return self.__sliderStart  
    # Returns the ending value of the slider bar
    def getSliderEnd(self) -> int: return self.__sliderEnd  
    # Returns the width used for the buttons 
    def getButtonWidth(self) -> int: return self.__buttonWidth 
    
# Listen to Creep by Radiohead