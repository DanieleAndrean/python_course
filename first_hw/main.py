from askInput import askInput, inputLoop
from Trainer import Trainer
from Pokemon import Pokemon
from PokeList import PkList
from MovesList import MvList
import os
import random
def main():

    # Username request
    errms=["Name must contain at least a letter, press Enter to retry: \n",""]
    trName=inputLoop("str","write your name: \n",errms)
    os.system("cls")
 
    #Trainer generation
    Tr=Trainer(trName)
    Starters=[]
    
    #Starters
    pk=next(poke for poke in PkList if poke["name"] == "bulbasaur")
    Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
                     
    pk=next(poke for poke in PkList if poke["name"] == "charmander")
    Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
    
    pk=next(poke for poke in PkList if poke["name"] == "squirtle")
    Starters.append(Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]]))
    
    #Starter Pokemon choice
    reqmsg="Select your first pokemon among the following: \n\n"+"1: "+str(Starters[0])+"2: "+str(Starters[1])+"3: "+str(Starters[2])
    errms=["You must insert a number","You can only choose between the provided options"]
    okInput=False
    FirstPoke=inputLoop("int",reqmsg,errms,[1,2,3])-1
    os.system("cls")
    #adding Starter
    Tr.addPokemon(Starters[FirstPoke])

    #combat simulaiton
    pk=next(poke for poke in PkList if poke["name"] == "squirtle")
    enemyPk=Pokemon(pk, [mv for mv in MvList if mv["name"] in pk["moves"]])

    combatTest(Tr,enemyPk)
   
#Combat handling funciton
def combatTest(Trainer,enemyPk):
   
    os.system("cls")
    print("Oh no an enemy Pokemon appears!!\n")
    print(str(enemyPk))

    askInput("","press Enter to fight:")
    
    #combat loop, combat ends either when the trainer has no more pokemons or when the enemy pokemon is defeated
    while(Trainer.hasPokemons() and not enemyPk.isKO()):
        #move choice
        reqmsg="Select a move among the following: \n\n"+Trainer.PokemonList[0].movesDisp()
        errmsg=["You must insert a number","You can only choose between the provided options"]
        mv=inputLoop("int",reqmsg,errmsg,[1,2,3])-1
        os.system("cls")
        print(Trainer.PokemonList[0].Name+" uses "+Trainer.PokemonList[0].moves[mv].name)
        
        #attack success check
        if Trainer.PokemonList[0].useMove(mv,enemyPk):
            print("attack succeded!! \n\n")
            print("enemy HP: "+str(enemyPk.showHP())+"\n\n")
            print("your Pokemon HP: "+str(Trainer.PokemonList[0].showHP()))
            
        else:
            print("attack missed")

        askInput("","Press Enter to continue:")
        os.system("cls")
        
        #enemy turn, handled automatically
        print("Enemy turn /!\\ \n\n")
        askInput("","Press Enter to continue:")
        os.system("cls")

        #randomly selected move
        mv=random.randint(1,len(enemyPk.moves))-1
        print(enemyPk.Name+" uses "+enemyPk.moves[mv].name)

        #attack success check
        if enemyPk.useMove(mv,Trainer.PokemonList[0]):
            
            print("attack succeded!! \n\n")
            print("enemy HP: "+str(enemyPk.showHP())+"\n\n")
            print("your Pokemon HP: "+str(Trainer.PokemonList[0].showHP()))
        else:
            print("attack missed")

        askInput("","Press Enter to continue:")
        os.system("cls")
        #end of turn
        
    #exit condition check
    if(enemyPk.isKO()):
        print("You won !!!")
    else:
        print("oh no you lost")


if __name__=="__main__":
    main()