# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from canvas_objects import CanvasNode, CanvasEdge

class TraversalModel():
    def __init__(self):  
        # Controller
        self.__controller = None   

        # Slider bar
        self.__minDelay = 1 
        self.__maxDelay = 1000
        self.__resolution = 1
        
        # Initial node coordinates an size 
        self.__initialX = 5
        self.__intialY = 5
        self.__circleSize = 25
        self.__initialNodeCoords = (self.__initialX, self.__intialY, 
                                    self.__initialX + self.__circleSize, 
                                    self.__intialY + self.__circleSize)
        
        # Canvas upper and lower bounds
        self.__canvasUpperBoundOffset = 4
        self.__canvasLowerBoundOffset = 2 
        # Minimum space between nodes 
        self.__nodesSpacingOffset = 20  
        # Number of nodes that can be on screen at once
        self.__maxNumNodes = 50
        
        # Values for physics calculations 
        self.__forceConstant = (1e-8) * 9e9 
        self.__maximumForceDistance = 75 
        
        # Array to contain references to CanvasNode objectd
        self.__nodes = []
        # Dictionary for edges, keys are tuples node IDs 
        self.__edges = {}

        # Minimum Weight edges can be 
        self.__minWeight = 1
        # Maximum weight edges can be 
        self.__maxWeight = 100 
        # Default weight given to each edge on creation 
        self.__defaultWeight = 20
        # Resolution of the weight slider
        self.__weightSliderResolution = 1

    # Adds controller         
    def addController(self, controller): 
        self.__controller = controller 
    
    # Getters for widgets on screen
    def getMinDelay(self): return self.__minDelay
    def getMaxDelay(self): return self.__maxDelay  
    def getResolution(self): return self.__resolution   

    # Getters for node data
    def getInitialCoords(self): return self.__initialNodeCoords    
    def getCircleSize(self): return self.__circleSize
    def getMaxNumNodes(self) -> int: return self.__maxNumNodes

    # Getters for minimum and maximum bounds of the canvas
    def getCanvasUpperBoundOffset(self) -> int: return self.__canvasUpperBoundOffset
    def getCanvasLowerBoundOffset(self) -> int: return self.__canvasLowerBoundOffset 
    def getSpaceBetweenNodes(self) -> int: return self.__nodesSpacingOffset 
    
    # Getters for data used in physics calculations
    def getForceConstant(self) -> float: return self.__forceConstant  
    def getMaximumForceDistance(self) -> int: return self.__maximumForceDistance  
    
    # Getters and setters for nodes array
    def getNodes(self) -> list[CanvasNode]: return self.__nodes
    def getNode(self, idx: int) -> CanvasNode: return self.__nodes[idx]
    def addNode(self, canvasNode : CanvasNode) -> None: self.__nodes.append(canvasNode)  
    
    # Getters and setters for edges dictionary 
    def getEdges(self) -> dict: return self.__edges 
    def getEdge(self, nodes : tuple) -> int: 
        if(nodes in self.__edges): return self.__edges[nodes] 
        else: return -1 
    def addEdge(self, nodes : tuple, edge : CanvasEdge) -> None: 
        self.__edges[nodes] = edge  
    def deleteEdge(self, nodes : tuple) -> None:
         self.__edges.pop(nodes)


    # Getters for edge weight 
    def getMinWeight(self) -> int: return self.__minWeight
    def getMaxWeight(self) -> int: return self.__maxWeight 
    def getDefaultWeight(self) -> int: return self.__defaultWeight
    def getWeightSliderResolution(self) -> int: return self.__weightSliderResolution 

    
 
# Listen to Jigsaws Falling Into Place by Radiohead