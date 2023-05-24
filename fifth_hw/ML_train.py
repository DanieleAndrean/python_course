import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestClassifier
from PokeData.load import PkDF
from tqdm import tqdm
import os


def Nprimes(n):
    primes=[2]
    i=3
    while(len(primes)<n):
        isPrime=True
        for j in primes:
            if i % j==0:
                isPrime=False
        if isPrime:
            primes.append(i)
        i+=1
    return primes

def main():

    types=PkDF["types"].values.tolist()
    singTyp=[]
    for el in types:
        singTyp.extend(el)
    singTyp=set(singTyp)    
    ntyp=len(singTyp)

    typeNum=dict(zip(singTyp,Nprimes(ntyp)))


    path=os.path.dirname(os.path.abspath(__file__))
    data=pd.read_csv(path+"\\Battles.csv",converters={"PkTyp": lambda x: x.strip("[]").replace("'","").split(", "),
                                                      "EnTyp": lambda x: x.strip("[]").replace("'","").split(", ")})
    print(data)
    features=["PkTyp","PkHP","PkAttack","PkDefense","PkSpecial","PkSpeed","EnTyp","EnHP",
              "EnAttack","EnDefense","EnSpecial","EnSpeed"]
    target=["Result"]

    dataTyp=data[["PkTyp","EnTyp"]].to_dict("records")

    for row in tqdm(dataTyp):
        pkCod=[typeNum[typ] for typ in row["PkTyp"]]
        enCod=[typeNum[typ] for typ in row["EnTyp"]]
        row["PkTyp"]=np.prod(pkCod)
        row["EnTyp"]=np.prod(enCod)

    data[["PkTyp","EnTyp"]]=pd.DataFrame(dataTyp)

    FeatTrn,FeatTst,TargTrn,TargTst = train_test_split(data[features],data[target],test_size = 0.30)
    
    logit=LogisticRegression(solver="newton-cholesky").fit(FeatTrn,TargTrn)
    rndFor=RandomForestClassifier(n_estimators=500, max_depth=10).fit(FeatTrn,TargTrn.values)
    predlog=logit.predict(FeatTst)
    predfor=rndFor.predict(FeatTst)
    
    logcm=confusion_matrix(TargTst.values,predlog,labels=["Vct","Def"])
    logdisp = ConfusionMatrixDisplay(confusion_matrix = logcm)
    logdisp.plot()
    forcm=confusion_matrix(TargTst.values,predfor,labels=["Vct","Def"])
    fordisp = ConfusionMatrixDisplay(confusion_matrix = forcm)
    fordisp.plot()

    plt.show()

if __name__=="__main__":
    main()



            