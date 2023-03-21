import askInput
class Trainer:
    def __init__(self,name):
        self.name=name
        self.MaxPokemons=6
        self.PokemonList=[]
        self.Items=[]


    #returns a string to display the current Pokemons owned
    def PokeDisp(self):
        PkDisp=""
        for i in range(len(self.PokemonList)):
            PkDisp=PkDisp+str(i)+": "+str(self.PokemonList[i]+"\n")
        
        return PkDisp
    
    #Returns true if the trainer has available pokemons i.e. pokemon not KO
    def hasPokemons(self):
        
        for i in range(len(self.PokemonList)):
            if(not self.PokemonList[i].isKO()):
                return True
        return False
        
    #adds a Pokemon to current move list, if the Trainer already has 6 Pokemons, the user is asked to choose which one to free
    def addPokemon(self,Pokemon):
        
        self.PokemonList.append(Pokemon)
        #max number of Pokemons check
        if len(self.PokemonList)>self.MaxPokemons:
            #request user which Pokemon to drop 
            drop=askInput("int","choose a Pokemon to set free:\n"+self.PokeDisp(),[1,2,3,4,5])
            self.dropMove(drop-1)
    

    #removes the Pokemon in position "drop" from Pokemon list 
    def dropPokemon(self,drop):
        self.PokemonList.pop(drop)

    