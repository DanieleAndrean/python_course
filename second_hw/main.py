from askInput import askInput, inputLoop
from Trainer import Trainer
from Pokemon import Pokemon
from PokeList import PkList
from MovesList import MvList
from ItemsList import ItList
from FSM import FiniteStateMachine
from GameStates import *
import matplotlib.pyplot as plt



def main():           
    #Starters
    Starters=[]
    pk=next(poke for poke in PkList if poke["name"] == "bulbasaur")
    Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
                    
    pk=next(poke for poke in PkList if poke["name"] == "charmander")
    Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
    
    pk=next(poke for poke in PkList if poke["name"] == "squirtle")
    Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))

    #Starting items
    StartItm=[]
    it=next(itm for itm in ItList if itm["name"]=="Pokeball")
    StartItm.append(Item(it,it["maxNum"]))

    it=next(itm for itm in ItList if itm["name"]=="Health Potion")
    StartItm.append(Item(it,it["maxNum"]))

    cc = CharCreate('Character Creation',[],Starters,StartItm)
    story= Story('Story',None,None)
    explore= Travel('Explore',None)
    pokeStore=Travel("Pokemon Store",None)
    pokeCenter=Travel("Pokemon Center",None)
    wildPk=WildEncounter("Wild Pokemon Encounter",None)
    quitGame=State("Quit Game",None)
    Game = FiniteStateMachine()
    
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
   # plt.figure(1)
   # Game.draw()

    Starters=[]
        
    

    while Game.state not in Game.final_states:

        Game.eval_current()
        target=Game.update()
        Game.do_transition(target, Game.get_transition_attributes(target))

main()