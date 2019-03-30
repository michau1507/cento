from Tkinter import *
import os
import sys


# import backend


# os.chdir('//srv-files//NGS-SeqData//mzawada//')

# family to use for archive: 2257970
# order for archive 62462210

# guido case:62463287, 2258936, 62463292
# michal case:62466148, 2261331, 62466152


def Get_Files():
    list1.delete(0,END)
    vcf1 = None
    vcf2 = None
    file_name = None
    # global order1
    # global family1
    order1 = order_id1.get().strip()
    family1 = family_id1.get().strip()
    analysis1 = analysis_type1.get().strip()
    final_file_name = output_file_name.get()
    filelist1 = []
    # //srv-files//NGS-SeqData//archive_files_dc.txt
    # list3_62456308_removed.txt (use 62456311)
    with open('//srv-files//NGS-SeqData//archive_files_dc.txt', 'r') as file1:
        for line in file1:
            if order1 in line and order1 != '':
                filelist1.append(line)

    show_lines1 = [i.strip('\n') for i in filelist1]
    # print(order1+'empty')

    vcf_files1 = []
    for i in show_lines1:
        if i.endswith('.hpcl.fboth.pass.vcf'):
            vcf_files1.append(i)
        elif i.endswith('.vcf') and analysis1 == 'WGS':
            vcf_files1.append(i)

    global order2
    global family2
    order2 = order_id2.get().strip()
    family2 = family_id2.get().strip()
    analysis2 = analysis_type2.get().strip()
    filelist2 = []
    with open('//srv-files//NGS-SeqData//archive_files_dc.txt', 'r') as file2:
        for line in file2:
            if order2 in line and order2 != '':
                filelist2.append(line)

    show_lines2 = [i.strip('\n') for i in filelist2]
    # print(show_lines)

    vcf_files2 = []
    for i in show_lines2:
        if i.endswith('.hpcl.fboth.pass.vcf'):
            vcf_files2.append(i)
        elif i.endswith('.vcf') and analysis2 == 'WGS':
            vcf_files2.append(i)

    # print(unique_lines)

    # /shares/seqshare/180329_K00541_0078_BHTKCNBBXX/Fastq/WESAGI/62454633_S10/62454633_S10.hpcl.fboth.pass.vcf
    # /shares/seqshare/180405_K00541_0080_BHTTV7BBXX/Fastq/WESAGI/62456308_S32/logs/62456310_S32.07.bcfc.bgzip.al.err
    example_for_file_list = '62456308'
    example_for_family_archive = '22234556'

    for i in vcf_files1:
        if order1 in i:
            vcf1 = i
        else:
            pass
    # //shares//archive//vcfarchive//vcfbackup//
    arch_dir1 = r"\\app0017.gelb.centogene.internal\\vcfarchive\\vcfbackup\\" + family1[-2:] + "\\" + family1

    if vcf1 == None and os.path.exists(arch_dir1) == True:
        for file in os.listdir(arch_dir1):
            if file.endswith('hpcl.fboth.pass.vcf.gz') and order1 in file:
                vcf1 = '/shares/archive/vcfarchive/vcfbackup/' + family1[-2:] + "/" + family1 + "/" + file
            elif file.endswith('.vcf.gz') and order1 in file and analysis1 == 'WGS':
                vcf1 = '/shares/archive/vcfarchive/vcfbackup/' + family1[-2:] + "/" + family1 + "/" + file

    for i in vcf_files2:
        if order2 in i:
            vcf2 = i
        else:
            pass

    arch_dir2 = r"\\app0017.gelb.centogene.internal\\vcfarchive\\vcfbackup\\" + family2[-2:] + "\\" + family2

    if vcf2 == None and os.path.exists(arch_dir2) == True:
        for file in os.listdir(arch_dir2):
            if file.endswith('hpcl.fboth.pass.vcf.gz') and order2 in file:
                vcf2 = '/shares/archive/vcfarchive/vcfbackup/' + family2[-2:] + "/" + family2 + "/" + file
            elif file.endswith('.vcf.gz') and order2 in file and analysis2 == 'WGS':
                vcf2 = '/shares/archive/vcfarchive/vcfbackup/' + family2[-2:] + "/" + family2 + "/" + file

    # new_family_folder1=r'//srv-files//NGS-SeqData//mzawada//vcf_compare_files//'+family1

    # if not os.path.exists(new_family_folder1):
    #	os.makedirs(new_family_folder1)

    # outfile=new_family_folder1

    if final_file_name != '':
        file_name = final_file_name
    else:
        file_name ='order1_vs_order2'

    new_family_folder1 = r'//srv-files//NGS-SeqData//vcf_comparison_results//' + family1
    if not os.path.exists(new_family_folder1):
        os.makedirs(new_family_folder1)

    quality = None
    if analysis1 == 'WGS':
        quality='30,100,10,4'
    else:
        quality='30,100,20,4'



    bed_WESAGI='/data/production/stable/data/regions/S07604514_Regions_merged.bed'
    bed_WESILLU='/data/production/stable/data/regions/nexterarapidcapture_exome_targetedregions_v1.2.bed'
    bed_CESEX='/data/production/stable/data/regions/TSOne_BaseAddOn_TargetedRegions.merged.bed'

    if analysis1 == 'WESILLU':
        bed1 = bed_WESILLU
    elif analysis1 == 'CESEX':
        bed1 = bed_CESEX
    else:
        bed1 = bed_WESAGI

    if analysis2 == 'WESILLU':
        bed2 = bed_WESILLU
    elif analysis2 == 'CESEX':
        bed2 = bed_CESEX
    else:
        bed2 = bed_WESAGI




    script = "python /data/production/stable/vcf_compare.py --vcf1="+vcf1+" --vcf2="+vcf2+" --outfile=/data/NGS-SeqData/vcf_comparison_results/"+family1+"/"+file_name+".txt --bed1="+bed1+" --bed2="+bed2+" --qual="+quality+" --no-debug"

    list1.insert(END, (vcf1), (vcf2), (script))

    return vcf1, vcf2, family1, file_name


