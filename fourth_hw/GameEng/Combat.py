from UserInput import *
from GameEng.FSM import FiniteStateMachine, State
from GameEng.CombatStates import *

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
            print("You successfully escaped!!")
            exitcon="Esc"
        
    askInput("","\nPress Enter to continue...")

    return exitcon


##############################################################################################
#                       TEST MODE   
##############################################################################################


def combatTest(Trainer,enemyPk):
    CbtEngine=FiniteStateMachine()
    
    EnT=EnemyTurn("Enemy Turn",testMode=True)
    Atk=TestCbt("Combat Menu")

    Vct=State("Victory")
    Def=State("Defeat")
    
    #states
    CbtEngine.add_state(Atk)
    CbtEngine.add_state(EnT)
    CbtEngine.add_state(Vct)
    CbtEngine.add_state(Def)
    
    #transitions
    CbtEngine.add_transition(Atk,EnT)
    CbtEngine.add_transition(Atk,Vct)
    CbtEngine.add_transition(Atk,Def)
    CbtEngine.add_transition(EnT,Def)
    CbtEngine.add_transition(EnT,Vct)
    CbtEngine.add_transition(EnT,Atk)
    

    CbtEngine.set_start_state(Atk)
    #final states
    CbtEngine.add_final_state(Vct)
    CbtEngine.add_final_state(Def)
    CbtEngine.initialize()
    nTurns=0
    while CbtEngine.state not in CbtEngine.final_states:
        nTurns+=1
        CbtEngine.eval_current(Trainer=Trainer,enemyPk=enemyPk,turn=nTurns-1)
        target=CbtEngine.update(Trainer=Trainer,enemyPk=enemyPk)
        CbtEngine.do_transition(target, CbtEngine.get_transition_attributes(target))

    exitcon=None
    percHP=(Trainer.PokemonList[0].showHP()/Trainer.PokemonList[0].showHP("max"))*100
    stats={"NTurns":nTurns,"PercHP":percHP,"Pokemon":Trainer.PokemonList[0].Name,
           "PokemonLvl":Trainer.PokemonList[0].Level,"EnemyPk":enemyPk.Name,"EnemyLvl":enemyPk.Level}
    match CbtEngine.state.name:
        case "Victory":
            exitcon="Vct"
        case "Defeat":
            exitcon="Def"
        

    return exitcon, stats
