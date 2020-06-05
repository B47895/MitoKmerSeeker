# cat mitochondrion.1.1.genomic.fna > database.txt
# cat mitochondrion.2.1.genomic.fna >> database.txt
# module load blast-2.9.0+
#makeblastdb -in database.txt -dbtype nucl -parse_seqids
#blastn -query targets.txt -db database.txt -out blasted_targets.txt -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -perc_identity 20 -num_threads 20
Out=open("blasted_targets.txt","r")
out=Out.readlines()
count=-1
eelmine=""
badsymbols=["[","]","(",")",",",">"]
tncs=[] #Targets and close species
limit=30
#Target Blast Result Analyser
for i in out:
    i=i.split("	")
    if i[0]!=eelmine:
        eelmine=i[0]
        count+=1
        tncs.append([i[0],[],[]]) #Name, close species families, close species.
        if i[0]==i[1]:
            j=i[-1].split(" ")
            tncs[count][0]=j[1]+" "+j[2]
    if len(tncs[count][2]) >= limit:
        limit=30
        continue
    if i[0]!=i[1]:
        add=i[-1].split(" ")[1]
        for k in badsymbols:
            add=add.replace(k,"")
        if add in tncs[count][1]: #If the family of the species is in the species list
            limit+=1
        else:
            tncs[count][1].append(add)
        k=i[-1].split(" ")
        if " x " in i[-1]:
            add=k[1]+" "+k[2]+" "+k[3]+" "+k[4]+" "+k[5]
        else:
            add=k[1]+" "+k[2] 
        for k in badsymbols:
            add=add.replace(k,"")
        if add not in tncs[count][2]:
            tncs[count][2].append(add)
        else:
            limit+= -1 #We didn't check for the same name as the last row before, so now we are
        #print(tncs[count][0]+" match "+i[-1]+" perc ident "+i[2])
for j in range(len(tncs)):
    tncs[j][2]=list(set(tncs[j][2]))
    print(tncs[j][0]+" nr of targets is: "+str(len(tncs[j][2])))
targets=[]
allelse=[]
for i in tncs:
    targets.append(i[0])
    for j in i[2]:
        allelse.append(j)
        allelse=list(set(allelse))
word=""
for i in allelse:
    word+="OR "+i+"[Organism] "
word=word[3:]
#for i in targets:
    #word+=" NOT "+i+"[Organism]"
word+=""" AND ("biomol dna"[Properties] AND "platform illumina"[Properties] AND "filetype fastq"[Properties])"""
print("Search for the following phrase in the SRA database (https://www.ncbi.nlm.nih.gov/sra)")
print(word)
print("Then download the sra_result.csv by pressing send to in the upper right corner of the results, then choose the destination as file and format as Run info. Download the file to the same folder as this program")
print("Once you have completed this step, press y and enter. NB! you MUST have the file SraRunInfo.csv in the folder, otherwise the program will give an error.")
y="y"
if input("")=="y":
    print("Searching for an appropriate set of files from sra_result.csv...")
else:
    print("There are no further instructions and the program shall still continue..")
Sra=open("SraRunInfo.csv","r")
sralist=[[],[]]
for i in Sra.readlines(): #Searching the sra file for best matches
    i=i.split(",")
    if len(i)<10:
        continue
    try:
        if int(i[7])>20000:
            #print(i[28])
            continue
    except ValueError:
        continue
    if i[28] in sralist[0]:
        for j in sralist[1]:
            if j[0]==i[28]:
                if j[2]<float(i[4]): #Comparing total bases and selecting the best
                    sralist[1].remove(j)
                    sralist[1].append([i[28],i[0],float(i[4])])
                    break #No need to check the list more
                else:
                    break
    elif i[28] in word:
        #print(i[28])
        sralist[0].append(i[28])
        sralist[1].append([i[28],i[0],float(i[4])])
wordlist=[[],[]] #For dl-ding
switch=0
for i in tncs:
    count=0
    for j in i[2]: #Searching through each species' close species
        if count>=5:
            break
        elif j in sralist[0]:
            count+=1
            if j not in wordlist[0]: #Seeing if it is in the previously made list and not already in the wordlist
                for k in sralist[1]: #Searching for the code
                    if j==k[0]:
                        switch=1
                        wordlist[0].append(j)
                        wordlist[1].append(k[1]+","+k[0])
                        break
                if switch==0:
                    print("Error: something's wrong. In coding..")
                switch=0
    if count==0:
        print("Error: Species "+i[0]+" still has no results in the SRA database. Oh no.")
        #print(i[2])
    else:
        print("Species "+i[0]+" has "+str(count)+" results in the SRA database.")
print("If this process has completed without any printed error messages, you are in luck. If it has and gave the Oh no message,")
print("Please increase the limit by n on 11th and 23rd lines of the code")
print("If not, you are free to run the downloading program")
print("")
todownload=open("todownload.txt","w")
for i in wordlist[1]:
    todownload.write(i+"\n")
todownload.close()
print(sralist)
    
    
