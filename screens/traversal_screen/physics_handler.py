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
    def __init__(self, model : TraversalModel, canvasBounds : tuple, canvasCentre : tuple) -> None: 
        self.__model = model   
        self.__canvasBounds = canvasBounds
        self.__centreX, self.__centreY = canvasCentre
        self.__gravityConstant = 2


    # Calculates distance between passed coords (pythagoras) 
    def __calculateDistance(self, x0 : int, y0 : int, x1 : int, y1 : int) -> float: 
        return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2)) 
    
    # Updates the forces in the passed nodes so they can be applied later 
    def __updateNodeForces(self, node : CanvasNode, forceX : float, forceY : float) -> None: 
        node.adjustForceX(forceX)
        node.adjustForceY(forceY)

    # Calculates node-node repulsion
    def calculateNodeRepulsion(self):
        n = len(self.__model.getNodes())
        circleSize = self.__model.getCircleSize()
        circleOffset = circleSize // 2 
        
        # Iterate through each pair of nodes 
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
                
                # Update the forces of each node so they can be applied later 
                self.__updateNodeForces(self.__model.getNode(i), -forceX, -forceY)
                self.__updateNodeForces(self.__model.getNode(j), forceX, forceY)  
    
    # Returns -1, 0, 1 depending if a is less than , equal to or greater than b 
    def __directionToCentre(self, a, b): 
        return (a > b) - (a < b)
    
    # Checks to see if any part of the node is outside the drawbable area
    def __checkLowerBounds(self, x0, y0): 
        lowerboundX, lowerBoundY, _, _ = self.__canvasBounds
        circleSize = self.__model.getCircleSize()
        return True if lowerboundX + circleSize >= x0 or\
            lowerBoundY + circleSize >= y0 else False

    # Checks to see if any part of the node is outside the drawbable area    
    def __checkUpperBounds(self, x1, y1): 
        _, _, upperBoundX, upperBoundY = self.__canvasBounds
        circleSize = self.__model.getCircleSize()
        return True if upperBoundX - circleSize <= x1 or\
            upperBoundY - circleSize <= y1 else False

    # Calculates gravity offset 
    def __calculateGravityOffset(self, x0, y0): 
        x0Offset = self.__gravityConstant * self.__directionToCentre(self.__centreX, x0)
        y0Offset = self.__gravityConstant * self.__directionToCentre(self.__centreY, y0) 
        return (x0Offset, y0Offset)

    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def applyGravity(self): 
        for node in self.__model.getNodes(): 
            x0, y0, x1, y1 = node.getCoords() 
            # If Node is out of bounds, try to move it back on screen
            if(self.__checkLowerBounds(x0, y0) or self.__checkUpperBounds(x1, y1)): 
                gravityX, gravityY = self.__calculateGravityOffset(x0, y0)
                self.__updateNodeCoords(node, gravityX, gravityY) 
    
    # Apply all calculated forces 
    def applyForces(self) -> None:
        for node in self.__model.getNodes():
            node.applyForces()
            node.resetForces()

            
