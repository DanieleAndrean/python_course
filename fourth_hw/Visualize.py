import pandas as pd
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from tqdm import tqdm
from PokeData.load import PkDF,MvDF
def main():
    path=os.path.dirname(os.path.abspath(__file__))
    BattlesDF=pd.read_csv(path+"\\Battles.csv")
     # Battle # Exitcond # NTurns # PercHP # Pokemon # PokemonLvl # EnemyPk # EnemyLvl # NGame
    TurnsDF=pd.read_csv(path+"\\Turns.csv")
    # Battle # Turn # Move # CurrHP # Damage # NGame
    turns=TurnsDF["Turn"].unique()
    battles=TurnsDF["Battle"].unique()
    games = TurnsDF["NGame"].unique()
    HpTurn=np.empty((len(games),len(battles),len(turns)))
    HpTurn.fill(np.nan)
    HpRed=np.empty((len(games),len(battles),len(turns)-1))
    HpRed.fill(np.nan)
    DmgTurn=np.empty((len(games),len(battles),len(turns)))
    DmgTurn.fill(np.nan)
    TurnsDict=TurnsDF.to_dict("records")
    
    BuGames=BattlesDF.loc[BattlesDF["Pokemon"]=="bulbasaur","NGame"].unique()
    ChGames=BattlesDF.loc[BattlesDF["Pokemon"]=="charmander","NGame"].unique()
    

    BuMovesLs=[]
    ChMovesLs=[]
    SqMovesLs=[]

    mvKeys=('Move', 'Damage')
    for row in tqdm(TurnsDict):
        t=row["Turn"]/2
        HpTurn[row["NGame"],row["Battle"],int(t)]=row["CurrHP"]
        DmgTurn[row["NGame"],row["Battle"],int(t)]=row["Damage"]
        if row["NGame"] in BuGames:
            BuMovesLs.append({k: row[k] for k in mvKeys})
        elif row["NGame"] in ChGames:
            ChMovesLs.append({k: row[k] for k in mvKeys})
        else:
            SqMovesLs.append({k: row[k] for k in mvKeys})

###############################################################################################################
#                                   PERCENTAGE OF HP LOST AT EACH TURN
##########################################################################################################
    
    for gg in tqdm(games):
        for bt in battles:

            currT=HpTurn[gg,bt,~np.isnan(HpTurn[gg,bt,:])]
            if len(currT)>1:
                HpRed[gg,bt,0]=(currT[0]-currT[1])/currT[0]*100
                for tt in range(1,len(currT)-1):
                        HpRed[gg,bt,tt]=(currT[tt]-currT[tt+1])/currT[0]*100
            else:
                 HpRed[gg,bt,0]=100

    avgLoss=np.empty(len(turns)-1)
    sdLoss=np.empty(avgLoss.shape)
    for tt in range(len(avgLoss)):
        avgLoss[tt]=np.nanmean(HpRed[:,:,tt])
        sdLoss[tt]=np.sqrt(np.nanvar(HpRed[:,:,tt]))

    fig1,hpax=plt.subplots()
    hpax.errorbar(turns[1:],avgLoss, yerr=sdLoss, fmt="o")
    hpax.set_xlabel("Turn")
    hpax.set_ylabel("Percentage HP reduction")
    hpax.set_title("Average percentage of HP lost at each battle turn")
    
###############################################################################################################
#                     DAMAGE DONE BY EACH POKEMON AND POKEMON TYPES DISTRIBUTION
##########################################################################################################
    BuMovesDF=pd.DataFrame(BuMovesLs)
    ChMovesDF=pd.DataFrame(ChMovesLs)
    SqMovesDF=pd.DataFrame(SqMovesLs)

    BuMoves=BuMovesDF["Move"].value_counts()   
    ChMoves=ChMovesDF["Move"].value_counts()
    SqMoves=SqMovesDF["Move"].value_counts()

    BattlesDict=BattlesDF.to_dict("records")
    PkDict=PkDF.to_dict("records")
    EncTypesList=[]
    EneTypes=[]

    for row in tqdm(BattlesDict):
        EncTypesList.extend(next(rr["types"] for rr in PkDict if rr["name"]==row["EnemyPk"]))
        EneTypes.append(next(rr["types"] for rr in PkDict if rr["name"]==row["EnemyPk"]))
        
    JsTypesList=[]
    for row in PkDict:
        JsTypesList.extend(row["types"])

    JsTypes=pd.DataFrame(JsTypesList).value_counts().to_dict()
    EncTypes=pd.DataFrame(EncTypesList).value_counts().to_dict()

    fig2,paxBu=plt.subplots()
    paxBu.pie(BuMoves,labels=BuMoves.index,autopct="%1.1f%%",rotatelabels=True,pctdistance=0.95, textprops={'fontsize': 7})
    paxBu.set_title("Percentage of damage done by Bulbasaur moves")
    fig3,paxCh=plt.subplots()
    paxCh.pie(ChMoves,labels=ChMoves.index,autopct="%1.1f%%",rotatelabels=True,pctdistance=0.95, textprops={'fontsize': 7})
    paxCh.set_title("Percentage of damage done by Charmander moves")
    fig4,paxSq=plt.subplots()
    paxSq.pie(SqMoves,labels=SqMoves.index,autopct="%1.1f%%",rotatelabels=True,pctdistance=0.95,  textprops={'fontsize': 7})
    paxSq.set_title("Percentage of damage done by Squirtle moves")
    
    fig5,(daxJs,daxEn)=plt.subplots(1,2)
    daxJs.barh([it[0] for it in JsTypes.keys()],[it for it in JsTypes.values()])
    daxEn.barh([it[0] for it in EncTypes.keys()],[it for it in EncTypes.values()])
    daxJs.set_title("Json file")
    daxJs.set_xlabel("Occurrencies")
    daxJs.set_ylabel("Types")
    daxEn.set_title("Encountered Pokemons")
    daxEn.set_xlabel("Occurrencies")
    daxEn.set_ylabel("Types")
    fig5.suptitle("Pokemon Types Distribution in Json File and Encountered Pokemons")



