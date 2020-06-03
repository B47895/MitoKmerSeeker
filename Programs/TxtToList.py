#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
import os, time, sys
from optparse import OptionParser
from copy import *
#Input: python TxtToList <desired txt version of a list> -w <length of the kmers> -o <desired name>
["Options:"]
parser=OptionParser()
parser.add_option("-w", "--window", help="Length of the window (bp)", default=32, dest="lenwin")
parser.add_option("-o", "--output", help="Name of the output list file (without extension)", default="out", dest="outname")
(options, args)=parser.parse_args()
out=str(options.outname)
len_window=int(options.lenwin) 
reader=open(sys.argv[1],"r")
Reader=reader.readlines()
writer=open("temp.txt","w")
counter=1
for j in Reader:
    j=j.split("	")
    if not j[0][0]=="N":
        for i in range(int(j[1].split("\n")[0])):
            writer.write(">kmer_"+str(counter)+"_"+str(i+1)+os.linesep)
            writer.write(j[0]+os.linesep)
        counter+=1
writer.close()
reader.close()
os.system("./glistmaker temp.txt -w "+str(len_window)+" -o "+out)
os.system("mv "+out+"_"+str(len_window)+".list "+out+".list")
os.system("rm temp.txt")
