import pandas as pd
import numpy as np
import random
import datetime

start = datetime.datetime.now()



def splitter(x):
    return [y.strip(" \n") for y in x.split(",")]

df = pd.read_csv("loldle.csv")
df = df.drop(columns=["Unnamed: 0"])
for s in ["Position","Species","Range type","Region"]:
    df[s] = df[s].apply(splitter)
df["Name"] = df["Name"].apply(lambda x: x.strip())




def comparison(x,y):
    res = []
    cols = []
    for col in x.index.tolist()[1:]:
        
        if col=="Name" or col=="comparison" or col=="score":
            continue
        
        elif col=="Release":
            if x[col]==y[col]:
                res.append('Green')
            elif x[col]>y[col]:
                res.append('Down')
            else:
                res.append('Up')
            cols.append(col)
        elif (type(x[col])==str):
            cols.append(col)
            if x[col]!=y[col]:
                res.append('Red')
            else:
                res.append('Green')
        
        else:
            cols.append(col)
            if (set(x[col])&set(y[col])==set(x[col])) and (set(x[col])==set(y[col])):
                # print(set(x[col])&set(y[col]))
                # print(set(x[col]))
                res.append("Green")
            elif set(x[col])&set(y[col])!=set():
                # print(set(x[col])&set(y[col]))
                # print(set(x[col]))
                res.append("Orange")
            else:
                res.append("Red")
    return res

results = {name:0 for name in df["Name"]}
global_counter = 0
for loop in range(50):
    for j in range(0,161):
        CHAMP = df.loc[j]
        for i in range(0,161):
            df_copy = df.copy()
            df_copy["score"] = [0 for i in range(161)]
            global_counter+=1
            guesses = 0
            last_guess = None
            starter = None
            while True:
                if guesses == 0:
                    guess_idx = i
                    guess = df_copy.loc[guess_idx].squeeze()
                    starter = guess
                    last_guess = guess
                else:
                    df_copy = df_copy.sample(frac=1).reset_index(drop=True)
                    comp = comparison(last_guess,CHAMP)
                    df_copy["comparison"] = df_copy.apply(lambda x: comparison(last_guess,x),axis=1)
                    df_copy["score"] += df_copy["comparison"].apply(lambda x: sum([1 if x1==x2 else 0 for x1,x2 in zip(x,comp)]))
                    
                    guess_idx = df_copy["score"].idxmax()
                    guess = df_copy.loc[guess_idx].squeeze()
                    last_guess = guess
                guesses+=1
                comp = comparison(guess,CHAMP)
                df_copy = df_copy.drop(guess_idx)
                if global_counter%1000==0:
                    print(global_counter)
                if comp == ["Green","Green","Green","Green","Green","Green","Green"]:
                    results[starter["Name"]]+=guesses
                    break
pd.DataFrame([[k,v] for k,v in results.items()],columns=["Starter","tot_guesses"]).to_csv("resultsx25t2.csv")

end = datetime.datetime.now()
print(end-start)
# df.apply(lambda x: comparison(x,CHAMP),axis=1)
