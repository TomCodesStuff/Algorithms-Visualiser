# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 

class CanvasEdge(): 
    def __init__(self, canvasID : int, coords : tuple, weight : int) -> None: 
        self.__canvasID = canvasID
        self.__coords = coords
        self.__weight = weight
        self.__isDirected = False 
    
    # Getter for canvas ID 
    def getCanvasID(self): 
        return self.__canvasID
    
    # Getter for weight/cost of edge
    def getWeight(self) -> int: 
        return self.__weight 
    def setWeight(self, weight : int) -> None: 
        self.__weight = weight
    
    # Coordinates Getter and setters
    def getCoords(self) -> tuple: 
        return self.__coords
    def updateCoords(self, coords : tuple) -> None:
        self.__coords = coords

# Listen to Live Forever by Oasis 