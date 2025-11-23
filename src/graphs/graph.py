from typing import Generator, List, Dict, Set, Iterable, Union, Tuple

class Vertice:
    def __init__(self, nome: str):
        self.nome = nome
        self.vizinhos: List['Vertice'] = []
        self.atributos: Dict[str, Union[str, int, float]] = {}
    
    
    def adicionar_vizinho(self, vizinho: 'Vertice') -> bool:
        adicionou = False
        if vizinho not in self.vizinhos:
            self.vizinhos.append(vizinho)
            self.vizinhos.sort(key=lambda vertice: vertice.nome)
            adicionou = True
        return adicionou
    
    def adicionar_vizinhos(self, vizinhos: List['Vertice']):
        for vizinho in vizinhos:
            self.adicionar_vizinho(vizinho)
    
    def remover_vizinho(self, vizinho: 'Vertice') -> bool:
        removeu = False
        if vizinho in self.vizinhos:
            self.vizinhos.remove(vizinho)
            removeu = True
        return removeu
    
    def remover_vizinhos(self, vizinhos: List['Vertice']):
        for vizinho in vizinhos:
            self.remover_vizinho(vizinho)

    def limpar_vizinhos(self):
        self.vizinhos.clear()

    def esta_conectado_a(self, vertice: 'Vertice') -> bool:
        return vertice in self.vizinhos
    
    def __str__(self):
        return self.nome


class Grafo:
    def __init__(self):
        self.vertices: Dict[str, Vertice] = {}
        self.arestas: Dict[tuple[str, str], Dict[str, Union[str, int, float]]] = {}
        self.adjacencias: Dict[str, Set[str]] = {}
        self.atributos_vertices: Dict[str, Dict] = {}

    def contem_vertice(self, vertice: Vertice) -> bool:
        return vertice.nome in self.vertices

    def adicionar_vertice(self, vertice: Vertice) -> bool:
        if not isinstance(vertice, Vertice):
            return False
            
        if vertice.nome in self.vertices:
            return False
        
        self.vertices[vertice.nome] = vertice
        self.adjacencias[vertice.nome] = set()
        self.atributos_vertices[vertice.nome] = vertice.atributos
        return True
    
    def adicionar_aresta(self, vertice_origem: Vertice, vertice_destino: Vertice, peso: float = 1.0, **atributos) -> bool:
        if not self.contem_vertice(vertice_origem) or not self.contem_vertice(vertice_destino):
            return False
        
        self.vertices[vertice_origem.nome].adicionar_vizinho(vertice_destino)
        self.vertices[vertice_destino.nome].adicionar_vizinho(vertice_origem)
        
        chave_aresta = tuple(sorted([vertice_origem.nome, vertice_destino.nome]))
        self.arestas[chave_aresta] = {'peso': peso, **atributos}
        
        self.adjacencias[vertice_origem.nome].add(vertice_destino.nome)
        self.adjacencias[vertice_destino.nome].add(vertice_origem.nome)
        
        return True

    def obter_peso(self, nome_vertice_a: str, nome_vertice_b: str) -> float:
        chave = tuple(sorted([nome_vertice_a, nome_vertice_b]))
        aresta = self.arestas.get(chave)
        return aresta['peso'] if aresta else float('inf')
    
    def obter_informacoes_aresta(self, nome_vertice_a: str, nome_vertice_b: str) -> Dict:
        chave = tuple(sorted([nome_vertice_a, nome_vertice_b]))
        return self.arestas.get(chave, {})
    
    def obter_vizinhos(self, nome_vertice: str) -> List[str]:
        if nome_vertice not in self.vertices:
            raise ValueError(f"Vértice '{nome_vertice}' não encontrado no grafo.")
        
        vertice = self.vertices[nome_vertice]
        return sorted([vizinho.nome for vizinho in vertice.vizinhos])

    def criar_subgrafo(self, nos_para_incluir: Iterable[Union[Vertice, str]]) -> 'Grafo':
        subgrafo = Grafo()
        
        nomes_incluidos = {str(vertice) for vertice in nos_para_incluir}

        for nome in nomes_incluidos:
            if nome in self.vertices:
                novo_vertice = Vertice(nome)
                novo_vertice.atributos = self.vertices[nome].atributos.copy()
                subgrafo.adicionar_vertice(novo_vertice)

        for nome in nomes_incluidos:
            vertice_original = self.vertices.get(nome)
            if not vertice_original:
                continue

            for vizinho in vertice_original.vizinhos:
                if vizinho.nome in nomes_incluidos:
                    chave_aresta = tuple(sorted([nome, vizinho.nome]))
                    info_aresta = self.arestas.get(chave_aresta, {'peso': 1.0}).copy()
                    peso_aresta = info_aresta.pop('peso', 1.0)
                    
                    subgrafo.adicionar_aresta(
                        subgrafo.vertices[nome],
                        subgrafo.vertices[vizinho.nome],
                        peso=peso_aresta,
                        **info_aresta
                    )

        return subgrafo
        
    @property
    def ordem(self) -> int:
        return len(self.vertices)
    
    @property
    def tamanho(self) -> int:
        return len(self.arestas)

    @property
    def densidade(self) -> float:
        if self.ordem < 2:
            return 0.0
        
        arestas_maximas = (self.ordem * (self.ordem - 1)) / 2
        return self.tamanho / arestas_maximas
    
    def caminho_mais_curto_dijkstra(self, origem: Union[Vertice, str], destino: Union[Vertice, str]) -> Tuple[float, List[str]]:
       
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        v_destino = self.vertices[str(destino)] if isinstance(destino, str) else destino
        
        return Sorting.dijkstra(self, v_origem, v_destino)
    
    def caminho_mais_curto_bellman_ford(self, origem: Union[Vertice, str], destino: Union[Vertice, str] = None):
        
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        
        if destino is None:
            return Sorting.bellman_ford(self, v_origem)
        
        v_destino = self.vertices[str(destino)] if isinstance(destino, str) else destino
        return Sorting.bellman_ford(self, v_origem, v_destino)
    
    def busca_em_largura(self, origem: Union[Vertice, str]):
       
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        return Sorting.breadth_first_search(self, v_origem)
    
    def busca_em_profundidade(self, origem: Union[Vertice, str]):
        
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        return Sorting.depth_first_search(self, v_origem)


