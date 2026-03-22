# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from ..array_algorithm import ArrayAlgorithmController

if TYPE_CHECKING: 
    from array_sort import SortScreen, SortModel
    from array_algorithm import Array

S = TypeVar("S", bound="SortScreen")
M = TypeVar("M", bound="SortModel")
D = TypeVar("D", bound="Array")


class SortController(ArrayAlgorithmController[S, M, D]):
    def __init__(self, screen, model, dataStructure):
        super().__init__(screen, model, dataStructure)
    
    # Changes the sort direction 
    def toggleSortDirection(self):
        # Changes the sort direction
        self.getDataStructure().toggleSortDirection()  
        # Disables the button that called the function and enables the currently disabled button
        self.getScreen().disableEnableButtons(self.getDataStructure().isAscending())

# Listen to Give Me Novacaine by Green Day