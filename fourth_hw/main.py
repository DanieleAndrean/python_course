from UserInput import askInput, inputLoop
from GameClasses.Pokemon import Pokemon
from GameClasses.TstTrainer import TstTrainer
from GameClasses.Item import Item
from GameEng.GameStates import *
from PokeData.load import PkDF,MvsDF
from PokeData.ItemsList import ItList
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def main():
    

    nSim=500
    Nbattles=150
    

    #Starters
    Starters=[]
    pk=PkDF[PkDF["name"]=="bulbasaur"]
    mv=MvsDF[MvsDF["type"] in  pk["types"] or MvsDF["type"]=="normal"].sample(n=2)
    Starters.append(Pokemon(pk, mv))
                    
    pk=PkDF[PkDF["name"]=="charmander"]
    mv=MvsDF[MvsDF["type"] in  pk["types"] or MvsDF["type"]=="normal"].sample(n=2)
    Starters.append(Pokemon(pk, mv))
    
    pk=PkDF[PkDF["name"]=="squirtle"]
    mv=MvsDF[MvsDF["type"] in  pk["types"] or MvsDF["type"]=="normal"].sample(n=2)
    Starters.append(Pokemon(pk, mv))


    res=pd.DataFrame()
    for i in range(nSim):
       Starter=random.choice(Starters)
       sim=SingleSim(Starter,Nbattles)
       tmp=pd.DataFrame(np.ones((Nbattles,1))*i,columns="TrainerIdx")
       res.append(pd.concat([tmp,sim.battles],axis=1))

    SaveFile="Results.csv"
    res.to_csv(SaveFile)
    
    
    
    
   

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
    
    while Game.state not in Game.final_states:
        Tr=Game.state.Trainer
        Game.eval_current(Battle=nbattles)
        if Game.state is pokeCenter:
            Tr.battles[nbattles]["Battle"]=nbattles+1
            nbattles+=1

        target=Game.update(Battle=nbattles)
        Game.do_transition(target) 
        

    return Tr



if __name__=="__main__":
    main()