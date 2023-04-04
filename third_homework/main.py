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
def main():

    
    nSim=5
    Nbattles=15
    BulabsaurRes=[]
    BulabsaurVct=np.empty((nSim,1),dtype=int)
    BulabsaurTurn=np.empty((nSim,Nbattles),dtype=int)
    BulabsaurPHP=np.empty((nSim,Nbattles),dtype=float)
    BulbasaurEneWin=dict()
    CharmanderRes=[]
    CharmanderVct=np.empty((nSim,1),dtype=int)
    CharmanderTurn=np.empty((nSim,Nbattles),dtype=int)
    CharmanderPHP=np.empty((nSim,Nbattles),dtype=float)
    CharmanderEneWin=dict()
    SquirtleRes=[]
    SquirtleVct=np.empty((nSim,1),dtype=int)
    SquirtleTurn=np.empty((nSim,Nbattles),dtype=int)
    SquirtlePHP=np.empty((nSim,Nbattles),dtype=float)
    SquirtleEneWin=dict()
    for i in range(nSim):
       BulabsaurRes.append(SingleSIm(0,Nbattles))
       j=0
       for b in BulabsaurRes[i].battles:
            vct=(1 if b["exitcond"]=="Vct" else 0)
            try:
                BulbasaurEneWin[b["enemyPk"]].append(vct)
            except KeyError:
                BulbasaurEneWin[b["enemyPk"]] = [vct]
            BulabsaurVct[i]+=vct
            BulabsaurTurn[i,j]=b["nTurns"]
            BulabsaurPHP[i,j]=b["percHP"]
            j+=1
           

       CharmanderRes.append(SingleSIm(1,Nbattles))
       j=0
       for b in CharmanderRes[i].battles:
            vct=(1 if b["exitcond"]=="Vct" else 0)
            try:
                CharmanderEneWin[b["enemyPk"]].append(vct)
            except KeyError:
                CharmanderEneWin[b["enemyPk"]] = [vct]
            CharmanderVct[i]+=vct
            CharmanderTurn[i,j]=b["nTurns"]
            CharmanderPHP[i,j]=b["percHP"]
            j+=1

       SquirtleRes.append(SingleSIm(2,Nbattles))
       j=0
       for b in SquirtleRes[i].battles:
            vct=(1 if b["exitcond"]=="Vct" else 0)
            try:
                SquirtleEneWin[b["enemyPk"]].append(vct)
            except KeyError:
                SquirtleEneWin[b["enemyPk"]] = [vct]
            SquirtleVct[i]+=vct
            SquirtleTurn[i,j]=b["nTurns"]
            SquirtlePHP[i,j]=b["percHP"]
            j+=1  
    
    mpl.plot([0,1,2],[np.sum(BulabsaurVct)/nSim,np.sum(CharmanderVct)/nSim,np.sum(SquirtleVct)/nSim],'or')
    mpl.ylabel("Average win number")
   
    
    
    f,ax1=mpl.subplots()
    ax1.boxplot((BulabsaurPHP.flatten(), CharmanderPHP.flatten(),SquirtlePHP.flatten()))
    ax1.set_xticklabels(['Bulbasaur', 'Charmander', 'Squirtle'])
    ax1.set_ylabel("Percentage of remaining HP")



    f,ax2=mpl.subplots()
    ax2.boxplot((BulabsaurTurn.flatten(), CharmanderTurn.flatten(),SquirtleTurn.flatten()))
    ax2.set_xticklabels(['Bulbasaur', 'Charmander', 'Squirtle'])
    ax2.set_ylabel("Number of Turns")



    mpl.show()


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