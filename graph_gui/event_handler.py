from tkinter import Canvas, Event
from .node_handler import NodeHandler 
from canvas_objects import CanvasNode


class EventHandler(): 
    def __init__(self, canvas : Canvas):
        self.__canvas = canvas
        self.__addCanvasEvents()
        self.__nodeHandler = NodeHandler() 

        # Flags to prevent events being incorrectly triggered 
        self.__isNodeBeingDeleted = False 
        self.__isEdgeBeingDrawn = False 
        self.__isEdgeBeingEdited = False  
        self.__isEdgeBeingDeleted = False 


    def __spawnNodeDoubleClick(self, event : Event) -> None:
        if self.__isNodeBeingDeleted: 
            self.__isNodeBeingDeleted = False
            return 
        if self.__isEdgeBeingDeleted: 
            self.__isEdgeBeingDeleted = False
            return
        if self.__isEdgeBeingDrawn: 
            self.__isEdgeBeingDeleted = False 
            return

        circleOffset = self.__nodeHandler.getCircleOffset()
        x0, y0 = event.x - circleOffset, event.y - circleOffset
        x1, y1 = event.x + circleOffset, event.y + circleOffset 
        self.spawnNode((x0, y0, x1, y1)) 
        self.__canvas.update()


    def __addCanvasEvents(self) -> None: 
        if self.__canvas is None: return 
        # Add event to delete current edge being drawn when the canvas is clicked
        # self.__canvas.bind("<Button-1>", lambda event: self.__edgeHandler.deleteEdgeOnClick(event))
        self.__canvas.bind("<Double-Button-1>", lambda event: self.__spawnNodeDoubleClick(event))


    
    def __drawNode(self, canvasNode : CanvasNode) -> None:
        x0, y0, x1, y1 = canvasNode.getCoords() 
        canvasID = self.__canvas.create_oval(x0, y0, x1, y1, outline="black", fill=canvasNode.getMainColour())
        canvasNode.setCanvasID(canvasID)


    def spawnNode(self, coords : tuple) -> int:  
        if coords == None: coords = self.__nodeHandler.getDefaultNodeCoords() 

        x0, y0, x1, y1 = coords  
        nodepadding = self.__nodeHandler.getNodePadding()
        circleOffset = self.__nodeHandler.getCircleOffset()
        nodeDistanceOffset = nodepadding + circleOffset

        if self.__isNodeBeingDeleted: 
            self.__isNodeBeingDeleted = False 
            return 1 
        
        # TODO check to see if edges need to be excluded 
        overlapping_nodes = self.__canvas.find_overlapping(x0 - nodeDistanceOffset, y0 - nodeDistanceOffset, 
                                                           x1 + nodeDistanceOffset, y1 + nodeDistanceOffset)
        # TODO add check for maximum number nodes 
        if not overlapping_nodes:
            canvasNode = self.__nodeHandler.createNode(coords) 
            self.__drawNode(canvasNode) 
            return 0
        return 1

