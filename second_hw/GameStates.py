from FSM import State
import os
from askInput import *
from Trainer import *
from Pokemon import *

class Story(State):
    def __init__(self,name,Trainer,choice):
        super().__init__(name,Trainer)
        self.choice=choice
    
    def run(self):
        
        reqmsg=("What do you want to do next?: \n\n"+
            "1: Explore\t\t"+
            "2: Go to Pokemon Center\n\n"+
            "3: Go to Pokemon Store\t\t"+
            "4: Quit Game")
        errms=["You must insert a number","You can only choose between the provided options"]
        self.choice=inputLoop("int",reqmsg,errms,[1,2,3,4])
        os.system("cls")
        
    def update(self,choices):
       
        match self.choice:
            case 1:
                return explore
            case 2:
                return pokemonCenter
            case 3:
                return pokemonStore
            case 4:
                return quitGame
            case _:
                raise Exception("Unknown state")
            
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    

class CharCreate(State):

    def __init__(self,name,Trainer,Starters,Items):
        super().__init__(name,Trainer)
        self.Starters=Starters
        self.Items=Items
    def run(self):
        # Username request
        errms=["Name must contain at least a letter, press Enter to retry: \n",""]
        trName=inputLoop("str","write your name: \n",errms)
        os.system("cls")
        #Starter Pokemon choice
        reqmsg=("Select your first pokemon among the following: \n\n"+
                "1: "+str(self.Starters[0])+
                "2: "+str(self.Starters[1])+
                "3: "+str(self.Starters[2])
                )
        errms=["You must insert a number","You can only choose between the provided options"]
        FirstPoke=inputLoop("int",reqmsg,errms,[1,2,3])-1
        os.system("cls")
        #Trainer generation
        self.Trainer=Trainer(trName,[],[])
        
        #adding Starter
        self.Trainer.addPokemon(self.Starters[FirstPoke])
        #adding initial items
        for i in self.Items:
            self.Trainer.addItem(i)
    
        
    def update(self,choices):
        return story
        
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