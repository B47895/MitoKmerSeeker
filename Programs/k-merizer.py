import os, time
len_window=32 #Change!
#Converts fastq files to k-mer lists.
print("Program starts at time: "+str(time.ctime(time.time())))
while True:
    count=0
    info=(os.popen("ls").read()).split("\n")
    info.remove("")
    for i in info:
        if ".fastq" not in i:
            info=[k for k in info if i not in k]
    if info==[]:
        break
    elif "_" not in info[0]:
        #Making a fasta version of the .fastq
        os.system("perl -ne 'y/@/>/;print($_.<>)&&<>&&<>' "+info[0]+" > "+info[0].split(".")[0]+".fasta")
        #Deleting the .fastq as it is no longer needed, ever.
        os.remove(info[0])
        #Making a k-mer list of the .fasta
        os.system("./glistmaker "+info[0].split(".")[0]+".fasta -w "+str(len_window)+" -o "+info[0].split(".")[0])
        #Renaming AKA deleting the _32 at the end.
        os.rename(info[0].split(".")[0]+"_"+str(len_window)+".list",info[0].split(".")[0]+".list")
        #Deleting the .fasta
        try:
            if os.path.getsize(info[0].split(".")[0]+".list")>1000:
                os.system("rm "+info[0].split(".")[0]+".fasta")
        except OSError:
            print("Issues with "+info[0])
    elif info[0].split("_")[0]==info[1].split("_")[0]:
        #converting to fasta, deleting previous .fastqs
        os.system("perl -ne 'y/@/>/;print($_.<>)&&<>&&<>' "+info[0]+" > "+info[0].split(".")[0]+".fasta")
        os.system("perl -ne 'y/@/>/;print($_.<>)&&<>&&<>' "+info[1]+" > "+info[1].split(".")[0]+".fasta")
        os.remove(info[0])
        os.remove(info[1])
        #Making k-mer lists
        os.system("./glistmaker "+info[0].split(".")[0]+".fasta -w "+str(len_window)+" -o "+info[0].split(".")[0])
        os.system("./glistmaker "+info[1].split(".")[0]+".fasta -w "+str(len_window)+" -o "+info[1].split(".")[0])
        os.system("./glistcompare "+info[0].split(".")[0]+"_"+str(len_window)+".list "+info[1].split(".")[0]+"_"+str(len_window)+".list -u -o temp")
        os.system("rm "+info[0].split(".")[0]+"_"+str(len_window)+".list")
        os.system("rm "+info[1].split(".")[0]+"_"+str(len_window)+".list")
        try:
            if os.path.getsize("temp_"+str(len_window)+"_union.list")>1000:
                os.rename("temp_"+str(len_window)+"_union.list",info[0].split("_")[0]+".list")
                os.system("rm "+info[0].split(".")[0]+".fasta")
                os.system("rm "+info[1].split(".")[0]+".fasta")
        except OSError:
            print("Issues with "+info[0]+" and "+info[1])
print("Done at time: "+str(time.ctime(time.time())))
