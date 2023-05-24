import copy
from GameClasses.Trainer import *
from GameEng.FSM import State, FiniteStateMachine
import os
from UserInput import inputLoop, askInput
from GameClasses.Pokemon import *
from GameEng.Combat import combatTest,combat
from PokeData.load import PkDF,MvDF

#########################################################################################
#                               CUSTOM STATE AND FSM                                    #
#########################################################################################
#redefeinition of the FSM class to override the update method
class GameEngine(FiniteStateMachine):
     # Method to identify the next transition of the FSM using the state update method
     # CHANGES COMPARED TO FiniteStateMachine:
     # -target state Trainer is updated with the current state trainer
    def update(self, *args, update='update', **kargs):
        choices = self.possible_transitions()
        if not choices:
            print("No transition possible, game engine halting.")
            return None
        elif len(choices) == 1:
            nextState=choices[0]
            nextState.setTrainer(self.state.getTrainer())
            return nextState
        elif callable(getattr(self.state, update, None)):
            method = getattr(self.state, update, None)
            nextState=method(choices, *args, **kargs)
            nextState.setTrainer(self.state.getTrainer())
            return nextState
        else:
            print("Update rule is undefined, game engine halting.")
            return None


# State with trainer attribute
class GameState(State):
    def __init__(self,name,Trainer):
        super().__init__(name)
        self.Trainer=Trainer

    #set the trainer
    def setTrainer(self,Trainer):
        self.Trainer=Trainer
    
    #return a deep copy of the trainer
    def getTrainer(self):
        return copy.deepcopy(self.Trainer)
    

##############################################################################
#                            STORY
# ############################################################################    
class Story(GameState):
    def __init__(self,name,Trainer,usrchoice):
        super().__init__(name,Trainer)
        self.usrchoice=usrchoice
    
    def run(self):
        print("Trainer: "+str(self.Trainer))
        print("Pokemons: "+self.Trainer.showPokemons())
        reqmsg=("What do you want to do next?: \n\n"+
            "1: Explore\t\t"+
            "2: Go to Pokemon Center\n\n"+
            "3: Go to Pokemon Store\t\t"+
            "4: Quit Game")
        errms=["You must insert a number","You can only choose between the provided options"]
        self.usrchoice=inputLoop("int",reqmsg,errms,[1,2,3,4])
        os.system("cls")
        
    def update(self,choices):
       
        match self.usrchoice:
            case 1:
                ch="Explore"
            case 2:
                ch="Pokemon Center"
            case 3:
                ch="Pokemon Store"
            case 4:
                ch="Quit Game"
            case _:
                raise Exception("Unknown state")
        
        return next(st for st in choices if st.name==ch ) 
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)

##############################################################################
#                        CHARACTER CREATION
# ############################################################################    

class CharCreate(GameState):

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
    
    # the update method is not needed as only one transition is possible and will be handled by the game engine
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)


##############################################################################
#                             TRAVEL
# ############################################################################    

# handles Pokemon Store, Pokemon Center and Exploration states
class Travel(GameState):

    def __init__(self,name,Trainer,**tstargs):
        super().__init__(name,Trainer)
        self.combatFlag=False
        self.testMode=False
        self.EncounterProb=0.8
        if "EncounterProb" in tstargs:
            self.EncounterProb=tstargs["EncounterProb"]
        if "testMode" in tstargs:
            self.testMode=tstargs["testMode"]

    def run(self,**tstargs):
        match self.name:
            # explore and eventually encounter pokemons
            case 'Explore':
                prob=random.random()
              
                if self.EncounterProb>prob:
                    self.combatFlag=True
                    if not self.testMode:
                        print("Something approaches you from the tall grass!!!")
                    
                else:
                    if not self.testMode:
                        print("Nothing happened during your exploration")
                if not self.testMode:
                    askInput("","\nPress Enter to continue...")
            
            # heal pokemons, restore moves PPs
            case 'Pokemon Center':
                for pk in self.Trainer.PokemonList:
                    pk.heal()
                    for mv in pk.moves:
                        mv.restorePP()
                if not self.testMode:
                    print("Your Pokemons have been healed!!")
                    askInput("","\nPress Enter to continue...")
                    os.system("cls")
            # restore items  
            case 'Pokemon Store':
                for it in self.Trainer.Items:
                    it.restore()
                print("Your Items have been restocked!!")
                askInput("","\nPress Enter to continue...")
                os.system("cls")
            case _:
                raise Exception("Undefined state")
            
    # always returns Story if there is no combat 
    def update(self,choices,**tstargs):
        if (self.name=="Explore") and self.combatFlag:
            self.combatFlag=False
            nextSt=next(st for st in choices if st.name=="Wild Pokemon Encounter")
        else:
            nextSt=next(st for st in choices if st.name=="Story") 
        return nextSt
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    
##############################################################################
#                        WILD POKEMON ENCOUNTER
##############################################################################    


class WildEncounter(GameState):

    def __init__(self,name,Trainer,**tstarg):
        super().__init__(name,Trainer)
        self.exitcond=None
        self.testMode=False
        if tstarg:
            self.testMode=tstarg["testMode"]
    
    def run(self,**tstargs):

        #generate enemy pk
        pk=PkDF.sample(n=1)
        mvs=MvDF[(MvDF["type"].isin(pk["types"].values[0])) | (MvDF["type"]=="normal")].sample(n=2)
        lvl=random.randint(1,20)
        enemyPk=Pokemon(pk,mvs,lvl)
        if not self.testMode:
            print("A wild Pokemon approches you: \n\n"+ str(enemyPk))
            askInput("","\nPress Enter to continue...")
            self.exitcond=combat(self.Trainer,enemyPk)
        else:
            ext, stats = combatTest(self.Trainer,enemyPk)
            self.exitcond=ext
            self.Trainer.saveBatt(tstargs["Battle"],{"Exitcond":ext,**stats})
        
    def update(self,choices,**tstargs):
        if self.exitcond=="Def":
            return next(st for st in choices if st.name=="Pokemon Center") 
        
        return next(st for st in choices if st.name=="Story") 
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)
    

#############################################################################
#                           TEST
##############################################################################
class TestStory(GameState):
    def __init__(self,name,Trainer,maxBattles):
        super().__init__(name,Trainer)
        self.maxBattles=maxBattles
        
    def update(self,choices,**tstargs):
       
        if(tstargs["Battle"]>=self.maxBattles):
            return next(st for st in choices if st.name=="Quit Game")
       
        return next(st for st in choices if st.name=="Wild Pokemon Encounter" ) 
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str(self)