#!/usr/bin/python3.7

import os
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    G = nx.read_graphml("callgraph.graphml")
    nx.draw(G)

