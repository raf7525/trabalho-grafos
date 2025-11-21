from typing import List, Dict, Set, Iterable, Union, Tuple

class Vertice:
    def __init__(self, nome: str):
        self.nome = nome
        self.vizinhos: List['Vertice'] = []
        self.atributos: Dict[str, Union[str, int, float]] = {}
    
    
    def adicionar_vizinho(self, vizinho: 'Vertice') -> bool:
        adicionou = False
        if vizinho not in self.vizinhos:
            self.vizinhos.append(vizinho)
            self.vizinhos.sort(key=lambda no: no.nome)
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

    def contem_no(self, no: Vertice) -> bool:
        return no.nome in self.vertices

    def adicionar_no(self, no: Vertice) -> bool:
        if not isinstance(no, Vertice):
            return False
            
        if no.nome in self.vertices:
            return False
        
        self.vertices[no.nome] = no
        self.adjacencias[no.nome] = set()
        self.atributos_vertices[no.nome] = no.atributos
        return True
    
    def adicionar_aresta(self, no_origem: Vertice, no_destino: Vertice, peso: float = 1.0, **atributos) -> bool:
        if not self.contem_no(no_origem) or not self.contem_no(no_destino):
            return False
        
        self.vertices[no_origem.nome].adicionar_vizinho(no_destino)
        self.vertices[no_destino.nome].adicionar_vizinho(no_origem)
        
        chave_aresta = tuple(sorted([no_origem.nome, no_destino.nome]))
        self.arestas[chave_aresta] = {'peso': peso, **atributos}
        
        self.adjacencias[no_origem.nome].add(no_destino.nome)
        self.adjacencias[no_destino.nome].add(no_origem.nome)
        
        return True

    def obter_peso(self, nome_no_a: str, nome_no_b: str) -> float:
        chave = tuple(sorted([nome_no_a, nome_no_b]))
        aresta = self.arestas.get(chave)
        return aresta['peso'] if aresta else float('inf')
    
    def obter_informacoes_aresta(self, nome_no_a: str, nome_no_b: str) -> Dict:
        chave = tuple(sorted([nome_no_a, nome_no_b]))
        return self.arestas.get(chave, {})
    
    def obter_vizinhos(self, nome_no: str) -> List[str]:
        if nome_no not in self.vertices:
            raise ValueError(f"Nó '{nome_no}' não encontrado no grafo.")
        
        no = self.vertices[nome_no]
        return sorted([vizinho.nome for vizinho in no.vizinhos])

    def criar_subgrafo(self, nos_para_incluir: Iterable[Union[Vertice, str]]) -> 'Grafo':
        subgrafo = Grafo()
        
        nomes_incluidos = {str(no) for no in nos_para_incluir}

        for nome in nomes_incluidos:
            if nome in self.vertices:
                novo_no = Vertice(nome)
                novo_no.atributos = self.vertices[nome].atributos.copy()
                subgrafo.adicionar_no(novo_no)

        for nome in nomes_incluidos:
            no_original = self.vertices.get(nome)
            if not no_original:
                continue

            for vizinho in no_original.vizinhos:
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
        """
        Encontra o caminho mais curto entre dois vértices usando o algoritmo de Dijkstra.
        Eficiente para grafos com pesos positivos.
        """
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        v_destino = self.vertices[str(destino)] if isinstance(destino, str) else destino
        
        return Sorting.dijkstra(self, v_origem, v_destino)
    
    def caminho_mais_curto_bellman_ford(self, origem: Union[Vertice, str], destino: Union[Vertice, str] = None):
        """
        Encontra o caminho mais curto entre dois vértices usando o algoritmo de Bellman-Ford.
        Funciona com pesos negativos e detecta ciclos negativos.
            Se destino for None: Tupla (distancias_dict, anterior_dict, tem_ciclo_negativo)
        """
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        
        if destino is None:
            return Sorting.bellman_ford(self, v_origem)
        
        v_destino = self.vertices[str(destino)] if isinstance(destino, str) else destino
        return Sorting.bellman_ford(self, v_origem, v_destino)
    
    def busca_em_largura(self, origem: Union[Vertice, str]):
        """
        Executa busca em largura (BFS) a partir de um vértice inicial.
        
        Retorna dict com:
            - niveis: nível de cada vértice na árvore BFS
            - distancias: distância em número de arestas
            - anterior: predecessor de cada vértice
            - arvore: estrutura da árvore de percurso
            - ordem_visita: ordem de visitação dos vértices
        """
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        return Sorting.breadth_first_search(self, v_origem)
    
    def busca_em_profundidade(self, origem: Union[Vertice, str]):
        """
        Executa busca em profundidade (DFS) a partir de um vértice inicial.
        
        Retorna dict com:
            - descoberta: timestamp de descoberta de cada vértice
            - finalizacao: timestamp de finalização de cada vértice
            - anterior: predecessor de cada vértice
            - classificacao_arestas: classificação das arestas
            - ordem_visita: ordem de descoberta dos vértices
            - tem_ciclo: indica se há ciclos no grafo
            - componentes: componentes conexos do grafo
        """
        from .algorithms import Sorting
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        return Sorting.depth_first_search(self, v_origem)

    def __str__(self) -> str:
        linhas = [f"Grafo com {self.ordem} nós e {self.tamanho} arestas"]
        linhas.append(f"Densidade: {self.densidade:.4f}")
        linhas.append("\nConexões:")
        
        for nome_no in sorted(self.vertices.keys()):
            vizinhos = [vizinho.nome for vizinho in self.vertices[nome_no].vizinhos]
            if vizinhos:
                linhas.append(f"  {nome_no} -> {', '.join(vizinhos)}")
        
        return "\n".join(linhas)