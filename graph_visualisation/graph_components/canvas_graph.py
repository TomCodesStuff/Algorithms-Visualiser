from typing import Set
from .canvas_node import CanvasNode
from data_structures import Graph

class CanvasGraph():
    def __init__(self, graph : Graph): 
        self.__graph = graph
        self.__nodes = set() 
        self.__edges = set()
    


    def addCanvasNode(self, canvasNode : CanvasNode) -> None: 
        self.__nodes.add(canvasNode) 


    def deleteCanvasNode(self, canvasNode : CanvasNode) -> None: 
        if canvasNode in self.__nodes:
            self.__nodes.remove(canvasNode)
    
    
    def getNodes(self) -> Set[CanvasNode]: 
        return self.__nodes 