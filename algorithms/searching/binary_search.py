# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class BinarySearch(Algorithm):
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Binary Search" 
    
    # Binary Search algorithm -> see markdown for explanation
    def run(self):
        # Sorts array 
        self.sortArray()
        array = self.getArray()
        target = self.getTarget()
        # Low and high variables used to adjust mid
        low = 0 
        high = len(array) - 1
               
        while(low <= high):
            # Calculate new mid
            mid = (low + high) // 2
            self.changeBarColour(mid, "red")
            # If element at mid is equal to the target
            if array[mid] == target:
                self.changeBarColour(mid, "green")
                self.updateArrayOnScreen()
                return 1
            # If element at mid is greater than the target
            elif array[mid] > target:
                # Disreguard upper end of array
                high = mid - 1
            # If element is less than the target
            # Disreguard lower end of the array
            else: low = mid + 1
            self.updateArrayOnScreen()
            self.delay() 
        return -1 
    
# Listen to Welcome to the DCC by Nothing But Thieves