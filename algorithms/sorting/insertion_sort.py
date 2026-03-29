# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from ..algorithm import Algorithm


class InsertionSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__() 

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Insertion Sort"  
    

    # Stable Selection Sort Algorithm
    def run(self) -> int: 
        n = len(self.getArray())
        # Iterate through array, the first element is considered as sorted 
        for i in range(1, n): 
            self.changeBarColour(i - 1, "orange")
            self.changeBarColour(i, "red")
            self.updateArrayOnScreen()
            self.delay()

            # The left pointer keeps track of sorted element being compared to the sorted element
            leftPtr = i - 1
            # The right pointer keeps track of the unsorted element
            rightPtr = i 
            # Iterate until the start of the sorted array or 
            # the unsorted element is in the right place 
            while(leftPtr >= 0 and self.isSwapNeeded(leftPtr, rightPtr)): 
                # Swap elements indexes leftPtr, rightPtr
                self.swapElements(leftPtr, rightPtr)
                leftPtr -= 1
                rightPtr -= 1  

                self.changeBarColour(i, "orange")
                self.changeBarColour(rightPtr, "red")
                self.updateArrayOnScreen()
                self.delay()
        
        self.coolEndingAnimation()
        return 1 

                     
# Listen to Highway to Hell by ACDC