from UserInput import askInput, inputLoop
from GameClasses.Pokemon import Pokemon
from GameClasses.Item import Item
from GameEng.GameStates import *
from PokeData.load import PkList,MvList
from PokeData.ItemsList import ItList
import matplotlib.pyplot as plt
import random


def main():           
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

    cc = CharCreate('Character Creation',None,Starters,StartItm)
    story= Story('Story',None,None)
    explore= Travel('Explore',None)
    pokeStore=Travel("Pokemon Store",None)
    pokeCenter=Travel("Pokemon Center",None)
    wildPk=WildEncounter("Wild Pokemon Encounter",None)
    quitGame=GameState("Quit Game",None)
    Game = GameEngine()
    
    Game.add_state(cc)
    Game.add_state(story)
    Game.add_state(explore)
    Game.add_state(pokeStore)
    Game.add_state(pokeCenter)    
    Game.add_state(wildPk)
    Game.add_state(quitGame)

    Game.add_transition(cc, story)
    Game.add_transition(story, explore)
    Game.add_transition(explore, wildPk)
    Game.add_transition(explore, story)   
    Game.add_transition(wildPk,pokeCenter)
    Game.add_transition(wildPk,story) 
    Game.add_transition(story, pokeStore)    
    Game.add_transition(pokeStore, story)    
    Game.add_transition(story, pokeCenter)  
    Game.add_transition(pokeCenter, story)
    Game.add_transition(story,quitGame)
    
    Game.set_start_state(cc)
    Game.add_final_state(quitGame)
    Game.initialize()
    

    while Game.state not in Game.final_states:

        Game.eval_current()
        target=Game.update()
        Game.do_transition(target) 

if __name__=="__main__":
    main()