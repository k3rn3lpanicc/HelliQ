import json, codecs
import os

studentsfile = "students.json"


def students():
    f=open(studentsfile,"r", encoding='utf-8')
    data=json.loads(f.read())
    f.close()
    return data

def searchs(key,value):
    data = students()
    for i in data:
        if(i[key]==value):
            return i
    return False

def printstudents(key):
    data = students()
    for i in data:
        if(key==""):
            print(i)
        else:
            print(i[key])

def checkstudent(idcode):
    data=students()
    for i in data:
        if(i['telcode']==idcode):
            return True
    return False

def change(key , value , key2,value2):
    data=students()
    for i in data:
        if(i[key]==value):
            i[key2] = value2
    save(data)
    return True


def save(students):
    data=students
    with open(studentsfile, 'wb') as f:
        json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)


def removestd(key, value):
    a = students()
    b=[]
    for i in a:
        if not i[key] == value:
            b.append(i)
    save(b)


def addstudent(name,telcode,isfirst,cllass):
    data = students()
    data.append({"name": name, "telcode": telcode, "isfirst": isfirst, "class": cllass, "isasking": "false","toid":"","state":"0"})
    with open(studentsfile, 'wb') as f:
        json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    print("done")


if not os.path.isfile(studentsfile):
    k = open(studentsfile, "w", encoding='utf-8')
    k.write('[]')
    k.close()
