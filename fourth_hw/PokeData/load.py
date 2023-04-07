import json
import os

datapath=os.path.dirname(__file__)
PkList = []
MvsList=[]
TypEffList=[]
with open(datapath+"\pokemons.json", 'r') as pkfile: # open the file containing the data
    for line in pkfile:
        p = json.loads(line) # convert each json line into a dictionary
        PkList.append(p)

with open(datapath+"\moves.json","r") as mvFile:
    for line in mvFile:
        m=json.loads(line)
        MvsList.append(m)

MvList=[mv for mv in MvsList if (not mv["power"]==None and not mv["accuracy"]==None and not mv["pp"]==None)]


with open(datapath+"\\type_effectiveness.json","r") as teFile:
    for line in teFile:
        te=json.loads(line)
        TypEffList.append(te)