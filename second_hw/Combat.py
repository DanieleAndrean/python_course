import os
from UserInput import *
import random
from FSM import FiniteStateMachine, State
from CombatStates import *
import matplotlib.pyplot as plt
#################################Combat handling funciton##############################################
def combat(Trainer,enemyPk):
   
    CbtEngine=FiniteStateMachine()
    #combat states
    Menu=CbtMenu("Combat Menu")
    Atk=Attack("Attack")
    Itm=UseItem("Use Item")
    PkChng=ChangePokemon("Change Pokemon")
    Fl=Flee("Flee")
    EnT=EnemyTurn("Enemy Turn")

    #end combat states
    Vct=State("Victory")
    Def=State("Defeat")
    Cgt=State("Caught")
    Esc=State("Escaped")

    #states
    CbtEngine.add_state(Menu)
    CbtEngine.add_state(Atk)
    CbtEngine.add_state(Itm)
    CbtEngine.add_state(PkChng)
    CbtEngine.add_state(Fl)
    CbtEngine.add_state(EnT)
    CbtEngine.add_state(Vct)
    CbtEngine.add_state(Def)
    CbtEngine.add_state(Cgt)
    CbtEngine.add_state(Esc)

    #possible Transitions
    CbtEngine.add_transition(Menu,Atk)
    CbtEngine.add_transition(Atk,Menu)
    CbtEngine.add_transition(Menu,Itm)
    CbtEngine.add_transition(Itm,Menu)
    CbtEngine.add_transition(Menu,PkChng)
    CbtEngine.add_transition(PkChng,Menu)
    CbtEngine.add_transition(Menu,Fl)
    CbtEngine.add_transition(Fl,Menu)
    CbtEngine.add_transition(Atk,EnT)
    CbtEngine.add_transition(Atk,Vct)
    CbtEngine.add_transition(Atk,Def)
    CbtEngine.add_transition(Itm,Itm)
    CbtEngine.add_transition(Itm,EnT)
    CbtEngine.add_transition(Itm,Cgt)
    CbtEngine.add_transition(PkChng,EnT)
    CbtEngine.add_transition(Fl,EnT)
    CbtEngine.add_transition(Fl,Esc)
    CbtEngine.add_transition(EnT,PkChng)
    CbtEngine.add_transition(EnT,Menu)
    CbtEngine.add_transition(EnT,Def)
    CbtEngine.add_transition(EnT,Vct)
    

    CbtEngine.set_start_state(Menu)
    #final states
    CbtEngine.add_final_state(Vct)
    CbtEngine.add_final_state(Def)
    CbtEngine.add_final_state(Esc)
    CbtEngine.add_final_state(Cgt)
    CbtEngine.initialize()
    
    while CbtEngine.state not in CbtEngine.final_states:

        CbtEngine.eval_current(Trainer=Trainer,enemyPk=enemyPk)
        target=CbtEngine.update(Trainer=Trainer,enemyPk=enemyPk)
        CbtEngine.do_transition(target, CbtEngine.get_transition_attributes(target))

    exitcon=None
    match CbtEngine.state.name:
        case "Victory":
            print("You Won !!!")
            exitcon="Vct"
        case "Defeat":
            print("All your Pokemons are KO!!!\nYou are being sent to the nearest Pokemon Center")
            exitcon="Def"
        case "Caught":
            print("Congratulations, you have a new Pokemon!!!")
            exitcon="Cgt"
        case "Escaped":
            #message already in the state run()
            exitcon="Esc"
        
    askInput("","\nPress Enter to continue...")

    return exitcon
