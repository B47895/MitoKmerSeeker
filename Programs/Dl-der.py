print("Run using nohup!! This will take DAYS!")
import os
read=open("todownload.txt","r")
for i in read.readlines():
    i=i.split(",")
    os.system("./sratoolkit/bin/prefetch "+i[0])