###############################################################################
#                           AVG DAMAGE PER STARTER POKEMON
##############################################################################
    avgDmg=np.empty(len(games))
    Pkmn=[]
    PkmnLvl=[]
    for gg in tqdm(games):
        totdmg=np.nansum(DmgTurn[gg,:,:],axis=1)
        avgDmg[gg]=np.nanmean(totdmg)
        Pkmn.extend(BattlesDF.loc[((BattlesDF["NGame"]==gg) & (BattlesDF["Battle"]==0)),"Pokemon"].values)
        PkmnLvl.extend(BattlesDF.loc[((BattlesDF["NGame"]==gg) & (BattlesDF["Battle"]==0)),"PokemonLvl"].values)

    
    PkDmg=pd.DataFrame({"Pokemon":Pkmn,
                        "PokemonLvl":PkmnLvl,
                        "AvgDmg":avgDmg})
    
    fig6,axDm=plt.subplots()
    wdt=0.2
    axDm.bar(PkDmg.loc[PkDmg["Pokemon"]=="bulbasaur","PokemonLvl"]-wdt,
             PkDmg.loc[PkDmg["Pokemon"]=="bulbasaur","AvgDmg"], width=wdt,color="g")
    axDm.bar(PkDmg.loc[PkDmg["Pokemon"]=="charmander","PokemonLvl"],
             PkDmg.loc[PkDmg["Pokemon"]=="charmander","AvgDmg"], width=wdt,color="r")
    axDm.bar(PkDmg.loc[PkDmg["Pokemon"]=="squirtle","PokemonLvl"]+wdt,
             PkDmg.loc[PkDmg["Pokemon"]=="squirtle","AvgDmg"], width=wdt,color="b")
    axDm.set_title("Average Damage per Level")
    axDm.set_xlabel("Level")
    axDm.set_ylabel("Average damage across all battles")
    axDm.legend(["bulbasaur","charmander","squirtle"])



###############################################################################
#                           PERCENTAGE WIN PER ENEMY TYPE ANDLEVEL
##############################################################################
    
    ResTypLvl=pd.DataFrame({"Result":BattlesDF["Exitcond"].values.tolist(),
                            "Type":[tuple(x) for x in EneTypes],
                            "Level":BattlesDF["EnemyLvl"].values.tolist()})
   
    
    battTypLvl=ResTypLvl.value_counts(["Type","Level"]).to_frame()
    battTypLvl["Type"]=[x[0] for x in battTypLvl.index]
    battTypLvl["Level"]=[x[1] for x in battTypLvl.index]
    WinTypLvl=ResTypLvl.loc[ResTypLvl["Result"]=="Vct",["Type","Level"]].value_counts().to_frame()
    WinTypLvl["Type"]=[x[0] for x in WinTypLvl.index]
    WinTypLvl["Level"]=[x[1] for x in WinTypLvl.index]

    perWin=np.empty((len(battTypLvl["Type"].unique()),len(battTypLvl["Level"].unique())))
    perWin.fill(np.nan)
    typs=battTypLvl["Type"].unique()
    btTLdict=battTypLvl.to_dict("records")
    WTLdict=WinTypLvl.to_dict("records")
    
    for row in btTLdict:
        currval=[rr["count"] for rr in WTLdict if((rr["Level"]==row["Level"]) and (rr["Type"]==row["Type"]))]
        pos=next(idx for idx in range(len(typs)) if typs[idx]==row["Type"])
        if currval:
            perWin[pos,row["Level"]-1]=currval[0]/row["count"]*100
        else:
            perWin[pos,row["Level"]-1]=0
        
    
    fig7,axIm=plt.subplots()
    axIm = sns.heatmap(perWin, yticklabels=typs, xticklabels=range(1,20))
    axIm.set_title("Percentage of Vicories for each type and level of enemy Pokemon")
    axIm.set_xlabel("Level")
    plt.show()


if __name__=="__main__":
    main()