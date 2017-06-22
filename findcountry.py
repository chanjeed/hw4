# coding: utf-8
import codecs
def makecountryset(file_name):
	countryset=[]
	file=open(file_name,"r") 
	lines=file.readlines()
	for name in lines:
		name=name.strip()
		countryset.append(name)

	file.close()
	return countryset
def read_page(file_name,countryset):
	countrypage={}
	count=0
	file = open(file_name,"r")
	for line in file:
    		(name,num)=(line.split()[1],line.split()[0])
    		if name in countryset :
    			print name
    			countrypage.update({num:[name,0]})
    			count+=1
    	file.close()
    	return count,countrypage

def read_links(file_name,countrypage):
	file = open(file_name,"r")
	file2 = open("referred_country","w")
	for line in file:
		items=line.split()
		if items[1] in countrypage:
			countrypage[items[1]][1]+=1
	top_country=[]
	for key in countrypage:
		top_country.append([countrypage[key][0],countrypage[key][1]])
	top_country.sort(key=lambda x:x[1],reverse=True)
	for i in top_country:
		file2.write("%s %d\n"%(i[0],i[1]))
	file.close()
	file2.close()

def countlinkfromjapan(file_name,countrypage):
	file = open(file_name,"r")
	count=0
	for line in file:
		items=line.split()
		if items[0]=="927119" and items[1] in countrypage:
			count+=1		
	file.close()
	return count
	

countryset=makecountryset("countryname.txt")
(count,countrypage)=read_page("pages.txt",countryset)
print "There are ",count,"country in Wikipedia"
#read_links("links.txt",countrypage)
count=countlinkfromjapan("links.txt",countrypage)
print "You can link to",count,"country from Japan"