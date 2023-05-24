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
from tqdm import tqdm
def main():
    

    nSim=1000
    Nbattles=500
    
    #Starters
    Starters=PkDF["name"].values.tolist()
                    
 
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
    
    results = Parallel(n_jobs=4)(delayed(process)(Starters,Nbattles,i) for i in tqdm(range(nSim)))
    
    battList=[]
    for j in range(nSim):

        for i in range(Nbattles):
            tmp=results[j][0][i]
            battList.extend([{"Game":tmp["NGame"],"Battle":tmp["Battle"],"Result":tmp["Exitcond"],"Pk":tmp["Pokemon"],
                            "PkLvl":tmp["PokemonLvl"],"PkTyp":tmp["PokemonTypes"],"PkHP":tmp["PokemonActStats"].hp,
                            "PkAttack":tmp["PokemonActStats"].attack,"PkDefense":tmp["PokemonActStats"].defense,
                            "PkSpecial":tmp["PokemonActStats"].special,"PkSpeed":tmp["PokemonActStats"].speed,
                            "En":tmp["EnemyPk"],"EnLvl":tmp["EnemyLvl"],"EnTyp":tmp["EnemyTypes"],"EnHP":tmp["EnemyActStats"].hp,
                            "EnAttack":tmp["EnemyActStats"].attack,"EnDefense":tmp["EnemyActStats"].defense,
                            "EnSpecial":tmp["EnemyActStats"].special,"EnSpeed":tmp["EnemyActStats"].speed
                            }])
        
       

    resBatt=pd.DataFrame(battList)
    
    
    path=os.path.dirname(os.path.abspath(__file__))
    BattFile=path+"\\Battles.csv"
    
    resBatt.to_csv(BattFile)
    


       
    
   

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