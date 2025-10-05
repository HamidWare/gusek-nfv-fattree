import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


k = 4
G = nx.Graph()

count = 0

# Servers
servers = []
for pod in range(k):
    for sw in range(k // 2):
        for srv in range(k // 2):
            server = str(count)
            servers.append(server)
            G.add_node(server, type='Server')
            count += 1

# Edge Switches
edge_switches = []
for pod in range(k):
    for sw in range(k // 2):
        edge = str(count)
        edge_switches.append(edge)
        G.add_node(edge, type='Edge')
        count += 1

# Aggregation Switches
agg_switches = []
for pod in range(k):
    for sw in range(k // 2):
        agg = str(count)
        agg_switches.append(agg)
        G.add_node(agg, type='Agg')
        count += 1

# Core Switches
core_switches = []
for i in range((k // 2) ** 2):
    core = str(count)
    core_switches.append(core)
    G.add_node(core, type='Core')
    count += 1

# Connect Servers to Edge Switches
for i, edge in enumerate(edge_switches):
    for server in servers[i * (k // 2):(i + 1) * (k // 2)]:
        G.add_edge(edge, server)

# Connect Edge to Aggregation
for pod in range(0, len(edge_switches), k // 2):
    for i, edge in enumerate(edge_switches[pod:pod + (k // 2)]):
        for j, agg in enumerate(agg_switches[pod:pod + (k // 2)]):
            G.add_edge(edge, agg)
            # make sure node 24 connects to nodes 32 and 33
            if j == 0:
                G.add_edge(agg, core_switches[i])
            elif j == 1:
                G.add_edge(agg, core_switches[i + (k // 2)])
                
                
# specific colors based on node types
node_colors = {
    'Server': 'yellow',
    'Edge': 'green',
    'Agg': 'blue',
    'Core': 'red',
}

# Generate the table
table_rows = []
for node1, node2 in G.edges():
    random_number = np.random.randint(10, 99)  # Generate random number between 10 and 100 inclusive
    table_rows.append([node1, node2, random_number])


# Create a Pandas DataFrame from the list of rows
df = pd.DataFrame(table_rows, columns=['Node1', 'Node2', 'RandomNumber'])

# Save the DataFrame
df.to_csv('cost of each link.csv', index=False, sep=' ')


# Show the DataFrame
print("Status Table:")
print(df)

print("Fat Tree Graph:")

# Arrange nodes in layers
layers = {
    'Core': core_switches,
    'Agg': agg_switches,
    'Edge': edge_switches,
    'Server': servers
}

pos = {}
y_pos = 0
for layer_name, nodes in layers.items():
    x_pos = 0
    for node in nodes:
        pos[node] = (x_pos, y_pos)
        x_pos += 1
    y_pos -= 1

nx.draw(G, pos, with_labels=True, node_size=1000, node_color=[node_colors[G.nodes[n]['type']] for n in G.nodes], font_size=10)
plt.show()
