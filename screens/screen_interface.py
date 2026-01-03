# If the file is run as is message this returned and program exits
if(__name__ == "__main__"):
    print("This is file shouldn't be run on it's own. \nIt should be imported only.")
    exit()

from abc import ABC, abstractmethod
# Abstract class - every screen must implement the initScreen method
class Screen(ABC):
    @abstractmethod
    def render(self): pass 


# Listen to Runnin' Wild by Airbourne