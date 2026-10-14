import math
import csv
from dataclasses import dataclass# utility tool to make structured classess specially for storing data
@dataclass(frozen=True)#frozen mean the object cannot be modified
# dataclass automatically generates __init__()
class Component:
    name:str# name of the componet
    failure_rate:float# failure/rate
    
    def reliability(self,t:float)->float:
        """ Calculate reliability using exponential distribution
        R(t) = e^(-lambda*t)"""
        return math.exp(-self.failure_rate*t)
    def unreliability(self,t:float)->float:
        """Calculate unreliability using exponential distribution
        Q(t) = 1-R(t)"""
        return 1-self.reliability(t)
def load_component(path:str)->dict[str,float]:#{component_name:failure_rate}
    with open(path,newline="") as f:
        return {r["names":Component(r["name"],float(r["failure_rate"]))]
        for r in csv.DictReader(f)}

       
    

