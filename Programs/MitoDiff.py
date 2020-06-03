#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
import itertools, sys, os.path,time
from optparse import OptionParser
from copy import *
"""
How this works:
1. The input is a raw txt file with a target species name on each line
2. The program reads mitochondrion.1.1.genomic.txt and mitochondrion.2.1.genomic.txt
files, which need to be in the folder for the program to work,
differentiates the targets species and puts them in the file
targets.txt; the nontargets are put in the file nontargets.txt.
If there are any target species which are repeated, they are put in the file
repeated.txt, while one of the repeated species stays in the targets.txt
file and needs to be removed manually if neccessary

Run command:
python MitoDiff.py <speciesnames.txt>

Example of the raw species names text file:
/File starts/
Salmo salar
Homo sapiens
/File ends/
"""
print("Program starts at time: "+str(time.ctime(time.time())))
#1
filename=str(sys.argv[1])
file = [line.rstrip("\n") for line in open(filename)] #Gets a list with the names
matching = [i.rstrip("\r") for i in file] #Strips another ending
#2
#Opening and reading the RefSeq database
Info1=open("mitochondrion.1.1.genomic.fna","r")
Info2=open("mitochondrion.2.1.genomic.fna","r")
info1=Info1.readlines()
info2=Info2.readlines()
#Opening all the writing files
W1=open("targets.txt","w")
W2=open("nontargets.txt","w")
W3=open("repeated.txt","w") 
switch=0
found=[]
k=""
for i in itertools.chain(info1, info2):
    if i[0]==">": #Reads the name line
        switch=0
        for k in matching: #Determines if the line is of the target species
            if k in i:
                if " x " in i and " x " not in k:
                    pass
                else:
                    if k in found:
                        switch=3
                        W3.write(i) #Writes repeated name
                        break
                    else:
                        switch=1
                        found.append(k)
                        W1.write(i) #Writes target name
                        break
        if switch==0: #Nontarget name
            switch=2
            W2.write(i)
    elif switch==1: #Target DNA
        W1.write(i)
    elif switch==2: #Nontarget DNA
        W2.write(i)
    elif switch==3: #Repeated DNA
        W3.write(i)
W1.close()
W2.close()
W3.close()
left = list(set(matching)-set(found))
print("done")
print("Species that weren't found:   ",left,len(left))
print("Done at time: "+str(time.ctime(time.time())))
