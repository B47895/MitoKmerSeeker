#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
import os, sys, os.path, time
from optparse import OptionParser
from copy import *

"""
Run using the command
python MitoIdent targets.txt nontargets.txt -w n -f n

Must have GenomeTester4 version 4.0 programs glistmaker, glistquery and glistcompare inside the folder
"""

["Options:"]
parser=OptionParser()
parser.add_option("-w", "--window", help="Length of the window (bp)", default=32, dest="lenwin")
parser.add_option("-f", "--frequency", help="The minimum number of sequences that should contain every specific kmers", default=1, dest="freq")
(options, args)=parser.parse_args()

len_window=int(options.lenwin) 
kmer_freq=int(options.freq)

###My code
print("Program starts at time: "+str(time.ctime(time.time())))
statistics=open("Statistics.csv","w")
statistics.write("Name,k-mer freq before 1st filter,k-mer freq after MitoIdent,,\n")
"""
My code fragments the file sys.argv[1] to view them as targets separately.
so the output of the program is n files, where n is equal to sys.argv[1]
number of lines that start with >
Variables:
..count..
Allows the cycle's each iteration to choose a different target species at a target
for the Identification program. 
..switch..
Allows the lines starting with > to be sorted into the appropriate file.
"""
count=0
print("Making a kmer list of all the nontargets..")
nontargets_file=sys.argv[2]
os.system("./glistmaker "+nontargets_file+" -w "+str(len_window)+" -o Nontarget_list")
while True:
    nontargets=open("nontargets.txt","w")
    targets=open("target.txt","w")
    all_targets_file=open(sys.argv[1])
    reading=all_targets_file.readlines()
    for i in range(len(reading)):
        if reading[i][0]==">": 
            if i==count: #Allows on each iteration choosing the next species from all_targets to take as targets
                switch=1
                name=reading[i].split(" ") #Later to name the file
                targets.write(reading[i])
            else:
                switch=2 #If it isn't the target on this iteration, that species goes from all_targets to nontargets
                nontargets.write(reading[i])
        elif switch==1: #If it's the target
            count+=1 #It increases the count. > row doesn't increase the count. So after target rows i=count+1 and the next goes to nontargets.
            targets.write(reading[i])
        elif switch==2:
            nontargets.write(reading[i])
    memo=name[1]+"_"+name[2]
    count+=1 #Loses the off-set on the next iteration
    targets.close()
    nontargets.close()
    all_targets_file.close()
    reading=len(reading) #To clear the memo and to exit the cycle in the very end.
    #End of my code
    #Creating k-mer lists from one FASTA file of target sequences:
    os.system("./glistmaker target.txt -w "+str(len_window)+" -o Target_list")
    print("Target(s) kmers done!")
    #For statistics case..
    os.system("./glistquery Target_list_"+str(len_window)+".list > Target_list.txt")
    info=os.popen("tail -n 2 Target_list.txt").read()
    info=info.split("\n")
    info[0]=info[0].split("\t")
    info[1]=info[1].split("\t")
    nontargets_file_name="nontargets.txt"
    os.remove("Target_list.txt")
    os.system("./glistmaker "+nontargets_file_name+" -w "+str(len_window)+" -o Nontarget_list_2") #My addition
    os.system("./glistcompare Nontarget_list_"+str(len_window)+".list Nontarget_list_2_"+str(len_window)+".list"+" --union -o Nontarget_kmers") #My addidion
    print("Nontargets kmers done!")
    os.system("./glistcompare Target_list_"+str(len_window)+".list Nontarget_kmers_"+str(len_window)+"_union.list -d -o Specific_kmers")
    print("Specific target kmers selected!")
    os.system("./glistquery Specific_kmers_"+str(len_window)+"_0_diff1.list > Specific_kmers_"+str(len_window)+"_"+memo+".txt")
    print("Specific kmers are visible in textfile now!")
    info2=os.popen("tail -n 2 Specific_kmers_"+str(len_window)+"_"+memo+".txt").read()
    info2=info2.split("\n")
    info2[0]=info2[0].split("\t")
    info2[1]=info2[1].split("\t")
    statistics.write(name[1]+" "+name[2]+","+str(float(info[1][1])/float(info[0][1]))+","+str(float(info2[1][1])/float(info2[0][1]))+",,\n")
    #Deleting unnecessary files ...
    os.remove("Target_list_"+str(len_window)+".list")
    os.remove("Specific_kmers_"+str(len_window)+"_0_diff1.list")
    os.remove("Nontarget_list_2_"+str(len_window)+".list")
    os.remove("Nontarget_kmers_"+str(len_window)+"_union.list")
    if count>=reading-2:
        break
#End of cycle
os.remove("nontargets.txt")
os.remove("Nontarget_list_"+str(len_window)+".list")
os.remove("target.txt")
statistics.close()
print("Done at time: "+str(time.ctime(time.time())))
