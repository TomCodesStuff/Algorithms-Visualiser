from tkinter import Canvas
from data_structures import Node
from ..events_model import EventsModel
from ..graph_components import CanvasGraph, CanvasNode


class CreationTool(): 
    def __init__(self, eventsModel : EventsModel): 
        self.__eventsModel = eventsModel


    # TODO re-add max number nodes check 
    def canNodeBeSpawned(self, canvas : Canvas, nodeCoords : tuple) -> bool: 
        if nodeCoords == (): nodeCoords = self.__eventsModel.getDefaultNodeCoords()
        x0, y0, x1, y1 = nodeCoords 
        overlapOffset = self.__eventsModel.getOverlapOffset()
        overlapping_nodes = canvas.find_overlapping(x0 - overlapOffset, y0 - overlapOffset, 
                                                    x1 + overlapOffset, y1 + overlapOffset)
        return True if len(overlapping_nodes) == 0 else False


    def renderNode(self, canvas : Canvas, canvasNode : CanvasNode) -> None: 
        x0, y0, x1, y1 = canvasNode.getCoords() 
        canvasID = canvas.create_oval(x0, y0, x1, y1, outline="black", fill=canvasNode.getColour())
        canvasNode.setCanvasID(canvasID)


    def createNode(self, canvasGraph : CanvasGraph, coords : tuple) -> CanvasNode:
        if coords == (): coords = self.__eventsModel.getDefaultNodeCoords()
        canvasNode = CanvasNode(Node(), coords, self.__eventsModel.getDefaultNodeSize()) 
        canvasGraph.addCanvasNode(canvasNode)
        return canvasNode


    def deleteNode(self, canvasGraph : CanvasGraph, canvasNode : CanvasNode):
        canvasGraph.deleteCanvasNode(canvasNode)
        