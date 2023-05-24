from GameClasses.Trainer import Trainer


class TstTrainer(Trainer):

    def __init__(self,name,Pokemons,Items):
       super().__init__(name,Pokemons,Items)
       self.battles=[]
       self.battleTurns=[]

    def saveBatt(self,battleidx,battleDict):
        self.battles[battleidx].update(battleDict)
    
    def saveTurn(self,turnDict):
        self.battleTurns.append(turnDict)