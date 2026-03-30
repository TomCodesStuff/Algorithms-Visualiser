# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class QuickSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Quick Sort"  
    

    # Quick Sort Algorithm
    # Pivot selection using median of three 
    def run(self) -> int:  
        self.__quickSortHelper(0, len(self.getArray()) - 1)
        self.updateArrayOnScreen() 
        self.delay() 
        self.coolEndingAnimation()
        return 1 
    
    # Recusive implementation of quick sort 
    def __quickSortHelper(self, start, end):   
        if(start >= end): return
        # Finds pivot and adjusts elements relative to pivot
        pivotIndex = self.__partition(start, end) 
        self.__quickSortHelper(start, pivotIndex - 1) 
        self.__quickSortHelper(pivotIndex + 1, end)
      
    def __partition(self, start, end):  
        # Middle of the array 
        mid = (start + end) // 2
        # Pivot is median of the elements at indexes start, mid, end 
        pivot, startPivotIdx = sorted([(self.getElement(start), start), (self.getElement(mid), mid), (self.getElement(end), end)])[1]   
        # The pivots index can change when elements are moved left/right of it
        pivotIdx = startPivotIdx
        
        # Iterate through any elements between pivot to end of array
        for i in range(startPivotIdx + 1, end + 1):  
            self.changeBarColour(pivotIdx, "orange")
            self.changeBarColour(i, "red")
            self.updateArrayOnScreen() 
            self.delay()

            # If element is less than/greater than or equal to the pivot 
            if(not self.isSwapNeeded(i, pivotIdx) or self.areElementsEqual(i, pivotIdx)):
                # Shift elements from pivot to i, one place right
                self.__shiftRight(pivotIdx, i)
                # Increment pivotIdx to point to new index of the pivot
                pivotIdx += 1
        
        # Iterate between elements between start of array and the pivot initial index
        i = 0 
        while(i != startPivotIdx): 
            self.changeBarColour(pivotIdx, "orange")
            self.changeBarColour(i, "red")
            self.updateArrayOnScreen() 
            self.delay()
            # If element is greater/smaller than the pivot 
            if(self.isSwapNeeded(i, pivotIdx) and not self.areElementsEqual(i, pivotIdx)):
                # Shift elements between i and the pivot one place left
                self.__shiftLeft(i, pivotIdx)   
                # Decrement pivotIdx to point to new index of the pivot
                pivotIdx -= 1  
                # Decrement startPivotIdx
                # i is not incremented as elements have been shifted so a different value is now at i
                startPivotIdx -= 1 
            # If element is less than or equal to pivot, move to next element
            else: i+=1
        return pivotIdx
    
    def __shiftRight(self, start, end): 
        index = end 
        value = self.getElement(end)
        while(index != start):  
            self.changeElement(index, self.getElement(index - 1))
            index-=1  
        self.changeElement(index, value)
        
   
        
    def __shiftLeft(self, start, end): 
        index = start 
        value = self.getElement(start)
        while(index != end):  
            self.changeElement(index, self.getElement(index + 1))
            index+=1  
        self.changeElement(index, value)  
      

                     
# Listen to Times like these by the Foo Fighters