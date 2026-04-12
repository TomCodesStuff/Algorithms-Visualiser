class EventsModel(): 
    def __init__(self):
        self.__nodeSpawnDist = 10  
        self.__defaultNodeSize = 20
        self.__overlapOffset = self.__nodeSpawnDist + self.__defaultNodeSize 
        
        # Default Node Coords
        self.__x = 5
        self.__y = 5
        self.__defaultNodeCoords = (self.__x, self.__y, 
                                    self.__x + self.__defaultNodeSize, 
                                    self.__y + self.__defaultNodeSize) 

        # Node colours 
        self.__defaultNodeColour = "blue"
        self.__nodeHoverColour = "red"

        # Account for small border around canvas 
        self.__canvasUpperBoundOffset = 4
        self.__canvasLowerBoundOffset = 2 

        self.__canvasWidth = 0
        self.__canvasHeight = 0
    

    def getDefaultNodeCoords(self) -> tuple: return self.__defaultNodeCoords
    def getDefaultNodeSize(self) -> int: return self.__defaultNodeSize
    def getOverlapOffset(self) -> int: return self.__overlapOffset 
    

    def getDefaultNodeColour(self) -> str: return self.__defaultNodeColour 
    def getNodeHoverColour(self) -> str: return self.__nodeHoverColour 
    

    def getNodeOffset(self) -> int: return self.__defaultNodeSize // 2 


    def getCanvasLowerBoundOffset(self) -> tuple: return self.__canvasLowerBoundOffset
    def getCanvasUpperBoundOffset(self) -> tuple:return self.__canvasUpperBoundOffset


    def getCanvasWidth(self) -> int: return self.__canvasWidth
    def getCanvasHeight(self) -> int: return self.__canvasHeight


    def setCanvasWidth(self, width : int) -> None: self.__canvasWidth = width
    def setCanvasHeight(self, height : int) -> None: self.__canvasHeight = height