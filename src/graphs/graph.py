import pandas as pd
from typing import List, Dict, Set, Iterable, Union
        
type NomeVertice = str

class Vertice:
    def __init__(self, nome: NomeVertice):
        self.nome = nome
        self.vizinhos: List[Vertice] = []
        
    
    def adicionar_vizinho(self, vizinho: 'Vertice') -> bool:
        resultado = False
        if vizinho not in self.vizinhos:
            self.vizinhos.append(vizinho)
            self.vizinhos.sort(key=lambda v: v.nome)
            resultado = True
        return resultado
    
    def adicionar_vizinhos(self, vizinhos: List['Vertice']):
        [self.adicionar_vizinho(vizinho) for vizinho in vizinhos]
    
    def remover_vizinho(self, vizinho: 'Vertice'):
        resultado = False
        if vizinho in self.vizinhos:
            self.vizinhos.remove(vizinho)
            resultado = True
        return resultado
    
    def remover_vizinhos(self, vizinhos: List['Vertice']):
        [self.remover_vizinho(vizinho) for vizinho in vizinhos]

    def limpar_vizinhos(self):
        self.vizinhos.clear()

    def tem_adjagencia(self, vertice: 'Vertice'):
        return vertice in self.vizinhos
    
    def __str__(self):
        return self.nome
    

class Grafo:
    def __init__(self):
        self.vertices: Dict[NomeVertice, Vertice] = {}
       
        self.adj: Dict[str, Set[str]] = {}
        self.nodes_attr: Dict[str, Dict] = {}

    def pertence_ao_grafo(self, vertice: Vertice) -> bool:
        return vertice.nome in self.vertices

    def adicionar_vertice(self, vertice: Vertice) -> bool:
        resultado = False
        vertice_tem_tipo_correto = isinstance(vertice, Vertice)
        vertice_nao_visitado = vertice.nome not in self.vertices

        if (vertice_tem_tipo_correto and vertice_nao_visitado):
            self.vertices.update({ vertice.nome: vertice })
           
            if vertice.nome not in self.adj:
                self.adj[vertice.nome] = set()
                self.nodes_attr[vertice.nome] = {}
            resultado = True
        return resultado
    
    def adicionar_aresta(self, vertice_a: Vertice, vertice_b: Vertice) -> bool:
        resultado = False
        if self.pertence_ao_grafo(vertice_a) and self.pertence_ao_grafo(vertice_b):
            vertice_a_obj = self.vertices.get(vertice_a.nome)
            vertice_b_obj = self.vertices.get(vertice_b.nome)
            
            if vertice_a_obj and vertice_b_obj:
                vertice_a_obj.adicionar_vizinho(vertice_b_obj)
                vertice_b_obj.adicionar_vizinho(vertice_a_obj)
                
                
                self.adj[vertice_a.nome].add(vertice_b.nome)
                self.adj[vertice_b.nome].add(vertice_a.nome)
                resultado = True
        return resultado

    def criar_subrafo(self, vertices_para_incluir: Iterable[Union[Vertice, str]]) -> 'Grafo':
        subgrafo = Grafo()
        
        nomes_vertices_incluidos = {str(v) for v in vertices_para_incluir}

        for nome in nomes_vertices_incluidos:
            subgrafo.adicionar_vertice(Vertice(nome))

        for nome in nomes_vertices_incluidos:
            vertice_original = self.vertices.get(nome)
            
            if not vertice_original:
                continue

            for vertice_vizinho in vertice_original.vizinhos:
                if vertice_vizinho.nome in nomes_vertices_incluidos:
                    vertice_a = subgrafo.vertices.get(nome)
                    vertice_b = subgrafo.vertices.get(vertice_vizinho.nome)
                    
                    if vertice_a and vertice_b:
                        subgrafo.adicionar_aresta(vertice_a, vertice_b)

        return subgrafo
    
    
    def get_neighbors(self, node_id: str) -> List[str]:
       
        if node_id not in self.vertices:
            raise ValueError(f"Nó '{node_id}' não encontrado no grafo.")
        
        vertice = self.vertices[node_id]
        return sorted([v.nome for v in vertice.vizinhos])
    
    def load_from_csv(self, nodes_path: str, edges_path: str):
        
        nodes_df = pd.read_csv(nodes_path)
        for _, row in nodes_df.iterrows():
            vertice = Vertice(row['bairro'])
            self.adicionar_vertice(vertice)
            
            self.nodes_attr[row['bairro']] = {'microrregiao': str(row['microrregiao'])}

        
        edges_df = pd.read_csv(edges_path)
        for _, row in edges_df.iterrows():
            origem = self.vertices.get(row['bairro_origem'])
            destino = self.vertices.get(row['bairro_destino'])
            
            if origem and destino:
                self.adicionar_aresta(origem, destino)
        
    @property
    def ordem(self) -> int:
        return len(self.vertices)

    @property
    def tamanho(self) -> int:
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def get_order(self) -> int:
        """Retorna a ordem do grafo (número de vértices)"""
        return len(self.vertices)

    def get_size(self) -> int:
        """Retorna o tamanho do grafo (número de arestas)"""
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    @staticmethod
    def calculate_density(order: int, size: int) -> float:
        if order < 2:
            return 0.0
        return (2 * size) / (order * (order - 1)) 
    
    def __str__(self) -> str:
        linhas = []
        for key in sorted(self.vertices.keys()):
            vizinhos = [v.nome for v in self.vertices[key].vizinhos]
            linhas.append(f"{key}: {vizinhos}")
        return "\n".join(linhas)