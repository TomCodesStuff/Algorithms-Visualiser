# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class TimSort(Algorithm):
    # Constructor
    def __init__(self): 
        super().__init__()  
        self.__minRunSize = 4


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Tim Sort"  


    # Tim Sort Algorithm
    def run(self) -> int:    
        n = len(self.getArray()) 
        # Calculates the size of the run 
        runSize = self.__calcMinRinSize(n)

        for i in range(0, n, runSize): 
            # Perform insertion sort on each run 
            self.insertionSort(i, min((i + runSize) - 1, n - 1))

        # While run size is less than the size of the array
        while(runSize < n):  
            # Iterate through each pair of sub arrays
            for i in range(0, n, runSize * 2):  
                # Ending index of the right sub array
                rightPtr = min(i + (runSize * 2) - 1, n - 1) 
                # Starting index of the right sub array
                rightArrStart = min(i + runSize, n - 1)
                # There can be an odd number of runs meaning one sub array is leftover and can't be merged
                # It's pointless to merge a sub array with itself 
                # So this check make sure merging is performed on two sub arrays only 
                if(rightArrStart < rightPtr):
                    self.mergeSubArrays(i, rightArrStart, rightPtr) 
            # Doubles run size has now the number of sub arrays as halved 
            # but they are now double in size 
            runSize *= 2 
        
        self.updateArrayOnScreen()
        self.delay()
        self.coolEndingAnimation()
        return 1 


    def mergeSubArrays(self, start, mid, end): 
        leftPtr = start
        rightPtr = mid 

        while(leftPtr <= mid - 1 and rightPtr <= end): 
            self.changeBarColour(leftPtr, "red")
            self.updateArrayOnScreen()
            self.delay() 

            if(self.isSwapNeeded(leftPtr, rightPtr)):
                self.shiftElements(leftPtr, rightPtr)
                leftPtr += 1 
                rightPtr += 1  
                mid += 1 
            else: leftPtr += 1 
 
    def shiftElements(self, leftPtr, rightPtr): 
        # Stores value at index rightPtr (as it is overwritten later)
        value = self.getElement(rightPtr)
        index = rightPtr 
        # Iterate until index = leftPtr
        while(index != leftPtr):   
            # Shift element at index one place to the left 
            self.swapElements(index, index - 1) 
            index -=  1
        self.changeElement(index, value)
        self.changeBarColour(rightPtr, "red")
        self.updateArrayOnScreen()
        self.delay()

    def insertionSort(self, start, end): 
        # Iterate between the indexes
        for i in range(start + 1, end + 1):  
            self.changeBarColour(i - 1, "orange")
            self.changeBarColour(i, "red")
            self.updateArrayOnScreen()
            self.delay()

            # The left pointer keeps track of sorted element being compared to the sorted element
            leftPtr = i - 1 
            # The right pointer keeps track of the unsorted element
            rightPtr = i 

            # Iterate until the beginning of the sorted array or
            # until the unsorted element is in the right place 
            while(leftPtr >= start and self.isSwapNeeded(leftPtr, rightPtr)):
                # Swap elements at the specified indexes
                self.swapElements(leftPtr, rightPtr)
                # Adjust the pointers
                leftPtr -= 1
                rightPtr -= 1

                self.changeBarColour(i, "orange")
                self.changeBarColour(rightPtr, "red")
                self.updateArrayOnScreen()
                self.delay()
 

    # TODO Fix spelling mistake and remove horrible magic numbers 
    def __calcMinRinSize(self, n : int) -> int:
        # If the length of the array is less than 64, the runsize is set to 4 
        # This is done for visualisation purposes, the actual implementation 
        # would just perform an insertion sort
        if(n < 64): return self.__minRunSize  
        # Gets binary representation of the number 
        binVal = bin(n)
        # Denary representation of the six most significant bits 
        # The index slicing starts at index 2 as the string returned 
        # by the bin() function starts with 0b<binary number>
        runSize = int(binVal[2:8], 2)
        # Add one to the run size oif any of the reamining bits are still set
        if(binVal[8:].count("1") >= 1): return runSize + 1
        return runSize

# Listen to No Surprises by Radiohead