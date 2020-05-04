import networkx as nx
from networkx.algorithms.approximation import min_weighted_dominating_set
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import os
"""
def solve(G):
   # Args:
    #    G: networkx.Graph
    #Returns:
    #    T: networkx.Graph

    # TODO: your code here!
    #try to check whether there exists a node that connects all, if so, just output that
    supernode_degree = G.number_of_nodes() - 1
    for vertex in G.nodes():
        if len(list(G.neighbors(vertex)))==supernode_degree:
            Gspecial = nx.Graph()
            Gspecial.add_node(vertex)
            return Gspecial
    for vertex in G.nodes():
        if len(list(G.neighbors(vertex))) == supernode_degree - 1:
            Gspecial2 = nx.Graph()
            for n in list(G.nodes):
                if n not in list(G.neighbors(vertex)):
                    Gspecial2.add_weighted_edges_from(
                        [(
                            list(G.neighbors(n))[0], vertex, G[list(G.neighbors(n))[0]][vertex]['weight']
                        )]
                    )
                    print (len(list(Gspecial2.nodes())))
                    print (G[list(G.neighbors(n))[0]][vertex]['weight'])
                    if nx.is_dominating_set(G, Gspecial2.nodes):
                        print ("Hello")
                    return Gspecial2
        #if len(list(G.neighbors(vertex)))==supernode_degree-1:
        #    Gspecial2 = nx.Graph()
        #    Gspecial2.add_node(vertex)
            #find that special vertex
        #    for n in list(G.nodes()):
        #        if n not in list(G.neighbors(vertex)):
        #            Gspecial2.add_node(n)
        #            Gspecial2.add_edge(G[vertex][n])
        #            nnei = list(G.neighbors(n))
        #            Gspecial2.add_node(nnei[0])
        #            Gspecial2.add_edge(G[nnei[0]][n])
        #    return Gspecial2
                
    return pruning(nx.minimum_spanning_tree(G))
"""


#Checks for supernode that connects all, if so, just output that
def chkspecialcase(G):
    supernode_degree = G.number_of_nodes() - 1
    for vertex in G.nodes():
        if len(G[vertex]) == supernode_degree:
            return vertex
    return False
# ALT solve: Uses built-in min dominating set to reduce nodes for computation
# then runs built-in union find to merge and then MST + prune
# ALT2 solve: Uses built-in A* pathing to connect ranked list (by neighbor count)
def solve(G):
    domset = min_weighted_dominating_set(G)
    ranklist = [i for i in domset]
    ranklist.sort(reverse=True, key=lambda x: len(G[x]))

    graph3 = nx.Graph()
    special = chkspecialcase(G)
    if special:
        graph3.add_node(special)
        return graph3
    for j in ranklist:
        if j == len(ranklist) - 1:
            return graph3
        k = j +1
        while k < len(ranklist):
            if nx.has_path(G, j, k):
            #graph3.add_edges_from(astar_path(G, j, j + 1,G.edges()['weights']))
            #graph3.add_edges_from(nx.astar_path(G, j, j + 1))
                a = nx.astar_path(G, j, k)
                for i in range(len(a)-1):
                    graph3.add_weighted_edges_from([(a[i],a[i+1], G[a[i]][a[i+1]]['weight'])])
			k += 1
    return graph3

    #return pruning(graph3)


def pruning(Gr):
    vertexcounter = {}
    for edge in Gr.edges():
        (v1,v2) =  (edge[0],edge[1])
        if v1 in vertexcounter :
            vertexcounter[v1]+=1
        else:
            vertexcounter[v1] = 1
        if v2 in vertexcounter :
            vertexcounter[v2]+=1
        else:
            vertexcounter[v2] = 1

    for vertexcount in vertexcounter:
        if vertexcounter[vertexcount] == 1:
            Gr.remove_node(vertexcount)
    return Gr


#pass

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

#if __name__ == '__main__':
#    assert len(sys.argv) == 2
#    path = sys.argv[1]
#    G = read_input_file(path)
#    T = solve(G)
    #print(read_output_file(path, G))
#    assert is_valid_network(G, T)
   
#    print("Average pairwise distance: {}".format(average_pairwise_distance(T)))
#    write_output_file(T, 'output.out')
#    print(read_output_file('output.out', G))
if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs"
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        G = read_input_file(f"{input_dir}/{input_path}")

        T = solve(G)
        #print(read_output_file(input_path, G))
        assert is_valid_network(G, T)
        write_output_file(T, f"{output_dir}/{graph_name}.out")