# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

import tkinter as tk 
from typing import TYPE_CHECKING, TypeVar
from ..algorithm_base import AlgorithmScreen
from data_structures import Graph

if TYPE_CHECKING: 
    from graph_traverse import TraversalController, TraversalModel

C = TypeVar("C", bound="TraversalController")
M = TypeVar("M", bound="TraversalModel")
D = TypeVar("D", bound="Graph")


class TraversalScreen(AlgorithmScreen[C, M, D]):  
    def __init__(self, window):
        super().__init__(window)

    # Creates the button that lets users add nodes to the canvas 
    def __createAddNodeButton(self) -> None: 
        self.__addNodeButton = tk.Button(self.getOptionsWidgetFrame(), text="Add Node.", width=10, relief="solid", 
                  font = (self.getFont(), self.getFontSize()), command=self.getController().spawnNode)
        self.__addNodeButton.pack(pady = (10, 0)) 


    # Changes the text colour of the add nodes button to the passed colour
    def setAddNodeButtonColour(self, colour : str) -> None: 
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
        self.__weightSlider = tk.Scale(self.__edgeWeightFrame, from_ = self.getModel().getMinWeight(), 
                                       to_=self.getModel().getMaxWeight(), resolution=self.getModel().getWeightSliderResolution(), 
                                       length = self.getOptionsWidgetFrame().winfo_width(), orient="horizontal", showvalue=False, 
                                       bg = "white", highlightbackground="white", command=self.__updateWeight)
        
        self.__updateWeight("No Edge Selected")
        self.__weightSlider.pack()


    # Updates text in label above weight slider 
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
        self.getController().saveEdge(self.__weightSlider.get())
        # Hides options to edit edge from view
        # self.disableWeightOptions()   


    def __deleteEdge(self) -> None:  
        # Deletes newly drawn weight or pre-existing weight 
        # TODO RE-implement this btw 
        self.getController().deleteEdge()
        # Hides options to edit edge from view 
        # self.disableWeightOptions()
  

    # Updates weight displayed in the slider bar 
    def updateWeightOnScreen(self, edgeWeight : int) -> None: 
        self.__weightSlider.set(edgeWeight)
        # If edges weight is the minimum weight
        if(edgeWeight == self.getModel().getMinWeight()):  
            # Need to manually change text above the slider 
            self.__updateWeight(str(self.getModel().getMinWeight()))

    
    # Resets position and disables weight slider 
    def resetWeightSlider(self) -> None: 
        # Resets text
        self.__updateWeight("No Edge Selected") 
        # Disables slider 
        self.__weightSlider.config(state="disabled")
    

    # Enables egde options so users can toggle them
    def enableWeightOptions(self, canvasEdge) -> None: 
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


    # Creates the widgets that allows users to toggle the visualisers settings
    def __createOptions(self) -> None: 
        self.__createAddNodeButton()
        self.__createAddEdgeOption()    


    def render(self) -> None: 
        self.createBaseLayout()
        self.__createOptions()  
        self.getController().createEventHandler(self.getCanvas()) 
        self.getController().repeatCanvasRefresh()
    

    # TODO cancel any running functions before algorithm runs 
    def prepare() -> None: pass 
    def coolEndingAnimation(self) -> None: pass 


# Listen Glass Spiders by Hot Milk
