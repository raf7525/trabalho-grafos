import pandas as pd
from typing import List, Dict, Set, Iterable

class Graph:
    def __init__(self):
       
        self.adj: Dict[str, Set[str]] = {}
        
        self.nodes_attr: Dict[str, Dict] = {}

    def add_node(self, node_id: str, attrs: Dict = None):
      
        if node_id not in self.adj:
            self.adj[node_id] = set()
            self.nodes_attr[node_id] = attrs if attrs else {}

    def add_edge(self, u: str, v: str):
       
        if u not in self.adj: self.add_node(u)
        if v not in self.adj: self.add_node(v)
        
        self.adj[u].add(v)
        self.adj[v].add(u)

    def load_from_csv(self, nodes_path: str, edges_path: str):
      
        nodes_df = pd.read_csv(nodes_path)
        for _, row in nodes_df.iterrows():
            self.add_node(row['bairro'], {'microrregiao': str(row['microrregiao'])})

       
        edges_df = pd.read_csv(edges_path)
        for _, row in edges_df.iterrows():
            self.add_edge(row['bairro_origem'], row['bairro_destino'])
    
    def get_order(self) -> int:
        
        return len(self.adj)

    def get_size(self) -> int:
        
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def get_neighbors(self, node_id: str) -> List[str]:
        
        if node_id not in self.adj:
            raise ValueError(f"Nó '{node_id}' não encontrado no grafo.")
        return sorted(list(self.adj[node_id]))

    def create_subgraph(self, nodes_to_include: Iterable[str]) -> 'Graph':
        
        subgraph = Graph()
        node_set = set(nodes_to_include)

        
        for node in node_set:
            if node in self.nodes_attr:
                subgraph.add_node(node, self.nodes_attr[node])
        
       
        for u in subgraph.adj:
           
            if u in self.adj:
                for v in self.adj[u]:
                    
                    if v in subgraph.adj:
                        subgraph.add_edge(u, v)
        
        return subgraph

    def __str__(self):
        
        return f"Grafo com {self.get_order()} nós e {self.get_size()} arestas."
