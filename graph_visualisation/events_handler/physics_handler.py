# If this isn't at the top the program breaks :/
# If the file is run as is this message is printed and the program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

    
import math
from ...screens.graph_traverse.traversal_model import TraversalModel 
from graph_visualisation.graph_components import CanvasNode


# Handles all physics-based calculations 
class PhysicsHandler():
    def __init__(self, model : TraversalModel, canvasCentre : tuple) -> None:  
        # Reference to model
        self.__model = model
        # Centre X-Y Coordinates the canvas 
        self.__canvasCentreX, self.__canvasCentreY = canvasCentre

        # Values for physics calculations 
        self.__forceConstant = 200
        self.__maxRepulsionDist = 50 
        self.__gravityConstant = 2
        self.__maximumGravityDist = 150
        self.__springConstant = 0.05


    # Calculates distance between passed coords (pythagoras) 
    def __calculateDistance(self, x0 : float, y0 : float, x1 : float, y1 : float) -> float: 
        return math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2)) 
    

    def __calculateStandarisedVector(self, coords : tuple, dist : float) -> tuple:
        x0, y0, x1, y1 = coords 
        return ((x1 - x0) / max(dist, 0.1), (y1 - y0) / max(dist, 0.1))


    # Updates the forces in the passed nodes so they can be applied later 
    def __updateNodeForces(self, node : CanvasNode, forceX : float, forceY : float) -> None:  
        if node.isBeingDragged(): return
        node.adjustForceX(forceX)
        node.adjustForceY(forceY) 


    # Calculates force that drags nodes towards centre of the canvas 
    # Acts as way to stop nodes going offscreen 
    def __calculateGravity(self):  
        circleOffset = self.__model.getCircleSize() // 2
        for node in self.__model.getNodes():  
            x0, y0, _, _ = node.getCoords() 
            circleCentreX = x0 + circleOffset
            circleCentreY = y0 + circleOffset
            
            dist = self.__calculateDistance(circleCentreX, circleCentreY, 
                                            self.__canvasCentreX, self.__canvasCentreY)
            
            if dist <= self.__maximumGravityDist: continue

            dx, dy = self.__calculateStandarisedVector((circleCentreX, circleCentreY, 
                                                        self.__canvasCentreX, self.__canvasCentreY), dist)

            forceX = dx * self.__gravityConstant 
            forceY = dy * self.__gravityConstant 
            self.__updateNodeForces(node, forceX, forceY)
            

    # Calculates node-node repulsion
    def __calculateNodeRepulsion(self):
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
                if(dist > self.__maxRepulsionDist): continue
                
                # Resultant force as a scalar 
                force = (self.__forceConstant) / max(dist, 1) 
                # Convert scalar coords into standardised vector form 
                dx, dy = self.__calculateStandarisedVector((centreX0, centreY0, centreX1, centreY1), dist) 
                # Calculate X-Y forces to be applied to each node
                forceX, forceY = dx * force, dy * force
                
                # Update each nodes forces 
                self.__updateNodeForces(self.__model.getNode(i), -forceX, -forceY) 
                self.__updateNodeForces(self.__model.getNode(j), forceX, forceY)   
    

    def __calculateEdgeRestoration(self) -> None:
        circleOffset = self.__model.getCircleSize() // 2  

        for canvasEdge in self.__model.getEdges():
            startNode, endNode = canvasEdge.getNodes() 
            x0, y0, _, _ = startNode.getCoords()
            x1, y1, _, _ = endNode.getCoords()

            centreX0, centreY0 = x0 + circleOffset, y0 + circleOffset
            centreX1, centreY1 = x1 + circleOffset, y1 + circleOffset

            dist = self.__calculateDistance(centreX0, centreY0, centreX1, centreY1)
            displacement = dist - canvasEdge.getScreenLen() 

            dx, dy = self.__calculateStandarisedVector((centreX0, centreY0, centreX1, centreY1), dist)  
            # Calcalate spring restoration force applied to both nodes 
            springForce = displacement * self.__springConstant
            forceX, forceY = springForce * dx, springForce * dy

            self.__updateNodeForces(startNode, forceX, forceY)
            self.__updateNodeForces(endNode, -forceX, -forceY)


    # Apply all calculated forces 
    def __applyForces(self) -> None:
        circleOffset = self.__model.getCircleSize() // 2  
        # Update coords of each node
        for node in self.__model.getNodes():
            if not node.isBeingDragged(): node.applyForces()
            node.resetForces()
        
        # Update coords of each edge 
        for canvasEdge in self.__model.getEdges():
            startNode, endNode = canvasEdge.getNodes()  
            x0, y0, _, _ = startNode.getCoords()
            x1, y1, _, _ = endNode.getCoords() 

            canvasEdge.updateCoords((x0 + circleOffset, y0 + circleOffset, 
                                    x1 + circleOffset, y1 +  circleOffset)) 
        
    
    # Caclulate and apply forces to each object drawn on screen
    def applyPhysics(self) -> None: 
        self.__calculateGravity()
        self.__calculateNodeRepulsion()
        self.__calculateEdgeRestoration()
        self.__applyForces()


# Listen to Yesterday by The Beatles  
