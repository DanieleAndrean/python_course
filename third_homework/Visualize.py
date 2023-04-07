import numpy as np
import matplotlib.pyplot as mpl
import pickle


def Visualize():

    with open("BulbasaurRes","rb") as Fin:
        BulbasaurRes=pickle.load(Fin)
    
    with open("CharmanderRes","rb") as Fin:
        CharmanderRes=pickle.load(Fin)
    
    with open("SquirtleRes","rb") as Fin:
        SquirtleRes=pickle.load(Fin)

    nSim=len(BulbasaurRes)
    Nbattles=len(BulbasaurRes[0].battles)
    
    BulbasaurVct=np.zeros((nSim,1),dtype=int)
    BulbasaurTurn=np.zeros((nSim,Nbattles),dtype=int)
    BulbasaurPHP=np.zeros((nSim,Nbattles),dtype=float)
    BulbasaurEneWin=dict()
    
    CharmanderVct=np.zeros((nSim,1),dtype=int)
    CharmanderTurn=np.zeros((nSim,Nbattles),dtype=int)
    CharmanderPHP=np.zeros((nSim,Nbattles),dtype=float)
    CharmanderEneWin=dict()
    
    SquirtleVct=np.zeros((nSim,1),dtype=int)
    SquirtleTurn=np.zeros((nSim,Nbattles),dtype=int)
    SquirtlePHP=np.zeros((nSim,Nbattles),dtype=float)
    SquirtleEneWin=dict()


    for i in range(nSim):
       
       j=0
       for b in BulbasaurRes[i].battles:
            php=b["percHP"]
            vct=(1 if b["exitcond"]=="Vct" else 0)
            try:
                BulbasaurEneWin[b["enemyPk"]].append((vct,php,b["nTurns"]))
            except KeyError:
                BulbasaurEneWin[b["enemyPk"]] = [(vct,php,b["nTurns"])]
            BulbasaurVct[i]+=vct
            BulbasaurTurn[i,j]=b["nTurns"]
            BulbasaurPHP[i,j]=php
            j+=1
           
       j=0
       for c in CharmanderRes[i].battles:
            php=c["percHP"]
            vct=(1 if c["exitcond"]=="Vct" else 0)
            try:
                CharmanderEneWin[c["enemyPk"]].append((vct,php,b["nTurns"]))
            except KeyError:
                CharmanderEneWin[c["enemyPk"]] = [(vct,php,b["nTurns"])]
            CharmanderVct[i]+=vct
            CharmanderTurn[i,j]=c["nTurns"]
            CharmanderPHP[i,j]=php
            j+=1

       j=0
       for s in SquirtleRes[i].battles:
            php=s["percHP"]
            vct=(1 if s["exitcond"]=="Vct" else 0)
            try:
                SquirtleEneWin[s["enemyPk"]].append((vct,php,b["nTurns"]))
            except KeyError:
                SquirtleEneWin[s["enemyPk"]] = [(vct,php,b["nTurns"])]
            SquirtleVct[i]+=vct
            SquirtleTurn[i,j]=s["nTurns"]
            SquirtlePHP[i,j]=php
            j+=1  

############################################FIGURE 1####################################################################
    mpl.plot(range(nSim),CharmanderVct,'or',markersize="1")
    mpl.plot(range(nSim),BulbasaurVct,'og',markersize="1")
    mpl.plot(range(nSim),SquirtleVct,'oc',markersize="1")
    mpl.plot(range(nSim),np.ones((nSim,1))*np.sum(BulbasaurVct)/nSim,'--g',label="Bulbasaur average victories",linewidth="2")
    mpl.plot(range(nSim),np.ones((nSim,1))*np.sum(CharmanderVct)/nSim,'--r',label="Charmander average victories",linewidth="2")
    mpl.plot(range(nSim),np.ones((nSim,1))*np.sum(SquirtleVct)/nSim,'--c',label="Squirtle average victories",linewidth="2") 
    mpl.legend()
    mpl.ylabel("Number of victories over 150 battles")
    mpl.xlabel("Game index")
    mpl.title("Number of victories for each starter")
   

