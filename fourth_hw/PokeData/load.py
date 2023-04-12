import json
import os
import pandas as pd

datapath=os.path.dirname(__file__)
PkDF = pd.DataFrame()
MvsDF=pd.DataFrame()
TypEffDF=pd.DataFrame()
with open(datapath+"\pokemons.json", 'r') as pkfile: # open the file containing the data
    for line in pkfile:
        p = json.loads(line) # convert each json line into a dictionary
        PkDF.concat(p)

with open(datapath+"\moves.json","r") as mvFile:
    for line in mvFile:
        m=json.loads(line)
        if (not m["power"]==None and not m["accuracy"]==None and not m["pp"]==None):
            MvsDF.concat(m)
        else:
            pass


with open(datapath+"\\type_effectiveness.json","r") as teFile:
    for line in teFile:
        te=json.loads(line)
        TypEffDF.concat(te)
