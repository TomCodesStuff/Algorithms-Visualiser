# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class BubbleSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Bubble Sort" 


    # Bubble Sort Algorithm
    def run(self) -> int: 
        array = self.getArray()  
        n = len(array)
        # Iterate through array
        for i in range(n): 
            # No swaps have been made
            swapped = False
            # Iterate from start of array to last sorted element
            for j in range(0, n - i - 1): 
                self.changeBarColour(j, "red") 
                self.updateArrayOnScreen() 
                self.delay()
                # If adjacent element needs to be swapped with current element
                if(self.isSwapNeeded(j, j + 1)): 
                    self.swapElements(j, j + 1)
                    self.swapBarColours(j, j + 1)
                    # Swap has been performed
                    swapped = True
            # If no swaps have been made, the array is sorted 
            if(not swapped):
                self.coolEndingAnimation() 
                return 1
        return 1

# Listen to Times like these by the Foo Fighters