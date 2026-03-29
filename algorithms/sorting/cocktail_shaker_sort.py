# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from ..algorithm import Algorithm


class CocktailShakerSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Cocktail Shaker Sort" 


    # Cocktail Shaker Sort Algorithm
    def run(self) -> int: 
        start = 0 
        end = len(self.getArray()) - 1 
        swapped = True

        # While elements have been swapped 
        while(swapped):
            # Set swapped to false
            swapped = False
            # Iterate between indexes start and end
            for i in range(start, end): 
                self.changeBarColour(i, "red") 
                self.updateArrayOnScreen() 
                self.delay()
                
                # If elements need to be swapped
                if(self.isSwapNeeded(i, i + 1)):
                    # Swap them
                    self.swapElements(i, i + 1) 
                    self.swapBarColours(i, i + 1)
                    # Set swapped to true
                    swapped = True
            
            self.changeBarColour(i, "red") 
            self.updateArrayOnScreen() 
            self.delay()

            # If no swaps were made, halt algorithm 
            if(not swapped): 
                self.updateArrayOnScreen()
                self.delay()
                self.coolEndingAnimation()
                return 1

            # Decrement end 
            end -= 1
            # Iterate between indexes end - 1 and start + 1
            for i in range(end - 1, start - 1, -1):
                self.changeBarColour(i, "red") 
                self.updateArrayOnScreen() 
                self.delay()
                # If elmenents need to be swapped, swap them
                if(self.isSwapNeeded(i, i + 1)): 
                    self.swapElements(i, i + 1)
                    # Set swapped to True 
                    swapped = True 
            # Increment start
            start += 1 

        self.updateArrayOnScreen()
        self.delay()
        self.coolEndingAnimation()
        return 1

# Listen to What You Know by Two Door Cinema Club 