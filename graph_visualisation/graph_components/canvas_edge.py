# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit() 


from .canvas_node import CanvasNode


class CanvasEdge(): 
    def __init__(self, coords : tuple, weight : int, colour : str) -> None: 
        # On screen coords of the edge
        self.__coords = coords
        # Weight/cost
        self.__weight = weight 
        self.__colour = colour
        
        # ID used to identify edge on the canvas
        self.__canvasID = -1
        
        # The node that the edges XY coords start at 
        self.__startNode = None  
        # The node that the edges XY coords end at
        self.__endNode = None 
        
        # Size edge should be onscreen 
        self.__screenLen = 0 


    # Getters
    def getCanvasID(self): return self.__canvasID
    def getWeight(self) -> int: return self.__weight 
    def getCoords(self) -> tuple: return self.__coords
    def getStartNode(self) -> CanvasNode|None: return self.__startNode
    def getEndNode(self) -> CanvasNode|None: return self.__endNode
    def getNodes(self) -> tuple: return (self.__startNode, self.__endNode) 
    def getScreenLen(self) -> int: return self.__screenLen
    def getColour(self) -> str: return self.__colour
    

    # Setters
    def setWeight(self, weight : int) -> None: 
        if weight > 0: self.__weight = weight
    

    def updateCoords(self, coords : tuple) -> None: 
        self.__coords = coords 
    

    def setStartNode(self, canvasNode : CanvasNode) -> None:
        self.__startNode = canvasNode 


    def setEndNode(self, canvasNode : CanvasNode) -> None:
        self.__endNode = canvasNode 


    # TODO error handling and adjustment for screen size
    def setscreenLen(self, val : int): self.__screenLen = val


    def setCanvasID(self, val : int) -> None: 
        self.__canvasID = val 


# Listen to Live Forever by Oasis 
