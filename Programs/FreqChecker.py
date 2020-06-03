#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
import os, random, time
#Workflow (will have to activate twice)
def Workflow(name):
    os.system("./glistcompare "+name+".list deletelater_32.list -i -o intersec") #intersec_32_intrsec.list
    os.system("./glistquery intersec_32_intrsec.list > temp.txt")
    Reader=open("temp.txt","r")
    relfreq=0
    for k in Reader.readlines():
        if k[0]!="N" and k!="" and k!="\n":
            k=k.split("	")
            for j in reader:
                if k[0] in j:
                    relfreq+=int(k[1].split("\n")[0])*int(j.split("\n")[0].split("	")[1])
                    break
    os.system("rm temp.txt intersec_32_intrsec.list")
    Reader.close()
    return(relfreq)
############################################################################################################
###########                  Start of the code                  ############################################
############################################################################################################
print("Program starts at time: "+str(time.ctime(time.time())))
#Seeing what species with k-mers are in the folder.
species=os.popen("ls -d final*").read()
species=species.split("\n")[:-1]
for i in range(len(species)):
    temp=species[i].split(".")[0].split("_")
    if len(temp)==3:
        species[i]=temp[1]+" "+temp[2]
        #print(temp,temp[1]+" "+temp[2])
checker=open("todownload.txt","r")
#Checking which binaries I have
listmaker=[]
referencegroup=[]
for i in checker.readlines():
    i=i.split("\n")[0]
    if i.split(",")[1] in species:
        listmaker.append(i)
    else:
        referencegroup.append(i)
for i in listmaker:
    reference=random.choice(referencegroup)
    i=i.split(",")
    i[1]=i[1].split(" ")
    Reader=open("final_"+i[1][0]+"_"+i[1][1]+".txt","r")
    reader=Reader.readlines()
    Reader.close()
    writer=open("temp.txt","w")
    counter=1
    for j in reader:
        j=j.split("	")
        if not j[0][0]=="N":
            for k in range(100):
                writer.write(">kmer_"+str(counter)+"_"+str(k+1)+os.linesep)
                writer.write(j[0]+os.linesep)
            counter+=1
    writer.close()
    os.system("./glistmaker temp.txt -w 32 -o deletelater")
    os.system("rm temp.txt")
    frequency=Workflow(i[0])
    referencefreq=Workflow(reference.split(",")[0])
    os.system("rm deletelater_32.list")
    print(i[1][0]+" "+i[1][1]+","+str(frequency)+",Negative control: ("+reference.split(",")[1].split("\n")[0]+"),"+str(referencefreq))
print("Done at time: "+str(time.ctime(time.time())))
