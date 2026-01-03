# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()
class SearchController():
    def __init__(self, screen, model, dataModel) -> None:
        self.__searchScreen = screen
        self.__searchModel = model
        self.__dataModel = dataModel
    
    # Returns the text to be displayed above the slider
    def updateSliderText(self, value : str) -> str:
        self.__updateTargetSetting(value)
        return self.__searchModel.getSliderText(int(value))
        
    # Updates the target setting attribute in the DataModel class 
    def __updateTargetSetting(self, value : str) -> None:
        self.__dataModel.setTargetSetting(int(value)) 
                    
# Listen to Give Me Novacaine by Green Day