import numpy as np
import time

PAGE_NUM_MAX=1483276


def read_page(file_name):
    pages=[]
    file = open(file_name, 'r')
    for line in file:
        (name,num)=(line.split()[1],line.split()[0])
        pages.append({"name":name,"id":num})
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
        return page_id

def find_name(pages,page_id):
    return str(pages[page_id]['name'])
def read_link(file_name):
    graph={}
    file = open(file_name, 'r')
    for line in file:
        node1,node2=line.split()
        print node1,node2
        if node1 not in graph:
            graph.update({node1:[]})
        graph[node1].append(node2) 
    file.close()
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
        last_node=temp_path[len(temp_path)-1]

        # path found
        if last_node == end:
            return temp_path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        if last_node  in graph.keys() and graph[last_node]!=[]:
            for next in graph[last_node]:
                if next not in temp_path:
                    new_path = []
                    new_path = temp_path + [next]
                    q.enq(new_path)
    print "Not found path"
    return []
start=time.clock()
pages=read_page("pages.txt")
end=time.clock()
print "FINISH READ PAGES time= ",end-start," [s]"
import operator
pages_sorted_name=sorted(pages,key=operator.itemgetter('name'))#Sort pages by Alphabet order
start=time.clock()
graph=read_link("links.txt")
end=time.clock()
print "FINISH READ LINKS time= ",end-start," [s]"
while(1):
    page_name=raw_input("Find page: ")
    id1=find_id(pages_sorted_name,page_name)
    page_name=raw_input("To page: ")
    id2=find_id(pages_sorted_name,page_name)
    path=bfs(graph,id1,id2)
    if path!=[]:
        print "Found path: "
        for id in path:
            print find_name(pages,int(id))+">>"