def show_results():
    import csv
    import glob

    family1 = family_id1.get().strip()

    final_file_name = output_file_name.get()

    if final_file_name != '':
        file_name=final_file_name
    else:
        file_name='order1_vs_order2'

    #option to take file by file name
    saved_results='//srv-files//NGS-SeqData//vcf_comparison_results//'+family1+'//'+file_name+'.txt'

    check_results_text='You are checking results for:'
    check_results_info='/srv-files//NGS-SeqData/vcf_comparison_results/'+family1+'/'+file_name+'.txt'


    #option to take the oldest file to display
    #list_of_files=glob.glob(r'//srv-files//NGS-SeqData//vcf_comparison_results//'+family1+'//*')
    #latest_file = max(list_of_files, key=os.path.getctime)


    try:
        with open(saved_results, 'r') as f:
            reader = csv.reader(f, delimiter="\t")
            d = list(reader)

            #no_filters_file1 = 'No filters file1: ' + d[2][9]
            #no_filters_file2 = 'No filters file2: ' + d[2][10]

            #by_bed_file1 = 'By bed file1: ' + d[2][18]
            #by_bed_file2 = 'By bed file2: ' + d[2][19]

            #by_SNP_file1 = 'By SNP file1: ' + d[2][27]
            #by_SNP_file2 = 'By SNP file2: ' + d[2][28]

            nice_table=[['Filters','all variants','good qual'],
                        ['---------------', '---------------', '---------------'],
                        ['No filters file1',d[2][9],'-'],
                        ['No filters file2',d[2][10],'-'],
                        ['By bed file1',d[2][18],d[2][45]],
                        ['By bed file2',d[2][19],d[2][46]],
                        ['By SNP file1',d[2][27],d[2][55]],
                        ['By SNP file2',d[2][28],d[2][56]]]
            #headers=['Filters','all variants','good qual']

        row_format = "{:<20} {:>20} {:>20}"

        # list1.insert(END, (no_filters_file1), (no_filters_file2), (by_bed_file1), (by_bed_file2), (by_SNP_file1), (by_SNP_file2))
        # list1.insert(0,row_format.format(*headers,sp=" "*2))

        list1.insert(END, (check_results_text), (check_results_info), (''))

        for i in nice_table:
            list1.insert(END, row_format.format(*i, sp=" " * 2))


    except IOError:
        error_text='Wrong output_file_name. Please use file from below availabe files for choosen '+family1+' family without .txt extension:'
        av_files_list=os.listdir('//srv-files//NGS-SeqData//vcf_comparison_results//'+family1)

        list1.insert(END, (error_text))
        for i in av_files_list:
            list1.insert(END, (i))













