import pandas as pd
import os 
def writeCSV(textDict,col,name):
    lis=[]
    for i in textDict :
        lis.append([i,str(textDict[i])])
    write(lis,col,name)


def write(str,col,name):
    if name is None:
        return "Name of text is None"
    if col is None:
        text=pd.DataFrame(str)
    else:
        text=pd.DataFrame(str,columns=col)
    text.to_csv(name+".csv")
    return "Writing is finished"

def writeText(text,fileName):
    if fileName==None:
        fileName="document.txt"
    if text != None:
        with open(fileName,'a',encoding='utf-8') as f:
            f.write(text)
    else:
        print("text is null")