from app_window import Window
from enums import ScreenType

if(__name__ == "__main__"):
    window = Window(750, 500) 
    window.create()
    window.loadScreen(ScreenType.MAIN_MENU)
    window.show() 
else:
    print("This file has no functions to import")
    
# Listen to Walk by Foo Fighters  
# Seriously listen to it, it means a lot to me