# vcf1_put='/shares/seqshare/180502_K00541_0083_AHV5LHBBXX/Fastq/WESAGI/62463287_S28/62463287_S28.hpcl.fboth.pass.vcf'
# vcf2_put='/shares/seqshare/180502_K00541_0083_AHV5LHBBXX/Fastq/WESAGI/62463292_S29/62463292_S29.hpcl.fboth.pass.vcf'

# below function use to connect with vcf_compare.py
# def test():
#	paths = Get_Files()
#
#	vcf1_put=paths[0]
#	vcf2_put=paths[1]



window = Tk()

window.wm_title('VCFcompare')

l1 = Label(window, text='Person 1')
l1.grid(row=0, column=1)

l2 = Label(window, text='Order ID')
l2.grid(row=1, column=0)

l3 = Label(window, text='Family ID')
l3.grid(row=2, column=0)

l4 = Label(window, text='Analysis type')
l4.grid(row=3, column=0)

l5 = Label(window, text='bed file*')
l5.grid(row=4, column=0)

l6 = Label(window, text='Person 2')
l6.grid(row=0, column=2)

l7 = Label(window, text='Output file name')
l7.grid(row=5, column=0)

l8 = Label(window, text='qual')
l8.grid(row=6, column=0)

l8 = Label(window, text='WESAGI/WESILLU/WGS/CESEX')
l8.grid(row=3, column=3)


order_id1 = StringVar()
e1 = Entry(window, textvariable=order_id1)
e1.grid(row=1, column=1)

family_id1 = StringVar()
e2 = Entry(window, textvariable=family_id1)
e2.grid(row=2, column=1)

analysis_type1 = StringVar()
e3 = Entry(window, textvariable=analysis_type1)
e3.grid(row=3, column=1)

bed_file1 = StringVar()
e4 = Entry(window, textvariable=bed_file1)
e4.grid(row=4, column=1)

order_id2 = StringVar()
e5 = Entry(window, textvariable=order_id2)
e5.grid(row=1, column=2)

family_id2 = StringVar()
e6 = Entry(window, textvariable=family_id2)
e6.grid(row=2, column=2)

analysis_type2 = StringVar()
e7 = Entry(window, textvariable=analysis_type2)
e7.grid(row=3, column=2)

bed_file2 = StringVar()
e8 = Entry(window, textvariable=bed_file2)
e8.grid(row=4, column=2)

output_file_name = StringVar()
e9 = Entry(window, textvariable=output_file_name)
e9.grid(row=5, column=1)

qual_stats = StringVar()
e10 = Entry(window, textvariable=qual_stats)
e10.grid(row=6, column=1)

b1 = Button(window, text='Get files', width=12, command=Get_Files)
b1.grid(row=7, column=0)

b2 = Button(window, text='Compare', width=12)
b2.grid(row=7, column=1)

b3 = Button(window, text='Clear', width=12)
b3.grid(row=7, column=2)

b4 = Button(window, text='Check results', width=12, command=show_results)
b4.grid(row=7, column=3)

list1 = Listbox(window, selectmode='extended', height=15, width=150)
list1.grid(row=8, column=0, rowspan=6, columnspan=6)

window.mainloop()
