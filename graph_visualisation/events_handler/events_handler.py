from tkinter import Canvas, Event
from ..events_model import EventsModel
from ..graph_components import CanvasGraph, CanvasNode 
from ..tools import * 


class EventsHandler(): 
    def __init__(self, canvas : Canvas, canvasGraph : CanvasGraph):
        self.__canvas = canvas
        self.__canvasGraph = canvasGraph
        
        self.__eventsModel = EventsModel()
        self.__eventsModel.setCanvasWidth(self.__canvas.winfo_width())
        self.__eventsModel.setCanvasHeight(self.__canvas.winfo_height())
        
        self.__creationTool = CreationTool(self.__eventsModel)
        self.__hoverTool = HoverTool(self.__eventsModel)
        self.__movementTool = MovementTool(self.__eventsModel)

        # Flags to prevent events being incorrectly triggered 
        self.__isNodeBeingDeleted = False 
        self.__isEdgeBeingDrawn = False 
        self.__isEdgeBeingEdited = False  
        self.__isEdgeBeingDeleted = False 

        self.__addCanvasEvents()


    def __canSpawnEventTrigger(self) -> bool: 
        if self.__isNodeBeingDeleted: 
            self.__isNodeBeingDeleted = False
            return False
        if self.__isEdgeBeingDeleted: 
            self.__isEdgeBeingDeleted = False
            return False
        if self.__isEdgeBeingDrawn: 
            self.__isEdgeBeingDrawn = False 
            return False
        return True 


    def __spawnNodeDoubleClick(self, event : Event) -> None:
        if not self.__canSpawnEventTrigger(): return
        circleOffset = self.__eventsModel.getNodeOffset()
        x0, y0 = event.x - circleOffset, event.y - circleOffset
        x1, y1 = event.x + circleOffset, event.y + circleOffset 
        self.spawnNode((x0, y0, x1, y1)) 


    def __addCanvasEvents(self) -> None: 
        if self.__canvas is None: return 
        # Add event to delete current edge being drawn when the canvas is clicked
        # self.__canvas.bind("<Button-1>", lambda event: self.__edgeHandler.deleteEdgeOnClick(event))
        self.__canvas.bind("<Double-Button-1>", lambda event: self.__spawnNodeDoubleClick(event))


    def __moveNode(self, event : Event, canvasNode : CanvasNode) -> None:  
        # self.__controller.deleteMovingEdgeEvent()
        self.__isEdgeBeingDrawn = False 
        # Stops the node from only being partially rendered (not sure why this works, I forgot)
        self.__canvas.config(cursor="arrow")
        canvasNode.setColour(self.__eventsModel.getNodeHoverColour())
        # self.__canvas.itemconfig(canvasNode.getCanvasID(), fill=self.__eventsModel.getNodeHoverColour()) 
        self.__movementTool.moveNode(canvasNode, (event.x, event.y))


    def __deleteNode(self, canvasNode : CanvasNode) -> None:  
        if self.__isEdgeBeingEdited: return
        self.__isNodeBeingDeleted = True  

        # TODO stop edge being drawn 
        # The event to draw an edge can still trigger 
        # so it needs to be deleted
        # self.__edgeHandler.deleteEdgeBeingDrawn()
        
        self.__canvas.delete(canvasNode.getCanvasID())
        self.__creationTool.deleteNode(self.__canvasGraph, canvasNode)
        # print(self.__canvasGraph.getNodes()) 
        

    # Add event handlers to the newly created node
    def __addNodeEvents(self, canvasNode : CanvasNode) -> None:     
        # Add event to change nodes colour when the mouse hovers over it
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Enter>", lambda _: self.__hoverTool.nodeOnHover(canvasNode))
        # Add event to change nodes colour when the mouse stops hovering over it
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Leave>", lambda _: self.__hoverTool.nodeOnLeave(canvasNode)) 
        # Add event listener to move node when it's dragged by the mouse 
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<B1-Motion>", lambda event: self.__moveNode(event, canvasNode))    
        # Add event listener to detect when mouse button released 
        # self.__canvas.tag_bind(canvasNode.getCanvasID(), "<ButtonRelease-1>", lambda _: self.__resetDragged(canvasNode))
        
        # Add event listener to add an edge when a node is clicked 
        # self.__canvas.tag_bind(circle, "<Button-1>", lambda _: self.__controller.handleNodeClickEvent(canvasNode))
        # Add event to delete a node when it is double clicked 
        self.__canvas.tag_bind(canvasNode.getCanvasID(), "<Double-Button-1>", lambda _: self.__deleteNode(canvasNode)) 



    def spawnNode(self, coords : tuple) -> bool: 
        if self.__isNodeBeingDeleted: 
            self.__isNodeBeingDeleted = False 
            return False

        if not self.__creationTool.canNodeBeSpawned(self.__canvas, coords): 
            return False 
        
        canvasNode = self.__creationTool.createNode(self.__canvasGraph, coords)
        self.__creationTool.renderNode(self.__canvas, canvasNode)
        self.__addNodeEvents(canvasNode) 
        # print(self.__canvasGraph.getNodes())
        return True 


