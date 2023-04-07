from GameEng.FSM import State
import os
from UserInput import *
from GameClasses.Trainer import *
from GameClasses.Pokemon import *

#################################################################
#                       COMBAT MENU                             #
#################################################################
class CbtMenu(State):
    def __init__(self,name):
        super().__init__(name)
        self.menumsg=("What do you want to do next: \n\n"+
                "1: Attack\t\t"+
                "2: Change Pokemon\n"
                "3: Use an Item\t\t"
                "4: flee")
        self.errmsg=["You must insert a number","You can only choose between the provided options"]
        self.usrchoice=None

    def run(self,**fighters):
        self.usrchoice=inputLoop("int",self.menumsg,self.errmsg,[1,2,3,4])
        os.system("cls")

    def update(self,choices,**fighters):
        match self.usrchoice:
            case 1:
                ch="Attack"
            case 2:
                ch="Change Pokemon"
            case 3: 
                ch="Use Item"
            case 4:
                ch="Flee"
            
            case _:
                raise Exception("Undefined State")

        return next(st for st in choices if st.name==ch)
    

    
#################################################################
#                       ATTACK                                  #
#################################################################

class Attack(State):

    def __init__(self,name):
        super().__init__(name)
        self.back=False

    def run(self,**fighters):
        Trainer=fighters["Trainer"]
        enemyPk=fighters["enemyPk"]

        availMoves=Trainer.PokemonList[0].availMoves() 
        btm=max(availMoves)+1
        msg=("Which move should "+Trainer.PokemonList[0].Name+" use?\n\n"+
                Trainer.PokemonList[0].movesDisp(availMoves)+
                "\n"+str(btm)+": Back to Menu")
        errmsg=["You must insert a number","You can only choose between the provided options"]
        mv=inputLoop("int",msg,errmsg,availMoves+[btm])
        os.system("cls")

        
        if not mv==btm:
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
        else:
            self.back=True
                
    def update(self,choices,**fighters):
        if self.back:
            self.back=False
            return next(st for st in choices if st.name=="Combat Menu")
        else:
            Trainer=fighters["Trainer"]
            enemyPk=fighters["enemyPk"]

            if enemyPk.isKO():
                return next(st for st in choices if st.name=="Victory")
            if(not Trainer.hasPokemons()):
                return next(st for st in choices if st.name=="Defeat")
            if(Trainer.PokemonList[0].isKO() and Trainer.hasPokemons()):
                return next(st for st in choices if st.name=="Change Pokemon")
            return next(st for st in choices if st.name=="Enemy Turn")



########################################################################################
#                                   CHANGE POKEMON
# ################################################################################### 

class ChangePokemon(State):

    def __init__(self,name):
        super().__init__(name)
        self.back=False

    def run(self,**fighters):
        Trainer=fighters["Trainer"]

        if Trainer.PokemonList[0].isKO():
            koMsg=Trainer.PokemonList[0].Name+" is KO, you must replace it"
        else:
            koMsg=""

        availPokes=[pk for pk in range(len(Trainer.PokemonList)) if not Trainer.PokemonList[pk].isKO()]
        btm=max(availPokes)+1
        msg=(koMsg+"\nChoose a Pokemon to replace "+Trainer.PokemonList[0].Name+" among the available ones:\n\n"+
                Trainer.showPokemons(availPokes)+
                "\n"+str(btm)+": Back to Menu")
        errmsg=["You must insert a number","You can only choose between the provided options"]
        switchPk=inputLoop("int",msg,errmsg,availPokes+[btm])
        os.system("cls")

        if not switchPk==btm:

            Trainer.PokemonList[0],Trainer.PokemonList[switchPk] = Trainer.PokemonList[switchPk],Trainer.PokemonList[0]

            print(Trainer.PokemonList[0].Name+" is now your active Pokemon!\n\n")
            askInput("","\nPress Enter to continue...")
            os.system("cls")

        else:
            self.back=True

    def update(self,choices,**fighters):
        if self.back:
            self.back=False
            return next(st for st in choices if st.name=="Combat Menu")
        else:
            return next(st for st in choices if st.name=="Enemy Turn")


#################################################################################
#                        USE ITEM
# #################################################################################        

