# from events_handler import EventsModel
from ..graph_components import CanvasNode


class HoverTool():
    def __init__(self, eventsModel):
        self.__eventsModel = eventsModel
    

    def nodeOnHover(self, canvasNode : CanvasNode) -> None:
        canvasNode.setColour(self.__eventsModel.getNodeHoverColour())


    def nodeOnLeave(self, canvasNode : CanvasNode) -> None:
        canvasNode.setColour(self.__eventsModel.getDefaultNodeColour())