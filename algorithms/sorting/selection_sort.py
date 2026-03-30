# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
   print("This is file shouldn't be run on it's own. \nIt should be imported only.")
   exit()


from algorithms import Algorithm


class SelectionSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__() 


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Selection Sort"  


    # Stable Selection Sort Algorithm
    def run(self) -> int: 
        n = len(self.getArray())   
        # Iterate through each element in the array
        for i in range(n): 
            # Index of the current smallest/largest element in the array
            swapIdx = i 
            # Iterate through elements from i + 1 to the end of the current array 
            for j in range(i + 1, n):  
                self.changeBarColour(j , "red") 
                self.updateArrayOnScreen() 
                self.delay()
                # If current element smaller/larger than previous smallest/largest element
                if(not self.isSwapNeeded(j, swapIdx)): swapIdx = j   
            # Shift elements right 
            self.__shiftRight(i, swapIdx) 
            
            self.changeBarColour(i, "orange")
            self.updateArrayOnScreen() 
            self.delay()
        
        self.updateArrayOnScreen()
        self.delay()
        self.coolEndingAnimation() 
        return 1
    
    # Shifts elements between the specified indexes one place right 
    def __shiftRight(self, start, end): 
        index = end 
        value = self.getElement(end)
        while(index != start):  
            self.changeElement(index, self.getElement(index - 1))
            index-=1  
        self.changeElement(index, value)
        
                     
# Listen to Ain't No Rest For The Wicked by Cage the Elephant