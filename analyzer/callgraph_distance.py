#!/usr/bin/python3.7

import os
import csv
import networkx as nx

if __name__ == "__main__":

    G = nx.read_graphml("/home/yanxx297/Project/crix/analyzer/build/lib/callgraph.graphml")
    corpus ={} 
    cutoff = nx.number_of_nodes(G)
    
    # store nodes in a dictionary for quick search
    nodes = {}
    for n in G.nodes:
        nodes[(G.nodes[n]['filename'], G.nodes[n]['funcname'])] = n

    # map syzkaller corpus to callgraph
    ccover = "/home/yanxx297/Project/mose/workdir/test"
    files = os.listdir(ccover)
    for file in files:
        with open(os.path.join(ccover, file)) as f:
            cf = csv.reader(f)
            for row in cf:
                id = (row[0],row[1])
                if id in nodes:
                    n = nodes[id]
                    G.nodes[n]['covered'] = True
                    if n not in corpus:
                        corpus[n] = {}
                    corpus[n][file] = None

    # find covered nodes nearby the crash
    target = nodes[("net/netfilter/nf_tables_api.c", "nf_tables_commit")]
    path = nx.single_source_shortest_path(G, target, cutoff)
    res = []
    for target in path :
        if G.nodes[target]['covered'] :
            res.append((target, path[target]))
            
    for n,p in res:
        print(n, p)
        for prog in corpus[n]:
            print(prog)
