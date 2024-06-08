# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from canvas_objects import CanvasNode, CanvasEdge
from .traversal_model import TraversalModel
from tkinter import Event 
import math

class TraversalController():
    def __init__(self, screen, model : TraversalModel): 
        self.__screen = screen 
        self.__model = model  
        
        # Attributes that handle drawing edges 
        self.__isEdgeBeingDrawn = False 
        self.__fromNode = None 
        self.__toNode = None 
        self.__currentEdge = None 
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
        else: self.__screen.changeNodeButtonColour("black")

        # X-Y coords of where the node will spawn -> this is the same for evey node 
        x0, y0, x1, y1 = self.__model.getInitialCoords()   
        # Draws the circle 
        circle = canvas.create_oval(x0, y0, x1, y1, outline = "black", fill="blue")     
        # Create corresponding object for the circle 
        canvasNode = CanvasNode(circle, (x0, y0, x1, y1))  
        # Adds node to array containing nodes 
        self.__model.addNode(canvasNode)
        # Add event to change nodes colour when the mouse hovers over them
        canvas.tag_bind(circle, "<Enter>", lambda _: self.__changeColourOnHover(canvasNode))
        # Add event to change nodes colour when the mouse hovers over them
        canvas.tag_bind(circle, "<Leave>", lambda _: self.__changeColourOnLeave(canvasNode)) 
        # Add event listener to move node when it's dragged by the mouse 
        canvas.tag_bind(circle, "<B1-Motion>", lambda event: self.__moveNode(event, canvasNode))   
        # Add event listener to add an edge when a node is clicked 
        canvas.tag_bind(circle, "<Button-1>", lambda _: self.__createEdge(canvasNode))

        # Updates screen so node can be seen onscreen
        self.__screen.getWindow().update() 
    
    # Creates a line that follows the mouse until another node is clicked 
    def __createEdge(self, canvasNode : CanvasNode):     
        # If edge is being drawn on screen
        if(self.__isEdgeBeingDrawn): 
            # Add Node ID to relevant label 
            self.__screen.updateToLabelText(str(canvasNode.getID()))
            # Disable canvas event listeners and sets boolean variable 
            self.__stopMovingEdge() 
            # Sets node, edge ends at to CanvasNode
            self.__toNode = canvasNode
            # Sets variable indicating edge is beind edited 
            self.__isEdgeBeingEdited = True 
            # Handles if edge already exists or if edge is new
            self.__handleEdge()  
        # If an edge is not being draw on screen
        else: 
            # If edge is being edited, prevent new one from being born
            if(self.__isEdgeBeingEdited): return
            # Add Node ID to relevant label 
            self.__screen.updateFromLabelText(str(canvasNode.getID())) 
            # Enables canvas event listeners and sets boolean variable 
            self.__createMovingEdge(canvasNode) 
            # Sets node, edge starts at to CanvasNode
            self.__fromNode = canvasNode
        # Updates window to display changes
        self.__screen.getWindow().update()  
    
    # Handles if edges starts and end at the same node 
    # or of an edge already exists between two nodes 
    def __handleEdge(self):
        # If edge starts and ends at the same node
        if(self.__fromNode == self.__toNode):  
            self.__handleSelfEdge()
            return
        
        # Get new or existing CanvasEdge object
        edge = self.__createCanvasEdge()
        # Updates current edge 
        self.__currentEdge = edge.getCanvasID()
        # Enable options that let users edit edges
        self.__screen.enableWeightOptions()
        # Update weight slider to show the edges weight
        self.__screen.updateWeightOnScreen(edge.getWeight())  
    
    # Creates and returns a new CanvasEdge object
    def __createCanvasEdge(self) -> CanvasEdge: 
        connectedNodes = (self.__fromNode, self.__toNode) 
        # If edge exists between the two nodes, 
        # return the already existing object 
        if(connectedNodes in self.__model.getEdges()): 
            self.__deleteEdge()  
            return self.__model.getEdge(connectedNodes) 
        elif(connectedNodes[::-1] in self.__model.getEdges()):  
            self.__deleteEdge()
            return self.__model.getEdge(connectedNodes[::-1]) 
        # Creates new object of edge is new 
        else: 
            # Moves edge to centre of the destination node 
            coords = self.__centreEdge(self.__toNode)
            # Create new object, weight is initially set to the default 
            newEdge = CanvasEdge(self.__currentEdge, coords, self.__model.getDefaultWeight()) 
            # Add node to dictionary 
            self.__model.addEdge(connectedNodes, newEdge)   
            # Return new object 
            return newEdge

    # Handles when an egde starts and ends at the same node 
    def __handleSelfEdge(self):
        # Delete edge
        self.__deleteEdge() 
        # Clear text in labels
        self.__screen.clearNodeLabelsText() 
        # Disable buttons and resets slider 
        self.__screen.disableWeightOptions()
        # Clear variables used when creating edges 
        self.__clearVariables()
        
    # Resets variables used when creating edges     
    def __clearVariables(self): 
        self.__fromNode = None 
        self.__toNode = None 
        self.__currentEdge = None  
        self.__isEdgeBeingEdited = False

    # Enables canvas events and sets boolean variable to true 
    def __createMovingEdge(self, canvasNode : CanvasNode):
        # Adds canvas event to draw lines
        self.__addCanvasEvent(canvasNode)
        # Sets variable to True
        self.__isEdgeBeingDrawn = True   
            
    # Disables canvas events and sets boolean variable to false 
    def __stopMovingEdge(self):
        # Remove event that draws line
        self.__deleteCanvasEvent()
        # Set edge being drawn to False
        self.__isEdgeBeingDrawn = False
        
    # Changes weight of current edge to passed value 
    def saveEdge(self, weight : int): 
        # Update weight of current edge object
        edge = self.__getCanvasEdge() 
        edge.setWeight(weight)
        # Clear variables used  
        self.__clearVariables()

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
        connectedNodes = (self.__fromNode, self.__toNode) 
        # If egdes exists with tuple of nodes as the key
        if(self.__model.getEdge(connectedNodes) != -1): 
            self.__model.deleteEdge(connectedNodes) 
        # Otherwise reverse key and delete edge at key
        else: self.__model.deleteEdge(connectedNodes[::-1])

    # Returns the Edge Canvas object
    def __getCanvasEdge(self) -> CanvasEdge: 
        connectedEdges = (self.__fromNode, self.__toNode)
        if(connectedEdges in self.__model.getEdges()): 
            return self.__model.getEdge(connectedEdges)
        else: return self.__model.getEdge(connectedEdges[::-1])
    
    # Deletes current edge being drawn if user clicks the canvas 
    def __deleteEdgeOnClick(self, event : Event):
        canvas = self.__screen.getCanvas() 
        collisions = canvas.find_overlapping(event.x, event.y , event.x, event.y) 
        if(len(collisions) == 1 and self.__currentEdge in collisions): 
            self.__deleteEdge()
            self.__stopMovingEdge() 
            self.__clearVariables() 

    # Deletes current edge from the screen 
    def __deleteEdge(self): 
        self.__screen.getCanvas().delete(self.__currentEdge) 
            
    # Add event to draw a line representing an edge
    def __addCanvasEvent(self, canvasNode : CanvasNode): 
        self.__screen.getCanvas().bind("<Motion>", lambda event: self.__drawEdge(event, canvasNode))

    # Removes the event that draws lines representing edges 
    def __deleteCanvasEvent(self):  
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
        if(self.__currentEdge == None): 
            # Create a new edge and assign it to a variable 
            self.__currentEdge = canvas.create_line(x0 + circleOffset, y0 + circleOffset, 
                                                    event.x, event.y, width = "3")  
            # Lowers the priority of the edge, so it appears below nodes 
            canvas.tag_lower(self.__currentEdge) 
        # If there is an edge being drawn on screen
        else:   
            # Gets current coordinates of the line
            lineCoords = canvas.coords(self.__currentEdge)
            # Change XY coordinates to where the mouse is
            lineCoords[2] = event.x 
            lineCoords[3] = event.y 
            # Updates the lines coordinates 
            canvas.coords(self.__currentEdge, lineCoords)
        
    # Draws an edge to the centre of the circle
    def __centreEdge(self, destinationNode : CanvasNode) -> tuple: 
        circleOffset = self.__model.getCircleSize() // 2 
        canvas = self.__screen.getCanvas()  
        # Get Coords of the destination node 
        x1, y1, _, _ = destinationNode.getCoords() 
        # Gets current coords of the edges
        coords = canvas.coords(self.__currentEdge) 
        # Update coords of the edge to be in the middle of the passed node
        coords[2] = x1 + circleOffset 
        coords[3] = y1 + circleOffset 
        # Send updated coords to the canvas
        canvas.coords(self.__currentEdge, coords)  
        # Return the updated coords of the edge 
        return coords 

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
        self.__deleteCanvasEvent()
        # Sets False so another edge cna be drawn later
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
        # Applies forces to each node 
        self.__calculateForces(canvasNode)

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





