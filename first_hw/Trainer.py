import askInput
import os
class Trainer:
    def __init__(self,name):
        self.name=name
        self.MaxPokemons=6
        self.PokemonList=[]
        self.Items=[]


    #returns a string to display the current Pokemons owned
    def PokeDisp(self,*sel):
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
    
    
    #Returns true if the trainer has available pokemons i.e. pokemon not KO
    def hasPokemons(self):
        
        for i in self.PokemonList:
            if(not i.isKO()):
                return True
        return False
        
    #adds a Pokemon to current move list, if the Trainer already has 6 Pokemons, the user is asked to choose which one to free
    def addPokemon(self,Pokemon):
        
        self.PokemonList.append(Pokemon)
        #max number of Pokemons check
        if len(self.PokemonList)>self.MaxPokemons:
            #request user which Pokemon to drop 
            askInput.askInput("","you are trying to catch a new Pokemon but you must free one.\nPress Enter to continue:")
            os.system("cls")
            errmsg=["You must provide a number","You must choose a value among the specified ones"]
            msg="choose a Pokemon to free:\n"+self.PokeDisp()
            drop=askInput.inputLoop("int",msg,errmsg,[0,1,2,3,4,5,6])
            self.dropPokemon(drop)
    

    #removes the Pokemon in position "drop" from Pokemon list 
    def dropPokemon(self,drop):
        self.PokemonList.pop(drop)

    