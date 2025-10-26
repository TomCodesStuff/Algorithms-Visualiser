class AlgorithmController():  

    def __init__(self, screen, model, dataModel):
        self.__screen = screen
        self.__model = model
        self.__dataModel = dataModel


    # TODO
    # Cancels any scheduled function calls left by a terminated thread
    def cancelScheduledProcesses(self):
        # If there are still processed scheduled from the terminated thread
            if(self.__screen.getWindow().getNumScheduledFunctions() > 0):  
                # Stop all processes 
                self.__screen.getWindow().cancelScheduledFunctions()  
    
    # TODO 
    # Schedule function to redraw array after a certain amount of time 
    # Prevents the canvas flickering as updating is done by the main GUI thread
    def scheduleArrayUpdate(self):
        self.__screen.getWindow().scheduleFunctionExecution(self.displayArray, 0)