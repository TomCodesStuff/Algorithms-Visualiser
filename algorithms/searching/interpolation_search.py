# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.") 
    exit()

from ..algorithm import Algorithm 

class InterpolationSearch(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()  
    
    
    def getName(self):
        return "Interpolation Search"
     

    def run(self): 
        self.sortArray()
        array = self.getArray() 
        target = self.getTarget()

        # Low and high variables, used to calculate pos
        low = 0
        high = len(array) - 1

        # Iterate whilse conditions are met 
        while(low <= high and target >= array[low] and target <= array[high]): 
            # Calculate pos (where algorithm guesses the target is)
            pos = low + (((target - array[low]) * (high - low)) // (array[high] - array[low]))   
            # target has been found
            if(array[pos] == target): 
                self.changeBarColour(pos, "green")
                self.updateArrayOnScreen()
                return 1  
            # If element at index pos is greater than target, adjust high
            if(array[pos] > target): high = pos - 1 
            # If element at index pos is less than target, adjust low
            elif(array[pos] < target): low = pos + 1
            self.changeBarColour(pos, "red")
            self.updateArrayOnScreen()
            self.delay()
        return 0 

# Listen to Under The Cover Of Darkness by The Strokes