# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class LinearSearch(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()

    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Linear Search" 
    

    # Linear Search Algorithm
    def run(self) -> int:   
        self.shuffleArray()     
        # Iterate through array one element at a time
        for index, num in enumerate(self.getArray()):
            # If current element is equal to the target
            if num == self.getTarget():
                # Set bar to green as target has been found
                self.changeBarColour(index, "green") 
                self.updateArrayOnScreen()
                return 1
            self.changeBarColour(index, "red")
            self.updateArrayOnScreen()
            self.delay()     
        return -1

# Listen to Karma Police By Radiohead