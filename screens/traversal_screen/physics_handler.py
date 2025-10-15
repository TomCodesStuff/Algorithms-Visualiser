# If this isn't at the top the program breaks :/
# If the file is run as is this message is printed and the program exits
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
        self.__canvasCentreX, self.__canvasCentreY = canvasCentre

        
    # Calculates distance between passed coords (pythagoras) 
    def __calculateDistance(self, x0 : float, y0 : float, x1 : float, y1 : float) -> float: 
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
        maxRepulsionDist = self.__model.getMaxRepulsionDist() 
        repulsionFadeDist = self.__model.getFadeDist()

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
                if(dist > maxRepulsionDist): continue
                
                # Linear fade allows for less jitter when nodes get closer to maximum repulsion distance 
                # Repulsion fade distance = 0.75 * maximum repulsion distance  
                fade = 1 - ((dist - repulsionFadeDist) / (repulsionFadeDist - maxRepulsionDist))

                # Resultant force as a scalar 
                force = self.__model.getForceConstant() / max(dist, 1) 
                # Convert scalar coords into standardised vector form 
                dx, dy = (centreX1 - centreX0) / max(dist, 0.1), (centreY1 - centreY0) / max(dist, 0.1)
                # Calculate X-Y forces to be applied to each node
                forceX, forceY = dx * force * fade, dy * force * fade
                
                # Update each nodes forces
                self.__updateNodeForces(self.__model.getNode(i), -forceX, -forceY) 
                self.__updateNodeForces(self.__model.getNode(j), forceX, forceY)  
    
    
    # Returns -1, 0, 1 depending if a is less than, equal to or greater than b 
    def __getAxisDirection(self, a, b): 
        return (a > b) - (a < b)
    

    # Checks if either passed X-Y values are less than lower bounds
    def __checkLowerBounds(self, x : float, y : float, lowerX : int, lowerY : int) -> bool: 
        return True if x <= lowerX or y <= lowerY else False 
    
    
    # Checks if either passed X-Y values are greater than upper bounds 
    def __checkUpperBounds(self, x : float, y : float, upperX : int, upperY : int) -> bool: 
        return True if x >= upperX or y >= upperY else False


    def __isNodeOffscreen(self, coords : tuple) -> bool: 
        # Node Coords
        x0, y0, x1, y1 = coords  
        # Upper and Lower bounds of the canvas 
        lowerX, lowerY, upperX, upperY = self.__canvasBounds 
        # Return True if node is out of bounds 
        return self.__checkLowerBounds(x0, y0, lowerX, lowerY) or \
            self.__checkUpperBounds(x1, y1, upperX, upperY) 


    def __calculateGravityForce(self, node: CanvasNode) -> tuple:  
        
        
        
        circleSize = self.__model.getCircleSize() 
        x0, y0, _, _ = node.getCoords()
        centreDirectionX = self.__getAxisDirection(self.__canvasCentreX,  x0 + circleSize)
        centreDirectionY = self.__getAxisDirection(self.__canvasCentreX,  y0 + circleSize)


        # Returns the X-Y directions relative to the centre of the canvas 
        return (centreDirectionX * node.getGravityPull(), 
                centreDirectionY * node.getGravityPull())
    
    
    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def applyGravity(self):  
        circleOffset = self.__model.getCircleSize() // 2
        for node in self.__model.getNodes(): 
            x0, y0, _, _ = node.getCoords() 
            circleCentreX = x0 + circleOffset
            circleCentreY = y0 + circleOffset
            print(circleCentreX, circleCentreY, self.__canvasCentreX, self.__canvasCentreY)
            dist = self.__calculateDistance(circleCentreX, circleCentreY, 
                                            self.__canvasCentreX, self.__canvasCentreY)
            
            if dist <= 150: continue
            
            dx = self.__canvasCentreX - circleCentreX
            dy = self.__canvasCentreY - circleCentreY

            dirX = dx / max(1, dist)
            dirY = dy / max(1, dist)

            forceX = dirX * min(0.01, 0.0001 * dist) 
            forceY = dirY * min(0.01, 0.0001 * dist) 
         
            self.__updateNodeForces(node, forceX, forceY)
            

    

    # Apply all calculated forces 
    def applyForces(self) -> None:
        for node in self.__model.getNodes():
            node.applyForces()
            node.resetForces()

            
# Listen to Yesterday by The Beatles  