class UseItem(State):
    def __init__(self,name):
        super().__init__(name)
        self.back=False
        self.backSelf=False
        self.caught=False

    def run(self,**fighters):
        Trainer=fighters["Trainer"]
        enemyPk=fighters["enemyPk"]

        availItems=[it for it in range(len(Trainer.Items)) if Trainer.Items[it].getNumIt()>0]
        btm=max(availItems)+1
        msg=("Choose an item to use among the available ones:\n\n"+
                Trainer.showItems(availItems)+
                "\n"+str(btm)+": Back to Menu")
        errmsg=["You must insert a number","You can only choose between the provided options"]
        itmsel=inputLoop("int",msg,errmsg,availItems+[btm])
        os.system("cls")

        if not itmsel==btm:
            itm=Trainer.Items[itmsel]
            itm.decIt(1)
            
            match itm.name:
                #Pokeball case
                case 'Pokeball':
                    catchProb=1-enemyPk.showHP()/enemyPk.baseStats.getMaxHP()
                    if catchProb>random.random():
                        print("You successfully captured "+enemyPk.Name+"!!\n")
                        Trainer.addPokemon(enemyPk)
                        self.caught=True
                    else:
                        print("Oh no "+enemyPk.Name+" escaped from the Pokeball!!\n")
                    
                # Helath Potion case
                case 'Health Potion':
                    availPk=[pk for pk in range(len(Trainer.PokemonList)) if not Trainer.PokemonList[pk].isKO()]
                    btIm=max(availPk)+1
                    msg=("On which Pokemon would you like to use the Potion?:\n\n"+
                        Trainer.showPokemons(availPk)+
                        "\n"+str(btIm)+": Back to Item Selection")
                    #ask user the target Pokemon
                    targetpk=inputLoop("int",msg,errmsg,availPk+[btIm])
                    os.system("cls")

                    if not targetpk==btIm:
                        Trainer.PokemonList[targetpk].heal(20)
                        print(Trainer.PokemonList[targetpk].Name+" recovers 20 HP!!\n")
                    else:
                        self.backSelf=True
            askInput("","\nPress Enter to continue...")
            os.system("cls")
        else:
            self.back=True
        
    def update(self,choices,**fighters):
        if self.back:
            self.back=False
            return next(st for st in choices if st.name=="Combat Menu")
        elif self.backSelf:
            self.backSelf=False
            return next(st for st in choices if st.name=="Use Item")
        elif self.caught:
            self.caught=False
            return next(st for st in choices if st.name=="Caught")
        else:
            return next(st for st in choices if st.name=="Enemy Turn")


########################################################################
#                       FLEE
########################################################################

class Flee(State):
    def __init__(self,name):
        super().__init__(name)
        self.back=False
        self.escapeFail=False
    
    def run(self,**fighters):
        msg="Do you really want to run away? (y/n)"
        errmsg=["you can only answer answer y (=yes) or n (=no)",
                "you can only answer answer y (=yes) or n (=no)"]
        yn=inputLoop("str",msg,errmsg,["y","n"])
        os.system("cls")
        if yn=="n":
            self.back=True
        else:
            runawayProb=0.6
            if(runawayProb>random.random()):
                pass
            
            else:
                print("You were not able to escape!!")
                self.escapeFail=True
                askInput("","Press Enter to continue...")
                os.system("cls") 
               

                
    def update(self,choices,**fighters):
        if self.back:
            self.back=False
            return next(st for st in choices if st.name=="Combat Menu")
        elif self.escapeFail:
            self.escapeFail=False
            return next(st for st in choices if st.name=="Enemy Turn")
        
        return next(st for st in choices if st.name=="Escaped")
        


#################################################################################
#                          ENEMY TURN                                           #
#################################################################################

class EnemyTurn(State):
    def __init__(self,name,**tstargs):
        super().__init__(name)
        self.testMode=False
        if tstargs:
            self.testMode=tstargs["testMode"]

    def run(self,**fighters):
        Trainer=fighters["Trainer"]
        enemyPk=fighters["enemyPk"]

        if(not self.testMode):
            print("Enemy turn /!\\ \n\n")
            askInput("","Press Enter to continue:")
            os.system("cls")
    
        #randomly selected move from available ones (PP>0)
        availMoves=enemyPk.availMoves()
        if(availMoves):
            mv=random.choice(availMoves)
       
            if(not self.testMode):
                print(enemyPk.Name+" uses "+enemyPk.moves[mv].name)

            #attack success check
            if enemyPk.useMove(mv,Trainer.PokemonList[0]):
                if(not self.testMode):
                    print("attack succeded!! \n\n")
                    print("enemy HP: "+str(enemyPk.showHP())+"\n\n")
                    print("your Pokemon HP: "+str(Trainer.PokemonList[0].showHP()))
            else:
                if(not self.testMode):
                    print("attack missed")
            if(not self.testMode):
                askInput("","\nPress Enter to continue:")
                os.system("cls")
        elif self.testMode:
            for mv in  enemyPk.moves:
                mv.restorePP()
        else:
            pass
    
    def update(self,choices,**fighters):
    
        Trainer=fighters["Trainer"]
        enemyPk=fighters["enemyPk"]
        
        if enemyPk.isKO():
            return next(st for st in choices if st.name=="Victory")
        if(not Trainer.hasPokemons()):
            return next(st for st in choices if st.name=="Defeat")
        if(not self.testMode):
            if(Trainer.PokemonList[0].isKO() and Trainer.hasPokemons()):
                return next(st for st in choices if st.name=="Change Pokemon")
            
        return next(st for st in choices if st.name=="Combat Menu")
    

#####################################################################################
#                       TEST
#####################################################################################

class TestCbt(State):

    def run(self,**fighters):
        Trainer=fighters["Trainer"]
        enemyPk=fighters["enemyPk"]

        availMoves=Trainer.PokemonList[0].availMoves()
        if availMoves:
            mv=random.choice(availMoves)
  
            Trainer.PokemonList[0].useMove(mv,enemyPk)
        else:
            for mv in  Trainer.PokemonList[0].moves:
                mv.restorePP()

    def update(self,choices,**fighters):
        
        Trainer=fighters["Trainer"]
        enemyPk=fighters["enemyPk"]

        if enemyPk.isKO():
            return next(st for st in choices if st.name=="Victory")
        if(not Trainer.hasPokemons()):
            return next(st for st in choices if st.name=="Defeat")
        return next(st for st in choices if st.name=="Enemy Turn")