############################################# FIGURE 2 #################################################################

    percHParray=np.array([BulbasaurPHP.flatten(), CharmanderPHP.flatten(),SquirtlePHP.flatten()])
    numTarray=np.array([BulbasaurTurn.flatten(), CharmanderTurn.flatten(),SquirtleTurn.flatten()])
    f,ax1=mpl.subplots()
    ax1.boxplot(percHParray.flatten(),positions=[1])
    ax2=mpl.twinx(ax1)
    ax2.boxplot(numTarray.flatten(),positions=[2])
    ax1.set_xticklabels(['PercentageHP', 'Number of Turns'])
    ax1.set_ylabel("Percentage of remaining HP")
    ax2.set_ylabel("Number of turns")
    mpl.title("Percentage of victories and number of turns boxplots") 

    meanPHP=np.mean(percHParray.flatten())
    medianPHP=np.median(percHParray.flatten())
    quantsPHP=np.quantile(percHParray.flatten(),[0.25,0.75])

    print("Mean percentage of remaining HP: "+str(meanPHP))
    print("Median percentage of remaining HP: "+str(medianPHP))
    print("Quantiles of remaining HP: \n"
          +"-25%: "+str(quantsPHP[0])+"\n"
          +"-75%: "+str(quantsPHP[1]))

    meanT=np.mean(numTarray.flatten())
    medianT=np.median(numTarray.flatten())
    quantsT=np.quantile(numTarray.flatten(),[0.25,0.75])

    print("\nMean number of turns: "+str(meanT))
    print("Median number of turns: "+str(medianT))
    print("Quantiles of number of turns: \n"
          +"-25%: "+str(quantsT[0])+"\n"
          +"-75%: "+str(quantsT[1]))
    
##################################################### FIGURE 3 ####################################################
##################################################### BULBASAUR ###################################################
    npk=len(BulbasaurEneWin)
    BperHP=[]
    Bperwin=np.zeros((npk,1))
    BmnHP=np.zeros((npk,1))
    BsdHP=np.zeros((npk,1))
    Bturn=[]
    idx=0
    for v in BulbasaurEneWin.values():
       
        BperHP.append([])
        Bturn.append([])
        for tp in v:
            Bperwin[idx]+=tp[0]
            BperHP[idx].append(tp[1])
            Bturn[idx].append(tp[2])
        BmnHP[idx]=np.mean(BperHP[idx])
        BsdHP[idx]=np.sqrt(np.var(BperHP[idx]))
        Bperwin[idx]=Bperwin[idx]/len(v)*100
        idx+=1

    Beasy=np.array([id for id in range(len(BulbasaurEneWin)) if 
           70<=Bperwin[id] and BmnHP[id]>=70])
    
    Bhard=np.array([id for id in range(len(BulbasaurEneWin)) if 
           50<=Bperwin[id]<=70 and np.mean(Bturn[id])>=medianT])

    Bks=np.array(list(BulbasaurEneWin.keys()))
    Bks_clean=np.array([Bks[i] if (i in Beasy or i in Bhard) else "" for i in range(npk) ])
    tks=np.array(range(len(Beasy)+len(Bhard)))

    meaningful=np.sort(np.concatenate((Beasy,Bhard)))
    mpl.figure()
    
    txt=("RED: skilled user suitable Pokemons\n"+
        "GREEN: unexperienced user suitable Pokemons")
    mpl.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=10)
    
    mpl.subplot(121)
    mpl.barh(tks,Bperwin[meaningful].flatten())
    mpl.yticks(tks, Bks_clean[meaningful],color='k')
    ax=mpl.gca()
    for i in tks:
        if  meaningful[i] in Beasy:
            ax.get_yticklabels()[i].set_color('g')
        elif meaningful[i] in Bhard:
            ax.get_yticklabels()[i].set_color('r')

    mpl.xlabel("Percentage of victories")

    mpl.subplot(122)
    mpl.barh(tks,BmnHP[meaningful].flatten(),xerr=BsdHP[meaningful].flatten())
    mpl.yticks(tks, Bks_clean[meaningful],color='k')
    ax=mpl.gca()
    for i in tks:
        if  meaningful[i] in Beasy:
            ax.get_yticklabels()[i].set_color('g')
        elif meaningful[i] in Bhard:
            ax.get_yticklabels()[i].set_color('r')
    mpl.xlabel("Mean %HP at the end of each turn")
    mpl.suptitle("Wild pokemon specific statistics for Bulbasaur")

