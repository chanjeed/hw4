import csv
import time
import math
import numpy as np
from scipy.sparse import lil_matrix, csr_matrix

#PAGE_NUM_MAX=1483276
PAGE_NUM_MAX=6

def read_page(file_name):
    pages=[]
    file = open(file_name, 'r')
    for line in file:
        (name,num)=(line.split()[1],line.split()[0])
        pages.append({"name":name,"id":int(num)})
    file.close()
    
    return pages

def find_id(pages,page_name):
    first=0
    last=len(pages)-1
    found=False
    page_id=-1

    while first<=last and not found: 
    
        mid=(first+last)/2
        if pages[mid]['name']==page_name:
            found=True
            page_id=pages[mid]['id']

        else:
            if page_name<pages[mid]['name']:
                last=mid-1
            else:
                first=mid+1
    
    if found:
        return page_id
    else:
        print "Not found %s"%(page_name)
        return -1

def find_name(pages,page_id):
    return pages[page_id]['name']

def read_link(file_name):
    origin=[]
    destination=[]
    link_num=np.zeros(PAGE_NUM_MAX+1,dtype=np.uint32)
    file = open(file_name, 'r')
    for line in file:
        node1,node2=line.split('\t')
        print node1,node2
        origin.append(int(node1))
        destination.append(int(node2))
        link_num[int(node1)]+=1
    file.close()
    graph = lil_matrix((PAGE_NUM_MAX+1,PAGE_NUM_MAX+1), dtype = np.uint32)
    for k in range(len(origin)):
        if k % 5000000 == 0:
            print('link', k)
        graph[destination[k], origin[k]] = 1    
    graph= graph.tocsr()
    return graph         
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enq(self, item):
        self.items.append(item)

    def deq(self):
        try:
            val=self.items[0]
            if len(self.items)==1:
                self.items=[]
            else:
                self.items=self.items[1:]
        except:
            pass
        return val

    def size(self):
        return len(self.items)    

def bfs(graph, start, end):
    temp_path=[start]
    # maintain a queue of paths
    q=Queue()
    # push the first path into the queue
    q.enq(temp_path)
    while (q.isEmpty()!=True):
        temp_path=q.deq()
        last_node=temp_path[len(str(temp_path))-1]

        # path found
        if last_node == end:
            return temp_path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
    
        for i in range(PAGE_NUM_MAX+1):
            if graph[i,last_node]==1:
                q.enq(i)

    print "Not found path"
    return []

start=time.clock()
pages=read_page("pages.txt")
end=time.clock()
print "FINISH READ PAGES time= ",end-start," [s]"
import operator
pages_sorted_name=sorted(pages,key=operator.itemgetter('name'))#Sort pages by Alphabet order

start=time.clock()
graph=read_link("links_mini.txt")
end=time.clock()
print "FINISH READ LINKS time= ",end-start," [s]"
while(1):
    page_name=raw_input("Find page: ")
    id1=find_id(pages_sorted_name,page_name)
    if id1==-1:
        continue
    page_name=raw_input("To page: ")
    id2=find_id(pages_sorted_name,page_name)
    if id2==-1:
        continue
    print "FIND ",id1,id2
    print graph
    path=bfs(graph,id1,id2)
    if path!=[]:
        print "Found path: ",path