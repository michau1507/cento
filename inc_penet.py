import requests
from bs4 import BeautifulSoup
import csv
import time

lol = list(csv.reader(open('MIM_numbers.txt', 'r'), delimiter='\t'))
#print(lol)

only_mim=[]
for i in lol:
    only_mim.append(i[0])


l1=['128100']
l=['100050','128100','236100','615206','118450']
# 128100','236100','118450' - inc. penetrane present
# "615206",'100050' inc. penetrance not present



found_inc_p=[]
found_red_p=[]
n=0

#instead of l list we an use only_mim list which contains all entries in OMIM. 
# I added time.sleep(1) line to not overload the server too much. 

for i in l1:
    print(('https://www.omim.org/clinicalSynopsis/'+i))
    r=requests.get('https://www.omim.org/clinicalSynopsis/'+i)
    c=r.content


    soup=BeautifulSoup(c,'html.parser')


    all1=soup.find_all('div',{'id':'csMiscellaneous'})
    print(all1)

    for d in all1:
        #print (i.text)
        
        if 'incomplete penetrance' in str(d.text).lower():
            #print(str(d.text))
            found_inc_p.append(i)
            time.sleep(1)
            n=n+1
            print(n,i)

            
        elif 'penetrance' in str(d.text).lower():
            #print(str(d.text)+'everything')
            found_red_p.append(i)
            time.sleep(1)
            n=n+1
            print(n)

with open('found_inc_p.txt', 'w') as f:
    for i in found_inc_p:
        f.write("%s\n" % i)

with open('found_red_p.txt', 'w') as k:
    for i in found_red_p:
        k.write("%s\n" % i)

print(found_inc_p)
print(found_red_p)






"""
all=soup.find_all('div',{'class':'property-card-primary-info'})
all[0].find('a',{'class':'listing-price'}).text.replace('\n','').replace(' ','')
all

l=[]
for i in all:
    d={}
    d['Address']=(i.find('div',{'class':'property-address'}).text.replace('\n','').replace(' ',''))
    d['City']=(i.find('div',{'class':'property-city'}).text.replace('\n','').replace(' ',''))
    d['price']=(i.find('a',{'class':'listing-price'}).text.replace('\n','').replace(' ',''))
    try:
        d['bedrooms']=(i.find('div',{'class':'property-beds'}).find('strong').text)
    except:
        d['bedrooms']=None
    try:
        d['bathrooms']=(i.find('div',{'class':'property-baths'}).find('strong').text)
    except:
        d['bathrooms']=None
    try:
        d['square feet']=(i.find('div',{'class':'property-sqft'}).find('strong').text)
    except:
        d['square feet']=None  
    l.append(d)
for i in l:
    print(i)
"""