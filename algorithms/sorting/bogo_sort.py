# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class BogoSort(Algorithm):
    # Constructor
    def __init__(self):
        super().__init__()


    # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self) -> str:
        return "Bogo Sort" 
    

    # Bogo Sort Algorithm
    def run(self) -> int: 
        sortedArray = sorted(self.getArray())
        # Continue until array is sorted
        while(sortedArray != self.getArray()): 
            # Randomly shuffle array
            self.shuffleArray(delay=False)
            self.delay() 
        
        self.coolEndingAnimation()
        return 1

# Listen to Times like these by the Foo Fighters