import UserInput
import os
import copy

class Item:
    def __init__(self,itDict,quantity):
        self.name=itDict["name"]
        self.quantity=quantity
        self.maxNum=itDict["maxNum"]
    
    def __str__(self):

        itstr="Item:\t"+self.name+"\tQuantity:\t"+str(self.quantity)
        return itstr
    #increases the Item quantity by the specified number
    def restore(self,*numOb):
        #if numOb is not empty
        if numOb:
            self.quantity+=numOb[0]
            if self.quantity>self.maxNum:
                self.quantity=self.maxNum
        else:
            self.quantity=self.maxNum
            
    
    #decreases the Item quantity by the specified number
    def decIt(self,numOb):

        self.quantity-=numOb
    
    #returns the Item's quantity
    def getNumIt(self):

        return copy.deepcopy(self.quantity)
    
#######################################################################################
################### TRAINER CLASS #####################################################
#######################################################################################
class Trainer:
    def __init__(self,name,Pokemons,Items):
        self.name=name
        self.MaxPokemons=6
        self.PokemonList=Pokemons
        self.Items=Items


    #returns a string to display the current Pokemons owned
    def showPokemons(self,*sel):
        if len(sel)==0: #display all
            pkDisp=""
            for i in range(len(self.PokemonList)):
                pkDisp=pkDisp+str(i)+": "+str(self.PokemonList[i])+"\n"
            
            return pkDisp
        else: #display selected
            idxs=sel[0]
            pkDisp=""
            for i in range(len(idxs)):
                    pkDisp=pkDisp+str(idxs[i])+": "+str(self.PokemonList[idxs[i]])+"\n"
            if pkDisp=="":
                raise Exception("No available Pokemons")
            return pkDisp
    
    def showItems(self,*sel):
        if len(sel)==0: #display all
            itDisp=""
            for i in range(len(self.Items)):
                itDisp=itDisp+str(i)+": "+str(self.Items[i])+"\n"
            
            return itDisp
        
        else: #display selected
            idxs=sel[0]
            itDisp=""
            for i in range(len(idxs)):
                    itDisp=itDisp+str(idxs[i])+": "+str(self.Items[idxs[i]])+"\n"
            if itDisp=="":
                raise Exception("No available Pokemons")
            return itDisp
    
    #Returns true if the trainer has available pokemons i.e. pokemon not KO
    def hasPokemons(self):
        
        for i in self.PokemonList:
            if not i.isKO():
                return True
        return False
        
    #adds a Pokemon to current move list, if the Trainer already has 6 Pokemons, the user is asked to choose which one to free
    def addPokemon(self,Pokemon):
        
        self.PokemonList.append(Pokemon)
        #max number of Pokemons check
        if len(self.PokemonList)>self.MaxPokemons:
            #request user which Pokemon to drop 
            UserInput.askInput("","you are trying to catch a new Pokemon but you must free one.\nPress Enter to continue:")
            os.system("cls")
            errmsg=["You must provide a number","You must choose a value among the specified ones"]
            msg="Choose a Pokemon to release:\n"+self.showPokemons()
            drop=UserInput.inputLoop("int",msg,errmsg,[0,1,2,3,4,5,6])
            self.dropPokemon(drop)
    

    #removes the Pokemon in position "drop" from Pokemon list 
    def dropPokemon(self,drop):
        self.PokemonList.pop(drop)

    def addItem(self,Item):

        self.Items.append(Item)

    def dropItem(self,Itemidx):

        self.Items.pop[Itemidx]
    