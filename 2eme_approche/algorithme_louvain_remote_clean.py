import pandas as pd
import networkx as nx


# On applique l'algorithme de Louvain pour détecter les communautés.
def louvain_communities(nodes_file, edges_file, output_file):
    nodes = pd.read_csv(nodes_file)
    edges = pd.read_csv(edges_file)

    G = nx.Graph()
    for _, row in nodes.iterrows():
        G.add_node(row['Id'], name=row['Label'], type=row['Type'])
    for _, row in edges.iterrows():
        G.add_edge(row['Source'], row['Target'], predicate=row['Label'])

    partition = nx.community.louvain_communities(G)

    c = {}
    for community_id, community in enumerate(partition):
        for node in community:
            c[node] = community_id

    nodes['community'] = nodes['Id'].map(c)

    nodes.to_csv(output_file, index=False)


louvain_communities(
    '/users/eleves-b/2022/martin.beaufils/Modal/nodes.csv',
    '/users/eleves-b/2022/martin.beaufils/Modal/edges.csv',
    '/users/eleves-b/2022/martin.beaufils/Modal/nodes_with_communities.csv'
)
