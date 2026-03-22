# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from ..array_algorithm import ArrayAlgorithmController

if TYPE_CHECKING: 
    from array_search import SearchScreen, SearchModel
    from array_algorithm import Array

S = TypeVar("S", bound="SearchScreen")
M = TypeVar("M", bound="SearchModel")
D = TypeVar("D", bound="Array")


class SearchController(ArrayAlgorithmController[S, M, D]):
    def __init__(self, screen, model, dataStructure):
        super().__init__(screen, model, dataStructure)
    

    # Returns the text to be displayed above the slider
    def updateSliderText(self, value : str) -> str:
        self.__updateTargetSetting(value)
        return self.getModel().getSliderText(int(value))


    # Updates the target setting attribute in the dataStructure class 
    def __updateTargetSetting(self, value : str) -> None:
        self.getDataStructure().setTargetSetting(int(value)) 
                    
# Listen to Give Me Novacaine by Green Day