import json, codecs
import os
import sys

aa=sys.argv
cm=aa[1]


fileadd="teachers.json"
def save(tch):
    data=tch
    with open(fileadd, 'wb') as f:
        json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)

def teachers(): 
    f=open(fileadd,"r", encoding='utf-8')
    data=json.loads(f.read())
    f.close()
    return data
def appendclass(key,value,key2,value2,cls):
    data = teachers()
    for i in range(len(data)):
        
        if(data[i][key]==value and data[i][key2]==value2):            
            data[i]["class"].append([cls,""])
            data[i]
    save(data)

def appendteacher(name,dars):
    data = teachers()
    name=name.replace("_"," ")
    data.append({'dars':dars,'name' : name  , 'class':[]})
    save(data)
def rmteacher(keys , values , key2s,value2s):
    data = teachers()
    k=0
    values=values.replace("_"," ")
    for i in range(len(data)):
        
        if(data[i][keys]==values and data[i][key2s]==value2s):            
            k=i
    data.remove(data[k])
    save(data)
def editid(name,dars,clas,idd):
    data = teachers()
    if(idd=="_"):
        idd=""
    for i in range(len(data)):
        if(data[i]['name']==name and data[i]['dars']==dars):
            for j in range(len(data[i]['class'])):
                           if(data[i]['class'][j][0]==clas):
                               data[i]['class'][j][1]=idd
    save(data)

for i in range(len(aa)):
    aa[i].replace("_"," ")

if (cm=="0"):
    appendclass(aa[3],aa[4],aa[5],aa[6],aa[2])
elif (cm=="1"):
    appendteacher(aa[2],aa[3]) 
if (cm=="s"):
    rmteacher(aa[2],aa[3] , aa[4], aa[5])
if(cm=="3"):
    editid(aa[2],aa[3],aa[4],aa[5])
