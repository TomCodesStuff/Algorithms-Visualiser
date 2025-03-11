# If this isn't at the top the program breaks :/
# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

    
import math
from .traversal_model import TraversalModel 
from canvas_objects import CanvasNode

# Handles all physics-based calculations 
class PhysicsHandler():
    def __init__(self, model : TraversalModel) -> None: 
        self.__model = model  

    
    # Calculates distance between passed coords (pythagoras) 
    def __calculateDistance(self, x0 : int, y0 : int, x1 : int, y1 : int) -> float: 
        return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2)) 
    

    # Updates coords of node using calculated forces 
    def __updateNodeCoords(self, node : CanvasNode, forceX : float, forceY : float) -> None:
        circleSize = self.__model.getCircleSize()
        x0, y0, _, _ = node.getCoords()  

        # New Coords need to be rounded to nearest number
        # Due to issue with floating point coords causing nodes to move left/right forever
        newX0 =  math.ceil(x0 + forceX)
        newy0 = math.ceil(y0 + forceY)  

        # Update coords in CanvasNode Object 
        node.updateCoords((newX0, newy0, newX0 + circleSize, newy0 + circleSize))


    # Calculates node-node repulsion
    def calculateNodeRepulsion(self):
        n = len(self.__model.getNodes())
        circleSize = self.__model.getCircleSize()
        circleOffset = circleSize // 2 
        
        # Iterate through each node 
        for i in range(n): 
            for j in range(i + 1, n):   
                # X-Y coordinates of the nodes
                x0, y0, _, _ = self.__model.getNode(i).getCoords()
                x1, y1, _, _, = self.__model.getNode(j).getCoords()   
                # X-Y coords of the centre of each circle
                centreX0, centreY0 = x0 + circleOffset, y0 + circleOffset
                centreX1, centreY1 = x1 + circleOffset, y1 + circleOffset
 
                # Calculated pythagorean distance between the circles
                dist = self.__calculateDistance(centreX0, centreY0, centreX1, centreY1)  
                # If the circles are too far apart the result force would be neglible 
                if(dist > self.__model.getMaximumForceDistance()): continue
                
                # Resultant force as a scalar 
                force = self.__model.getForceConstant() / max(dist, 1) 

                # Convert scalar force to vector form
                forceX = ((centreX1 - centreX0) / dist) * force
                forceY = ((centreY1 - centreY0) / dist) * force   
                
                # Update the coords of each node 
                self.__updateNodeCoords(self.__model.getNode(i), -forceX, -forceY)
                self.__updateNodeCoords(self.__model.getNode(j), forceX, forceY)
                

    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def applyGravity(self): pass 
