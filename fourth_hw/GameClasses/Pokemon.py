import copy
import numpy as np
import UserInput
import random
import math
import os
from PokeData.load import TypEffDF
from to1D import to_1D
import pandas as pd
########################################################
#               STATS CLASSES
######################################################
class baseStats:
    def __init__(self,bsSeries):
        bsDict=to_1D(bsSeries)
        self.hp=bsDict["hp"].values[0]
        self.attack=bsDict["attack"].values[0]
        self.defense=bsDict["defense"].values[0]
        self.speed=bsDict["speed"].values[0]
        self.special=bsDict["special"].values[0]

    def update(self,hp,attack,defense,speed,special):
        self.hp=hp
        self.attack=attack
        self.defense=defense
        self.speed=speed
        self.special=special

    def getMaxHP(self):
        return copy.deepcopy(self.hp)
    def getAtk(self):
        return copy.deepcopy(self.attack)
    def getDef(self):
        return copy.deepcopy(self.defense)
    def getSpc(self):
        return copy.deepcopy(self.special)
    def getSpd(self):
        return copy.deepcopy(self.speed)
    

class actualStats(baseStats):

    def __init__(self,bStats,lvl):
        self.hp=math.floor(bStats.getMaxHP()*2*lvl/100)+lvl+10
        self.attack=math.floor(bStats.getAtk()*2*lvl/100)+5
        self.defense=math.floor(bStats.getDef()*2*lvl/100)+5
        self.speed=math.floor(bStats.getSpd()*2*lvl/100)+5
        self.special=math.floor(bStats.getSpc()*2*lvl/100)+5

    def update(self,lvl,bStats):
        self.hp=math.floor(bStats.getMaxHP()*2*lvl/100)+lvl+10
        self.attack=math.floor(bStats.getAtk()*2*lvl/100)+5
        self.defense=math.floor(bStats.getDef()*2*lvl/100)+5
        self.speed=math.floor(bStats.getSpd()*2*lvl/100)+5
        self.special=math.floor(bStats.getSpc()*2*lvl/100)+5
    
    
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
        self.maxPP=moveDict["pp"]
        self.pp=self.maxPP

    def decPP(self):
        self.pp-=1

    def restorePP(self,*numPP):
        #if numPP is not empty
        if numPP:
            self.pp+=numPP[0]
            if self.pp>self.maxPP:
                self.pp=self.maxPP
        else:
            self.pp=self.maxPP
        
    def getPP(self):
        return copy.deepcopy(self.pp)
    
    def __str__(self):
        movestr=self.name+"  type:"+self.type+"  power:"+str(self.power)+"\n"
        return movestr
    

#################################################
############### POKEMON CLASS ###################
#################################################
class Pokemon:
    def __init__(self,PokeDict,moves,lvl):
        self.Level=lvl
        self.Name=PokeDict["name"]
        self.MaxMoves=4
        self.Types=to_1D(PokeDict["types"]).values.tolist()[0]
        self.baseStats=baseStats(PokeDict["baseStats"])
        self.actualStats=actualStats(self.baseStats,self.Level)
        self.moves=[]
        for idx, m in moves.iterrows():
            self.moves.append(Move(m))
        self.currentHP=self.actualStats.getMaxHP()
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
    def showHP(self,*maxFlag):
        if maxFlag:
            if maxFlag[0]=="max":
                return self.actualStats.getMaxHP()
        return copy.deepcopy(self.currentHP)    
    
    #Updates stats based on new level
    def lvlUp(self,lvl):
        self.actualStats.update(lvl,self.baseStats)
    #returns a string to display the current moves
    def movesDisp(self,*sel):
        if len(sel)==0: #display all
            mvDisp=""
            for i in range(len(self.moves)):
                mvDisp=mvDisp+str(i)+": "+str(self.moves[i])+"  PP: "+str(self.moves[i].getPP())+"\n"
            
            return mvDisp
        else: #display selected
            idxs=sel[0]
            mvDisp=""
            for i in range(len(idxs)):
                    mvDisp=mvDisp+str(idxs[i])+": "+str(self.moves[idxs[i]])+"  PP: "+str(self.moves[idxs[i]].getPP())+"\n"
            if mvDisp=="":
                raise Exception("No available moves")
            return mvDisp
    

    #returns a list of indexes with available moves only
    def availMoves(self):
        idxs=[]
        for i in range(len(self.moves)):
            if(self.moves[i].getPP()>0):
                idxs.append(i)
        return idxs


    #adds a move to current move list, if the Pokemon already knows 4 moves, the user is asked to choose which one to forget
    def addMove(self,mv):
        
        self.moves.append(Move(mv))
        #max number of moves check
        if len(self.moves)>self.MaxMoves:
            #request user which move to drop
            UserInput.askInput("",self.Name+" is trying to learn a new move but it must forget one.\n Press Enter to continue")
            os.system("cls")
            errmsg=["You must provide a number","You must choose a value among the specified ones"]
            msg="choose a move to forget:\n"+self.movesDisp()
            drop=UserInput.inputLoop("int",msg,errmsg,[0,1,2,3,4])
            self.dropMove(drop)
    
    #removes the move in position "drop" from moves list 
    def dropMove(self,drop):
        self.moves.pop(drop)


    #decrease current HP by the specified amount
    def decHP(self,HPloss):
      
        self.currentHP-=HPloss
        if self.currentHP<=0:
            self.currentHP=0
            self.KO=True

    def heal(self,*quantity):
        #if quantity is not empty
        if quantity:
            self.currentHP+=quantity[0]
            if self.currentHP>self.actualStats.getMaxHP():
                self.currentHP=self.actualStats.getMaxHP()
        else:
            self.currentHP=self.actualStats.getMaxHP()
            self.KO=False
            

    #uses the selected move and resolves it effects
    def useMove(self,mv,target):
        selMove=self.moves[mv]
        selMove.decPP()

        succProb=random.random()
        #dmg computation
        if selMove.accuracy>succProb:
            if selMove.category=="physical":
                atk=self.actualStats.getAtk()
                dfn=target.actualStats.getDef()
            else:
                atk=self.actualStats.getSpc()
                dfn=target.actualStats.getSpc()

            #stability modifier calculation
            if selMove.type in self.Types:
                stability=1.5
            else:
                stability=1

            eff=TypEffDF[(TypEffDF["attack"]==selMove.type) & (TypEffDF["defend"].isin(target.Types))]
            eff=pd.concat([eff,pd.DataFrame([{"effectiveness":1,"attack":"default","defend":"default"}])])
            effect=np.prod(eff["effectiveness"].values[0])
            #critical modifier calculation
            if random.random()<self.actualStats.getSpd()/512:
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




