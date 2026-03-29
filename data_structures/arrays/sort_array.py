from .array import Array
from enums import SortDirection


class SortArray(Array): 
    def __init__(self):
        super().__init__()
        self.__sortDirection = SortDirection.ASCENDING 
    

    def setSortingDirecion(self, value : SortDirection) -> None:
        self.__sortDirection = value 
    

    def getSortingDirection(self) -> SortDirection:
        return self.__sortDirection 


# Checks if elements need to be swapped 
    def isSwapNeeded(self, i : int, j : int) -> bool: 
        if(self.__sortDirection == SortDirection.ASCENDING):
            return self.getAt(i) > self.getAt(j) 
        else: return self.getAt(i) < self.getAt(j) 

# Listen to Snuff by Slipknot
