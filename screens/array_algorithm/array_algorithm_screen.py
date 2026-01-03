
# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


import tkinter as tk
import random 
from algorithm_base import AlgorithmScreen


class ArrayAlgorithmScreen(AlgorithmScreen):
    def __init__(self, window):
        super().__init__(window)


    # Creates a slider that allows users to alter an arrays size
    def __createArrayAdjuster(self) -> None:
        self.__arraySizeSlider = tk.Scale(self.getOptionsWidgetFrame(), from_ = 1, to_ = self.__model.getMaxBars(), 
                                          length = self.getOptionsWidgetFrame().winfo_width(),\
            orient = "horizontal", bg = "white", highlightbackground = "white", command = self.__controller.adjustArray)
        self.__arraySizeSlider.pack(pady = (10, 0))
        self.addToggleableWidget(self.__arraySizeSlider)


    # Creates buttons the allow algorithms to be sorted and shuffled
    def __createSortShuffleButtons(self) -> None: 
        self.__arraySortShuffleFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white") 
        self.__arraySortShuffleFrame.pack(pady=(20, 0)) 

        self.__sortButton = tk.Button(self.__arraySortShuffleFrame, text="Sort.", width = 7, relief = "solid", 
                                      font = (self.getFont(), self.getFontSize()), command=self.__sortArray)
        self.__sortButton.grid(row = 0, column = 0, padx = (9,5)) 
        self.__shuffleButton = tk.Button(self.__arraySortShuffleFrame, text="Shuffle.", width = 7, relief = "solid", 
                                         font = (self.getFont(), self.getFontSize()), command=self.__shuffleArray)
        self.__shuffleButton.grid(row = 0, column = 1, padx = (3,8)) 
        self.addToggleableWidget(self.__sortButton)
        self.addToggleableWidget(self.__shuffleButton)
    

    # Makes sure that target generated has (almost) equal chance to be in the array or not 
    def targetRandom(self) -> int: 
        # Generates decimal between 0 and 1 
        # If decimal is less than or equal to 0.5 make the target in the array 
        # Gives a roughly 50-50 chance for target to be in the array or out the array
        if(random.random() < 0.5): return self.targetIn()
        # Else call function to generate the target so it is not in the array
        else: return self.targetOut()
    

    # Guarantees target is in the array
    def targetIn(self) -> int: 
       # Randomly chooses index from array and returns the number at that index
       return self.__dataModel.getArray()[random.randint(0, len(self.__dataModel.getArray()) - 1)] 


    # Guarantees target is not in array
    # TODO -> if want target to not be in the array choose a number from 0 to lowest val in array 
    #      -> or make list of nums from min to max excluding elements and select from there 
    def targetOut(self) -> int: 
        # Chooses a number between the range of arrays smallest value - 20 and arrays largest value + 20
        target = random.randint(min(self.__dataModel.getArray()) - self.__model.getBuffer(), 
                                max(self.__dataModel.getArray()) + self.__model.getBuffer())
        # If generated number in array re-run function
        if target in self.__dataModel.getArray(): self.targetOut()
        # If generated number not in array then just return value
        else: return target
            

    # Sorts and displays the array
    def __sortArray(self) -> None:
        self.__dataModel.sortArray()
        self.__controller.displayArray() 
    

    # Shuffles and displays the array
    def __shuffleArray(self) -> None:
        self.__dataModel.shuffleArray()
        self.__controller.displayArray()  


    # This functions handles creating and displaying the options the user is presented with
    def createArrayOptions(self) -> None: 
        self.__createArrayAdjuster()
        self.__createSortShuffleButtons()

         
    def render(self):
        self.createBaseLayout()
        self.createArrayOptions()
    