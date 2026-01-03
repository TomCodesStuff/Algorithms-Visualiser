
# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()
 

from algorithms.handlers import callAlgorithm, getAlgorithms
import tkinter as tk 
from tkinter import ttk
import random
import threading

class SharedLayout():
    
    # Creates basic layout and shared settings 
    def createBaseLayout(self) -> None:
        # Creates basic layout of the screen
        self.createTemplate()
        # Override home button function
        self.__overrideHomeButtonCommand()

        # Stores data needed for calculating size of the on-screen widgets
        self.__model = None
        # Stores data relating to the algorithm 
        self.__dataModel = None
        # Handles the logic 
        self.__controller = None
        
        # Adds reference to the controller 
        self.__dataModel.addController(self.__controller) 
        # Thread algorithm runs in
        self.__algorithmThread = None

        # Array containing widgets to be diabled when an algorithm runs and renabled when an algorithm resumes 
        self.__disableEnableArray = []

        # Creating and displaying options
        self.__createOptions() 
        # Sets the default delay
        self.__setDelay()

    # This functions handles creating and displaying the options the user is presented with
    def __createOptions(self) -> None: 
        self.__createAlgorithmOptions()               
        self.__createSpeedAdjuster()
        self.__createArrayAdjuster()
        self.__createSortShuffleButtons()
        self.__createStopSolveButtons()

    # Creates a combo box which displays all algorithms 
    def __createAlgorithmOptions(self) -> None:
        #combo box, allows the user to choose what algorithm they want
        self.__algorithmOptions = ttk.Combobox(self.getOptionsWidgetFrame(), textvariable = tk.StringVar(), state = "readonly", 
                                               font = (self.getFont(), self.getFontSize()),\
             width = self.getOptionsWidgetFrame().winfo_width())
        self.__algorithmOptions.set('Select an algorithm.')
        # Removes the blue highlighting when something is selected that annoyed me
        self.__algorithmOptions.bind("<<ComboboxSelected>>", lambda _: self.getOptionsWidgetFrame().focus())
        self.__algorithmOptions.pack(pady = (10,0)) 
    
    def loadAlgorithmOptions(self, algorithmsType : str) -> None:
        self.__algorithmOptions['value'] = getAlgorithms(algorithmsType)
    
    # Creates a slider that allows users to adjust an algorithms speed
    def __createSpeedAdjuster(self) -> None:
        # Creates a slider that goes from the maximum delay to the minmum delay 
        # Every time the sliders value is changed the updateDelay() method is called to update the value seen on screen
        self.__speedSlider = tk.Scale(self.getOptionsWidgetFrame(), from_ = self.__model.getMaxDelay(), to_ = self.__model.getMinDelay(), 
                                      resolution=self.__model.getDefaultResolution(), 
                                      length = self.getOptionsWidgetFrame().winfo_width(), orient = "horizontal", showvalue = False, 
                                      bg =  "white", highlightbackground = "white", command = self.__updateDelay)
        self.__speedSlider.pack(pady = (10, 0))  
        self.__speedSlider.set(self.__model.getMaxDelay())
        # When the user stops moving the slider the slider is updated in the DataModel class 
        self.__speedSlider.bind("<ButtonRelease-1>", lambda _ : self.__setDelay()) 
        # Time units of the delay 
        self.__sliderUnitsText = "Seconds" 
        # Used to check if units needs to be converted to milliseconds when algorithm is run 
        self.__isMilliSeconds = False
    
    # Creates a slider that allows users to alter an arrays size
    def __createArrayAdjuster(self) -> None:
        self.__arraySizeSlider = tk.Scale(self.getOptionsWidgetFrame(), from_ = 1, to_ = self.__model.getMaxBars(), 
                                          length = self.getOptionsWidgetFrame().winfo_width(),\
            orient = "horizontal", bg = "white", highlightbackground = "white", command = self.__controller.adjustArray)
        self.__arraySizeSlider.pack(pady = (10, 0))

    # Creates buttons the allow algorithms to be sorted and shuffled
    def __createSortShuffleButtons(self) -> None: 
        self.__arraySortShuffleFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white") 
        self.__arraySortShuffleFrame.pack(pady=(20, 0)) 

        self.__sortButton = tk.Button(self.__arraySortShuffleFrame, text="Sort.", width = 7, relief = "solid", 
                                      font = (self.getFont(), self.getFontSize()), command=self.__sortArray)
        self.__sortButton.grid(row = 0, column = 0, padx = (9,5)) 
        self.__shuffleButton = tk.Button(self.__arraySortShuffleFrame, text="Shuffle.", width = 7, relief = "solid", 
                                         font = (self.getFont(), self.getFontSize()), command=self.__shuffleArray)
        self.__shuffleButton.grid(row = 0, column = 1, padx = (3,8)) 
    
    # Creates buttons that lets user execute algorithms or stop them
    def __createStopSolveButtons(self) -> None:
        # Frame to store stop and solve buttons in a grid layout
        algorithmToggleFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white")
        algorithmToggleFrame.pack(side = "bottom", pady = (0,5))
        # Allows user to see the algorithm in action
        self.__solveStopButton = tk.Button(algorithmToggleFrame, text = "Solve.", width = 7, relief = "solid", 
                                           font = (self.getFont(), self.getFontSize()), 
                                           command = lambda: self.__initAlgorithm())
        self.__solveStopButton.grid(row = 0, column = 0, padx = (0,5)) 
        # Allows user to stop algorithm whilst it's running - button is initially disabled
        self.__pauseResumeButton = tk.Button(algorithmToggleFrame, text = "Pause.", width = 7, relief = "solid", 
                                             font = (self.getFont(), self.getFontSize()), 
                                             state = "disabled", command = lambda : self.__pauseAlgorithm())
        self.__pauseResumeButton.grid(row = 0, column = 1)  


    # When the slider has changed value a label is added with the relevant speed 
    def __updateDelay(self, value : str) -> None: 
        self.__speedSlider.config(label = f"Delay: {value} {self.__sliderUnitsText}")  
 
    # Changes the to_ and from_ values of the speed slider, also lets the units be changed to millseconds or seconds 
    def configSpeedSlider(self, to_ : int, from_ : int, interval : int, milliseconds : bool =False) -> None: 
        if(to_ > from_): to_, from_ = from_, to_
        if(milliseconds):
                self.__sliderUnitsText = "Milliseconds" 
                self.__isMilliSeconds = True
        else: 
            self.__sliderUnitsText = "Seconds"    
            self.__isMilliSeconds = False 
        
        self.__speedSlider.config(to_ = to_, from_= from_, resolution = interval)
        self.__speedSlider.set(from_)
        self.__updateDelay(str(from_))
        self.__setDelay()

    # Makes sure that target generated has (almost) equal chance to be in the array or not 
    def targetRandom(self) -> int: 
        # Generates decimal between 0 and 1 
        # If decimal is less than or equal to 0.5 make the target in the array 
        # Gives a roughly 50-50 chance for target to be in the array or out the array
        if(random.random() < 0.5): return self.targetIn()
        # Else call function to generate the target so it is not in the array
        else: return self.targetOut()
    
    # Guarantees target is in the array
    def targetIn(self) -> int: 
       # Randomly chooses index from array and returns integers at that index
       return self.__dataModel.getArray()[random.randint(0, len(self.__dataModel.getArray()) - 1)] 

    # Guarantees target is not in array
    def targetOut(self) -> int: 
        # Chooses a number between the range of arrays smallest value - 20 and arrays largest value + 20
        target = random.randint(min(self.__dataModel.getArray()) - self.__model.getBuffer(), 
                                max(self.__dataModel.getArray()) + self.__model.getBuffer())
        # If generated number in array recall function
        if target in self.__dataModel.getArray(): self.targetOut()
        # If generated number not in array then just return value
        else: return target
        
    # Call algorithm user has selected
    def __initAlgorithm(self) -> None:  
        # Doesn't do anything if user hasn't chosen an algorithm
        if(self.__getAlgorithmChoice() == 'Select an algorithm.'): 
            self.__algorithmOptions.config(foreground = "red")
        else:
            # Disables solve button and enables stop button
            self.__solveToStop()
            # Sets flag indicating the algorithm needs to halt to false
            if(self.__dataModel.isStopped()): self.__dataModel.clearStopFlag()
            self.__widgetsAlgorithmStarts()
            # Generates the target based on the setting (Only applicable when searching)
            self.__controller.generateTarget(self.__dataModel.getTargetSetting()) 
            # Call algorithm -> so this program actually has a use
            self.__algorithmThread = threading.Thread(target=callAlgorithm, 
                                                      args=(self.__dataModel, self.__getAlgorithmChoice(), 
                                                            self.__getAlgorithmType(), 
                                                            self.__widgetsAlgorithmStops))
            # Start Thread
            self.__algorithmThread.start()
    
    # Forces current running algorithm thread to terminate (safely)
    def __stopAlgorithm(self) -> None:
        # Sets to flag to True -> this is what tells the thread/s to stop
        self.__dataModel.setStopFlag()   
        # If the algorithm has been paused
        if(self.__dataModel.isPaused()):
            # Tell algorithm to resume, so it can stop...
            self.__resumeAlgorithm()  
        # Otherwise makes sure pause/resume button has the correct text/function
        else: 
            self.__resumeToPause() 
        self.__widgetsAlgorithmStops()
    
    # Returns algorithm the user has selected 
    def __getAlgorithmChoice(self) -> str:
        return self.__algorithmOptions.get()  
    
    def __getAlgorithmType(self) -> str: 
        return self.__algorithmOptions.get().split(" ")[-1].lower()
    
    def __setDelay(self) -> None:  
        if(self.__isMilliSeconds):  
            self.__dataModel.setDelay(self.__speedSlider.get() / 1000)
        else:  self.__dataModel.setDelay(self.__speedSlider.get())
  
    # Changes solve button text and function it calls when it's pressed
    def __solveToStop(self) -> None:
        self.__solveStopButton.config(text="Stop.", command=self.__stopAlgorithm)
    
    # Changes stop button text and function it calls when it's pressed
    def __stopToSolve(self) -> None:
        self.__solveStopButton.config(text="Solve.", command=self.__initAlgorithm) 
    
    # Changes pause button text and function it calls when it's pressed
    def __pauseToResume(self) -> None: 
         self.__pauseResumeButton.config(text="Resume.", command=self.__resumeAlgorithm) 

    # Changes resume button text and function it calls when it's pressed    
    def __resumeToPause(self) -> None:
        self.__pauseResumeButton.config(text="Pause.", command=self.__pauseAlgorithm)
        
    # Holds the lock, pausing the algorithm Thread
    def __pauseAlgorithm(self) -> None:
        self.__dataModel.acquireLock() 
        self.__pauseToResume()
       
    # Releases the lock, letting the algorithm thread run again
    def __resumeAlgorithm(self) -> None: 
        self.__dataModel.releaseLock()
        self.__resumeToPause()
    
    # Enables the button to pause/resume algorithm
    def __enablePauseResumeButton(self) -> None:
        self.__pauseResumeButton.config(state="active")
    
    # Disables the button to pause/resume algorithm
    def __disablePauseResumeButton(self) -> None:
        self.__pauseResumeButton.config(state="disabled") 
    
    # Changes the function of the home buttton
    def __overrideHomeButtonCommand(self) -> None:
        self.getHomeButton().config(command=self.__loadHomeScreen) 
    
    # Ensures any algorithm threads are terminated before moving to the homescreen
    def __loadHomeScreen(self) -> None: 
        # If a thread exists and it is still running
        if(self.__algorithmThread and self.__algorithmThread.is_alive()): 
            # Tell the thread to stop
            self.__stopAlgorithm()  
            self.__controller.cancelScheduledProcesses()
        self.loadHomeScreen()

    # Sorts and displays the array
    def __sortArray(self) -> None:
        self.__dataModel.sortArray()
        self.__controller.displayArray() 
    
    # Enables the button to sort the array
    def __enableSortButton(self) -> None:
        self.__sortButton.config(state="active")
    
    # Disables the button to sort the array
    def __disableSortButton(self) -> None:
        self.__sortButton.config(state="disabled")
    
    # Shuffles and displays the array
    def __shuffleArray(self) -> None:
        self.__dataModel.shuffleArray()
        self.__controller.displayArray()  
    
    # Enables the button to shuffle the array
    def __enableShuffleButton(self) -> None:
        self.__shuffleButton.config(state="active")
    
    # Disables the button to shuffle the array
    def __disableShuffleButton(self) -> None:
        self.__shuffleButton.config(state="disabled")
    
    # Enables the slider to change the array size
    def __enableArraySizeSlider(self) -> None:
        self.__arraySizeSlider.config(state="active")
    
    # Disables the slider to change the array size
    def __disableArraySizeSlider(self) -> None:
        self.__arraySizeSlider.config(state = "disabled")
    
    # Enables/Disables widgets when algorithms runs
    def __widgetsAlgorithmStarts(self) -> None:
        self.__disableArraySizeSlider()
        self.__disableSortButton()
        self.__disableShuffleButton() 
        self.__solveToStop()
        self.__enablePauseResumeButton()
        self.__disableWidgetsInArray()
    
    # Enables/Disables widgets when algorithms stops
    def __widgetsAlgorithmStops(self) -> None:
        self.__enableArraySizeSlider()
        self.__enableSortButton()
        self.__enableShuffleButton()  
        self.__stopToSolve()
        self.__disablePauseResumeButton()  
        self.__enableWidgetsInArray()
    
    # Adds widget to array which will be disabled when algorithms are run
    def addWidgetToArray(self, item) -> None: 
        self.__disableEnableArray.append(item)
    
    # Removes the passed widget from the array
    def removeWidgetFromArray(self, item) -> None: 
        self.__disableEnableArray.remove(item)

    # Disables all widgets in the array
    def __disableWidgetsInArray(self): 
        for widget in self.__disableEnableArray: 
            widget.config(state="disabled")
    
    # Enables all widgets in the array 
    def __enableWidgetsInArray(self): 
        for widget in self.__disableEnableArray: 
            widget.config(state="active")
    
    # Returns the data model class
    def getDataModel(self) -> None:
        return self.__dataModel
    
# Listen to Whatsername by Green Day    