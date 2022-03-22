class Entity:
    unitID = 0;
    pos = [0,0]
    health = 0;
    magic = 0;
    strength = 0;
    behaviorTree = [];
    
    def __init__(self):
        
        print("created new object")
    
    
    def createBehaviorTree(self):
        print("created behaviorTree")
    
    
    def move(self):
        print("moved")
    
    
    