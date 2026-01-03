# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

class SortController():
    def __init__(self, screen, model, dataModel) -> None:
        self.__screen = screen 
        self.__model = model 
        self.__dataModel = dataModel
    
    # Changes the sort direction 
    def toggleSortDirection(self):
        # Changes the sort direction
        self.__dataModel.toggleSortDirection()  
        # Disables the button that called the function and enables the currently disabled button
        self.__screen.disableEnableButtons(self.__dataModel.isAscending())

# Listen to Give Me Novacaine by Green Day