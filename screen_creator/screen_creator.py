from __future__ import annotations
from typing import TYPE_CHECKING, Type, Tuple 
from screens import *
from enums import ScreenType

if TYPE_CHECKING:
    from app_window import Window
    Screen = Type[AlgorithmScreen]
    Controller = Type[AlgorithmController]
    Model = Type[AlgorithmModel]
    

class ScreenCreator(): 
    @staticmethod
    def __createAlgorithmScreen(window : Window, mvcClasses :  Tuple[Screen, Controller, Model]) -> AlgorithmScreen: 
        screenClass, controllerClass, modelClass, dataModelClass = mvcClasses
        screen = screenClass(window)
        model = modelClass()
        dataModel = None 
        controller = controllerClass(screen, model, dataModel)
        
        screen.setController(controller)
        screen.setModel(model)
        screen.setDataModel(dataModel)
        return screen 


    @classmethod
    def createScreen(cls, window : Window, screenType : ScreenType) -> ScreenInterface|None:
        match screenType:
            case ScreenType.MAIN_MENU: return MainMenu(window)  
            case ScreenType.SEARCH: 
                return cls.__createAlgorithmScreen(window, (
                    AlgorithmScreen, 
                    AlgorithmController, 
                    AlgorithmModel, 
                    None))
            #case scr.ScreenType.SORT:
            #    return cls.__createAlgorithmScreen(window, (
            #        scr.SortScreen, 
            #        scr.SortController, 
            #        scr.SortModel, 
            #        scr.SharedDataModel))
            #case scr.ScreenType.TRAVERSAL:
            #    return cls.__createAlgorithmScreen(window, (
            #        scr.TraversalScreen, 
            #        scr.TraversalController, 
            #        scr.TraversalModel, 
            #        scr.SharedDataModel))
            #case _: return None


