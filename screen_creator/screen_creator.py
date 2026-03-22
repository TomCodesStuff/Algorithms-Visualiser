from __future__ import annotations
from typing import TYPE_CHECKING, Type, Tuple 
from screens import *
from .screen_enums import ScreenType

# TODO NOT a fan of this wtf 

if TYPE_CHECKING:
    from app_window import Window
    ScreenClass = Type[AlgorithmScreen]
    ControllerClass = Type[AlgorithmController]
    ModelClass = Type[AlgorithmModel]


class ScreenCreator(): 
    @staticmethod
    def __createScreen(window : Window, mvcClasses : Tuple[ScreenClass, ControllerClass, ModelClass] ) -> AlgorithmScreen: 
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
            case ScreenType.INTRO: return MainMenu(window)  
            case ScreenType.SEARCH: 
                return cls.__createScreen(window, (
                    AlgorithmScreen, 
                    AlgorithmController, 
                    AlgorithmModel, 
                    None))
            #case scr.ScreenType.SORT:
            #    return cls.__createScreen(window, (
            #        scr.SortScreen, 
            #        scr.SortController, 
            #        scr.SortModel, 
            #        scr.SharedDataModel))
            #case scr.ScreenType.TRAVERSAL:
            #    return cls.__createScreen(window, (
            #        scr.TraversalScreen, 
            #        scr.TraversalController, 
            #        scr.TraversalModel, 
            #        scr.SharedDataModel))
            #case _: return None


