# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from ..algorithm import Algorithm


class GnomeSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Gnome Sort" 


    # Gnome Sort Algorithm
    def run(self) -> int: 
        # Length of the array
        n = len(self.getArray())
        pos = 0  
        # While pos is less than the length of the array
        while(pos < n): 
            self.changeBarColour(pos, "red")
            self.updateArrayOnScreen()
            self.delay()

            # If pos is at the start of the array, increment pos
            if(pos == 0): pos += 1 
            # If element at pos and pos - 1 need to be swapped
            if(self.isSwapNeeded(pos - 1, pos)):
                self.swapElements(pos, pos - 1)
                self.changeBarColour(pos - 1, "red")
                self.updateArrayOnScreen()
                self.delay()
                # Decrement pos
                pos -= 1
            # If elements at pos and pos - 1 are in the right place
            else: 
                # Increment pos 
                pos += 1  
        
        self.updateArrayOnScreen()
        self.delay()
        self.coolEndingAnimation()
        return 1 
        
# Listen to Smells Like Teen Spirit by Nirvana 