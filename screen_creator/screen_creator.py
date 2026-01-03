from __future__ import annotations
from typing import TYPE_CHECKING, Type, Tuple 
import screens as scr 

if TYPE_CHECKING: 
    from app_window import Window 
    MVCClasses = Tuple[
        Type[scr.AlgorithmScreen],
        Type[scr.AlgorithmController],
        Type[scr.AlgorithmModel],
        Type[scr.AlgorithmDataModel]
    ]


class ScreenCreator(): 
    
    @staticmethod
    def __createClasses(window : Window, mvcClasses : MVCClasses) -> scr.AlgorithmScreen: 
        Screen, Controller, Model, DataModel = mvcClasses
        screen = Screen(window)
        model = Model()
        dataModel = DataModel()
        controller = Controller(screen, model, dataModel)
        
        screen.setController(controller)
        screen.setModel(model)
        screen.setDataModel(dataModel)
        return screen 


    @classmethod
    def createScreen(cls, window : Window, screenType : scr.ScreenType) -> scr.Screen|None:
        match screenType:
            case scr.ScreenType.INTRO: return scr.IntroductionScreen(window)  
            case scr.ScreenType.SEARCH: 
                return cls.__createClasses(window, (
                    scr.SearchScreen, 
                    scr.SearchController, 
                    scr.SearchModel, 
                    scr.SharedDataModel))
            case scr.ScreenType.SORT:
                return cls.__createClasses(window, (
                    scr.SortScreen, 
                    scr.SortController, 
                    scr.SortModel, 
                    scr.SharedDataModel))
            case scr.ScreenType.TRAVERSAL:
                return cls.__createClasses(window, (
                    scr.TraversalScreen, 
                    scr.TraversalController, 
                    scr.TraversalModel, 
                    scr.SharedDataModel))
            case _: return None


