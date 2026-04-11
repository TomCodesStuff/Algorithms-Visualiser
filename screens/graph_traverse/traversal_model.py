# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from typing import Set
from ..algorithm_base import AlgorithmModel
from canvas_objects import CanvasNode, CanvasEdge


class TraversalModel(AlgorithmModel):
    def __init__(self): 
        super().__init__() 

        self.setDelayToMilliseconds()
        self.setResolution(1)
        self.setMinDelay(1)
        self.setMaxDelay(1000)


        # Canvas upper and lower bounds
        self.__canvasUpperBoundOffset = 4
        self.__canvasLowerBoundOffset = 2 
        
        # Minimum space between nodes 
        self.__nodesSpacingOffset = 20  
        # Number of nodes that can be on screen at once
        self.__maxNumNodes = 20
               
        # Array to contain references to CanvasNode objects
        self.__nodes = []
        # Set for edges
        self.__edges = set()
        # Minimum Weight edges can be 
        self.__minWeight = 1
        # Maximum weight edges can be 
        self.__maxWeight = 100 
        # Default weight given to each edge on creation 
        self.__defaultWeight = 20
        # Resolution of the weight slider
        self.__weightSliderResolution = 1

        # Minimum and Maximum on screen size for edges
        self.__edgeMinScreenLen = 55
        self.__edgeMaxScreenLen = 200

        # Smallest distance nodes can be apart on screen 
        self.__minScreenDist = 50
        # Largest distance nodes can be apart on screen 
        self.__maxScreenDist = 50 

        # Time delay when updating the canvas   
        self.__updateDelay = 50


    # Getters for distances between nodes on screen 
    def getMinScreenDist(self) -> int: return self.__minScreenDist
    def getMaxScreenDist(self) -> int: return self.__maxScreenDist


    def getMaxNumNodes(self) -> int: return self.__maxNumNodes


    # Getters for minimum and maximum bounds of the canvas
    def getCanvasUpperBoundOffset(self) -> int: return self.__canvasUpperBoundOffset
    def getCanvasLowerBoundOffset(self) -> int: return self.__canvasLowerBoundOffset 
    def getSpaceBetweenNodes(self) -> int: return self.__nodesSpacingOffset 


    # Getters and setters for nodes array
    def getNodes(self) -> list[CanvasNode]: return self.__nodes
    def getNode(self, idx: int) -> CanvasNode: return self.__nodes[idx]
    def addNode(self, canvasNode : CanvasNode) -> None: self.__nodes.append(canvasNode)  
    def deleteNode(self, canvasNode : CanvasNode) -> None: self.__nodes.remove(canvasNode)


    # Getters and setters for edges set 
    def getEdges(self) -> Set[CanvasEdge]: return self.__edges 
    def addEdge(self, edge : CanvasEdge) -> None: self.__edges.add(edge)
    def deleteEdge(self, edge : CanvasEdge) -> None: self.__edges.discard(edge)


    # Getters for edge weight 
    def getMinWeight(self) -> int: return self.__minWeight
    def getMaxWeight(self) -> int: return self.__maxWeight 
    def getDefaultWeight(self) -> int: return self.__defaultWeight
    def getWeightSliderResolution(self) -> int: return self.__weightSliderResolution 


    # Getter for delay used when updating the canvas
    def getUpdateDelay(self) -> int: return self.__updateDelay 


    def getEdgeMinScreenLen(self) -> int: return self.__edgeMinScreenLen
    def getEdgeMaxScreenLen(self) -> int: return self.__edgeMaxScreenLen


# Listen to Jigsaws Falling Into Place by Radiohead
