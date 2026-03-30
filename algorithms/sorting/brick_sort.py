# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class BrickSort(Algorithm):
    # Constructor
    def __init__(self,):
       super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Brick Sort" 
    

    # Brick Sort Algorithm
    def run(self) -> int: 
        # Length of the array
        n = len(self.getArray())
        swapped = True 
        # While swapped is true
        while(swapped):
            swapped = False
            # Iterate through odd indexes of the array
            for i in range(1, n - 1, 2): 
                self.changeBarColour(i, "red") 
                self.updateArrayOnScreen() 
                self.delay()
                # If elements are in the wrong the order
                if(self.isSwapNeeded(i, i + 1)):
                    # Swap elements
                    self.swapElements(i, i + 1)
                    self.changeBarColour(i, "red") 
                    self.updateArrayOnScreen() 
                    self.delay()
                    swapped = True
            
            self.changeBarColour(i, "red") 
            self.updateArrayOnScreen() 
            self.delay()
            
            # If no swaps are performed
            if(not swapped): break

            swapped = False
            # Iterate through even indexes of the array
            for i in range(0, n - 1, 2):
                self.changeBarColour(i, "red") 
                self.updateArrayOnScreen() 
                self.delay()
                # If elements are in the wrong the order
                if(self.isSwapNeeded(i, i + 1)):
                    # Swap elements
                    self.swapElements(i, i + 1)
                    self.changeBarColour(i, "red") 
                    self.updateArrayOnScreen() 
                    self.delay()
                    swapped = True  
        self.updateArrayOnScreen()
        self.delay() 
        self.coolEndingAnimation()
        return 1

# Listen to Lithium by Nirvana 