from canvas_objects import CanvasNode


class NodeHandler():
    def __init__(self) -> None:
        # # Store reference to canvas (makes things a lot easier)  
        # self.__canvas = canvas
        # # Store reference to model (to access data needed for nodes)
        # self.__model = model  
        # # Stores reference to the controller (literally needed for one function only)
        # self.__controller = controller
        # # Reference to edge handler (just needed cause events are a pain)
        # self.__edgeHandler = edgeHandler
        # # Flag to ensure events don't trigger when node being deleted
        # self.__isNodeBeingDeleted = False    

        self.__nodes = []
        self.__nodePadding = 10  

        self.__defaultX = 5
        self.__defaultY = 5
        self.__defaultNodeSize = 20
        self.__defaultNodeCoords = (self.__defaultX, self.__defaultY, 
                                    self.__defaultX + self.__defaultNodeSize, 
                                    self.__defaultY + self.__defaultNodeSize)


    # Getters 
    def getNodePadding(self) -> int: return self.__nodePadding 
    def getDefaultNodeCoords(self) -> tuple: return self.__defaultNodeCoords
    def getDefaultNodeSize(self) -> int: return self.__defaultNodeSize
    def getCircleOffset(self) -> int: return self.__defaultNodeSize // 2


    def createNode(self, coords) -> CanvasNode:
        canvasNode = CanvasNode(coords)
        self.__nodes.append(canvasNode)
        return canvasNode 

    # # Getter to check if a node is being deleted 
    # def isNodeBeingDeleted(self) -> bool: return self.__isNodeBeingDeleted 
    # # Setter used to flag when a node is being deleted
    # def setNodeBeingDeleted(self, state : bool) -> None:  
    #     self.__isNodeBeingDeleted = state 


    # # Changes the nodes colour the mouse is hovering to red
    # def __changeColourOnHover(self, canvasNode : CanvasNode) -> None: 
    #     self.__canvas.itemconfig(canvasNode.getCanvasID(), fill = canvasNode.getHighlightColour())


    # # Changes the mouse stops hovering over a node it's colour is set to blue 
    # def __changeColourOnLeave(self, canvasNode : CanvasNode) -> None:
    #     self.__canvas.itemconfig(canvasNode.getCanvasID(), fill = canvasNode.getMainColour())
      

    # # Deletes the node from the canvas
    # def __deleteNodeFromCanvas(self, canvasNode : CanvasNode) -> None:
    #     self.__canvas.delete(canvasNode.getCanvasID())  

    
    # # Moves centre of node to align with the cursor 
    # # Also handles when mouse is moved away from the canvas
    # def __calculateCoords(self, x : int, y : int) -> tuple:  
    #     # Values needed for calculations
    #     circleSize = self.__model.getCircleSize() 
    #     circleOffset = circleSize // 2 

    #     # Checks if mouse has gone out of bounds to the left 
    #     # Stops the node from moving off the canvas
    #     xCoord = max(x - circleOffset, self.__model.getCanvasLowerBoundOffset()) 
    #     # Checks if mouse has gone out of bounds to the right 
    #     # Stops the node from moving off the canvas
    #     xCoord = min(xCoord, self.__canvas.winfo_width()\
    #                   - self.__model.getCanvasUpperBoundOffset() - circleSize) 

    #     # Checks if mouse has gone out of bounds by going above the canvas
    #     # Stops the node from moving off the canvas 
    #     yCoord = max(y - circleOffset, self.__model.getCanvasLowerBoundOffset()) 
    #     # Checks if mouse has gone out of bounds by going below the canvas
    #     # Stops the node from moving off the canvas 
    #     yCoord = min(yCoord, self.__canvas.winfo_height()\
    #                   - self.__model.getCanvasUpperBoundOffset() - circleSize)  

    #     # The above could be done in one line but just because it can doesn't mean it should 
    #     # Doing it in one line would make the calculations very hard to read  
    #     return(xCoord, yCoord)


    # # Move node to cursors position on the canvas  
    # def __moveNode(self, event : Event, canvasNode : CanvasNode) -> None:  
    #     # Disables canvas event that draws edges if it binded 
    #     self.__controller.deleteMovingEdgeEvent()
    #     # Sets boolean to False so another edge can be drawn later
    #     self.__edgeHandler.setEdgeBeingDrawn(False) 
    #     # Radius of nodes 
    #     circleSize = self.__model.getCircleSize()
        
    #     # I don't know why but this stops the circles only being partially 
    #     # drawn when being moved around (works on windows only but Linux may not have issue)
    #     self.__canvas.configure(cursor='arrow')

    #     # Sets the circles colour to Red, makes sure the colour remains 
    #     # Red even if the mouse is moved off the circle 
    #     self.__canvas.itemconfig(canvasNode.getCanvasID(), fill = canvasNode.getHighlightColour())

    #     # Handles if the mouse moves outside of canvas 
    #     # Also makes sure centre of node aligns with cursor
    #     xCoord, yCoord = self.__calculateCoords(event.x, event.y)
    #     # Set is dragged flag to True 
    #     canvasNode.setDragged()
    #     # Updates coords in the CanvasNode object
    #     canvasNode.updateCoords((xCoord, yCoord, xCoord + circleSize, yCoord + circleSize))
        

    # # Deletes a node when the user double clicks on it 
    # def __deleteNodeOnDoubleClick(self, canvasNode : CanvasNode) -> None:
    #     # A node can't be deleted if an edge connected to it is being edited 
    #     if(self.__edgeHandler.isEdgeBeingEdited()): return 
        
    #     # Set variables indicating node is being deleted to True  
    #     # (This is used to stop another canvas event triggering) 
    #     self.__isNodeBeingDeleted = True 

    #     # The event to draw an edge can still trigger 
    #     # so it needs to be deleted
    #     self.__edgeHandler.deleteEdgeBeingDrawn()

    #     # Iterate through all edges 
    #     while(canvasNode.getEdges() != []): 
    #         # Assign values to variables so edge can be deleted
    #         self.__edgeHandler.initVariables(canvasNode.getEdges()[0])
    #         # Delete Edge  
    #         self.__edgeHandler.deleteEdge()
        
    #     # Delete node from the canvas
    #     self.__deleteNodeFromCanvas(canvasNode) 
    #     # Delete node object from array stored in model 
    #     self.__model.deleteNode(canvasNode) 

    
    # # Reset boolean flag allows forces to be applied when node stopped being dragged
    # def __resetDragged(self, canvasNode : CanvasNode): 
    #     canvasNode.resetDragged()
    
    # # Add event handlers to the newly created node
    # def __addNodeEvents(self, circle : int, canvasNode : CanvasNode) -> None:     
    #     # Add event to change nodes colour when the mouse hovers over it
    #     self.__canvas.tag_bind(circle, "<Enter>", lambda _: self.__changeColourOnHover(canvasNode))
    #     # Add event to change nodes colour when the mouse stops hovering over it
    #     self.__canvas.tag_bind(circle, "<Leave>", lambda _: self.__changeColourOnLeave(canvasNode)) 
        
    #     # Add event listener to move node when it's dragged by the mouse 
    #     self.__canvas.tag_bind(circle, "<B1-Motion>", lambda event: self.__moveNode(event, canvasNode))    
    #     # Add event listener to detect when mouse button released 
    #     self.__canvas.tag_bind(circle, "<ButtonRelease-1>", lambda _: self.__resetDragged(canvasNode))
        
    #     # Add event listener to add an edge when a node is clicked 
    #     self.__canvas.tag_bind(circle, "<Button-1>", lambda _: self.__controller.handleNodeClickEvent(canvasNode))
    #     # Add event to delete a node when it is double clicked 
    #     self.__canvas.tag_bind(circle, "<Double-Button-1>", lambda _: self.__deleteNodeOnDoubleClick(canvasNode)) 

    
    # # Draws a circle (node) on the canvas  
    # def spawnNode(self, coords : tuple) -> int:   
    #     # This function can be called at the same time a node is being deleted
    #     # (Double clicking a circle also triggers the double click canvas event)
        
    #     # Check if a node is being deleted (I have no clue why this works, it just does)
    #     if(self.__isNodeBeingDeleted): 
    #         self.__isNodeBeingDeleted = False 
    #         return -1

    #     # Checks if a new node can be spawned
    #     if(not self.__canNodeBeSpawned(coords)): return 0

    #     # Draws a new circle on the canvas at the specified coords
    #     # Returns the ID of the new circle
    #     circleID = self.__drawNode(coords) 
    #     # Creates an object for the new node
    #     canvasNode = self.__createCanvasNodeObject(circleID, coords) 
    #     # Adds event handlers to new node 
    #     self.__addNodeEvents(circleID, canvasNode) 
    #     # Return to indicate success
    #     return 1

# Listen to Hertz by Amyl and the Sniffers 
