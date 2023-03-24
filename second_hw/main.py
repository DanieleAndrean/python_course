from askInput import askInput, inputLoop
from Trainer import Trainer
from Pokemon import Pokemon
from PokeList import PkList
from MovesList import MvList
from FSM import FiniteStateMachine
from GameStates import *
import matplotlib.pyplot as plt

cc = CharCreate('Character Creation',None)
story= Story('Story',None)
explore= Travel('Explore',None)
pokeStore=Travel("Pokemon Store",None)
pokeCenter=Travel("Pokemon Center",None)
wildPk=WildEncounter("Wild Pokemon Encounter",None)

def main():           
    
    Game = FiniteStateMachine()
    
    Game.add_state(cc)
    Game.add_state(story)
    Game.add_state(explore)
    Game.add_state(pokeStore)
    Game.add_state(pokeCenter)    
    Game.add_state(wildPk)


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
         
    
    Game.set_start_state(cc)
    Game.initialize()
    plt.figure(1)
    Game.draw()

main()