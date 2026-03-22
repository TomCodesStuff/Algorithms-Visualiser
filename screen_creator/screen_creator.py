from __future__ import annotations
from typing import TYPE_CHECKING, Type, Tuple 
from screens import *
from enums import ScreenType

if TYPE_CHECKING:
    from app_window import Window
    Screen = Type[AlgorithmScreen]
    Controller = Type[AlgorithmController]
    Model = Type[AlgorithmModel]
    Hello = Type[DataStructure]

class ScreenCreator(): 
    @staticmethod
    def __createAlgorithmScreen(window : Window, mvcClasses :  Tuple[Screen, Controller, Model, Hello]) -> AlgorithmScreen: 
        screenClass, controllerClass, modelClass, dataStructureClass = mvcClasses
        screen = screenClass(window)
        model = modelClass()
        dataStructure = dataStructureClass()
        controller = controllerClass(screen, model, dataStructure)
        
        screen.setController(controller)
        screen.setModel(model)
        screen.setDataStructure(dataStructure)
        return screen 


    @classmethod
    def createScreen(cls, window : Window, screenType : ScreenType) -> ScreenInterface|None:
        match screenType:
            case ScreenType.MAIN_MENU: return MainMenu(window)  
            case ScreenType.SEARCH: 
                return cls.__createAlgorithmScreen(window, (
                    SearchScreen, 
                    SearchController, 
                    SearchModel, 
                    Array))
            case ScreenType.SORT:
               return cls.__createAlgorithmScreen(window, (
                   SortScreen, 
                   SortController, 
                   SortModel, 
                   Array))
            #case scr.ScreenType.TRAVERSAL:
            #    return cls.__createAlgorithmScreen(window, (
            #        scr.TraversalScreen, 
            #        scr.TraversalController, 
            #        scr.TraversalModel, 
            #        scr.ShareddataStructure))
            #case _: return None


