from canvas_objects import CanvasNode, CanvasEdge
from .traversal_model import TraversalModel
from tkinter import Canvas, Event


class EdgeHandler():
    def __init__(self, canvas : Canvas, controller, model : TraversalModel ) -> None:
        # References to needed objects 
        self.__canvas = canvas
        self.__controller = controller 
        self.__model = model 
        
        # Booleans to handle cases when multiple events trigger at once
        self.__isEdgeBeingDrawn = False 
        self.__isEdgeBeingEdited = False  
        self.__isEdgeBeingDeleted = False
        
        # Store references to nodes edge connects 
        self.__nodeEdgeStart = None 
        self.__nodeEdgeEnd = None 

        # Canvas ID if edge user is interacting with
        self.__currentEdgeID = None 
        # Stores reference to corresponding edge object 
        self.__currentEdgeObj = None

    
    # Getters 
    def isEdgeBeingEdited(self) -> bool: return self.__isEdgeBeingEdited
    def isEdgeBeingDrawn(self) -> bool: return self.__isEdgeBeingDrawn   
    def isEdgeBeingDeleted(self) -> bool: return self.__isEdgeBeingDeleted

    # Setters 
    def setEdgeBeingEdited(self, state : bool) -> None: 
        self.__isEdgeBeingEdited = state
    def setEdgeBeingDrawn(self, state : bool) -> None: 
        self.__isEdgeBeingDrawn = state 
    def setEdgeBeingDeleted(self, state : bool) -> None: 
        self.__isEdgeBeingDeleted = state 

    # Setters 
    def setConnectionStartNode(self, canvasNode : CanvasNode) -> None: 
        self.__nodeEdgeStart = canvasNode 
    def setConnectionEndNode(self, canvasNode : CanvasNode) -> None: 
        self.__nodeEdgeEnd = canvasNode
    
    # Getters 
    def getEdgeBeingEdited(self) -> CanvasEdge: return self.__currentEdgeObj
    def getCurrentEdgeID(self) -> int: return self.__currentEdgeID 
    def getCurrentEdgeObj(self) -> CanvasEdge: return self.__currentEdgeObj
    def getEdgeStartNode(self) -> CanvasNode: return self.__nodeEdgeStart
    def getEdgeEndNode(self) -> CanvasNode: return self.__nodeEdgeEnd
    
    # Setter 
    def setCurrentEdgeID(self, currentEdgeID: int) -> None: 
        self.__currentEdgeID = currentEdgeID


    # Assign values to variables so functions to edit/delete edges can work
    def initVariables(self, canvasEdge : CanvasEdge): 
        self.__currentEdgeID = canvasEdge.getCanvasID() 
        self.__currentEdgeObj = canvasEdge 
        self.__nodeEdgeStart, self.__nodeEdgeEnd = canvasEdge.getNodes() 


    # Resets variables used when creating edges     
    def clearVariables(self) -> None: 
        self.__nodeEdgeStart = None 
        self.__nodeEdgeEnd = None 
        self.__currentEdgeID = None  
        self.__currentEdgeObj = None
        self.setEdgeBeingEdited(False)
        

    # Deletes current edge from the screen 
    def __deleteEdgeFromCanvas(self): 
        # Delete edge from canvas
        self.__canvas.delete(self.__currentEdgeID) 
            
    # Handles when an egde starts and ends at the same node 
    def __handleSelfEdge(self) -> None:
        # Delete edge
        self.__deleteEdgeFromCanvas() 
        # Clear variables used when creating edges 
        self.clearVariables()


    def __editEdgeOnClick(self, canvasEdge : CanvasEdge) -> None: 
        if(self.__isEdgeBeingDrawn or self.__isEdgeBeingEdited): return 

        # Assign values to variables needed to edit edges 
        self.setEdgeBeingEdited(True)
        self.initVariables(canvasEdge)
        
        # Show option on screen to an edge 
        self.__controller.enableEdgeWeightOptions()
    

     # Deletes egde from relevant data structure 
    def __deleteEdgeFromDict(self): 
        connectedNodes = (self.__nodeEdgeStart, self.__nodeEdgeEnd) 
        # If egdes exists with tuple of nodes as the key
        if(self.__model.getEdge(connectedNodes) != -1): 
            self.__model.deleteEdge(connectedNodes) 
        # Otherwise reverse key and delete edge at key
        else: self.__model.deleteEdge(connectedNodes[::-1])

    
    # Deletes the newly drawn edge or existing edge
    def deleteEdge(self): 
        # Deletes edge from relevant data structure 
        self.__deleteEdgeFromDict() 
        # Deletes drawn edge
        self.__deleteEdgeFromCanvas() 
        # Delete reference of CanvasEdge Object in the CanvasNode objects
        self.__nodeEdgeStart.deleteConnectionFromSet(self.__currentEdgeObj)
        self.__nodeEdgeEnd.deleteConnectionFromSet(self.__currentEdgeObj)
        # Resets variables  
        self.clearVariables()  
    

    # Deletes edge current being drawn (follwing users mouse)
    def deleteEdgeBeingDrawn(self) -> None: 
        self.__deleteEdgeFromCanvas()
        self.__controller.stopMovingEdge()
        self.clearVariables() 


     # Deletes current edge being drawn if user clicks the canvas 
    def deleteEdgeOnClick(self, event : Event): 
        # This event can trigger when an edge is being edited 
        # Deleting the edge when it shouldn't be 
        if(self.__isEdgeBeingEdited): return
        collisions = self.__canvas.find_overlapping(event.x, event.y , event.x, event.y) 
        if(len(collisions) == 1 and self.__currentEdgeID in collisions): 
            self.__deleteEdgeFromCanvas()
            self.__controller.stopMovingEdge() 
            self.clearVariables() 
    
    # Delete an edge when a user double clicks on it
    def __deleteEdgeOnDoubleClick(self, canvasEdge : CanvasEdge):    
        self.setEdgeBeingDeleted(True)
        self.initVariables(canvasEdge)
        # Hide options to edit edge if they are currently visible
        self.__controller.disableEdgeWeightOptions()
        # Delete edge 
        self.deleteEdge() 
    

    # Add event handlers to edges for interactability 
    def __addEdgeEvents(self, edge : int, canvasEdge : CanvasEdge) -> None:  
        self.__canvas.tag_bind(edge, "<Button-1>", lambda _: self.__editEdgeOnClick(canvasEdge))
        self.__canvas.tag_bind(edge, "<Double-Button-1>", lambda _: self.__deleteEdgeOnDoubleClick(canvasEdge)) 


    # Calculates the screen length of an edge using it's weight
    def calculateEdgeScreenLength(self, weight : int) -> int:
        # output = output_start + ((output_end - output_start) / (input_end - input_start)) * (input - input_start)
        minScreenLength, maxScreenLength = self.__model.getEdgeMinScreenLen(), self.__model.getEdgeMaxScreenLen()
        minWeight, maxWeight = self.__model.getMinWeight(), self.__model.getMaxWeight() 

        return round(minScreenLength + ((maxScreenLength - minScreenLength) / (maxWeight - minWeight)) * 
                     (weight - minWeight))


    # Creates and returns a new CanvasEdge object
    def __createCanvasEdge(self) -> CanvasEdge: 
        # Edges are stored in a dictionary with the key being a tuple of the two nodes being connected
        connectedNodes = (self.__nodeEdgeStart, self.__nodeEdgeEnd) 
        
        #TODO Clean this up 
        
        # If edge exists between the two nodes, 
        # return the already existing object 
        if(connectedNodes in self.__model.getEdges()): 
            self.__deleteEdgeFromCanvas()  
            return self.__model.getEdge(connectedNodes) 
        
        # Checks if reverse tuple of the connected nodes is in the dictionary 
        elif(connectedNodes[::-1] in self.__model.getEdges()):  
            self.__deleteEdgeFromCanvas()
            return self.__model.getEdge(connectedNodes[::-1]) 
        
        # Adjust edge coords it's in the correct place 
        adjustedCoords = self.__controller.centreEdge()
        # Default weight 
        defaultWeight = self.__model.getDefaultWeight()

        # Create new object, weight is initially set to the default 
        newEdge = CanvasEdge(self.__currentEdgeID, adjustedCoords, defaultWeight, self.calculateEdgeScreenLength(defaultWeight))
        # Add node to dictionary 
        self.__model.addEdge(newEdge)   
        # Add references to nodes in CanvasEdge object
        newEdge.addNodes(self.__nodeEdgeStart, self.__nodeEdgeEnd) 
        # Add reference to edge in CanvasNode objects 
        self.__nodeEdgeStart.addConnectionToSet(newEdge)
        self.__nodeEdgeEnd.addConnectionToSet(newEdge)
        # Adds events to the edge 
        self.__addEdgeEvents(self.__currentEdgeID, newEdge)
        # Return new object 
        return newEdge


    # Creates a new CanvasEdge Object 
    def __createNewEdge(self) -> CanvasEdge: 
        # Get new or existing CanvasEdge object
        edge = self.__createCanvasEdge()
        # Updates current edge 
        self.__currentEdgeID = edge.getCanvasID() 
        return edge


    # Case handling for potential duplicate or self edges 
    def __handleNewEdge(self) -> None:
        # If edge starts and ends at the same node
        if(self.__nodeEdgeStart == self.__nodeEdgeEnd):  
            self.__handleSelfEdge() 
        else: 
            self.__currentEdgeObj = self.__createNewEdge()
            self.__controller.enableEdgeWeightOptions()
  
    
    # Handles when a edge connects two nodes together 
    def handleNodeConnection(self, canvasNode : CanvasNode) -> None:
        # Stop Edge following mouse event 
        self.__controller.stopMovingEdge() 
        # Sets variable indicating edge is being edited 
        self.setEdgeBeingEdited(True)
        # Sets node edge ends to current node 
        self.setConnectionEndNode(canvasNode)
        # Sanity Checking before new edge can be created
        self.__handleNewEdge()   
    

    def spawnEdge(self, canvasNode : CanvasNode): 
        # Store reference to node the new edge starts from  
        self.setConnectionStartNode(canvasNode) 

# Listen to Why does it always rain on me by Travis 