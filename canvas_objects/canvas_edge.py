# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 

class CanvasEdge(): 
    def __init__(self, canvasID : int, coords : tuple, weight : int, screenSize : int) -> None: 
        # ID used to identify edge on the canvas
        self.__canvasID = canvasID
        # On screen coords of the edge
        self.__coords = coords
        # Weight/cost
        self.__weight = weight 
        # The node that the edges XY coords start at 
        self.__startNode = None  
        # The node that the edges XY coords end at
        self.__endNode = None 
        # Size edge should be onscreen 
        self.__screenSize = screenSize
    
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
    
    # Getter/Setters for adding the nodes the edge connects  
    # Takes in CanvasNode Objects
    def addNodes(self, startNode, endNode): 
        self.__startNode = startNode 
        self.__endNode = endNode 
    
    def getNodes(self) -> tuple: return (self.__startNode, self.__endNode) 
    
    def getScreenSize(self) -> int: return self.__screenSize
    
    # TODO error hanlding and adjustment for screen size
    def setScreenSize(self, val : int): self.__screenSize = val

# Listen to Live Forever by Oasis 