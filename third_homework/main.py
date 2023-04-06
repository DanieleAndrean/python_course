from UserInput import askInput, inputLoop
from GameClasses.Pokemon import Pokemon
from GameClasses.TstTrainer import TstTrainer
from GameClasses.Item import Item
from GameEng.GameStates import *
from PokeData.load import PkList,MvList
from PokeData.ItemsList import ItList
import random
import numpy as np
import matplotlib.pyplot as mpl
import pickle

def main():
    
    nSim=500
    Nbattles=150
    BulabsaurRes=[]
    BulabsaurVct=np.zeros((nSim,1),dtype=int)
    BulabsaurTurn=np.zeros((nSim,Nbattles),dtype=int)
    BulabsaurPHP=np.zeros((nSim,Nbattles),dtype=float)
    BulbasaurEneWin=dict()
    CharmanderRes=[]
    CharmanderVct=np.zeros((nSim,1),dtype=int)
    CharmanderTurn=np.zeros((nSim,Nbattles),dtype=int)
    CharmanderPHP=np.zeros((nSim,Nbattles),dtype=float)
    CharmanderEneWin=dict()
    SquirtleRes=[]
    SquirtleVct=np.zeros((nSim,1),dtype=int)
    SquirtleTurn=np.zeros((nSim,Nbattles),dtype=int)
    SquirtlePHP=np.zeros((nSim,Nbattles),dtype=float)
    SquirtleEneWin=dict()

    for i in range(nSim):
       BulabsaurRes.append(SingleSIm(0,Nbattles))
       j=0
       for b in BulabsaurRes[i].battles:
            php=b["percHP"]
            vct=(1 if b["exitcond"]=="Vct" else 0)
            try:
                BulbasaurEneWin[b["enemyPk"]].append((vct,php,b["nTurns"]))
            except KeyError:
                BulbasaurEneWin[b["enemyPk"]] = [(vct,php,b["nTurns"])]
            BulabsaurVct[i]+=vct
            BulabsaurTurn[i,j]=b["nTurns"]
            BulabsaurPHP[i,j]=php
            j+=1
           

       CharmanderRes.append(SingleSIm(1,Nbattles))
       j=0
       for c in CharmanderRes[i].battles:
            php=c["percHP"]
            vct=(1 if c["exitcond"]=="Vct" else 0)
            try:
                CharmanderEneWin[c["enemyPk"]].append((vct,php,b["nTurns"]))
            except KeyError:
                CharmanderEneWin[c["enemyPk"]] = [(vct,php,b["nTurns"])]
            CharmanderVct[i]+=vct
            CharmanderTurn[i,j]=c["nTurns"]
            CharmanderPHP[i,j]=php
            j+=1

       SquirtleRes.append(SingleSIm(2,Nbattles))
       j=0
       for s in SquirtleRes[i].battles:
            php=s["percHP"]
            vct=(1 if s["exitcond"]=="Vct" else 0)
            try:
                SquirtleEneWin[s["enemyPk"]].append((vct,php,b["nTurns"]))
            except KeyError:
                SquirtleEneWin[s["enemyPk"]] = [(vct,php,b["nTurns"])]
            SquirtleVct[i]+=vct
            SquirtleTurn[i,j]=s["nTurns"]
            SquirtlePHP[i,j]=php
            j+=1  
    
    
    with open("BulbasaurRes","wb") as Fout: # open a file in "write byte" mode
        pickle.dump(BulabsaurRes, Fout) # save the object inside the file

    with open("CharmanderRes","wb") as Fout: # open a file in "write byte" mode
        pickle.dump(CharmanderRes, Fout) # save the object inside the file

    with open("SquirtleRes","wb") as Fout: # open a file in "write byte" mode
        pickle.dump(SquirtleRes, Fout) # save the object inside the file 

    
   

##########################################################################################################
#                                        SIMFUNCTION
#############################################################################################################





def SingleSIm(Starter,Nbattles):           
    
    #Starters
    Starters=[]
    pk=next(poke for poke in PkList if poke["name"] == "bulbasaur")
    mv=random.sample([m for m in MvList if m["type"] in pk["types"] or m["type"]=="normal"],2)
    Starters.append(Pokemon(pk, mv))
                    
    pk=next(poke for poke in PkList if poke["name"] == "charmander")
    mv=random.sample([m for m in MvList if m["type"] in pk["types"] or m["type"]=="normal"],2)
    Starters.append(Pokemon(pk, mv))
    
    pk=next(poke for poke in PkList if poke["name"] == "squirtle")
    mv=random.sample([m for m in MvList if m["type"] in pk["types"] or m["type"]=="normal"],2)
    Starters.append(Pokemon(pk, mv))
    #Starting items
    StartItm=[]
    it=next(itm for itm in ItList if itm["name"]=="Pokeball")
    StartItm.append(Item(it,it["maxNum"]))

    it=next(itm for itm in ItList if itm["name"]=="Health Potion")
    StartItm.append(Item(it,it["maxNum"]))

    Tr=TstTrainer("Test",[],StartItm)
    Tr.PokemonList.append(Starters[Starter])

    

    #cc = CharCreate('Character Creation',None,Starters,StartItm)
    story= TestStory('Story',Tr,Nbattles)
    #explore= Travel('Explore',None,EncounterProb=1)
    #pokeStore=Travel("Pokemon Store",None)
    pokeCenter=Travel("Pokemon Center",None,testMode=True,EncounterProb=1)
    wildPk=WildEncounter("Wild Pokemon Encounter",None,testMode=True)
    quitGame=GameState("Quit Game",None)
    Game = GameEngine()
    
    #Game.add_state(cc)
    Game.add_state(story)
    #Game.add_state(explore)
    #Game.add_state(pokeStore)
    Game.add_state(pokeCenter)    
    Game.add_state(wildPk)
    Game.add_state(quitGame)

    #Game.add_transition(cc, story)
    #Game.add_transition(story, explore)
    Game.add_transition(story, wildPk)
    #Game.add_transition(explore, story)   
    Game.add_transition(wildPk,pokeCenter)
    #Game.add_transition(wildPk,story) 
    #Game.add_transition(story, pokeStore)    
    #Game.add_transition(pokeStore, story)    
    #Game.add_transition(story, pokeCenter)  
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