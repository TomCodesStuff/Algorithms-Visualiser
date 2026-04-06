# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import math 

class CanvasNode():
    # Static variable shared between each instance 
    nodeID = 1

    def __init__(self, canvasID : int, coords : tuple, nodeSize : int) -> None: 
        # ID of the node on the canvas
        self.__canvasID = canvasID 
        # Node ID
        self.__ID = CanvasNode.nodeID 
        # Size of the node 
        self.__nodeSize = nodeSize
        CanvasNode.nodeID += 1 
        # X-Y Coordindates of the node on screen
        self.__coords = coords
        # TODO
        self.__velocity = (0, 0)
        # Dictionary mapping nodes connected by edges 
        # Keys are the node objects with the values being the weight of the connection
        self.__connectedNodes = {} 
        # Main colour of the node
        self.__colour = "Blue"
        # Colour of the node when it is hovered over 
        self.__highlightColour = "Red"
        # A List containing references to edges that connects nodes to eachother 
        self.__edges = []
        # Values that adjust the nodes position on screen, determined by forces applied on the Node 
        self.__forceX, self.__forceY = 0, 0 
        # Boolean flag, when a user is moving a node forces are not applied
        self.__isBeingDragged = False 

        
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
    def getConnectionsSet(self) -> set: return self.__edges


    # Adds a connection between this node and another node
    def addConnection(self, nodeID : int, weight : int) -> None: 
        self.__connectedNodes[nodeID] = weight 


    # Gets a connection and it's weight given a node
    # Returns -1 if the connection doesn't exist
    def getConnection(self, nodeID: int) -> int:
        if(nodeID not in self.__connectedNodes): return -1 
        return self.__connectedNodes[nodeID] 


    # Adds a CanvasEdge Object to the list 
    def addConnectionToSet(self, edge) -> None: self.__edges.append(edge) 


    # Delete a CanvasEdge from the list 
    # (Otherwise errors happen when an edge is deleted)
    def deleteConnectionFromSet(self, egde) -> None:  
        self.__edges.remove(egde)   


    # Return all edges connected the node 
    def getEdges(self) -> list: return self.__edges


    # Adjust Force applied in X-axis
    def adjustForceX(self, forceX : int) -> None:
        self.__forceX += forceX 


    # Adjust Force applied in Y-axis
    def adjustForceY(self, forceY : int) -> None:
        self.__forceY += forceY 


    # Resets values that apply forces to a node
    def resetForces(self) -> None:
        self.__forceX = 0
        self.__forceY = 0
    

    def __roundForce(self, force : float, coord : float) -> float: 
         return math.floor(coord) if force < 0 else math.ceil(coord)


    def applyForces(self) -> None:  
        
        # Get top-left coordinates of the node 
        x0, y0, _, _ = self.__coords 
        
        # Calculate new x0 and y0 
        # Coords needed to be rounded to prevent issues with floating point precision 
        newX0 = x0 + self.__forceX
        newY0 = y0 + self.__forceY

        # Update coords 
        self.__coords = (newX0, newY0, newX0 + self.__nodeSize, newY0 + self.__nodeSize)  
    

    # Function for dragging objects
    def isBeingDragged(self) -> bool: return self.__isBeingDragged
    def setDragged(self) -> bool: self.__isBeingDragged = True
    def resetDragged(self) -> bool: self.__isBeingDragged = False

# Listen to Paralyzer by Finger Eleven     
