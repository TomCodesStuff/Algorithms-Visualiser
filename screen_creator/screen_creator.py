from __future__ import annotations
from typing import TYPE_CHECKING, Type, Tuple 
import screens as scr 

# TODO NOT a fan of this wtf 

if TYPE_CHECKING:
    from app_window import Window

    ScreenClass = Type[scr.AlgorithmScreen]
    ControllerClass = Type[scr.AlgorithmController]
    ModelClass = Type[scr.AlgorithmModel]


class ScreenCreator(): 
    @staticmethod
    def __createScreen(window : Window, mvcClasses : Tuple[ScreenClass, ControllerClass, ModelClass] ) -> scr.AlgorithmScreen: 
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
    def createScreen(cls, window : Window, screenType : scr.ScreenType) -> scr.Screen|None:
        match screenType:
            case scr.ScreenType.INTRO: return scr.IntroductionScreen(window)  
            case scr.ScreenType.SEARCH: 
                return cls.__createScreen(window, (
                    scr.AlgorithmScreen, 
                    scr.AlgorithmController, 
                    scr.AlgorithmModel, 
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


