from __future__ import annotations

# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from typing import Set, TYPE_CHECKING
from data_structures import Node 

if TYPE_CHECKING: 
    from ..graph_components import CanvasEdge


class CanvasNode():
    # Static variable shared between each instance 
    nodeID = 1

    def __init__(self, node : Node, coords : tuple, nodeSize : int) -> None: 
        # Reference to abstracted node object
        self.__node = node
        # X-Y Coordindates of the node on screen
        self.__coords = coords
        # Size of the node 
        self.__nodeSize = nodeSize

        self.__ID = CanvasNode.nodeID 
        CanvasNode.nodeID += 1 
        
        # ID of the node on the canvas
        self.__canvasID = -1  

        # A set containing references to edges that connects nodes to eachother 
        self.__edges = set()
        
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
    def getColour(self) -> str: return self.__node.getColour()
    def getEdges(self) -> Set[CanvasEdge]: return self.__edges

    # Setters 
    def setCanvasID(self, canvasID : int) -> None:  self.__canvasID = canvasID
    def setColour(self, colour : str) -> None: self.__node.setColour(colour)  
    

    # Adds a CanvasEdge Object to the list 
    def addEdge(self, canvasEdge : CanvasEdge) -> None: 
        self.__edges.add(canvasEdge) 


    def removeEdge(self, canvasEdge : CanvasEdge) -> None: 
        if canvasEdge in self.__edges: 
            self.__edges.remove(canvasEdge)


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
