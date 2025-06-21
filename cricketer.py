from random import randint

class Cricketer:

    def __init__(self, name: str, jerseyNumber: int) -> None:
        self.name=name
        self.jerseyNumber=jerseyNumber
    
    def batting(self) -> int:
        return randint(0, 6)
    
    def bowling(self) -> int:
        return randint(0, 6)
