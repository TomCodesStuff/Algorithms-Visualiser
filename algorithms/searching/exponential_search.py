# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.") 
    exit()


from algorithms import Algorithm


class ExponentialSearch(Algorithm):
    def __init__(self):
        super().__init__()  
    
     # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Exponential Search" 
    
    def run(self): 
        array = self.getArray()
        target = self.getTarget() 

        self.sortArray()
        # If the target is the first element of the array
        if(array[0] == target): return 1 
        
        # Start at index 1
        i = 1
        n = len(array) 
        
        # Find the range the target could be in 
        # While i is less than the length of the array 
        # and the current value is less than or equal to the target
        while(i < n and array[i] <= target):  
            # Double the value i
            i = i << 1 
        
        # Perform a binary search within the calculated range i // 2 - min(i, n - 1)
        # min(i, n - 1) is needed as i could be larger than the size of the array
        return self.binarySearch(i // 2, min(i, n - 1)) 
    
    def binarySearch(self, left, right):
        array = self.getArray()
        target = self.getTarget()  
        upperBound = right 
        lowerBound = left 

        # Loop until left pointer is greater than the right pointer
        while(left <= right):  
            self.changeBarColour(lowerBound, "orange")
            self.changeBarColour(upperBound, "orange")
            # Calculate new mid
            mid = (left + right) // 2  
            # If value at index mid is the target
            if(array[mid] == target): 
                self.changeBarColour(mid, "green")
                self.updateArrayOnScreen()
                return 1 
            # If the value at index mid is greater than the target, reduce right pointer
            if(array[mid] > target): right = mid - 1
            # If the value at index mid is less than the target, increase left pointer
            elif(array[mid] < target): left = mid + 1
            
            self.changeBarColour(mid, "red")
            self.updateArrayOnScreen()
            self.delay()
        
        # Element is not in array
        return 0
    
# Listen to Welcome To Paradise By Green Day