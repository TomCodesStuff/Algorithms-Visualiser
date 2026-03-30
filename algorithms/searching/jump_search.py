# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm
import math 


class JumpSearch(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Jump Search" 


    def run(self):
        # Sorts array 
        self.sortArray()
        
        array = self.getArray()
        target = self.getTarget()
    
        # length of array
        n = len(array)
        # Square root length of array to find jump size
        step = int(math.sqrt(n))
        # Store index of last jump
        prev = 0
        # Find block closest to target -> if it exists
        while(array[min(step, n) - 1] < target):
            prev = step
            self.changeBarColour(prev, "red")
            self.updateArrayOnScreen()
            if prev >= n: 
                return 0
            step += int(math.sqrt(n))
            self.delay()  
        
        # Linear search to find target
        # Start at index of last jump and stops at index of next jump 
        for i in range(prev, prev + int(math.sqrt(n))):
            self.changeBarColour(i, "red")
            # If current elment > target then target not in array
            if array[i] > target:
                self.updateArrayOnScreen()
                return 1 
            # If current element is equal to target
            if array[i] == target:
                self.changeBarColour(i, "green")
                self.updateArrayOnScreen()
                return 1  
            self.updateArrayOnScreen()
            self.delay()  
        return -1
    
# Listen to Waiting For The End by Linkin Park