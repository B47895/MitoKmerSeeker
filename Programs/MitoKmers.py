#! /usr/bin/env python3.3
# -*- coding:UTF-8 -*-
######################################################################
#This is an umberella program for the rest of the programs in the process.
#!!!!
#You MUST read the code to run this program and comment different parts
#out for this to run as intended.
#The code contains pointers for what to do.
######################################################################
#First, functions are defined for parts which can be run together.
#!!!!
#Do NOT edit anything here!
import os
def MitoDiff(i,speciesfilename):
    if os.path.exists("mitochondrion.1.1.genomic.fna") and os.path.exists("mitochondrion.2.1.genomic.fna") and os.path.exists("MitoDiff.py"):
        if os.path.exists("targets.txt") or os.path.exists("nontargets.txt") or os.path.exists("repeated.txt"):
            print("There are files in the folder which will be overwritten. If you wish for this to happen, the program will continue automatically or you have to change the first parameter of the initialkmers command to 1. (it is set to 0 by default)")
            if i==0:
                return("Program ended.")
        os.system("python MitoDiff.py "+speciesfilename)
        return("Program finished.")
    return("Necessary programs aren't in folder!")
def MitoFilterAndBlast(n,path):
    if os.path.exists("MitoIdent.py") and os.path.exists("MitoBlast.py") and os.path.exists("glistmaker") and os.path.exists("glistquery") and os.path.exists("glistcompare") and os.path.exists("nontargets.txt") and os.path.exists("mitochondrion.2.1.genomic.fna") and os.path.exists("Statistics.csv"):
        os.system("python MitoIdent.py targets.txt nontargets.txt -w "+str(n))
        os.system("python MitoBlast.py "+path)
        return("Program finished")
    return("Necessary programs aren't in folder!")
def CloseSpecFinder():
    if os.path.exists("CloseSpecFinder.py"):
        os.system("cat mitochondrion.1.1.genomic.fna > database.txt")
        os.system("cat mitochondrion.2.1.genomic.fna >> database.txt")
        os.system("module load blast-2.9.0+ && makeblastdb -in database.txt -dbtype nucl -parse_seqids")
        os.system("module load blast-2.9.0+ && blastn -query targets.txt -db database.txt -out blasted_targets.txt -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -perc_identity 20 -num_threads 20")
        os.system("python CloseSpecFinder.py")
        return("Program finished")
    return("Necessary programs aren't in folder!")
def DownloadUnpack():
    if os.path.exists("todownload.txt") and os.path.exists("Dl-der.py"):
        os.system("python Dl-der.py")
        os.system("fastq-dump --skip-technical -F --split-3 SRR*")
        os.system("fastq-dump --skip-technical -F --split-3 ERR*")
        return("Program finished. Check nohup file for failures.")
    return("Necessary programs aren't in folder!")
def MitoFilter():
    if os.path.exists("blasted_targets.txt") and os.path.exists("MitoFilter.py") and os.path.exists("k-merizer.py") and os.path.exists("Statistics.csv") and os.path.exists("todownload.txt") and os.path.exists("glistmaker") and os.path.exists("glistquery") and os.path.exists("glistcompare"):
        os.system("python MitoFilter.py")
        return("Program finished.")
    return("Necessary programs aren't in folder!")
################################################################
#  Edit stuff under this line   ################################
################################################################

#Run only one of the print commands in one run, unless noted
#All of them are suggested to be run in nohup.

print(MitoDiff(1,"rawnames.txt")) #Change the txt filename. First parameter is a safeguard
"""
After running the previous program you need to check if you have seqences in
repeated.txt. If yo do, choose what to do with them (add them to targets,
add some of them to targets, add all to nontargets, etc
"""
print(MitoFilterAndBlast(32,"/storage9/db/ncbi")) #Second parameter need to be changed to the corresponding path to nt, refseq_genomic and other_genomic databases
print(CloseSpecFinder()) #No nohup. For MitoFilter
print(DownloadUnpack()) #For mitofilter. Super long.
print(MitoFilter()) #If you are running MitoFilterAndBlast with a parameter
#                   other than 32, go to MitoFilter and k-merizer code and 
#                   change len_window to such.

