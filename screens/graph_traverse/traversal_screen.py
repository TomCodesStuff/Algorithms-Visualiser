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

        self.__nodeOptionsFrame = None 




    # Creates the button that lets users add nodes to the canvas 
    def __createAddNodeButton(self) -> None: 
        self.__addNodeButton = tk.Button(self.__nodeOptionsFrame, text="Spawn.", width=6, relief="solid", 
                                         font = (self.getFont(), self.getFontSize()), command=self.getController().spawnNode)
        self.__addNodeButton.grid(row = 1, column = 0, pady = (5, 0), padx=(0, 10))  
    

    def __createDeleteNodeButton(self) -> None:
        self.__deleteNodeButton = tk.Button(self.__nodeOptionsFrame, text="Delete.", width=6, relief="solid", 
                                            font = (self.getFont(), self.getFontSize()), 
                                            command=self.getController().deleteNode)
        self.__deleteNodeButton.grid(row = 1, column = 1, pady = (5, 0), padx=(10, 0))  


    def __createNodeOptions(self) -> None: 
        self.__nodeOptionsFrame = tk.Frame(self.getOptionsWidgetFrame(), bg="white") 
        self.__nodeOptionsFrame.pack()

        tk.Label(self.__nodeOptionsFrame, text="Node Options:", font=(self.getFont(), self.getFontSize()), bg="white")\
            .grid(row=0, column=0, pady=(10, 0), columnspan=2)

        self.__createAddNodeButton() 
        self.__createDeleteNodeButton()


    # Changes the text colour of the add nodes button to the passed colour
    def setAddNodeButtonColour(self, colour : str) -> None: 
        self.__addNodeButton.config(fg = colour) 
    

    def setDeleteNodeButtonColour(self, colour: str) -> None:
        self.__deleteNodeButton.config(fg = colour)


    # Updates text in label above weight slider 
    def __updateWeight(self, value : str) -> None:
        self.__weightSlider.config(label = f"Weight: {value}")    


    # Create option to let users change an edges weight/cost
    def __createWeightSlider(self) -> None:
        # Frame to store entry widget to let users to choose an edges weight
        self.__edgeWeightFrame = tk.Frame(self.__edgeOptionsFrame, background="white") 
        self.__edgeWeightFrame.pack(pady=(5, 0))
        self.__weightSlider = tk.Scale(self.__edgeWeightFrame, from_ = self.getModel().getMinWeight(), 
                                       to_=self.getModel().getMaxWeight(), resolution=self.getModel().getWeightSliderResolution(), 
                                       length = self.getOptionsWidgetFrame().winfo_width(), orient="horizontal", showvalue=False, 
                                       bg = "white", highlightbackground="white", command=self.__updateWeight)
        
        self.__updateWeight("No Edge Selected")
        self.__weightSlider.pack()


    # Create option to decide if edge is directed/undirected
    def __createEdgeDirectionButtons(self) -> None:
        # Add Radio buttons 
        self.__directionButtonFrame = tk.Frame(self.__edgeOptionsFrame, background="white")
        self.__directionButtonFrame.pack()

        self.__leftArrowButton = tk.Button(self.__directionButtonFrame, text = "<-", width=3, relief = "solid", 
                                           font=(self.getModel().getArrowFont(), self.getFontSize())) 
        self.__leftArrowButton.grid(row=0, column=0, pady=(5, 0), padx=(0, 10)) 

        self.__doubleArrowButton = tk.Button(self.__directionButtonFrame, text = "<->", width=3, relief = "solid", 
                                             font=(self.getModel().getArrowFont(), self.getFontSize())) 
        self.__doubleArrowButton.grid(row=0, column=1, pady=(5, 0)) 

        self.__rightArrowButton = tk.Button(self.__directionButtonFrame, text = "->", width=3, relief = "solid", 
                                            font=(self.getModel().getArrowFont(), self.getFontSize())) 
        self.__rightArrowButto.grid(row=0, column=2, pady=(5, 0), padx=(10, 0))       
       

    # Create button to save edge 
    def __createFinishButton(self) -> None:
        self.__saveEdgeButton = tk.Button(self.__edgeConfirmationFrame, text = "Finish.", width=6, relief = "solid", 
                                          font=(self.getFont(), self.getFontSize()), command=self.__saveEdge)
        self.__saveEdgeButton.grid(row=0, column=0, padx=(0, 10)) 


    # Create button to delete edge 
    def __createDeleteEdgeButton(self) -> None:
        self.__deleteEdgeButton = tk.Button(self.__edgeConfirmationFrame, text="Delete.", width=6, relief="solid",
                                            font=(self.getFont(), self.getFontSize()), command=self.__deleteEdge)
        self.__deleteEdgeButton.grid(row=0, column=1, padx=(10, 0))


    # Create buttons to save or delete an edge    
    def __createEdgeConfirmationButtons(self): 
        self.__edgeConfirmationFrame = tk.Frame(self.__edgeOptionsFrame, background="white")
        self.__edgeConfirmationFrame.pack(pady=(10, 0)) 
        self.__createFinishButton()
        self.__createDeleteEdgeButton()


    # Wrapper function to create a Radio Button
    def __createRadioButton(self, frame : tk.Frame, text : str, value:int) -> tk.Radiobutton: 
        return tk.Radiobutton(frame, text=text, background="white", 
                       variable=self.__edgeType, value=value, font=(self.getFont(), 11))


    def __hideEdgeOptions(self): 
        self.__edgeOptionsFrame.pack_forget() 


    def __showEdgeOptions(self) -> None: 
        self.__edgeOptionsFrame.pack()


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
    def showEdgeOptions(self, canvasEdge) -> None: 
        # Update weight slider 
        self.__updateWeight(canvasEdge.getWeight())  
        
        # Enables buttons and slider (so they work)
        self.__saveEdgeButton.config(state="active")
        self.__deleteEdgeButton.config(state="active")  
        self.__weightSlider.config(state="active")
        
        # Moves thumb of slider to correct value -> scale must be active first 
        self.__weightSlider.set(canvasEdge.getWeight())

        # Show edge options 
        self.__showEdgeOptions()


     # Creates options to add edges or edit existing ones
    def __createEdgeOptions(self) -> None: 
        # Frame containing widgets for adding an option
        self.__edgeOptionsFrame = tk.Frame(self.getOptionsWidgetFrame(), background="white")  
        # Display frame on screen
        self.__edgeOptionsFrame.pack(pady=(10, 0))  
        # Label 
        tk.Label(self.__edgeOptionsFrame, text="Edge Options:", font=(self.getFont(), self.getFontSize()), bg="white")\
            .pack(pady=(10, 0))
        # Calls slider to adjust weight
        self.__createWeightSlider() 
        # Create buttons to toggle direction
        self.__createEdgeDirectionButtons() 
        # Create buttons to confirm changes 
        self.__createEdgeConfirmationButtons()


    # Creates the widgets that allows users to toggle the visualisers settings
    def __createOptions(self) -> None:  
        self.__createNodeOptions()
        self.__createEdgeOptions()    


    def render(self) -> None: 
        self.createBaseLayout()
        self.__createOptions()  
        self.getController().createEventHandler(self.getCanvas()) 
        self.getController().repeatCanvasRefresh()
    

    # TODO cancel any running functions before algorithm runs 
    def prepare() -> None: pass 
    def coolEndingAnimation(self) -> None: pass 


# Listen Glass Spiders by Hot Milk
