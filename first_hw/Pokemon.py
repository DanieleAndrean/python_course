import copy
import askInput
import random
import math

class baseStats:
    def __init__(self,bsDict):
        self.hp=bsDict["hp"]
        self.attack=bsDict["attack"]
        self.defense=bsDict["defense"]
        self.speed=bsDict["speed"]
        self.special=bsDict["special"]

    def update(self,hp,attack,defense,speed,special):
        self.hp=hp
        self.attack=attack
        self.defense=defense
        self.speed=speed
        self.special=special


#################################################
############### MOVE CLASS ###################
#################################################

class Move:
    def __init__(self,moveDict):
        self.name=moveDict["name"]
        self.type=moveDict["type"]
        self.category=moveDict["category"]
        self.power=moveDict["power"]
        self.accuracy=moveDict["accuracy"]
        self.pp=moveDict["pp"]

    def decPP(self):
        self.pp-=1

    def getPP(self):
        return copy.deepcopy(self.pp)
    
    def __str__(self):
        movestr=self.name+"  type:"+self.type+"  power:"+str(self.power)+"\n"
        return movestr
    

#################################################
############### POKEMON CLASS ###################
#################################################
class Pokemon:
    def __init__(self,PokeDict,moves):
        self.Level=1
        self.Name=PokeDict["name"]
        self.MaxMoves=4
        self.Types=PokeDict["types"]
        self.baseStats=baseStats(PokeDict["baseStats"])
        self.moves=[]
        for i in range(len(moves)):
            self.moves.append(Move(moves[i]))
        self.currentHP=self.baseStats.hp
        self.Pokedex=PokeDict["national_pokedex_number"]
        self.KO=False

    def __str__(self):
        typ=""
        for i in range(len(self.Types)):
            typ=typ+self.Types[i]+" "
        Pokestr=self.Name+"\t lv: "+str(self.Level)+"\t  type: "+typ+"\n"
        return Pokestr
    
    #tells if Pokemon is KO
    def isKO(self):
        return copy.deepcopy(self.KO)
    
    #returns a copy of the current HP
    def showHP(self):
        return copy.deepcopy(self.currentHP)    
    
    #returns a string to display the current moves
    def movesDisp(self,PPonly):
        if not PPonly:
            mvDisp=""
            for i in range(len(self.moves)):
                mvDisp=mvDisp+str(i+1)+": "+str(self.moves[i])+"\n"
            
            return mvDisp
        else:
            mvDisp=""
            for i in range(len(self.moves)):
                if self.moves[i].getPP()>0:
                    mvDisp=mvDisp+str(i+1)+": "+str(self.moves[i])+"\n"
            if mvDisp=="":
                raise Exception("No available moves")
            return mvDisp
    
    #adds a move to current move list, if the Pokemon already knows 4 moves, the user is asked to choose which one to forget
    def addMove(self,move):
        
        self.moves.append(move)
        #max number of moves check
        if len(self.moves)>self.MaxMoves:
            #request user which move to drop
            errmsg=["You must provide a number","You must choose a value among the specified ones"]
            msg="choose a move to forget:\n"+self.movesDisp()
            drop=askInput.inputLoop("int",msg,errmsg,[1,2,3,4,5])-1
            self.dropMove(drop)
    
    #removes the move in position "drop" from moves list 
    def dropMove(self,drop):
        self.moves.pop(drop)


    #decrease current HP by the specified amount
    def decHP(self,HPloss):
        if self.currentHP>HPloss:
            self.currentHP-=HPloss
        else:
            self.currentHP=0
            self.KO=True

    #uses the selected move and resolves it effects
    def useMove(self,mv,target):
        selMove=self.moves[mv]
        selMove.decPP()

        succProb=random.random()
        #dmg computation
        if selMove.accuracy>succProb:
            if selMove.category=="physical":
                atk=self.baseStats.attack
                dfn=target.baseStats.defense
            else:
                atk=self.baseStats.special
                dfn=target.baseStats.special

            #stability modifier calculation
            if selMove.type in self.Types:
                stability=1.5
            else:
                stability=1
        
            effect=1
            #critical modifier calculation
            if random.random()<self.baseStats.speed/512:
                critical=2
            else:
                critical=1
            
            luck=0.85+(0.15)*random.random()
            modif=stability*effect*critical*luck
            dmg=math.floor((((2*self.Level+10)/250)*(atk/dfn)*selMove.power+2)*modif)
            #apply damage
            target.decHP(dmg)

            return True #attack succeded
        
        else:
            return False #attack missed




