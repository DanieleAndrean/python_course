from FSM import State
import os
from askInput import *
from Trainer import *
from Pokemon import *

class Story(State):
    def run(self):
        pass
        
    def update(self,):
        pass
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    

class CharCreate(State):

    def run(self,**kwargs):
        # Username request
        errms=["Name must contain at least a letter, press Enter to retry: \n",""]
        trName=inputLoop("str","write your name: \n",errms)
        os.system("cls")
    
        #Trainer generation
        Tr=Trainer(trName)
        Starters=[]
        
        #Starters
        pk=next(poke for poke in PkList if poke["name"] == "bulbasaur")
        Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
                        
        pk=next(poke for poke in PkList if poke["name"] == "charmander")
        Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
        
        pk=next(poke for poke in PkList if poke["name"] == "squirtle")
        Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
        
        #Starter Pokemon choice
        reqmsg="Select your first pokemon among the following: \n\n"+"1: "+str(Starters[0])+"2: "+str(Starters[1])+"3: "+str(Starters[2])
        errms=["You must insert a number","You can only choose between the provided options"]
        okInput=False
        FirstPoke=inputLoop("int",reqmsg,errms,[1,2,3])-1
        os.system("cls")
        #adding Starter
        Tr.addPokemon(Starters[FirstPoke])

    
        
    def update(self,):
        pass
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)


    
class Travel(State):

    def run(self):
        pass
        
    def update(self,):
        pass
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    

class WildEncounter(State):
    def run(self):
        pass
        
    def update(self,):
        pass
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)