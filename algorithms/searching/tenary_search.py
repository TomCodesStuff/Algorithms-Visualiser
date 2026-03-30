# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm 


class TenarySearch(Algorithm): 
    # Constructor
    def __init__(self):
        super().__init__()
    

    def getName(self):
        return "Tenary Search"
    

    def run(self): 
        self.sortArray()
        array = self.getArray()
        target = self.getTarget() 

        # Left and right variables, used to adjust mid1 and mid2
        left = 0 
        right = len(array) - 1

        # loop while left variable is less than or equal to the right variable 
        while(left <= right):  
            # Calculate mid1 and mid2 values
            mid1 = left + (right - left) // 3 
            mid2 = right - (right - left) // 3  
            # Sets bar colours
            self.changeBarColour(mid1, "red")
            self.changeBarColour(mid2, "red")

            # If value at mid1 is the target
            if(array[mid1] == target): 
                self.changeBarColour(mid1, "green") 
                self.changeBarColour(mid2, "black") 
                self.updateArrayOnScreen()
                return 1 
            # If value at mid2 is the target
            if(array[mid2] == target): 
                self.changeBarColour(mid1, "black") 
                self.changeBarColour(mid2, "green") 
                self.updateArrayOnScreen()
                return 1  

            # If target is less than value at mid1, adjust right variable
            if(target < array[mid1]): right = mid1 - 1 
            # If target is greater than value at mid2, adjust left variable
            elif(target > array[mid2]): left = mid2 + 1  
            # If target is somewhere inbetween mid1 and mid2, adjust left and right variables 
            else: 
                left = mid1 + 1 
                right = mid2 - 1 
            self.updateArrayOnScreen()
            self.delay()
        return -1 

# Listen to Times Like These By Foo Fighters 