class GrafoDirecionado(Grafo):
    def adicionar_aresta(self, vertice_origem: Vertice, vertice_destino: Vertice, peso: float = 1.0, **atributos) -> bool:
        if not self.contem_vertice(vertice_origem) or not self.contem_vertice(vertice_destino):
            return False
        
        
        self.vertices[vertice_origem.nome].adicionar_vizinho(vertice_destino)
        
        
        chave_aresta = (vertice_origem.nome, vertice_destino.nome)
        self.arestas[chave_aresta] = {'peso': peso, **atributos}
        
        self.adjacencias[vertice_origem.nome].add(vertice_destino.nome)
        
        return True

    def remover_aresta(self, vertice_origem: Vertice, vertice_destino: Vertice) -> bool:
        if not self.contem_vertice(vertice_origem) or not self.contem_vertice(vertice_destino):
            return False
        
        removeu_origem = self.vertices[vertice_origem.nome].remover_vizinho(vertice_destino)
        
        chave_aresta = (vertice_origem.nome, vertice_destino.nome)
        if chave_aresta in self.arestas:
            del self.arestas[chave_aresta]
        
        self.adjacencias[vertice_origem.nome].discard(vertice_destino.nome)
        
        return removeu_origem


    def obter_peso(self, nome_vertice_a: str, nome_vertice_b: str) -> float:
        chave = (nome_vertice_a, nome_vertice_b)
        
        if chave in self.arestas:
            return self.arestas[chave]['peso']
        else:
            return float('inf')
    
    def obter_informacoes_aresta(self, nome_vertice_a: str, nome_vertice_b: str) -> Dict:
        chave = (nome_vertice_a, nome_vertice_b)
        
        if chave in self.arestas:
            return self.arestas[chave]
        else:
            return {}

    def obter_arestas_direcionadas(self) -> Generator[Tuple[str, str, float], None, None]:
        
        for (u_name, v_name), attrs in self.arestas.items():
            peso = attrs.get('peso', 1.0)
            yield u_name, v_name, peso