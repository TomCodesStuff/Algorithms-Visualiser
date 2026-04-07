# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING, TypeVar
from tkinter import Event, BOTH 
from canvas_objects import CanvasNode, CanvasEdge
from data_structures import Array
from ..algorithm_base import AlgorithmController
from .node_handler import NodeHandler
from .edge_handler import EdgeHandler 
from .physics_handler import PhysicsHandler

if TYPE_CHECKING: 
    from graph_traverse import TraversalScreen, TraversalModel


S = TypeVar("S", bound="TraversalScreen")
M = TypeVar("M", bound="TraversalModel")
D = TypeVar("D", bound="Array")

class TraversalController(AlgorithmController[S, M, D]):
    def __init__(self, screen : S, model : M, dataStructure : D):
        super().__init__(screen, model, dataStructure)

        # # Handles creation and deletion of edges 
        # self.__edgeHandler = EdgeHandler(self.__screen.getCanvas(), self, model) 
        # # Handles creation and deletion of nodes 
        # self.__nodeHandler = NodeHandler(self.__screen.getCanvas(), self, 
        #                                  model, self.__edgeHandler)   
        # # Handles 'physics based' calculations 
        # self.__physicsHandler = PhysicsHandler(self.__model, self.__getCanvasCentreCoords())  
        # # Refreshes canvas periodically   
        # self.__updateCanvas()

    def refreshCanvas() -> None: pass

    # Calculates and returns coords of the centre of the canvas  
    def __getCanvasCentreCoords(self) -> tuple: 
        canvas = self.__screen.getCanvas() 
        return (canvas.winfo_width() // 2, 
                canvas.winfo_height() // 2)
 

    # Returns True if an edge is being edited by a user 
    def isEdgeBeingEdited(self) -> bool: 
        return self.__edgeHandler.isEdgeBeingEdited()


    # Updates Screen to display options
    def enableEdgeWeightOptions(self) -> None:
        self.__screen.enableWeightOptions(self.__edgeHandler.getEdgeBeingEdited()) 
    

    # Updates Screen to hide options
    def disableEdgeWeightOptions(self) -> None:
        self.__screen.disableWeightOptions()


    # Draws a circle (node) on the canvas 
    def spawnNode(self, coords = None):
        if(coords == None): coords = self.__model.getInitialCoords()    
        if(self.__nodeHandler.spawnNode(coords) > 0):
            # Change the "Add Node" button's text to black 
            self.__screen.changeNodeButtonColour("black") 
        else:
            # Change the "Add Node" button's text to red 
            self.__screen.changeNodeButtonColour("red")  
        # Refresh screen to show changes  
        self.__screen.getWindow().update()  
    

    def handleNodeClickEvent(self, canvasNode : CanvasNode) -> None: 
         # If an edge is being edited, prevent a new one from being created
        if(self.__edgeHandler.isEdgeBeingEdited()): return

        # If an edge is already being drawn on screen
        if(self.__edgeHandler.isEdgeBeingDrawn()):
            # If edge successfully created 
            self.__edgeHandler.handleNodeConnection(canvasNode) 
        # If an edge is not currently being draw on screen
        else: 
            self.__createMovingEdge(canvasNode)
            self.__edgeHandler.setConnectionStartNode(canvasNode)
        # Updates window to display changes
        self.__screen.getWindow().update()   


    # Enables canvas events and sets boolean variable to true 
    def __createMovingEdge(self, canvasNode : CanvasNode) -> None:
        # Adds canvas event to draw lines
        self.__addMovingEdgeEvent(canvasNode)
        # Sets variable to True
        self.__edgeHandler.setEdgeBeingDrawn(True)


    # Disables canvas event that causes edge to follow mouse 
    def stopMovingEdge(self) -> None:
        # Remove event that draws line
        self.deleteMovingEdgeEvent()
        # Set edge being drawn to False
        self.__edgeHandler.setEdgeBeingDrawn(False)


    # Changes weight of current edge to passed value 
    def saveEdge(self, newWeight : int) -> None: 
        # Update weight of current edge object
        self.__edgeHandler.getCurrentEdgeObj().setWeight(newWeight)  
        # Update screen length if edge
        self.__edgeHandler.getCurrentEdgeObj().setscreenLen(self.__edgeHandler.calculateEdgeScreenLength(newWeight))
        # Clear variables used  
        self.__edgeHandler.clearVariables()  

    
    # Delete an edge from screen and relevant data structures
    def deleteEdge(self) -> None: 
        canvas = self.__screen.getCanvas()
        canvas.delete(self.__edgeHandler.getCurrentEdgeID())
        self.__model.deleteEdge(self.__edgeHandler.getCurrentEdgeObj())
        # Clear Variables 
        self.__edgeHandler.clearVariables()

    
    # Returns the Edge Canvas object
    def __getCanvasEdge(self) -> CanvasEdge: 
        connectedEdges = (self.__edgeHandler.getEdgeStartNode(), self.__edgeHandler.getEdgeEndNode())
        if(connectedEdges in self.__model.getEdges()): 
            return self.__model.getEdge(connectedEdges)
        else: return self.__model.getEdge(connectedEdges[::-1]) 


    def centreEdge(self) -> tuple: 
        circleOffset = self.__model.getCircleSize() // 2 
        # Reference to canvas 
        canvas = self.__screen.getCanvas()  
        x0, y0, _, _ = self.__edgeHandler.getEdgeStartNode().getCoords()
        # Get Coords of the destination node 
        x1, y1, _, _ = self.__edgeHandler.getEdgeEndNode().getCoords() 
        coords = (x0 + circleOffset, y0 + circleOffset, 
                  x1 + circleOffset, y1 + circleOffset)
        # Send updated coords to the canvas
        canvas.coords(self.__edgeHandler.getCurrentEdgeID(), coords)  
        # Return the updated coords of the edge 
        return coords 


    def __drawEdge(self, event : Event, canvasNode : CanvasNode) -> None:  
        canvas = self.__screen.getCanvas()   
        circleOffset = self.__model.getCircleSize() // 2
        x0, y0, _, _ = canvasNode.getCoords() 
        lineCoords, edgeID = None, None 

        # Checks if mouse has left the node the edge starts from
        collisions = canvas.find_overlapping(event.x, event.y, event.x, event.y)  
        # If the mouse is still in the node, the edge is not drawn yet
        if(canvasNode.getCanvasID() in collisions): return  
        # If there is no current edge 
        if(self.__edgeHandler.getCurrentEdgeID() is None): 
            # Create a new edge on screen
            edgeID = canvas.create_line(x0 + circleOffset, y0 + circleOffset, 
                                                    event.x, event.y, width = "3", arrow=BOTH)   
            self.__edgeHandler.setCurrentEdgeID(edgeID)
            # Lowers the priority of the edge, so it appears below nodes 
            canvas.tag_lower(edgeID) 
        # If there is an edge being drawn on screen
        else:    
            # Updates edge to follow mouse 
            # (Also if the node has moved the edges starting position is updated)
            lineCoords = (x0 + circleOffset, y0 + circleOffset, event.x, event.y)
            # Updates the lines coordinates 
            canvas.coords(self.__edgeHandler.getCurrentEdgeID(), lineCoords)

            
    # Add event to draw a line representing an edge
    def __addMovingEdgeEvent(self, canvasNode : CanvasNode): 
        self.__screen.getCanvas().bind("<Motion>", lambda event: self.__drawEdge(event, canvasNode))


    # Removes the event that draws lines representing edges 
    def deleteMovingEdgeEvent(self):  
        canvas = self.__screen.getCanvas()
        if("<Motion>" in canvas.bind()):
            canvas.unbind("<Motion>")


    # Updates position of nodes on the canvas
    def __redrawNodes(self): 
        canvas = self.__screen.getCanvas()
        for node in self.__model.getNodes():  
            x0, y0, _, _ = node.getCoords()
            canvas.moveto(node.getCanvasID(), round(x0), round(y0))
    

    # Update positions of edges on the canvas 
    def __redrawEdges(self):  
        circleOffset = self.__model.getCircleSize() // 2
        canvas = self.__screen.getCanvas()
        for edge in self.__model.getEdges():   
            startNode, endNode = edge.getNodes()
            x0, y0, _, _ = startNode.getCoords()
            x1, y1, _, _ = endNode.getCoords()
            canvas.coords(edge.getCanvasID(), round(x0 + circleOffset), round(y0 + circleOffset),
                          round(x1 + circleOffset), round(y1 + circleOffset))

        # If the user is creating an edge, the edges position is updated
        # (In case the start node is being moved on screen) 
        if self.__edgeHandler.isEdgeBeingDrawn() and self.__edgeHandler.getCurrentEdgeID(): 
            x0, y0, _, _ = self.__edgeHandler.getEdgeStartNode().getCoords()
            _, _, x1, y1 = canvas.coords(self.__edgeHandler.getCurrentEdgeID())
            newCoords = (x0 + circleOffset, y0 + circleOffset, x1, y1)
            # Updates the lines coordinates  
            canvas.coords(self.__edgeHandler.getCurrentEdgeID(), newCoords)


    # Spawns node when user double clicks the canvas 
    def __spawnNodeOnDoubleClick(self, event : Event) -> None:  
        # Sanity checking to prevent event triggering when it shouldn't 
        if(self.__nodeHandler.isNodeBeingDeleted()):
            self.__nodeHandler.setNodeBeingDeleted(False)
            return  
        if(self.__edgeHandler.isEdgeBeingDeleted()): 
            self.__edgeHandler.setEdgeBeingDeleted(False)
            return 
        if(self.__edgeHandler.isEdgeBeingDrawn() or 
           self.__edgeHandler.isEdgeBeingDrawn()): return
        
        circleOffset = self.__model.getCircleSize() // 2
        # X-Y coords of new node is where the users clicks 
        x0, y0, x1, y1 = event.x - circleOffset, event.y - circleOffset,\
            event.x + circleOffset, event.y + circleOffset
        self.spawnNode((x0, y0, x1, y1))
        

    # Add events to the canvas so users can interact with it 
    def addCanvasEvents(self): 
        canvas = self.__screen.getCanvas() 
        # Add event to delete current edge being drawn when the canvas is clicked
        canvas.bind("<Button-1>", lambda event: self.__edgeHandler.deleteEdgeOnClick(event))
        canvas.bind("<Double-Button-1>", lambda event: self.__spawnNodeOnDoubleClick(event))
    

    # Updates canvas to display nodes and edges interacting  
    # Need way to stop this being called when screen moves 
    def __updateCanvas(self) -> None: 
        
        self.__physicsHandler.applyPhysics()
        
        # Update positions updated of nodes onscreen 
        self.__redrawNodes()   
        # Update positions of edges onscreen
        self.__redrawEdges()
        # Update canvas 
        self.__screen.getWindow().update()
        # Schedule function to run after 50ms
        self.__screen.getWindow().scheduleFunctionExecution(self.__updateCanvas,
                                                            self.__model.getUpdateDelay())


# Listen to Paranoid by Black Sabbath
