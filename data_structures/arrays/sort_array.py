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


# Listen to Snuff by Slipknot
