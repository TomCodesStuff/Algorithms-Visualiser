# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from canvas_objects import CanvasNode, CanvasEdge
from .traversal_model import TraversalModel 
from tkinter import Event, BOTH 
import math

class TraversalController():
    def __init__(self, screen, model : TraversalModel): 
        self.__screen = screen 
        self.__model = model  
        
        # Attributes that handle drawing edges 
        
        # Attributes that handle drawing edges 
        self.__isEdgeBeingDrawn = False 
        self.__edgeStartNode = None 
        self.__edgeEndNode = None 
        self.__currentEdgeID = None
        self.__currentEdgeObj = None 
        self.__isEdgeBeingEdited = False

    def addCanvasEvents(self): 
        canvas = self.__screen.getCanvas() 
        # Add event to delete current edge being drawn when the canvas is clicked
        canvas.bind("<Button-1>", lambda event: self.__deleteEdgeOnClick(event))

    # Draws a circle (node) on the canvas 
    def spawnNode(self):   
        # Gets a reference to the canvas 
        canvas = self.__screen.getCanvas()   

        # If no more nodes can currently be spawned
        if(not self.__canNodeBeSpawned()):   
            # Change the add node buttons text to red 
            self.__screen.changeNodeButtonColour("red")
            return  
        
        # if node can be drawn, change the buttons colour back to black
        self.__screen.changeNodeButtonColour("black")
        # X-Y coords of where the node will spawn -> this is the same for evey node 
        x0, y0, x1, y1 = self.__model.getInitialCoords()   
        # Draws the circle 
        circle = canvas.create_oval(x0, y0, x1, y1, outline = "black", fill="blue")     
        # Create corresponding object for the circle 
        canvasNode = CanvasNode(circle, (x0, y0, x1, y1))  
        # Adds node to array containing nodes 
        self.__model.addNode(canvasNode)
        
        # Adds event handlers to new node 
        self.__addNodeEvents(circle, canvasNode)

        # Updates screen so node can be seen onscreen
        self.__screen.getWindow().update() 
    
    def __addNodeEvents(self, circle : int, canvasNode : CanvasNode) -> None:
        # Gets a reference to the canvas 
        canvas = self.__screen.getCanvas() 
        
        # Add event to change nodes colour when the mouse hovers over them
        canvas.tag_bind(circle, "<Enter>", lambda _: self.__changeColourOnHover(canvasNode))
        # Add event to change nodes colour when the mouse hovers over them
        canvas.tag_bind(circle, "<Leave>", lambda _: self.__changeColourOnLeave(canvasNode)) 
        # Add event listener to move node when it's dragged by the mouse 
        canvas.tag_bind(circle, "<B1-Motion>", lambda event: self.__moveNode(event, canvasNode))   
        # Add event listener to add an edge when a node is clicked 
        canvas.tag_bind(circle, "<Button-1>", lambda _: self.__createEdge(canvasNode))


    # Creates a line that follows the mouse until another node is clicked 
    def __createEdge(self, canvasNode : CanvasNode):  

        # If an edge is being edited, prevent a new one from being created
        if(self.__isEdgeBeingEdited): return

        # If an edge is already being drawn on screen
        if(self.__isEdgeBeingDrawn):
            # If an edge is already being drawn  
            self.__stopMovingEdge() 
            # Sets variable indicating edge is being edited 
            self.__isEdgeBeingEdited = True 
            # Sets node edge ends to current node 
            self.__edgeEndNode = canvasNode 
            # Checks edge can be created before creating new CanvadEdge Object 
            # and adding the new object to relevant data structures  
            self.__handleNewEdge()  
         
        # If an edge is not currently being draw on screen
        else: 
            self.__createMovingEdge(canvasNode)
            # Store reference to node the new edge starts from  
            self.__edgeStartNode = canvasNode
        # Updates window to display changes
        self.__screen.getWindow().update()  
    
    # Case handling for potential duplicate or self edges 
    def __handleNewEdge(self) -> None:
        # If edge starts and ends at the same node
        if(self.__edgeStartNode == self.__edgeEndNode):  
            self.__handleSelfEdge()
        else: 
            self.__currentEdgeObj = self.__createNewEdge()
            self.__screen.enableWeightOptions(self.__currentEdgeObj)
    
    def __createNewEdge(self) -> CanvasEdge: 
        # Get new or existing CanvasEdge object
        edge = self.__createCanvasEdge()
        # Updates current edge 
        self.__currentEdgeID = edge.getCanvasID()
        return edge

    # Creates and returns a new CanvasEdge object
    def __createCanvasEdge(self) -> CanvasEdge: 
        # Edges are stored in a dictionary with the key being a tuple of the two nodes being connected
        connectedNodes = (self.__edgeStartNode, self.__edgeEndNode) 
        # If edge exists between the two nodes, 
        # return the already existing object 
        if(connectedNodes in self.__model.getEdges()): 
            self.__deleteEdge()  
            return self.__model.getEdge(connectedNodes) 
        # Checks if reverse tuple of the connected nodes is in the dictionary 
        elif(connectedNodes[::-1] in self.__model.getEdges()):  
            self.__deleteEdge()
            return self.__model.getEdge(connectedNodes[::-1]) 
        # Creates new object of edge is new 
        else: 
            # Moves edge to centre of the destination node 
            coords = self.__centreEdge() 
            # Adjusts edge so arrow/s can be shown
            # coords = self.__adjustEdgeCoords()
            # Create new object, weight is initially set to the default 
            newEdge = CanvasEdge(self.__currentEdgeID, coords, self.__model.getDefaultWeight()) 
            # Add node to dictionary 
            self.__model.addEdge(connectedNodes, newEdge)   
            # Return new object 
            return newEdge

    # Handles when an egde starts and ends at the same node 
    def __handleSelfEdge(self) -> None:
        # Delete edge
        self.__deleteEdge() 
        # Clear variables used when creating edges 
        self.__clearVariables()
        
    # Resets variables used when creating edges     
    def __clearVariables(self) -> None: 
        self.__edgeStartNode = None 
        self.__edgeEndNode = None 
        self.__currentEdgeID = None  
        self.__currentEdgeObj = None
        self.__isEdgeBeingEdited = False

    # Enables canvas events and sets boolean variable to true 
    def __createMovingEdge(self, canvasNode : CanvasNode) -> None:
        # Adds canvas event to draw lines
        self.__addMovingEdgeEvent(canvasNode)
        # Sets variable to True
        self.__isEdgeBeingDrawn = True   
            
    # Disables canvas events and sets boolean variable to false 
    def __stopMovingEdge(self) -> None:
        # Remove event that draws line
        self.__deleteMovingEdgeEvent()
        # Set edge being drawn to False
        self.__isEdgeBeingDrawn = False
        
    # Changes weight of current edge to passed value 
    def saveEdge(self, newWeight : int) -> None: 
        # Update weight of current edge object
        self.__currentEdgeObj.setWeight(newWeight) 
        # Adjust distance between nodes to match new weight
        self.__adjustScreenDistance()
        # Clear variables used  
        self.__clearVariables() 
       
    # Adjusts size of the edge to be more representative of its weight 
    def __adjustScreenDistance(self) -> None:  
        # Reference to canvas
        canvas = self.__screen.getCanvas()
        # Start and end coords of edge 
        x2, y2, x3, y3 = self.__currentEdgeObj.getCoords()
        # New ending X-Y coords of the edge 
        adjustedX, adjustedY = 0, 0

        # Maps the edges weight onto the range defining 
        # the maxiumum and minimum on screen distance between nodes 
        scaledDist = self.__calculateScaledDist()
        
        # Get on screen length of edge 
        onScreenDist = self.__calculateDistance(x2, y2, x3, y3)

        # If the length does not need changing
        if(onScreenDist == scaledDist): return

        # If the edge is a diagonal line 
        if(x2 != x3 and y2 != y3):
            adjustedX, adjustedY = self.__handleDiagonalLine()   
        elif(scaledDist < onScreenDist): 
            adjustedX, adjustedY = self.__handleGrowingStraightLine() 

        else: adjustedX, adjustedY = self.__handleShrinkingStraightLine()

        # Edge case of grows outside screen 
        # - push as far as can in direction -> then just move node/s 
        # - push as rest/far can in other direction  
        # TODO (so I can come back easier)

        # Update coords on screen
        canvas.coords(self.__currentEdgeID, x2, y2, adjustedX, adjustedY) 
        # Update coords in CanvasEdge Object 
        self.__currentEdgeObj.updateCoords(canvas.coords(self.__currentEdgeID))
        # Since the edge has been shrunk, one of the nodes need to reconnected to the end of the edge 
        self.__reconnectNodeToEdge()   
        self.__handleOutOfBounds()

    # Handles when a node is pushed off screen when an edges length is increased
    # (This is a bit jank but I don't care) 
    # (Can cause the edges length to shrink a little but I really don't care)
    def __handleOutOfBounds(self):
        # Reference to canvas
        canvas = self.__screen.getCanvas()
        # Size of nodes
        circleSize = self.__model.getCircleSize()  
        # Offset added to calculate coords of a nodes centre
        circleCentreOffset = circleSize // 2

        # Coords of node potentially offscreen
        x0, y0, x1, y1 = self.__edgeEndNode.getCoords()  
        # Offsets will be used to calculate how far the 
        # node still on screen needs to move to preserve edge length
        xOffset, yOffset = 0, 0

        # If node is offscreen to the left
        if(x0 < 0):  
            # Calculate offset to be added to x coords of node still on screen
            xOffset = self.__model.getCanvasUpperBoundOffset() - x0  
            # Calculate new x coords of node that is offscreen
            x0 = self.__model.getCanvasUpperBoundOffset()
            x1 = x0 + circleSize
        # If the node is offscreen to the right
        if(x1 > canvas.winfo_width()):
            # Calculate offset to be added to x coords of node still on screen
            xOffset = canvas.winfo_width() - self.__model.getCanvasUpperBoundOffset() - x1
            # Calculate new x coords of node that is offscreen
            x1 = canvas.winfo_width() - self.__model.getCanvasUpperBoundOffset()  
            x0 = x1 - circleSize
        # If the node is above the viewable screen
        if(y0 < 0): 
            # Calculate offset to be added to y coords of node still on screen
            yOffset = self.__model.getCanvasUpperBoundOffset() - y0
            # Calculate new y coords of node that is offscreen
            y0 = self.__model.getCanvasUpperBoundOffset() 
            y1 = y0 + circleSize
        # If the node is below the viewable screen 
        if(y1 > canvas.winfo_height()):
            # Calculate offset to be added to y coords of node still on screen
            yOffset = canvas.winfo_height() - self.__model.getCanvasUpperBoundOffset() - y1
             # Calculate new y coords of node that is offscreen
            y1 = canvas.winfo_height() - self.__model.getCanvasUpperBoundOffset() 
            y1 = y0 + circleSize
        
        # Precision with floating points can cause nodes to shrink noticeably 
        # Make sure size of nodes is still preserved 
        if(y1 - y0 != self.__model.getCircleSize()): 
            y1 += (circleSize - (y1 - y0))

        # Update coords of node so it's back on screen 
        canvas.coords(self.__edgeEndNode.getCanvasID(), x0, y0, x1, y1) 
        # Update coords in node Object 
        self.__edgeEndNode.updateCoords((x0, y0, x1, y1))

        # Get coords of node that was not pushed off screen
        x2, y2, x3, y3 = self.__edgeStartNode.getCoords()  
        # Add offsets to the nodes coords so the length of the edge is kept the same  
        x2 += xOffset 
        x3 += xOffset 
        y2 += yOffset 
        y3 += yOffset
        
        # Update coords of node so it's back on screen 
        canvas.coords(self.__edgeStartNode.getCanvasID(), math.floor(x2), math.floor(y2), 
                      math.floor(x3), math.floor(y3)) 
        # Update coords in node Object 
        self.__edgeStartNode.updateCoords((x2, y2, x3, y3))

        # Get updated starting coords of nodes (also used to test that objects are keeping accurate coords)
        x0, y0, _, _ = self.__edgeEndNode.getCoords()
        x2, y2, _, _ = self.__edgeStartNode.getCoords()  

        # Updates edge so it is reconnected to the nodes 
        canvas.coords(self.__currentEdgeID, x0 + circleCentreOffset, y0 + circleCentreOffset, 
                      x2 + circleCentreOffset, y2 + circleCentreOffset) 
        self.__currentEdgeObj.updateCoords((x0 + circleCentreOffset, y0 + circleCentreOffset,
                                             x2 + circleCentreOffset, y2 + circleCentreOffset))

    # Increases an edges length to match it's weight 
    def __handleGrowingStraightLine(self): 

        # Start and end coords of edge 
        x2, y2, x3, y3 = self.__currentEdgeObj.getCoords()
        adjustedX, adjustedY = 0, 0

        # Maps the edges weight onto the range defining 
        # the maxiumum and minimum on screen distance between nodes 
        scaledDist = self.__calculateScaledDist()
        
        if(x2 == x3):
            adjustedX = x2 
            # If egde goes from the top of the screen to the bottom
            if(y2 < y3): adjustedY = y2 + scaledDist
            # If egde goes from the bottom of the screen to the top
            else: adjustedY = y2 - scaledDist 
        elif(y2 == y3):
            # Furthest Y coordinate remains unchanged
            adjustedY = y3
            # If edge goes from left to right
            if(x2 < x3): adjustedX = x2 + scaledDist
            # If the edge goes from right to left 
            else: adjustedX = x2 - scaledDist   
        
        return adjustedX, adjustedY

    # Shrinks and edge to match it's weight 
    def __handleShrinkingStraightLine(self):
        # Start and end coords of edge 
        x2, y2, x3, y3 = self.__currentEdgeObj.getCoords()

        # Maps the edges weight onto the range defining 
        # the maxiumum and minimum on screen distance between nodes 
        scaledDist = self.__calculateScaledDist()

        # Straight line along the y-axis
        if(x2 == x3):   
            # Furthest X coordinate remains unchanged
            adjustedX = x3 
            # If egde goes from the top of the screen to the bottom
            if(y2 < y3): adjustedY = y2 + scaledDist
            # If egde goes from the bottom of the screen to the top
            else: adjustedY = y2 - scaledDist
        # Straight line along the x-axis
        elif(y2 == y3): 
            # Furthest Y coordinate remains unchanged
            adjustedY = y3
            # If edge goes from left to right
            if(x2 < x3): adjustedX = x2 + scaledDist
            # If the edge goes from right to left 
            else: adjustedX = x2 - scaledDist    

        return adjustedX, adjustedY    
        
    # Calculated new coords of a diagonal edge    
    def __handleDiagonalLine(self) -> tuple:
         # Start and end coords of edge 
        x2, y2, x3, y3 = self.__currentEdgeObj.getCoords()
        
        # New X-Y Coords for the end of the edge 
        adjustedX, adjustedY = 0, 0
        
        # Maps the edges weight onto the range defining 
        # the maxiumum and minimum on screen distance between nodes 
        scaledDist = self.__calculateScaledDist()
        
        # Get on screen length of edge 
        onScreenDist = self.__calculateDistance(x2, y2, x3, y3)

        # There are four cases for a given edges direction             
        if(y2 > y3):  
            # Calculate theta using y2 and y3
            theta = self.__calculateTheta(abs(y2 - y3), onScreenDist) 
            # Calculate Offsets needed to calculate new coords 
            yOffset, xOffset = self.__calculateXYOffsets(theta, scaledDist) 
            # Calculates new coords by adding or subtracting offsets 
            if(x2 > x3):
                adjustedX = x2 - xOffset 
                adjustedY = y2 - yOffset
            else:
                adjustedX = x2 + xOffset 
                adjustedY = y2 - yOffset
        else: 
            # Calculate theta using x2 and x3
            theta = self.__calculateTheta(abs(x2 - x3), onScreenDist) 
            # Calculared offsets to calculate new coords 
            xOffset, yOffset = self.__calculateXYOffsets(theta, scaledDist)
            # Calculates new coords by adding or subtracting offsets 
            if(x2 > x3):
                adjustedX = x2 - xOffset 
                adjustedY = y2 + yOffset
            else:
                adjustedX = x2 + xOffset 
                adjustedY = y2 + yOffset  
        return (adjustedX, adjustedY)

    def __reconnectNodeToEdge(self): 
        # Reference to canvas
        canvas = self.__screen.getCanvas() 
        # Offset needed calculate nodes new coords
        circleOffset = self.__model.getCircleSize() // 2 
        # Only need the last coords of the edge 
        _, _, x0, y0 = self.__currentEdgeObj.getCoords() 
        # Updates on screen position of the node 
        # Needs to rounded or floating point precision causes node to "vibrate"
        canvas.coords(self.__edgeEndNode.getCanvasID(), 
                      math.ceil(x0 - circleOffset), math.ceil(y0 - circleOffset), 
                      math.ceil(x0 + circleOffset), math.ceil(y0 + circleOffset)) 
        # Update coords in the CanvasNode Object
        self.__edgeEndNode.updateCoords(canvas.coords(self.__edgeEndNode.getCanvasID()))

    # Returns the value of the angle between the hypotenuse and adjacent side in radians 
    def __calculateTheta(self, oppsiteLength : int, hypotenuseLength : int) -> float: 
        return math.asin(abs(oppsiteLength) / hypotenuseLength)         

    # Calculates the offsets needed to scale the edges length with it's weight
    def __calculateXYOffsets(self, theta : float, hypotenuseLength : float) -> tuple:
        return (math.sin(theta) * hypotenuseLength, math.cos(theta) * hypotenuseLength)
        
    # Maps an edges weight onto a range which defines the maximum 
    # and minimum on screen distance between nodes
    def __calculateScaledDist(self) -> int: 
        return math.ceil(self.__model.getMinScreenDist() + \
                ((self.__model.getMaxScreenDist() - self.__model.getMinScreenDist()) / 
                 (self.__model.getMaxWeight() - self.__model.getMinWeight())) * \
                (self.__currentEdgeObj.getWeight() - self.__model.getMinWeight()))

    # Deletes the newly drawn edge or existing edge
    def deleteEdge(self): 
        # Deletes edge from relevant data structure 
        self.__deleteEdgeFromDict()
        # Deletes drawn edge
        self.__deleteEdge() 
        # Restets variables  
        self.__clearVariables()
   
    # Deletes egde from relevant data structure 
    def __deleteEdgeFromDict(self): 
        connectedNodes = (self.__edgeStartNode, self.__edgeEndNode) 
        # If egdes exists with tuple of nodes as the key
        if(self.__model.getEdge(connectedNodes) != -1): 
            self.__model.deleteEdge(connectedNodes) 
        # Otherwise reverse key and delete edge at key
        else: self.__model.deleteEdge(connectedNodes[::-1])

    # Returns the Edge Canvas object
    def __getCanvasEdge(self) -> CanvasEdge: 
        connectedEdges = (self.__edgeStartNode, self.__edgeEndNode)
        if(connectedEdges in self.__model.getEdges()): 
            return self.__model.getEdge(connectedEdges)
        else: return self.__model.getEdge(connectedEdges[::-1])
    
    # Deletes current edge being drawn if user clicks the canvas 
    
    # Deletes current edge being drawn if user clicks the canvas 
    def __deleteEdgeOnClick(self, event : Event):
        canvas = self.__screen.getCanvas() 
        collisions = canvas.find_overlapping(event.x, event.y , event.x, event.y) 
        if(len(collisions) == 1 and self.__currentEdgeID in collisions): 
            self.__deleteEdge()
            self.__stopMovingEdge() 
            self.__clearVariables() 

    # Deletes current edge from the screen 
    def __deleteEdge(self): 
        self.__screen.getCanvas().delete(self.__currentEdgeID) 
            
    # Add event to draw a line representing an edge
    def __addMovingEdgeEvent(self, canvasNode : CanvasNode): 
        self.__screen.getCanvas().bind("<Motion>", lambda event: self.__drawEdge(event, canvasNode))

    # Removes the event that draws lines representing edges 
    def __deleteMovingEdgeEvent(self):  
        canvas = self.__screen.getCanvas()
        if("<Motion>" in canvas.bind()):
            canvas.unbind("<Motion>")

    # Draws an edge from the given circle to the mouses current position
    def __drawEdge(self, event : Event, canvasNode : CanvasNode) -> None:  
        canvas = self.__screen.getCanvas()   
        circleOffset = self.__model.getCircleSize() // 2
        x0, y0, _, _ = canvasNode.getCoords() 
        lineCoords = None

        # Checks if mouse has left the node the edge starts from
        collisions = canvas.find_overlapping(event.x, event.y, event.x, event.y)  
        # If the mouse is still in the node, the edge is not drawn yet
        if(canvasNode.getCanvasID() in collisions): return  
        # If there is no current edge 
        if(self.__currentEdgeID == None): 
            # Create a new edge and assign it to a variable 
            self.__currentEdgeID = canvas.create_line(x0 + circleOffset, y0 + circleOffset, 
                                                    event.x, event.y, width = "3", arrow=BOTH)  
            # Lowers the priority of the edge, so it appears below nodes 
            canvas.tag_lower(self.__currentEdgeID) 
        # If there is an edge being drawn on screen
        else:   
            # Gets current coordinates of the line
            lineCoords = canvas.coords(self.__currentEdgeID)
            # Change XY coordinates to where the mouse is
            lineCoords[2] = event.x 
            lineCoords[3] = event.y 
            # Updates the lines coordinates 
            canvas.coords(self.__currentEdgeID, lineCoords)
        
    # Draws an edge to the centre of the circle
    def __centreEdge(self) -> tuple: 
        circleOffset = self.__model.getCircleSize() // 2 
        # Reference to canvas 
        canvas = self.__screen.getCanvas()  
        # Get Coords of the destination node 
        x1, y1, _, _ = self.__edgeEndNode.getCoords() 
        # Gets current coords of the edges
        coords = canvas.coords(self.__currentEdgeID) 
        # Update coords of the edge to be in the middle of the passed node
        coords[2] = x1 + circleOffset 
        coords[3] = y1 + circleOffset 
        # Send updated coords to the canvas
        canvas.coords(self.__currentEdgeID, coords)  
        # Return the updated coords of the edge 
        return coords 
    
    # Adjusts position of the edge 
    # Allows the arrow/s to not be hidden in the centre of each node
    def __adjustEdgeCoords(self) -> tuple:

        canvas = self.__screen.getCanvas()    
        circleRadius = self.__model.getCircleSize() // 2 

        # x,y coords of both nodes
        x0, y0, _, _ = self.__edgeStartNode.getCoords()
        x1, y1, _, _ = self.__edgeEndNode.getCoords() 

        # calculates centre coords of each node 
        x0 += circleRadius 
        y0 += circleRadius 
        
        x1 += circleRadius 
        y1 += circleRadius  

        # Gets current coords of the edge
        coords = canvas.coords(self.__currentEdgeID)   

        # Calculate direction of the edge in relation to the circle
        dx = coords[0] - x1
        dy = coords[1] - y1 

        # Length of the line 
        length = math.sqrt((dx**2 + dy**2)) 

        # Normalise vectors 
        dx /= length 
        dy /= length 

        # X coord of the circumference, the arrow touches
        px = x1 + circleRadius * dx 
        # Y coord of the circumference, the arrow touches
        py = y1 + circleRadius * dy

        # Readjust line 
        canvas.coords(self.__currentEdgeID, coords[0], coords[1], px, py)
        # Return updated coords of the line 
        return canvas.coords(self.__currentEdgeID)

    # Checks if a new node can be added to the screen.  
    # Nodes can be added to the screen if there are no 
    # other nodes in a given radius or if the maximum number
    # of nodes has not been exceeded 
    def __canNodeBeSpawned(self): 
        # Coordinates the node will be drawn at 
        x0, y0, x1, y1 = self.__model.getInitialCoords()  
        spaceBetweenNodes = self.__model.getSpaceBetweenNodes() * 2  
        # Get's ID of any nodes within a set radius 
        conflictingNodes = list(self.__screen.getCanvas()
                                .find_overlapping(
                                    x0 - spaceBetweenNodes, 
                                    y0 - spaceBetweenNodes, 
                                    x1 + spaceBetweenNodes,
                                    y1 + spaceBetweenNodes)) 
        # Returnd True if the node can be drawn, else False 
        return False if conflictingNodes or \
            len(self.__model.getNodes()) == self.__model.getMaxNumNodes() else True
        
    # Moves the node to follow the users mouse 
    def __moveNode(self, event : Event, canvasNode : CanvasNode) -> None:   
        # Disables canvas event that draws edges if it binded 
        self.__deleteMovingEdgeEvent()
        # Sets False so another edge can be drawn later
        self.__isEdgeBeingDrawn = False

        # Reference to the canvas 
        canvas = self.__screen.getCanvas()
        # Radius of the nodes
        circleSize = self.__model.getCircleSize()  
        # I don't know why but this stops the circles only being partially 
        # drawn when being moved around (works on windows only)
        canvas.configure(cursor='arrow')
        # Sets the circles colour to Red, makes sure the colour remains 
        # red even if the mouse is moved off the circle 
        self.__screen.changeCircleColour(canvasNode.getCanvasID(), "Red")

        # Handles if the mouse moves of off the canvas 
        xCoord, yCoord = self.__adjustCoords(event.x, event.y)

        # Updates coords in the CanvasNode object
        canvasNode.updateCoords((xCoord, yCoord, xCoord + circleSize, yCoord + circleSize))
        
        
        # Applies forces to each node -> disabled for now 
        # self.__calculateForces(canvasNode)

        # Updates coords in the CanvasNode object
        canvasNode.updateCoords((xCoord, yCoord, xCoord + circleSize, yCoord + circleSize))
        self.__redrawNodes()
        self.__redrawEdges()
        
        # Moves center of the circle to the coordinates specified 
        #canvas.moveto(canvasNode.getCanvasID(), xCoord, yCoord) 
        
        # Updates screen so node can be seen onscreen
        self.__screen.getWindow().update()

    # Changes the coordinates of a circle when when the user drags it across the screen
    def __adjustCoords(self, x : int, y : int) -> tuple:  
        
        canvas = self.__screen.getCanvas()
        circleSize = self.__model.getCircleSize()
        circleOffset = circleSize // 2 
        self.__stopMovingEdge()
        
        # Checks if mouse has gone out of bounds to the left 
        # Stops the node from moving off the canvas
        xCoord = max(x - circleOffset, self.__model.getCanvasLowerBoundOffset()) 
        # Checks if mouse has gone out of bounds to the right 
        # Stops the node from moving off the canvas
        xCoord = min(xCoord, canvas.winfo_width() - self.__model.getCanvasUpperBoundOffset() - circleSize) 

        # Checks if mouse has gone out of bounds by going above the canvas
        # Stops the node from moving off the canvas 
        yCoord = max(y - circleOffset, self.__model.getCanvasLowerBoundOffset()) 
        # Checks if mouse has gone out of bounds by going below the canvas
        # Stops the node from moving off the canvas 
        yCoord = min(yCoord, canvas.winfo_height() - self.__model.getCanvasUpperBoundOffset() - circleSize)  

        # The above could be done in one line but just because it can doesn't mean it should 
        # Doing it in one line would make the calculations very hard to read  
        return(xCoord, yCoord)

    # Updates position of nodes on the canvas
    def __redrawNodes(self): 
        canvas = self.__screen.getCanvas()
        for node in self.__model.getNodes():  
            x0, y0, _, _ = node.getCoords()
            canvas.moveto(node.getCanvasID(), x0, y0)
    
    # Update positions of edges on the canvas 
    def __redrawEdges(self):
        canvas = self.__screen.getCanvas() 
        circleOffset = self.__model.getCircleSize() // 2  
        # Iterate through each edge
        for connectedNodes, canvasEdge in self.__model.getEdges().items(): 
            # Get coords of the nodes the edge connects
            x0, y0, _, _ = connectedNodes[0].getCoords() 
            x1, y1, _, _ = connectedNodes[1].getCoords() 
            
            # Get coords of the edge
            coords = canvasEdge.getCoords()

            # Update coords of edge 
            coords[0] = x0 + circleOffset 
            coords[1] = y0 + circleOffset 
            coords[2] = x1 + circleOffset 
            coords[3] = y1 + circleOffset
            
            # Update coords of edge on the canvas
            canvas.coords(canvasEdge.getCanvasID(), coords)  
            # Update coords in canvasEdge object 
            canvasEdge.updateCoords(coords)

    # Changes the nodes colour the mouse is hovering to red
    def __changeColourOnHover(self, canvasNode : CanvasNode) -> None: 
        self.__screen.changeCircleColour(canvasNode.getCanvasID(), 
                                         canvasNode.getHighlightColour())
    
    # Changes the mouse stops hovering over a node it's colour is set to blue 
    def __changeColourOnLeave(self, canvasNode : CanvasNode) -> None:
        self.__screen.changeCircleColour(canvasNode.getCanvasID(), 
                                         canvasNode.getMainColour())

    # Calculates the forces that will be applied to each node 
    def __calculateForces(self, canvasNode : CanvasNode): 
        n = len(self.__model.getNodes())
        circleSize = self.__model.getCircleSize()
        circleOffset = circleSize// 2 
        # Step one apply Coulombs laws to each node  
        for i in range(n): 
            for j in range(i + 1, n):   
                # XY coordinates of the nodes
                x0, y0, _, _ = self.__model.getNode(i).getCoords()
                x1, y1, _, _, = self.__model.getNode(j).getCoords()   
                # XY coords of the centre of each circle
                centreX0, centreY0 = x0 + circleOffset, y0 + circleOffset
                centreX1, centreY1 = x1 + circleOffset, y1 + circleOffset
 
                # Calculated pythagorean distance between the circles
                dist = self.__calculateDistance(centreX0, centreY0, centreX1, centreY1)  
                # If the circles are far apart the result force would be neglible 
                if(dist > self.__model.getMaximumForceDistance()): 
                    continue
                
                # Resultant force as a scalar 
                force = self.__model.getForceConstant() / max(dist, 1) 

                # Convert scalar force to vector form
                forceX = ((centreX1 - centreX0) / dist) * force
                forceY = ((centreY1 - centreY0) / dist) * force 

                # Update coords of each node 
                self.__updatedCoords(x0, y0, -forceX, -forceY, self.__model.getNode(i))
                self.__updatedCoords(x1, y1, forceX, forceY, self.__model.getNode(j))
           
    # Updates the X-Y coordinates using the resultant forces
    def __updatedCoords(self, x : int, y : int, forceX : int, forceY : int, canavsNode : CanvasNode):  
        circleSize = self.__model.getCircleSize()
        canvas = self.__screen.getCanvas()
        x0 = x + forceX 
        y0 = y + forceY

        # If the resulting force along the x-axis causes the node 
        # to go out of bounds to the left or the right of the canvas 
        # The x-axis resultant force is reversed 
        if(x0 <= self.__model.getCanvasLowerBoundOffset() 
           or x0 >= canvas.winfo_width() - self.__model.getCanvasUpperBoundOffset() - circleSize): 
            x0 = x - forceX
        
        # If the resulting force along the y-axis causes the node 
        # to go out of bounds above or below the canvas 
        # The y-axis resultant force is reversed 
        if(y0 <= self.__model.getCanvasLowerBoundOffset() or y0 >= 
           canvas.winfo_height() - self.__model.getCanvasUpperBoundOffset() - circleSize): 
            y0 = y - forceY

        # Rounds the new coordinates up to the nearest whole number
        x0 = math.ceil(x0)
        y0 = math.ceil(y0)

        # Updates the coordinates of the relevant node 
        canavsNode.updateCoords((x0, y0, x0 + circleSize, y0 + circleSize)) 
    
    # Calculates distance between two nodes using the pythagoras theorem 
    def __calculateDistance(self, x0 : int, y0 : int, x1 : int, y1 : int) -> float: 
        return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))

    
# Listen to Paranoid by Black Sabbath