##################################################### CHARMANDER ###################################################
    npk=len(CharmanderEneWin)
    CperHP=[]
    Cperwin=np.zeros((npk,1))
    CmnHP=np.zeros((npk,1))
    CsdHP=np.zeros((npk,1))
    Cturn=[]
    idx=0
    for v in CharmanderEneWin.values():
       
        CperHP.append([])
        Cturn.append([])
        for tp in v:
            Cperwin[idx]+=tp[0]
            CperHP[idx].append(tp[1])
            Cturn[idx].append(tp[2])
        CmnHP[idx]=np.mean(CperHP[idx])
        CsdHP[idx]=np.sqrt(np.var(CperHP[idx]))
        Cperwin[idx]=Cperwin[idx]/len(v)*100
        idx+=1

    Ceasy=np.array([id for id in range(len(CharmanderEneWin)) if 
           70<=Cperwin[id] and CmnHP[id]>=70])
    
    Chard=np.array([id for id in range(len(CharmanderEneWin)) if 
           50<=Cperwin[id]<=70 and np.mean(Cturn[id])>=medianT])

    Cks=np.array(list(CharmanderEneWin.keys()))
    Cks_clean=np.array([Cks[i] if (i in Ceasy or i in Chard) else "" for i in range(npk) ])
    tks=np.array(range(len(Ceasy)+len(Chard)))

    meaningful=np.sort(np.concatenate((Ceasy,Chard)))
    mpl.figure()
    
    txt=("\n\nRED: skilled user suitable Pokemons\n"+
        "GREEN: unexperienced user suitable Pokemons")
    mpl.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=10)

    mpl.subplot(121)
    mpl.barh(tks,Cperwin[meaningful].flatten())
    mpl.yticks(tks, Cks_clean[meaningful] ,color='k')
    ax=mpl.gca()
    for i in tks:
        if  meaningful[i] in Ceasy:
            ax.get_yticklabels()[i].set_color('g')
        elif meaningful[i] in Chard:
            ax.get_yticklabels()[i].set_color('r')


    mpl.xlabel("Percentage of victories")

    mpl.subplot(122)
    mpl.barh(tks,CmnHP[meaningful].flatten(),xerr=CsdHP[meaningful].flatten())
    mpl.yticks(tks, Cks_clean[meaningful],color='k')
    ax=mpl.gca()
    for i in tks:
        if  meaningful[i] in Ceasy:
            ax.get_yticklabels()[i].set_color('g')
        elif meaningful[i] in Chard:
            ax.get_yticklabels()[i].set_color('r')
    mpl.xlabel("Mean %HP at the end of each turn")
    mpl.suptitle("Wild pokemon specific statistics for Charmander")

    ##################################################### SQUIRTLE ###################################################
    npk=len(SquirtleEneWin)
    SperHP=[]
    Sperwin=np.zeros((npk,1))
    SmnHP=np.zeros((npk,1))
    SsdHP=np.zeros((npk,1))
    Sturn=[]
    idx=0
    for v in SquirtleEneWin.values():
       
        SperHP.append([])
        Sturn.append([])
        for tp in v:
            Sperwin[idx]+=tp[0]
            SperHP[idx].append(tp[1])
            Sturn[idx].append(tp[2])
        SmnHP[idx]=np.mean(SperHP[idx])
        SsdHP[idx]=np.sqrt(np.var(SperHP[idx]))
        Sperwin[idx]=Sperwin[idx]/len(v)*100
        idx+=1

    Seasy=np.array([id for id in range(len(SquirtleEneWin)) if 
           70<=Sperwin[id] and SmnHP[id]>=70])
    
    Shard=np.array([id for id in range(len(SquirtleEneWin)) if 
           50<=Sperwin[id]<=70 and np.mean(Sturn[id])>=medianT])

    Sks=np.array(list(SquirtleEneWin.keys()))
    Sks_clean=np.array([Sks[i] if (i in Seasy or i in Shard) else "" for i in range(npk) ])
    tks=np.array(range(len(Seasy)+len(Shard)))

    meaningful=np.sort(np.concatenate((Seasy,Shard)))


    mpl.figure()
    
    txt=("RED: skilled user suitable Pokemons\n"+
        "GREEN: unexperienced user suitable Pokemons")
    mpl.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=10)

    mpl.subplot(121)
    mpl.barh(tks,Sperwin[meaningful].flatten())
    mpl.yticks(tks, Sks_clean[meaningful],color='k')
    ax=mpl.gca()
    for i in tks:
        if  meaningful[i] in Seasy:
            ax.get_yticklabels()[i].set_color('g')
        elif meaningful[i] in Shard:
            ax.get_yticklabels()[i].set_color('r')

    mpl.xlabel("Percentage of victories")

    mpl.subplot(122)
    mpl.barh(tks,SmnHP[meaningful].flatten(),xerr=SsdHP[meaningful].flatten())
    mpl.yticks(tks, Sks_clean[meaningful],color='k')
    ax=mpl.gca()
    for i in tks:
        if  meaningful[i] in Seasy:
            ax.get_yticklabels()[i].set_color('g')
        elif meaningful[i] in Shard:
            ax.get_yticklabels()[i].set_color('r')
    mpl.xlabel("Mean %HP at the end of each turn")
    mpl.suptitle("Wild pokemon specific statistics for Squirtle")
    mpl.show()

Visualize()