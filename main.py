import os
import sys
import math
import heapq as hpq


class PriorityQ:

    def __init__(self,heap):
        self.pq = heap                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task

    def add_task(self,task, priority=0):
        'Add a new task or update the priority of an existing task'
        if task in self.entry_finder:
            self.remove_task(task)
        entry = [priority, task]
        self.entry_finder[task] = entry
        hpq.heappush(self.pq, entry)

    def remove_task(self,task):
        'Mark an existing task as REMOVED.  Raise KeyError if not found.'
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED
    
    def pop_task(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, task = hpq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return priority, task
        raise KeyError('pop from an empty priority queue')

class Node:

    def __init__(self):

        self.adj = []
        self.dist = math.inf
    

class Graph:

    def __init__(self):

        self.num_nodes = 0
        self.nodes = {}

    def init_graph(self,adj_list):
        
        lines = adj_list.readlines()
        for line in lines:
            line = line.strip()
            line_list = line.split()
            node_id = line_list[0]
            self.nodes[node_id] = Node()
            self.num_nodes += 1
            for edge in range(1,len(line_list)):
                edge_adj = line_list[edge].split(',')
                edge_id = edge_adj[0]
                edge_len = edge_adj[1]
                self.nodes[node_id].adj.append([edge_id,edge_len])
                

    def dji(self,start_v):
        my_q = []
        pq = PriorityQ(my_q)
        for v in self.nodes:
            if v == start_v:
                #heap_node = [0,v]
                pq.add_task(v,0)
                self.nodes[v].dist = 0
            else:
                pq.add_task(v,math.inf)
        

        # Shortest tree set
        STSet = []
        while len(STSet) != self.num_nodes:

           
            current_dist, current_v = pq.pop_task()
            STSet.append(current_v)
            for conn in self.nodes[current_v].adj:
                u = conn[0]
                w = conn[1]
                if (u not in STSet):
                    if current_dist + int(w) < pq.entry_finder[u][0]:
                        new_dist = current_dist + int(w)
                        pq.remove_task(u)
                        pq.add_task(u,new_dist)
                        self.nodes[u].dist = new_dist


def main(adj_file):


    adj_list = open(adj_file,'r')


    Gr = Graph()
    Gr.init_graph(adj_list)
    adj_list.close()

    print("Num Node = ", Gr.num_nodes)
    Gr.dji("1")
    out_list = []
    for dest in [7,37,59,82,99,115,133,165,188,197]:
        out_list.append(str(Gr.nodes[str(dest)].dist))

    print(",".join(out_list))
    
    
    return 0


if __name__ == "__main__":

    main(sys.argv[1])


