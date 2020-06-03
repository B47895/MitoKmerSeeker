#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
import os, time
print("Runing all the FASTQ files into sets of k-mers")
os.system("python k-merizer.py")
print("Program starts at time: "+str(time.ctime(time.time())))
#Paramaters
len_window=32
tncs=[] #Targets and close species
last="species name checking"
badsymbols=["[","]","(",")",",",">"]
ref=open("blasted_targets.txt","r")
count=-1
for i in ref.readlines(): #Determining targets and their close species
    i=i.split("	")
    if i[0]!=last:
        last=i[0]
        tncs.append([i[0],[]])
        count+=1
        if i[0]==i[1]:
            j=i[-1].split(" ")
            tncs[count][0]=j[1]+" "+j[2]
    if i[0]!=i[1]:
        k=i[-1].split(" ")
        if " x " in i[-1]:
            add=k[1]+" "+k[2]+" "+k[3]+" "+k[4]+" "+k[5]
        else:
            add=k[1]+" "+k[2] 
        for k in badsymbols:
            add=add.replace(k,"")
        if add not in tncs[count][1]:
            tncs[count][1].append(add)
ref.close()
Stats=open("Statistics.csv","r")
stats=Stats.readlines()
writestats=open("Tempstats.csv","w")
Ref=open("todownload.txt","r")
ref=Ref.readlines()
Ref.close()
namelookup=[[]]
writestats.write(stats[0].split("\n")[0]+"Close species,number of kmers after filter,freq of kmers after filter,,")
for i in range(len(ref)):
    ref[i]=ref[i].split("\n")[0].split(",")
    namelookup[0].append(ref[i][1])
namelookup.append(ref)
ref="" #clearing memory
for i in tncs:
    name=i[0].split(" ")
    os.system("./glistmaker BlastSpecific_"+name[0]+"_"+name[1]+"_kmers.txt -w "+str(len_window)+" -o "+name[0]+"_"+name[1]) #species_name_32.list
    targetlist_file=name[0]+"_"+name[1]+"_"+str(len_window)+".list"
    #Checking for close species
    union=""
    forstats=""
    count=0
    for j in i[1]:
        if j in namelookup[0]:
            for k in namelookup[1]:
                if j in k[1] and os.popen("ls -d "+k[0]+".list").read()!="":
                    union+=k[0]+".list "
                    forstats+=";"+k[1]
                    count+=1
    if union=="":
        print(name[0]+" "+name[1]+" has failed to find close target species from the folder!")
        continue
    print(name[0]+" "+name[1])
    print("./glistcompare "+union+" -u -o nontarget")
    forstats=forstats[1:]
    if count>1:
        os.system("./glistcompare "+union+" -u -o nontarget") #nontarget_32_union.list
        os.system("./glistcompare "+name[0]+"_"+name[1]+"_"+str(len_window)+".list nontarget_"+str(len_window)+"_union.list -d -o "+name[0]+"_"+name[1]) #species_name_32_0_diff1.list
    else:
        os.system("./glistcompare "+name[0]+"_"+name[1]+"_"+str(len_window)+".list "+union+" -d -o "+name[0]+"_"+name[1])
    os.system("./glistquery "+name[0]+"_"+name[1]+"_"+str(len_window)+"_0_diff1.list > f_wrongfreq_"+name[0]+"_"+name[1]+".txt")
    #Correcting the frequencies
    #First, making a list of the k-mers
    Ref=open("f_wrongfreq_"+name[0]+"_"+name[1]+".txt","r")
    refmers=[]
    for j in Ref.readlines():
        j=j.split("	")
        if len(j)>1:
            refmers.append(j[0])
    Ref.close()
    Rightfreq=open("BlastSpecific_"+name[0]+"_"+name[1]+"_kmers.txt","r")
    rightfreq=Rightfreq.readlines()
    Rightfreq.close()
    Rightfreq=open("final_"+name[0]+"_"+name[1]+".txt","w")
    count=float(0)
    freqcount=float(0)
    for j in rightfreq:
        if j[0]==">":
            freq=j.split("_")[-3]
        elif j.split("\n")[0]!="" and j.split("\n")[0] in refmers:
            count+=1
            freqcount+=float(freq)
            Rightfreq.write(j.split("\n")[0]+"	"+freq+"\n")
    Rightfreq.close()
    #clearing memo
    refmers=""
    rightfreq=""
    os.system("rm f_wrongfreq_"+name[0]+"_"+name[1]+".txt "+name[0]+"_"+name[1]+"_"+str(len_window)+".list "+name[0]+"_"+name[1]+"_"+str(len_window)+"_0_diff1.list nontarget_"+str(len_window)+"_union.list")
    for j in stats:
        if name[0]+" "+name[1] in j:
            writestats.write(j.split("\n")[0]+forstats+","+str(int(count))+","+str(freqcount/count)+",,")
            break
writestats.close()
print("Done at time: "+str(time.ctime(time.time())))
        
            
            
            
            
    
