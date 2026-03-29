# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from ..algorithm import Algorithm


class MergeSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Merge Sort" 
    

    # (In place) Merge Sort Algorithm
    def run(self) -> int: 
        # Call function to peform splitting into sub arrays 
        self.mergeSortHelper(0, len(self.getArray()) - 1)
        self.coolEndingAnimation() 
        return 1
    
    def mergeSortHelper(self, leftPtr, rightPtr):   
        # If sub-arrays are of size one, they are considered sorted 
        if(leftPtr >= rightPtr): return  
        # Calculates middle of sub-array
        mid = (leftPtr + rightPtr) // 2 
        # Splits sub-array in half into two subarrays
        self.mergeSortHelper(leftPtr, mid)
        self.mergeSortHelper(mid+1, rightPtr)
        # Merges the sub-arrays by sorting them
        self.mergeArrays(leftPtr, mid, rightPtr)

    def mergeArrays(self, start, mid, end):  
        leftPtr = start 
        rightPtr = mid + 1 
        # Iterate through both arrays
        while(leftPtr <= mid and rightPtr <= end): 
            self.changeBarColour(leftPtr, "red")
            self.updateArrayOnScreen()
            self.delay() 
            # If elements are out of order 
            if(self.isSwapNeeded(leftPtr, rightPtr)):  
                # Shift all elements left 
                self.shiftArrayElements(leftPtr, rightPtr)
                leftPtr += 1
                mid += 1 
                rightPtr += 1 
            else: 
                leftPtr += 1 
            
    def shiftArrayElements(self, leftPtr, rightPtr):   
        # Stores value at index rightPtr (as it is overwritten later)
        value = self.getElement(rightPtr)
        index = rightPtr 
        # Iterate until index = leftPtr
        while(index != leftPtr):   
            # Shift element at index one place to the left
            self.swapElements(index, index - 1) 
            index -=  1
        
        # Change element at leftPtr to stored value 
        self.changeElement(leftPtr, value) 
        self.changeBarColour(rightPtr, "red")
        self.updateArrayOnScreen()
        self.delay()

# Listen to Wake Me Up When September Ends by Green Day
