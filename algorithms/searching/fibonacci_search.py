# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()


from algorithms import Algorithm


class FibonacciSearch(Algorithm):
    def __init__(self):
        super().__init__() 
    
     # Returns algorithms name -> user sees this when selecting algorithm
    def getName(self):
        return "Fibonacci Search"  
    
    def run(self): 
        array =  self.getArray() 
        target = self.getTarget()
        # Starting fibonacci numbers
        fibNMin2, fibNMin1, fibN = self.generateFibNums() 
        # offset, used to calculate index that is compared to target
        offset = -1  
        
        n = len(array)
        self.sortArray()
        
        # Iterate while there are still elements to check
        while(fibN > 1):  
            # Calculate index of element to check
            index = min(offset + fibNMin2, n - 1) 
            # if value at index is less than target
            if(array[index] < target): 
                # Move all Fibonacci numbers two fibonacci numbers down
                fibN = fibNMin1 
                fibNMin1 = fibNMin2 
                fibNMin2 = fibN - fibNMin1
                offset = index 
            # if value at index is greater than target
            elif(array[index] > target): 
                    # Move all Fibonacci numbers one fibonacci number down
                    fibN = fibNMin2  
                    fibNMin1 = fibNMin1 - fibNMin2 
                    fibNMin2 = fibN - fibNMin1  
            # target has been found at index
            else:
                self.changeBarColour(index, "green")
                self.updateArrayOnScreen()
                return 1  

            self.changeBarColour(index, "red")
            self.updateArrayOnScreen()
            self.delay()
        
        # Comparing last element to the target 
        if(fibNMin1 and array[n - 1] == target): 
            self.changeBarColour(index, "green")
            self.updateArrayOnScreen()
            return 1 
        else:
            self.changeBarColour(index, "red")
            self.updateArrayOnScreen() 
            return -1 

    # Calculate the starting fibonacci numbers, based on array size
    def generateFibNums(self) -> tuple: 
        fibNMin2 = 0 
        fibNMin1 = 1 
        fibN = fibNMin1 + fibNMin2

        n = len(self.getArray())
        while(fibN < n): 
            fibNMin2 = fibNMin1 
            fibNMin1 = fibN 
            fibN = fibNMin2 + fibNMin1 
        return (fibNMin2, fibNMin1, fibN)

# Listen to Ain't No Rest For The Wicked By Cage The Elephant