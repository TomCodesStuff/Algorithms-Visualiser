from __future__ import annotations 

# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from typing import TYPE_CHECKING
import screens as scr 

if TYPE_CHECKING:
    from app_window import Window

    ScreenClass = type[scr.AlgorithmScreen]
    ControllerClass = type[scr.AlgorithmController]
    ModelClass = type[scr.AlgorithmModel]
    DataModelClass = type[scr.AlgorithmDataModel]


class ScreenCreator(): 
    @staticmethod
    def __createScreen(window : Window, mvcClasses : tuple[ScreenClass, ControllerClass, ModelClass, DataModelClass] ) -> scr.AlgorithmScreen: 
        screenClass, controllerClass, modelClass, dataModelClass = mvcClasses
        screen = screenClass(window)
        model = modelClass()
        dataModel = dataModelClass()
        controller = controllerClass(screen, model, dataModel)
        screen.setController(controller)
        screen.setModel(model)
        screen.setDataModel(dataModel)
        return screen 


    @classmethod
    def createScreen(cls, window : Window, screenType : str) -> scr.Screen|None:
        match screenType:
            case scr.ScreenType.INTRO: return scr.IntroductionScreen(window)  
            case scr.ScreenType.SEARCH: 
                return cls.__createScreen(window, (
                    scr.AlgorithmScreen, 
                    scr.AlgorithmController, 
                    scr.AlgorithmModel, 
                    scr.AlgorithmDataModel))
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