The lists of 32-mers inside this folder are in the GenomeTester4 tabular format with the 32-mer and its frequency (in the mitochondria) on the same line.

The k-mers were produced by the following steps:
1. Executing MitoDiff.py using the command "python MitoDiff.py <raw species names file name in the folder>" with the RefSeq mitochondria within the folder. Any files with the names "targets.txt", "nontargets.txt" and "repeated.txt" will be overwritten
2. Adding the repeated.txt species to nontargets.txt and moving the related species from targets.txt to nontargets.txt
3. Executing MitoIdent.py using the command "python MitoIdent.py targets.txt nontargets.txt" with the GenomeTester4 toolkit's programs glistmaker, glistquery and glistcompare in the folder 
4. Executing MitoBlast.py with the specific_kmers_32 txt files in the folder using the command "python MitoBlast.py /path/to/databases" where the path to databases leads to the nt, refseq_genomic and other_genomic databases.
5. Executing CloseSpecFinder.py using the command "python CloseSpecFinder.py" and previously running the commands given at the beginning of the program and following the instructions given by the code.
6. Executing Dl-der.py using the command "nohup python Dl-der.py &" with the file todownload.txt inside the folder.
7. Executing the commands "fastq-dump --skip-technical -F --split-3 SRR*" and "fastq-dump --skip-technical -F --split-3 ERR*"
8. Executing MitoFilter.py in the folder with the downloaded FASTQ files and k-mer lists using the command "python MitoFilter.py "It will convert ALL .fastq files in the folders into .list files using GenomeTester4.
