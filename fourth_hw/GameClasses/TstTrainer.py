from GameClasses.Trainer import Trainer
import pandas as pd

class TstTrainer(Trainer):

    def __init__(self,name,Pokemons,Items):
       super().__init__(name,Pokemons,Items)
       self.battles=pd.DataFrame()

    def saveBatt(self,battleDict):
        self.battles.concat(battleDict)