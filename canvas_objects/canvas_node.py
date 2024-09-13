# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

class CanvasNode():
    # Static variable shared between each instance 
    nodeID = 1

    def __init__(self, canvasID : int, coords : tuple) -> None: 
        # ID of the node on the canvas
        self.__canvasID = canvasID 
        # Node ID
        self.__ID = CanvasNode.nodeID
        CanvasNode.nodeID += 1 
        # X-Y Coorindates of the node on screen
        self.__coords = coords
        # Edges between this and other nodes 
        # and the weight of each edge
        self.__connectedNodes = {} 
        # Main colour of the node
        self.__colour = "Blue"
        # Colour of the node when it is hovered over 
        self.__highlightColour = "Red"
    
    # Updates the coordinates of the node to be accurate to the coordinates on screen
    def updateCoords(self, coords : tuple) -> None: 
        self.__coords = coords

    # Getters 
    def getCanvasID(self) -> int: return self.__canvasID 
    def getXCoord(self) -> int: return self.__coords[0]
    def getYCoord(self) -> int: return self.__coords[1]
    def getCoords(self) -> tuple: return self.__coords
    def getID(self) -> int: return self.__ID    
    def getMainColour(self) -> str: return self.__colour 
    def getHighlightColour(self) -> str: return self.__highlightColour 

    # Adds a connection between this node and another node
    def addConnection(self, nodeID : int, weight : int) -> None: 
        self.__connectedNodes[nodeID] = weight 
    
    # Gets a connection and it's weight given a node
    # Returns -1 if the connection doesn't exist
    def getConnection(self, nodeID: int) -> int:
        if(nodeID not in self.__connectedNodes): return -1 
        return self.__connectedNodes[nodeID]
    
# Listen to Paralyzer by Finger Eleven     