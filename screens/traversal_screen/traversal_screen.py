# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import screens as sc 
import tkinter as tk 
from tkinter import ttk 
from .traversal_controller import TraversalController
from .traversal_model import TraversalModel
from canvas_objects import CanvasNode, CanvasEdge

class TraversalScreen(sc.Screen, sc.ScreenTemplate): 
    def initScreen(self) -> None:
        self.createTemplate() 

        # Create model class
        self.__model = TraversalModel() 
        # Create controller class and add referencces to screen and model
        self.__controller = TraversalController(self, self.__model)
        # Add reference to controller to the model object
        self.__model.addController(self.__controller)
        # Add event handlers to the canvas
        self.__controller.addCanvasEvents() 
        # Create the options users can interact with 
        self.__createOptions()  
        
    # Creates the widgets that allows users to toggle the visualisers settings
    def __createOptions(self) -> None: 
        self.__createAlgorithmOptions() 
        self.__createSpeedAdjuster()
        self.__createAddNodeButton()
        self.__createAddEdgeOption()
        self.__createStopSolveButtons()

    # Create the combo box that displays the algorithms users can see visualised 
    def __createAlgorithmOptions(self) -> None:
        # combo box, allows the user to choose what algorithm they want
        self.__algorithmOptions = ttk.Combobox(self.getOptionsWidgetFrame(), textvariable = tk.StringVar(), 
                                               state = "readonly", font = (self.getFont(), self.getFontSize()),\
             width = self.getOptionsWidgetFrame().winfo_width())
        self.__algorithmOptions.set('Select an algorithm.')
        # Removes the blue highlighting when something is selected that annoyed me
        self.__algorithmOptions.bind("<<ComboboxSelected>>", lambda _: self.getOptionsWidgetFrame().focus())
        self.__algorithmOptions.pack(pady = (10,0)) 
    
    # Creates a slider that allows users to adjust an algorithms speed
    def __createSpeedAdjuster(self) -> None:
        # Creates a slider that goes from the maximum delay to the minmum delay 
        # Every time the sliders value is changed the updatetDelay() method is called to update the value seen on screen
        self.__speedSlider = tk.Scale(self.getOptionsWidgetFrame(), from_=self.__model.getMaxDelay(), 
                                      to_=self.__model.getMinDelay(), resolution=self.__model.getResolution(), 
                                      length=self.getOptionsWidgetFrame().winfo_width(), orient="horizontal", showvalue=False, 
                                      bg="white", highlightbackground="white", command=self.__updateDelay)
        self.__speedSlider.pack(pady = (10, 0))  
        self.__speedSlider.set(self.__model.getMaxDelay())
        # When the user stops moving the slider the slider is updated in the DataModel class 
        self.__speedSlider.bind("<ButtonRelease-1>", lambda _ : self.__setDelay()) 
     
    def __updateDelay(self, value : str) -> None:
        self.__speedSlider.config(label = f"Delay: {value} Milliseconds")  

    def __setDelay(self) -> None:
        pass   

    # Creates the button that lets users add nodes to the canvas 
    def __createAddNodeButton(self) -> None: 
        self.__addNodeButton = tk.Button(self.getOptionsWidgetFrame(), text="Add Node.", width=10, relief="solid", 
                  font = (self.getFont(), self.getFontSize()), command=self.__controller.spawnNode)
        self.__addNodeButton.pack(pady = (10, 0)) 
        
    # Changes the text colour of the add nodes button to the passed colour
    def changeNodeButtonColour(self, colour : str) -> None: 
        self.__addNodeButton.config(fg = colour)

    # Creates options to add edges or edit existing ones
    def __createAddEdgeOption(self) -> None: 
        # Frame containing widgets for adding an option
        self.__edgeNodesFrame = tk.Frame(self.getOptionsWidgetFrame(), background="white") 
        # Display frame on screen
        self.__edgeNodesFrame.pack(pady=(10, 0))  

        # Calls functions to create add edge options 
        self.__createEdgeWeightOption() 
        self.__createEdgeDirectionOptions() 
        self.__createEdgeConfirmationButtons()

        # Hide the options until they are needed 
        self.__hideEdgeOptions()
    
    # Create option to let users change an edges weight/cost
    def __createEdgeWeightOption(self) -> None:
        # Frame to store entry widget to let users to choose an edges weight
        self.__edgeWeightFrame = tk.Frame(self.__edgeNodesFrame, background="white") 
        self.__edgeWeightFrame.pack(pady=(10,0))
        self.__weightSlider = tk.Scale(self.__edgeWeightFrame, from_ = self.__model.getMinWeight(), 
                                       to_=self.__model.getMaxWeight(), resolution=self.__model.getWeightSliderResolution(), 
                                       length = self.getOptionsWidgetFrame().winfo_width(), orient="horizontal", showvalue=False, 
                                       bg = "white", highlightbackground="white", command=self.__updateWeight)
        
        self.__updateWeight("No Edge Selected")
        self.__weightSlider.pack()

    # Updates text in label abive weight slider 
    # Updates text in label abive weight slider 
    def __updateWeight(self, value : str) -> None:
        self.__weightSlider.config(label = f"Weight: {value}")    

    # Create option to decide if edge is directed/undirected
    def __createEdgeDirectionOptions(self) -> None:
        # Add Radio buttons for directed and undirected edges 
        self.__radioButtonFrame = tk.Frame(self.__edgeNodesFrame, background="white")
        self.__radioButtonFrame.pack(pady=(10, 0))
        # Stores the value of the currently selected radio button
        self.__edgeType = tk.IntVar() 
        # Radio Button to indicate edge is undirected
        self.__createRadioButton(self.__radioButtonFrame, "Undirected", 0).grid(row=0, column=0)
        # Radio Button to indicate edge is directed 
        self.__createRadioButton(self.__radioButtonFrame, "Directed", 1).grid(row=0, column=1) 

    # Create buttons to save or delete an edge    
    def __createEdgeConfirmationButtons(self): 
        self.__edgeConfirmationFrame = tk.Frame(self.__edgeNodesFrame, background="white")
        self.__edgeConfirmationFrame.pack(pady=(10, 0)) 
        self.__createSaveEdgeButton()
        self.__createDeleteEdgeButton()

    # Create button to save edge 
    def __createSaveEdgeButton(self) -> None:
        self.__saveEdgeButton = tk.Button(self.__edgeConfirmationFrame, text = "Save.", width=6, relief = "solid", 
                                          font=(self.getFont(), self.getFontSize()), command=self.__saveEdge)
        self.__saveEdgeButton.grid(row=0, column=0, padx=(0, 5)) 
    
    # Create button to delete edge 
    def __createDeleteEdgeButton(self) -> None:
        self.__deleteEdgeButton = tk.Button(self.__edgeConfirmationFrame, text="Delete.", width=6, relief="solid",
                                            font=(self.getFont(), self.getFontSize()), command=self.__deleteEdge)
        self.__deleteEdgeButton.grid(row=0, column=1, padx=(10, 0))

    # Wrapper function to create a Radio Button
    def __createRadioButton(self, frame : tk.Frame, text : str, value:int) -> tk.Radiobutton: 
        return tk.Radiobutton(frame, text=text, background="white", 
                       variable=self.__edgeType, value=value, font=(self.getFont(), 11))

    # Wrapper function for making labels 
    def __createLabel(self, frame : tk.Frame, text : str = "", width : int = 0) -> tk.Label:  
        label = tk.Label(frame, text=text, width=width, background="white", 
                        font=(self.getFont(), self.getFontSize()))   
        # Add width to label if it is specified 
        if(width): label.config(width=width)
        return label
    
    def __hideEdgeOptions(self): 
        self.__edgeNodesFrame.pack_forget() 
    
    def __showEdgeOptions(self) -> None: 
        self.__edgeNodesFrame.pack()

    def __saveEdge(self) -> None:     
        # Updates egdes weight 
        self.__controller.saveEdge(self.__weightSlider.get())
        # Hides options to edit edge from view
        self.disableWeightOptions()   

    def __deleteEdge(self) -> None:  
        # Deletes newly drawn weight or pre-existing weight 
        self.__controller.deleteEdge()
        # Hides options to edit edge from view 
        self.disableWeightOptions()
  

    # Updates weight displayed in the slider bar 
    def updateWeightOnScreen(self, edgeWeight : int) -> None: 
        self.__weightSlider.set(edgeWeight)
        # If edges weight is the minimum weight
        if(edgeWeight == self.__model.getMinWeight()):  
            # Need to manually change text above the slider 
            self.__updateWeight(str(self.__model.getMinWeight()))

    
    # Resets position and disables weight slider 
    def resetWeightSlider(self) -> None: 
        # Resets text
        self.__updateWeight("No Edge Selected") 
        # Disables slider 
        self.__weightSlider.config(state="disabled")
    
    # Enables egde options so users can toggle them
    def enableWeightOptions(self, canvasEdge : CanvasEdge) -> None: 
        # Update weight slider 
        self.__updateWeight(canvasEdge.getWeight())  
        # Enables buttons and slider (so they work lol)
        self.__saveEdgeButton.config(state="active")
        self.__deleteEdgeButton.config(state="active")  
        self.__weightSlider.config(state="active")
        # Moves thumb of slider to correct value -> scale must be active first 
        self.__weightSlider.set(canvasEdge.getWeight())

        # Show edge options 
        self.__showEdgeOptions()
    
    # Disables edge options and resets weight slider 
    def disableWeightOptions(self) -> None:  
        # Disables buttons
        self.__saveEdgeButton.config(state="disabled")
        self.__deleteEdgeButton.config(state="disabled") 
        # Disable and reset weight slider 
        self.resetWeightSlider()
        # Makes edge Options invisible 
        self.__hideEdgeOptions()

    # Creates buttons that lets user execute algorithms or stop them
    def __createStopSolveButtons(self) -> None:
        # Frame to store stop and solve buttons in a grid layout
        algorithmToggleFrame = tk.Frame(self.getOptionsWidgetFrame(), bg = "white")
        algorithmToggleFrame.pack(side = "bottom", pady = (0,5))
        # Allows user to see the algorithm in action
        self.__solveStopButton = tk.Button(algorithmToggleFrame, text = "Solve.", width = 7, relief = "solid", 
                                           font = (self.getFont(), self.getFontSize()))
        self.__solveStopButton.grid(row = 0, column = 0, padx = (0,5)) 
        # Allows user to stop algorithm whilst it's running - button is initially disabled
        self.__pauseResumeButton = tk.Button(algorithmToggleFrame, text = "Pause.", width = 7, relief = "solid", 
                                             font = (self.getFont(), self.getFontSize()), state = "disabled")
        self.__pauseResumeButton.grid(row = 0, column = 1)   
    
    # Changes colour of the given circle to the colour specified
    def changeCircleColour(self, circle : int, colour : str) -> None: 
        self.getCanvas().itemconfig(circle, fill = colour)

# Listen to Can't Stop by The Red Hot Chili Peppers 