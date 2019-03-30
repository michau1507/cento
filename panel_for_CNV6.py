from Tkinter import *
import time
import pandas as pd
import os
from openpyxl import load_workbook


family_id=None
order_id=None

"""

ILLU='//srv-files//NGS-SeqData//Illumina//{}'.format(familyID)
print(ILLU)
print(os.path.exists('//srv-files//NGS-SeqData//Illumina//'))


if os.path.exists(ILLU) == True:
	for file in os.listdir(ILLU):
		if file.endswith('.xls') and orderID in file:


		df=pd.read_excel('test_CNV.xls')

		df=pd.DataFrame(df)
		#print(df['Approved Symbol'])

		a=['CFAP74','PRDM16','FAM231C'] CFAP74,PRDM16,FAM231C,AGRN
		df2=df[df['Approved Symbol'].apply(lambda x: any(i in x for i in a))]
		df2.to_excel('output.xlsx')
		62516442 2305019
		Genome: 2302292 62514081
		2307232 62519070

"""

df=pd.read_excel('panels_and_genes.xlsx')
df=pd.DataFrame(df)
dic=pd.Series(df.genes.values,index=df.panels).to_dict()
dic=dict((k.encode('utf-8'),v.encode('utf-8').replace(' ','').split(',')) for (k,v) in dic.items())



def create_file():

	familyID=family_id.get().strip()
	orderID=order_id.get().strip()
	ILLU='//srv-files//NGS-SeqData//Illumina//{}'.format(familyID)
	print(ILLU)
	print(os.path.exists('//srv-files//NGS-SeqData//Illumina//'))
	b=[]
	file_list=[]
	if os.path.exists(ILLU) == True:
		for file in os.listdir(ILLU):
			if len(cust_file.get())==0 and var1.get()==0 and file.endswith('.xls') and (orderID+'_Patient-CNMOPS' in file) and (file not in file_list):
				file_list.append(os.path.join(ILLU,file))
								
			elif len(cust_file.get())==0 and var1.get()==1 and file.endswith('.xls') and ((familyID+'_Family-CompleteReport' in file) or (orderID+'_Patient-CompleteReport' in file)) and (file not in file_list):
				file_list.append(os.path.join(ILLU,file))
				
			elif cust_file.get()!='' and (os.path.join(ILLU,cust_file.get()) not in file_list):
				file_list.append(os.path.join(ILLU,cust_file.get()))
	
				
	if len(file_list)!=0:

		try:
			latest_file = max(file_list, key=os.path.getctime)				
		except WindowsError:
			list1.delete(0,END)
			list1.insert(END,'File not found.')


						
		df=pd.read_table(latest_file,encoding='latin-1')
		df=pd.DataFrame(df)
		
		sel_panels=list2.get(0,END)
		for i in sel_panels:
			if i not in dic.keys():
				for k in i.split(','):
					b.append(k.strip())
			if i in dic.keys():
				b=b+dic[i]

		print(b)
		print(file_list)
		print(latest_file[44:])
		print(cust_file.get())
		
		
		def checker(x):
			splited=x.split(',')
			return (any(i in splited for i in b))

		#df2=df[df['Approved Symbol'].apply(checker)]
		df2=df[df['Approved Symbol'].apply(lambda x: any(i in x for i in b))]

		path=ILLU+'//'+orderID+'_SV_filtered_'+'.xlsx'
		writer = pd.ExcelWriter(path, engine='openpyxl')
		#book = load_workbook(ILLU+orderID+'_'+familyID+'SV_filtered.xlsx')
		#writer.book = book
		#df.to_excel(writer, sheet_name='Unfiltered')
		df2.to_excel(writer, sheet_name='Filtered')
		writer.save()
		writer.close()

		#writer = pd.ExcelWriter(ILLU+orderID+'_'+familyID+'SV_filtered.xlsx')
		#df.to_excel(writer,'unfiltered')
		#df2.to_excel(writer,'filtered')
		#writer.save()
		print(sel_panels)

		list1.delete(0,END)
		list1.insert(END,'Used file:')
		list1.insert(END,latest_file[44:])

	else:
		list1.delete(0,END)
		list1.insert(END,'File not found. Try to use custom file field.')


def search():
	list1.delete(0,END)
	for i in dic.keys():
		if panel.get().lower() in i.lower():
			list1.insert(END,i)


def add_panel():
	try:
		index=list1.curselection()[0]
		selected_tuple=list1.get(index)
		list2.insert(END, selected_tuple)
	except IndexError:
		pass

def remove():
	try:
		index=list2.curselection()[0]
		list2.delete(index)
	except IndexError:
		pass


def add_genes():
	genes=gene_list.get()
	list2.insert(END, genes)
	e4.delete(0,END)

def clear():
	list2.delete(0,END)
	e1.delete(0,END)
	e2.delete(0,END)
	e5.delete(0,END)



window = Tk()

window.wm_title("Panel_for_CNV")

l1 = Label(window, text='Order ID*')
l1.grid(row=0, column=0)

l2 = Label(window, text='Family ID*')
l2.grid(row=1, column=0)

l3 = Label(window, text='Custom file:')
l3.grid(row=0, column=3)

l4 = Label(window, text="(* - required)")
l4.grid(row=2, column=0)


order_id = StringVar()
e1 = Entry(window, textvariable=order_id)
e1.grid(row=0, column=1)

family_id = StringVar()
e2 = Entry(window, textvariable=family_id)
e2.grid(row=1, column=1)

panel=StringVar()
e3 = Entry(window, textvariable=panel, width=60)
e3.grid(row=4, column=0, columnspan=3)

gene_list=StringVar()
e4 = Entry(window, textvariable=gene_list, width=60)
e4.grid(row=4, column=4,columnspan=3)

cust_file = StringVar()
e5 = Entry(window, textvariable=cust_file, width=60)
e5.grid(row=0, column=4, columnspan=2)



b1 = Button(window, text='Create a file!', width=12, command=create_file)
b1.grid(row=2, column=3)

b2 = Button(window, text='Clear', width=12, command=clear)
b2.grid(row=4, column=3)

b3 = Button(window, text='Add ->', width=12, command=add_panel)
b3.grid(row=5, column=3)

b4 = Button(window, text='Search', width=12, command=search)
b4.grid(row=3, column=0)

b5 = Button(window, text='Add genes',width=12, command=add_genes)
b5.grid(row=3, column=4)

b6 = Button(window, text='Remove', width=12, command=remove)
b6.grid(row=6, column=3)

var1 = IntVar()
c1 = Checkbutton(window, text='WGS', variable=var1)
c1.grid(row=2, column=1)

list1 = Listbox(window, selectmode='extended', height=15, width=60)
list1.grid(row=5, column=0, rowspan=14, columnspan=3)

list2 = Listbox(window, selectmode='extended', height=15, width=60)
list2.grid(row=5, column=4, rowspan=14, columnspan=3)


window.mainloop()