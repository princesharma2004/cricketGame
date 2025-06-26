from random import randint

class Cricketer:

    def __init__(self, id: int, name: str, playerType: str) -> None:
        self.id=id
        self.name=name
        self.playerType=playerType
    
    def batting(self) -> int:
        return int(randint(0, 6))
    
    def bowling(self) -> int:
        return int(randint(0, 6))
