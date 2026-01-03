# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


import tkinter as tk 


class SortScreen():    
    def initScreen(self) -> None:
        self.createBaseLayout()
        self.loadAlgorithmOptions("sort")
       
        # Controller and Model classes
        self.__sortModel = None
        self.__sortController = None

        self.__createSortOptionButtons()
        self.configSpeedSlider(to_= self.__sortModel.getSliderEnd(), from_=self.__sortModel.getSliderStart(),
                               interval=self.__sortModel.getSlidernterval(), milliseconds=True)
        self.addWidgetToArray(self.__descendingOption)
    
    # Creates the buttons that lets userr change between sorting by ascending or descending order
    def __createSortOptionButtons(self):
        self.__radioButtonsFrame = tk.Frame(self.getOptionsWidgetFrame(), background="white")
        self.__radioButtonsFrame.pack(pady=(10, 0)) 
        self.__createAscRadioButton()
        self.__createDescRadioButton()

    # Creates the button to toggle ascending order
    def __createAscRadioButton(self):
        self.__ascendingOption = tk.Button(self.__radioButtonsFrame, text="Sort Ascending.", width = self.__sortModel.getButtonWidth(), 
                                           relief = "solid", font = (self.getFont(), self.getFontSize()), state="disabled", command=self.__sortController.toggleSortDirection)
        self.__ascendingOption.pack()
    
    # Creates the button to toggle descending order
    def __createDescRadioButton(self):
        self.__descendingOption = tk.Button(self.__radioButtonsFrame, text="Sort Descending.", width = self.__sortModel.getButtonWidth(), 
                                            relief = "solid", font = (self.getFont(), self.getFontSize()), command=self.__sortController.toggleSortDirection)
        self.__descendingOption.pack(pady=(5, 0))
    
    # Disable and enables the sort direction buttons when one is pressed 
    def disableEnableButtons(self, isAscending: bool): 
        if(isAscending): 
            self.__ascendingOption.config(state="disabled")
            self.__descendingOption.config(state="active")  
            self.removeWidgetFromArray(self.__ascendingOption)
            self.addWidgetToArray(self.__descendingOption)
        else:
            self.__ascendingOption.config(state="active")
            self.__descendingOption.config(state="disabled") 
            self.addWidgetToArray(self.__ascendingOption)
            self.removeWidgetFromArray(self.__descendingOption)


# Wretches and Kings by Linkin Park                 