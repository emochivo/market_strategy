'''
CECS 427 Project 4
Date: April 8, 2025
Written by: Chi Vo
'''

import argparse
import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy


'''FUNCTIONS'''

def market_strategy(G):
    
    # Extract node lists based on bipartite property
    node_list_A, node_list_B = [], []
    for node in G.nodes():
        if G.nodes[node]['bipartite'] == 0:
            node_list_A.append(node)
        else:
            node_list_B.append(node)
    
    # Initialize matrices
    valuation_matrix = [[None for _ in range(len(node_list_A))] for _ in range(len(node_list_B))]
    price = [G.nodes[i]['price'] for i in node_list_A]
    
    # Populate valuation matrix
    for edge in G.edges():
        source, target = int(edge[0]), int(edge[1])
        valuation_matrix[target-int(node_list_B[0])][source] = G.edges[edge]['valuation']

    # Calculate the layoff matrix
    layoff_matrix = deepcopy(valuation_matrix)
    chosen_node_in_A = []; temp = []
    price_each_round = []
    layoff_each_round = []
    iterations = 0
    max_iterations = len(node_list_A) * len(node_list_B)  # Safety limit
    
    while len(set(temp)) < len(node_list_A) and iterations < max_iterations:
        # Reset choices for this iteration
        temp = []
        
        # Find maximum value choices
        for i in range(len(layoff_matrix)):
            if any(v is not None for v in layoff_matrix[i]):
                max_val = max((v for v in layoff_matrix[i] if v is not None), default=None)
                if max_val is not None:
                    chosen_idx = layoff_matrix[i].index(max_val)
                    temp.append(chosen_idx)
        chosen_node_in_A.append(temp)
        
        # Update prices for items with multiple buyers
        for node in set(temp):
            if temp.count(node) > 1:
                price[node] += 1
        price_each_round.append(price.copy())
                
        # Update layoff matrix
        for i in range(len(layoff_matrix)):
            for j in range(len(layoff_matrix[i])):
                if valuation_matrix[i][j] is not None:
                    layoff_matrix[i][j] = valuation_matrix[i][j] - price[j]
        layoff_each_round.append(deepcopy(layoff_matrix))

        iterations += 1
    
    return price_each_round, layoff_each_round, chosen_node_in_A
        

def plot(G):

    G_copy = deepcopy(G)

    # Get the price last round and the last chosen nodes
    price_each_round, layoff_each_round, chosen_nodes = market_strategy(G_copy)[0][-1], market_strategy(G_copy)[1][-1], market_strategy(G_copy)[-1][-1]  

    # Add the attribute 'color' to the edges of the graph
    for edge in G_copy.edges():
        G_copy.edges[edge]['color'] = 'black'
        G_copy.edges[edge]['weight'] = 1.0

    # Change the color of the edges that are chosen in the market strategy to red
    for i in range(len(chosen_nodes)):
        G_copy[str(chosen_nodes[i])][str(i+3)]['color'] = 'red'
        G_copy[str(chosen_nodes[i])][str(i+3)]['weight'] = 2.0

    node_list_A, node_list_B = [], []
    for node in G_copy.nodes():
        if G_copy.nodes[node]['bipartite'] == 0:
            node_list_A.append(node)
        else:
            node_list_B.append(node)
    

    colors = [G_copy.edges[edge]['color'] for edge in G_copy.edges()]
    weights = [G_copy.edges[edge]['weight'] for edge in G_copy.edges()]
    # Create a layout for the nodes
    pos = nx.bipartite_layout(G_copy, nodes=node_list_A)
    nx.draw_networkx(G_copy, pos=pos, with_labels=True, \
                     font_size=9, node_size=260, font_color='#ffffff',edge_color=colors, width=weights)
    plt.title(G.name)
    plt.text(1, -1, f"Price: {price_each_round}", fontsize=10, ha='right')
    plt.text(1, -1.1, f"Layoff: {layoff_each_round}", fontsize=10, ha='right')
    plt.show()



def interactive(G):
    # Get the price last round and the last chosen nodes
    price_each_round, layoff_each_round, chosen_nodes = market_strategy(G)[0], market_strategy(G)[1], market_strategy(G)[-1] 
    print("Layoff each round: ", layoff_each_round)

    for k in range(len(price_each_round)):
        G_copy = deepcopy(G)
        # Add the attribute 'color' to the edges of the graph
        for edge in G_copy.edges():
            G_copy.edges[edge]['color'] = 'black'
            G_copy.edges[edge]['weight'] = 1.0

        # Change the color of the edges that are chosen in the market strategy to red
        for i in range(len(chosen_nodes[k])):
            G_copy[str(chosen_nodes[k][i])][str(i+3)]['color'] = 'red'
            G_copy[str(chosen_nodes[k][i])][str(i+3)]['weight'] = 2.0

        node_list_A, node_list_B = [], []
        for node in G_copy.nodes():
            if G_copy.nodes[node]['bipartite'] == 0:
                node_list_A.append(node)
            else:
                node_list_B.append(node)
        

        colors = [G_copy.edges[edge]['color'] for edge in G_copy.edges()]
        weights = [G_copy.edges[edge]['weight'] for edge in G_copy.edges()]
        # Create a layout for the nodes
        pos = nx.bipartite_layout(G_copy, nodes=node_list_A)
        nx.draw_networkx(G_copy, pos=pos, with_labels=True, \
                        font_size=9, node_size=260, font_color='#ffffff',edge_color=colors, width=weights)
        plt.title(f'Round {k+1}')
        plt.text(1, -1, f"Price: {price_each_round[k]}", fontsize=10, ha='right')
        plt.text(1, -1.1, f"Layoff: {layoff_each_round[k]}", fontsize=10, ha='right')
        plt.show()



'''MAIN CODE'''
parser = argparse.ArgumentParser(prog='market_strategy', description='Market Strategy Analysis')

parser.add_argument("inputfile", type=str)
parser.add_argument("--plot", action="store_true")
parser.add_argument("--interactive", action="store_true")


args = parser.parse_args()

if args.inputfile:
    inputFile = args.inputfile
    G = nx.read_gml(inputFile) # read the graph from the input .gml file

if args.plot:
    plot(G)

if args.interactive:
    interactive(G)