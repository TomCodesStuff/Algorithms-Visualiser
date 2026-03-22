# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from ..array_algorithm import ArrayAlgorithmModel

class SortModel(ArrayAlgorithmModel):

    def __init__(self):
        super().__init__()
        self.__buttonWidth = 16

        self.setDelayToMilliseconds()
        self.setResolution(1)
        self.setMinDelay(1)
        self.setMaxDelay(1000)


    # Returns the width used for the buttons 
    def getButtonWidth(self) -> int: return self.__buttonWidth 
    
# Listen to Creep by Radiohead