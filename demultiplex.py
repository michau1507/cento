import csv
import os
import shutil
import gzip

barcodes = dict(csv.reader(open('samples.csv', 'r'), delimiter=','))


def mismatch(a,b):
	mismatches=[]
	l=len(a)	
	for i in list(range(0,l)):
		if a[i]!=b[i]:
			mismatches.append(i)	
	if len(mismatches)<=1:
		return a		
	else:
		return b



def demultiplexing(allowed):
#I didn't want to use readlines() function because uploading whole .fastq file consumes more memory. 
#Better iterate through file without uploading.  
	#with open('demultiplex.fastq', 'r') as file1: this line in case of file which is gunzipped, aso line 44 should be then removed
	with gzip.open('demultiplex.fastq.gz', 'rb') as file1:

		counter=0
		u_counter=0
		total_count=0
		unassigned_count=0

		line1=""
		line2=""
		line3=""
		line4=""

		u_line1=""
		u_line2=""
		u_line3=""
		u_line4=""

		for line in file1:
			line=line.decode("utf-8") # in case of gunzipped fastq file this line has to be removed

			if line.startswith('@') and counter==0 and allowed=="y" and any(value in mismatch(value,(line.split(':')[9].strip('\n'))) for value in barcodes.values()):		
				line1=line
				counter=1
			
			elif line.startswith('@') and counter==0 and allowed=="n" and any(value in line for value in barcodes.values()):
				line1=line
				counter=1

			elif counter==1:
				line2=line
				counter=2
		
			elif counter==2:
				line3=line
				counter=3
				
			elif counter==3:
				line4=line
				counter=0
				barcd=line1.split(':')[9].strip('\n')
				corrected_barcd=[value for value in barcodes.values() if value in mismatch(value,(barcd))][0]
				d_key=list(barcodes.keys())[list(barcodes.values()).index(corrected_barcd)]				
				total_count=total_count+1
			
				if allowed=="y":					
					with open(('demultiplexed_mismatch_allowed/'+d_key+'.fastq'),'a') as file2:
						file2.write(line1+line2+line3+line4)
				elif allowed=="n":
					with open(('demultiplexed_mismatch_not_allowed/'+d_key+'.fastq'),'a') as file2:
						file2.write(line1+line2+line3+line4)

#This part of function is to check if there are some unassigned reads (not matching to bracode in samples.csv) and mismatch of one base in barcode is not allowed. 
#Unassigned reads will be saved in seperate file.
			elif line.startswith('@') and u_counter==0 and allowed=="n" and (not any(value in line for value in barcodes.values())):
				u_line1=line
				u_counter=1
								

			elif u_counter==1:
				u_line2=line
				u_counter=2
				
				
			elif u_counter==2:
				u_line3=line
				u_counter=3
				
				
			elif u_counter==3:
				u_line4=line
				u_counter=0

				with open('demultiplexed_mismatch_not_allowed/unassigned.fastq','a') as file3:
					file3.write(u_line1+u_line2+u_line3+u_line4)

				total_count=total_count+1
				unassigned_count=unassigned_count+1

	assigned_count=total_count-unassigned_count

	print("{} percent reads have been assigned.".format(round(assigned_count*100/total_count,1)))

def talk():
	allowed=""
	allowed2=""
	allowed=input("Would you like to demultimlex with one mismatch allowed? (y/n/exit)").lower()
	if allowed == "y":
		print(allowed)
		shutil.rmtree('demultiplexed_mismatch_allowed', ignore_errors=True) #in case files exists already, they need to be deleted, so the reads are not duplicated there. 
		os.makedirs("demultiplexed_mismatch_allowed")
		demultiplexing(allowed)
	elif allowed =="n":
		print(allowed)
		shutil.rmtree('demultiplexed_mismatch_not_allowed', ignore_errors=True)
		os.makedirs("demultiplexed_mismatch_not_allowed")
		demultiplexing(allowed)
		allowed2=input("Would you like to demultimlex again with one mismatch allowed? (y/n)").lower()
		if allowed2 == "y":
			print(allowed2)
			shutil.rmtree('demultiplexed_mismatch_allowed', ignore_errors=True) 
			os.makedirs("demultiplexed_mismatch_allowed")
			demultiplexing(allowed2)
		else:
			pass


	elif allowed=="exit":
		pass	
	else:
		talk()

talk()