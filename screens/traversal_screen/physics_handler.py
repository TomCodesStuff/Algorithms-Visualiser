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
        # Reference to model
        self.__model = model
        # Edges of the canvas   
        self.__canvasBounds = canvasBounds
        # Centre X-Y Coordinates the canvas 
        self.__centreX, self.__centreY = canvasCentre
        # Intensity of gravity 
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
    
    # Returns -1, 0, 1 depending if a is less than, equal to or greater than b 
    def __getDirection(self, a, b): 
        return (a > b) - (a < b)
    
    # TODO Delete this 
    def __calculateGravityIntensity(self, coord : int, centreCoord : int) -> int:  
        return max((abs(coord - centreCoord) // 100) - 0.75, 0)

    # Calculates gravity offset 
    def __calculateGravityOffset(self, x0, y0):  
        gravity = round(self.__calculateDistance(x0, y0, self.__centreX, self.__centreY) * 0.01, 2) 
        forceX = gravity * self.__getDirection(self.__centreX, x0)
        forceY = gravity * self.__getDirection(self.__centreY, y0) 
        print(forceY)
        return (forceX, forceY)

    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def applyGravity(self):  


        for node in self.__model.getNodes():  
            x0, y0, _, _ = node.getCoords() 
            forceX, forceY = self.__calculateGravityOffset(x0, y0)
            self.__updateNodeForces(node, forceX, forceY)
            continue

    
    # Apply all calculated forces 
    def applyForces(self) -> None:
        for node in self.__model.getNodes():
            node.applyForces()
            node.resetForces()

            
# ((abs(x0 - centreX) - 100) // 100)
# Yesterday all my problems seemed so far away 