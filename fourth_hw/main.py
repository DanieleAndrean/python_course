from UserInput import askInput, inputLoop
from GameClasses.Pokemon import Pokemon
from GameClasses.TstTrainer import TstTrainer
from GameClasses.Item import Item
from GameEng.GameStates import *
from PokeData.load import PkDF,MvDF
from PokeData.ItemsList import ItList
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from joblib import Parallel, delayed
def main():
    

    nSim=1000
    Nbattles=150
    
    #Starters
    Starters=["bulbasaur","charmander","squirtle"]
                    
 
    def process(Starters,Nbattles,i):
       battList=[]
       turnList=[]
       StarterName=random.choice(Starters)
       lvl=random.randint(1,20)
       pk=PkDF[PkDF["name"]==StarterName]
       mv=MvDF[(MvDF["type"].isin(pk["types"].values[0])) | (MvDF["type"]=="normal")].sample(n=2)
       Starter=Pokemon(pk, mv,lvl)
       
       sim=SingleSim(Starter,Nbattles)
       for item in sim.battles: item['NGame']=i
       for item in sim.battleTurns: item['NGame']=i
       battList=sim.battles
       battList.pop()
       turnList=sim.battleTurns
       turnList.pop()
       return battList,turnList
    
    results = Parallel(n_jobs=4)(delayed(process)(Starters,Nbattles,i) for i in range(nSim))
    
    battList=[]
    turnList=[]
    for i in range(len(results)):
        battList.extend(results[i][0])
        turnList.extend(results[i][1])
       

    resBatt=pd.DataFrame(battList)
    
    resTurn=pd.DataFrame(turnList)
    path=os.path.dirname(os.path.abspath(__file__))
    BattFile=path+"\\Battles.csv"
    TurnFile=path+"\\Turns.csv"
    resBatt.to_csv(BattFile)
    resTurn.to_csv(TurnFile)


       
    
   

##########################################################################################################
#                                        SIMFUNCTION
#############################################################################################################

def SingleSim(Starter,Nbattles):           
    
    
    #Starting items
    StartItm=[]
    
    Tr=TstTrainer("Test",[],StartItm)
    Tr.PokemonList.append(Starter)

    
    story= TestStory('Story',Tr,Nbattles)

    pokeCenter=Travel("Pokemon Center",None,testMode=True,EncounterProb=1)
    wildPk=WildEncounter("Wild Pokemon Encounter",None,testMode=True)
    quitGame=GameState("Quit Game",None)
    Game = GameEngine()
    
    
    Game.add_state(story)
    Game.add_state(pokeCenter)    
    Game.add_state(wildPk)
    Game.add_state(quitGame)

    Game.add_transition(story, wildPk)
    Game.add_transition(wildPk,pokeCenter)
    Game.add_transition(pokeCenter, story)
    Game.add_transition(story,quitGame)
    
    Game.set_start_state(story)
    Game.add_final_state(quitGame)
    Game.initialize()
    
    nbattles=0
    Tr.battles.append({"Battle":nbattles})
    while Game.state not in Game.final_states:
        Tr=Game.state.Trainer
        Game.eval_current(Battle=nbattles)
        if Game.state is pokeCenter:
            Tr.battles.append({"Battle":nbattles+1})
            nbattles+=1

        target=Game.update(Battle=nbattles)
        Game.do_transition(target) 
        

    return Tr



if __name__=="__main__":
    main()