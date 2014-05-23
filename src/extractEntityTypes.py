# -*- coding: cp1252 -*-
import sqlite3 as lite
import os.path
import re
from collections import defaultdict
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

listOfTables=[]
dict_entity=defaultdict(int)
con = lite.connect('test3.db')
con.text_factory = str
cur = con.cursor() 


for i in range(1,12976):
        print i
        name="H:\\MS\\Web Mining\\Assignment\\Assignment 4\\Data\\Sample InfoBoxes\\page"+str(i)+".txt"
        if os.path.isfile(name):
            with open(name,'rb') as f:
                page=f.read()
                data=page.split('\n')
                    
                tableName=data[0].split("Infobox")[1]
                if len(tableName.split("|"))>1:
                    tableName=tableName.split("|")[0]
                    
                tableName=tableName.lower().replace("\n","").replace("|","").replace("/","_").lstrip().rstrip().replace(" ","_").replace("-","_")
                
                if tableName.startswith('_'):
                        tableName=tableName[1:]

                dict_entity[tableName]+=1   
                if tableName not in listOfTables:
                    listOfTables.append(tableName)
                    sql='CREATE TABLE if not exists ' + tableName + '(attribute_name, value, attribute_type, min_value, max_value, units, PRIMARY KEY (attribute_name))'
                    cur.execute(sql)    
                    
                row=[0]*6
                count=0
                for i in range(1,len(data)):
                        if "=" in data[i]:
                            if data[i].split("="):
                                    key_value=data[i].split("=")
                                    key_value[0]=key_value[0][1:]
                                    if key_value[0].startswith(' '):
                                        key_value[0]=key_value[0][1:]
                                    row[0]=key_value[0]
                                    row[5]='Not Applicable'
                                    if key_value[1]!=' \n':
                                            count+=1
                                            value=key_value[1].strip()
                                            if is_number(value):
                                                dataType='number'
                                                row[3]=value
                                                row[4]=value
                                            else:
                                                #print key_value[1]
                                                if '[[' in value or 'www' in value:
                                                        dataType='Link'
                                                elif is_number(value):
                                                        dataType='Number'
                                                        row[3]=value
                                                        row[4]=value
                                                elif "date" in key_value[0].lower() or re.search("(January|February|March|April|May|June|July|August|September|October|November|December)",key_value[1]):
                                                        dataType='Date'
                                                elif re.search('[0-9]+:[0-9]',key_value[1]) or re.search('[0-9]+–[0-9]*',key_value[1]):
                                                        dataType='Duration'
                                                elif re.search('[[0-9]+:[0-9]]+[,/]+[[0-9]+:[0-9]]',key_value[1]) or re.search('[[0-9]+–[0-9]*]+[,/][[0-9]+–[0-9]*]+',key_value[1]):
                                                        dataType='Set of Duration'
                                                elif re.search('[,/]+',key_value[1]):
                                                        dataType='Set of Strings'
                                                elif key_value[1].isspace() or key_value[1]=="" or key_value[1]=="NULL":
                                                        dataType='Others'
                                                else:
                                                        dataType='String'
                                                row[3]=-1
                                                row[4]=-1

                                            #find unit
                                            if  dataType!='Date':
                                                    temp=value.replace(" ","")
                                                    if temp.isalnum():
                                                        parts=re.findall(r'\d+|\D+',temp)
                                                        if len(parts)==2:
                                                            for part in parts:
                                                                if not is_number(part):
                                                                    row[5]=part
                                                
                                            row[1]=value
                                            row[2]=dataType
                                            
                                                
                            try:
                                    sql="INSERT INTO "+tableName+"(attribute_name, value, attribute_type, min_value, max_value, units) VALUES (?,?, ?, ?, ?, ?);"
                                    cur.executemany(sql, (row,))
                                    con.commit()
                                    
                            except lite.IntegrityError:
                                    sql="SELECT * FROM "+tableName+" WHERE attribute_name=?"
                                    cur.execute(sql,(row[0],))
                                    for key in cur:
                                        #print key
                                        if key[2]=='number' and row[2]=='number':
                                            if key[3]<row[3]:
                                                sql="UPDATE "+tableName+ " SET min_value=? WHERE attribute_name=?"
                                                #print sql
                                                cur.execute(sql, (row[3], key[0]))
                                            if key[4]>row[4]:
                                                sql="UPDATE "+tableName+ " SET max_value=? WHERE attribute_name=?"
                                                #print sql
                                                cur.execute(sql, (row[4], key[0]))    
                                        elif key[1].isspace() or key_value[1]=="" or key_value[1]=="NULL":
                                            sql="UPDATE "+tableName+ " SET value=? WHERE attribute_name=?"
                                            #print sql
                                            cur.execute(sql, (row[1], key[0]))
                                    

for i in range(0,len(listOfTables)):
        tableName=listOfTables[i]
        sql="select * from "+tableName
        rows=con.execute(sql)
        output="H:\\MS\\Web Mining\\Assignment\\Assignment 4\\Data\\Entity Types\\" +tableName+ ".txt"
        out=open(output,"w")
        for row in rows:
                #print row[0]+'\t'+row[1]+'\t'+str(row[2])+'\t'+str(row[3])+'\n'
                out.write(str(row[0])+'\t'+str(row[2])+'\t'+str(row[3])+'\t'+str(row[4])+'\t'+str(row[5])+'\n')
        out.close()

f=open("H:\\MS\\Web Mining\\Assignment\\Assignment 4\\Data\\Entity Types\\ListOfEntities.txt","w")
f.write("\n".join(listOfTables))
f.close()

data=[]
for key in dict_entity:
    data.append(key+"\t"+str(dict_entity[key])+"\n")

f=open("H:\\MS\\Web Mining\\Assignment\\Assignment 4\\Data\\Entity Types\\NumberOfEntitiesPerEntityType.txt","w")
f.write("\n".join(data))
f.close()
