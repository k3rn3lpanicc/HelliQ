import json, codecs
import os

studentsfile = "students.json"


def students():
    f=open(studentsfile,"r", encoding='utf-8')
    data=json.loads(f.read())
    f.close()
    return data


def printstudents(key):
    data = students()
    for i in data:
        if(key==""):
            print(i)
        else:
            print(i[key])


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


def addstudent(name,telcode,melli):
    data = students()
    data.append({"name": name, "telcode": telcode, "melli": melli})
    with open(studentsfile, 'wb') as f:
        json.dump(data, codecs.getwriter('utf-8')(f), ensure_ascii=False)
    print("done")


if not os.path.isfile(studentsfile):
    k = open(studentsfile, "w", encoding='utf-8')
    k.write('[]')
    k.close()
