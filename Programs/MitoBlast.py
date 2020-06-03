#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
import os, sys, os.path, time
from optparse import OptionParser
from copy import *
"""
Usage
python MitoBlast.py /path/to/database
for example:
python MitoBlast.py /storage9/db/ncbi
where the ncbi folder contains nt, refseq_genomic and other_genomic databases.
"""
print("Program starts at time: "+str(time.ctime(time.time())))
#Turning the list files into FASTA files.
open_ref=open("targets.txt","r")
reading=open_ref.readlines()
for i in reading:
    if i[0]==">":
        i=i.split(" ")
        searching="Specific_kmers_32_"+i[1]+"_"+i[2]+".txt"
        print(i[1]+" "+i[2])
        counter=1
        reader=open(searching,"r")
        name=i[1]+"_"+i[2]+"_blasting.txt"
        writer=open(name,"w")
        for j in reader.readlines():
            j=j.split("	")
            if not j[0][0]=="N":
                writer.write(">"+i[1]+"_"+i[2]+"_"+j[1].split("\n")[0]+"_kmer_"+str(counter)+os.linesep)
                writer.write(j[0]+os.linesep)
                counter+=1
        writer.close()
        reader.close()
##########################################
#Running BLAST
path=str(sys.argv[1])
for i in reading:
    if i[0]==">":
        i=i.split(" ")
        name=i[1]+"_"+i[2]+"_blasting.txt"
        print("Blasting "+i[1]+" "+i[2])
        print("blasting nt")
        os.system("module load blast-2.9.0+ && blastn -query "+name+" -db "+path+"/nt -out "+i[1]+"_"+i[2]+"_kmers_nt.txt -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -perc_identity 90 -qcov_hsp_perc 100 -num_threads 20")
        print("blasting refseq_genomic")
        os.system("module load blast-2.9.0+ && blastn -query "+name+" -db "+path+"/refseq_genomic -out "+i[1]+"_"+i[2]+"_kmers_refseq_genomic.txt -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -perc_identity 90 -qcov_hsp_perc 100 -num_threads 20")
        print("blasting other_genomic")
        os.system("module load blast-2.9.0+ && blastn -query "+name+" -db "+path+"/other_genomic -out "+i[1]+"_"+i[2]+"_kmers_other_genomic.txt -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -perc_identity 90 -qcov_hsp_perc 100 -num_threads 20")
##########################################
#Checking the balst results and creating the filtered list.
output1=open("Withcopies.txt","w")
statistics=open("Statistics.csv","r")
Readstats=statistics.readlines()
Tempor=open("Temporarystats.csv","w")
writing=Readstats[0].split("\n")
Tempor.write(writing[0]+"Left,Total,nt,other,refseq,FreqAfterBlast,,\n")
for i in reading:
    if i[0]==">":
        i=i.split(" ")
        databases=["nt","other_genomic","refseq_genomic"]
        found=[]
        stats=[[],[],[]]
        for k in databases:
            searching=i[1]+"_"+i[2]+"_kmers_"+k+".txt"
            reader=open(searching,"r")
            for j in reader.readlines():
                j=j.split("	")
                nr=int(j[0].split("_")[-1])
                if not i[1]+" "+i[2] in j[-1]: #If blast returned a species that is the same as the target species
                    found.append(nr)
                    stats[databases.index(k)].append(nr)
            reader.close()
        stats[0]=list(set(stats[0]))
        stats[1]=list(set(stats[1]))
        stats[2]=list(set(stats[2]))
        found=list(set(found)) #Removes repeated entries from the list.
        output1.write(i[1]+" "+i[2]+" "+str(found)+os.linesep)
        ref=open(i[1]+"_"+i[2]+"_blasting.txt","r")
        output2=open("BlastSpecific_"+i[1]+"_"+i[2]+"_kmers.txt","w")
        switch=0
        count=0
        Gcount=0
        ntotal=0
        for k in ref.readlines():
            if k[0]==">":
                Gcount+=1
                nr=int(k.split("_")[-1])
                if not nr in found:  
                    count+=1
                    switch=1
                    output2.write(k)
                    ntotal+=float(k.split("_")[2])
            elif switch==1:
                output2.write(k)
                switch=0
        for k in range(len(Readstats)):
            writing=Readstats[k].split(",")
            if writing[0]==i[1]+" "+i[2]:
                break
        Tempor.write(Readstats[k].split("\n")[0]+str(count)+","+str(Gcount)+","+str(len(stats[0]))+","+str(len(stats[1]))+","+str(len(stats[2]))+","+str(ntotal/count)+"\n")
        output2.close()
        ref.close()
output1.close()
statistics.close()
Tempor.close()
statistics.close()
os.rename("Statistics.csv","Statistics_from_MitoDiff.csv")
os.rename("Temporarystats.csv","Statistics.csv")

print("Done at time: "+str(time.ctime(time.time())))
