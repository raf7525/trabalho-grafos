from typing import List, Dict, Set, Iterable, Union, Tuple, Generator
import copy

class Vertice:
    def __init__(self, nome: str):
        self.nome = nome
        self.vizinhos: List['Vertice'] = []
        self.atributos: Dict[str, Union[str, int, float]] = {}
    
    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]
        
        novo_vertice = type(self)(self.nome)
        memo[id(self)] = novo_vertice

        novo_vertice.atributos = copy.deepcopy(self.atributos, memo)
        
        # A lista de vizinhos é inicializada vazia e preenchida posteriormente
        # para evitar recursão infinita.
        novo_vertice.vizinhos = [] 
        
        return novo_vertice

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

    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]
            
        novo_grafo = type(self)()
        memo[id(self)] = novo_grafo

        # Primeira passagem: Copia profunda de todos os vértices.
        for nome_vertice, vertice_original in self.vertices.items():
            novo_vertice = copy.deepcopy(vertice_original, memo) 
            novo_grafo.vertices[nome_vertice] = novo_vertice
        
        # Segunda passagem: Restabelece as conexões entre vizinhos
        for nome_vertice, vertice_original in self.vertices.items():
            vertice_atual_novo = novo_grafo.vertices[nome_vertice]
            for vizinho_original in vertice_original.vizinhos:
                vizinho_novo = novo_grafo.vertices[vizinho_original.nome]
                vertice_atual_novo.vizinhos.append(vizinho_novo)
            vertice_atual_novo.vizinhos.sort(key=lambda no: no.nome)

        novo_grafo.arestas = copy.deepcopy(self.arestas, memo)
        novo_grafo.adjacencias = copy.deepcopy(self.adjacencias, memo)
        novo_grafo.atributos_vertices = copy.deepcopy(self.atributos_vertices, memo)
        
        return novo_grafo

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

    def remover_aresta(self, vertice_origem: Vertice, vertice_destino: Vertice) -> bool:
        if not self.contem_vertice(vertice_origem) or not self.contem_vertice(vertice_destino):
            return False
        
        removeu_origem = self.vertices[vertice_origem.nome].remover_vizinho(vertice_destino)
        removeu_destino = self.vertices[vertice_destino.nome].remover_vizinho(vertice_origem)
        
        chave_aresta = tuple(sorted([vertice_origem.nome, vertice_destino.nome]))
        if chave_aresta in self.arestas:
            del self.arestas[chave_aresta]
        
        self.adjacencias[vertice_origem.nome].discard(vertice_destino.nome)
        self.adjacencias[vertice_destino.nome].discard(vertice_origem.nome)
        
        return removeu_origem and removeu_destino

    def obter_peso(self, nome_vertice_a: str, nome_vertice_b: str) -> float:
        chave = tuple(sorted([nome_vertice_a, nome_vertice_b]))
        aresta = self.arestas.get(chave)
        return aresta['peso'] if aresta else float('inf')
    
    def obter_informacoes_aresta(self, nome_vertice_a: str, nome_vertice_b: str) -> Dict:
        chave = tuple(sorted([nome_vertice_a, nome_vertice_b]))
        return self.arestas.get(chave, {})
    
    def obter_vizinhos(self, nome_vertice: str) -> List[str]:
        if nome_vertice not in self.vertices:
            raise ValueError(f"Nó '{nome_vertice}' não encontrado no grafo.")
        
        vertice = self.vertices[nome_vertice]
        return sorted([vizinho.nome for vizinho in vertice.vizinhos])

    def get_all_directed_edges(self) -> Generator[Tuple[str, str, float], None, None]:
        """
        Gera todas as arestas direcionadas (u, v, peso) para o grafo.
        Para um grafo não direcionado, cada aresta armazenada (u, v) gera duas arestas direcionadas.
        """
        for (u_name, v_name), attrs in self.arestas.items():
            peso = attrs.get('peso', 1.0)
            yield u_name, v_name, peso
            yield v_name, u_name, peso # Retorna o inverso para grafo não direcionado

    def criar_subgrafo(self, vertices_para_incluir: Iterable[Union[Vertice, str]]) -> 'Grafo':
        subgrafo = Grafo()
        
        nomes_incluidos = {str(vertice) for vertice in vertices_para_incluir}

        for nome in nomes_incluidos:
            if nome in self.vertices:
                subgrafo.adicionar_vertice(copy.deepcopy(self.vertices[nome]))

        for nome in nomes_incluidos:
            no_original = self.vertices.get(nome)
            if not no_original:
                continue

            for vizinho in no_original.vizinhos:
                if vizinho.nome in nomes_incluidos:
                    info_aresta_original = self.obter_informacoes_aresta(nome, vizinho.nome)
                    
                    if not ( (nome, vizinho.nome) in subgrafo.arestas or (vizinho.nome, nome) in subgrafo.arestas):
                        peso_aresta = info_aresta_original.pop('peso', 1.0)
                        
                        subgrafo.adicionar_aresta(
                            subgrafo.vertices[nome],
                            subgrafo.vertices[vizinho.nome],
                            peso=peso_aresta,
                            **info_aresta_original
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
        from graphs.algorithms import Algorithms
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        v_destino = self.vertices[str(destino)] if isinstance(destino, str) else destino
        
        return Algorithms.dijkstra(self, v_origem, v_destino)
    
    def caminho_mais_curto_bellman_ford(self, origem: Union[Vertice, str], destino: Union[Vertice, str] = None):
        """
        Encontra o caminho mais curto entre dois vértices usando o algoritmo de Bellman-Ford.
        Funciona com pesos negativos e detecta ciclos negativos.
            Se destino for None: Tupla (distancias_dict, anterior_dict, tem_ciclo_negativo)
        """
        from graphs.algorithms import Algorithms
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        
        if destino is None:
            return Algorithms.bellman_ford(self, v_origem)
        
        v_destino = self.vertices[str(destino)] if isinstance(destino, str) else destino
        return Algorithms.bellman_ford(self, v_origem, v_destino)
    
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
        from graphs.algorithms import Algorithms
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        return Algorithms.breadth_first_search(self, v_origem)
    
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
        from graphs.algorithms import Algorithms
        
        v_origem = self.vertices[str(origem)] if isinstance(origem, str) else origem
        return Algorithms.depth_first_search(self, v_origem)

    def __str__(self) -> str:
        linhas = [f"Grafo com {self.ordem} nós e {self.tamanho} arestas"]
        linhas.append(f"Densidade: {self.densidade:.4f}")
        linhas.append("\nConexões:")
        
        for nome_no in sorted(self.vertices.keys()):
            vizinhos = [vizinho.nome for vizinho in self.vertices[nome_no].vizinhos]
            if vizinhos:
                linhas.append(f"  {nome_no} -> {', '.join(vizinhos)}")
        
        return "\n".join(linhas)


class DirectedGrafo(Grafo):
    def adicionar_aresta(self, vertice_origem: Vertice, vertice_destino: Vertice, peso: float = 1.0, **atributos) -> bool:
        if not self.contem_vertice(vertice_origem) or not self.contem_vertice(vertice_destino):
            return False
        
        # Para grafo direcionado, adiciona vizinho apenas na origem
        self.vertices[vertice_origem.nome].adicionar_vizinho(vertice_destino)
        
        # Chave da aresta é (origem, destino) - não ordenada
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

    def get_all_directed_edges(self) -> Generator[Tuple[str, str, float], None, None]:
        """
        Gera todas as arestas direcionadas (u, v, peso) para o grafo.
        Para um grafo direcionado, cada aresta armazenada (u, v) gera uma aresta direcionada.
        """
        for (u_name, v_name), attrs in self.arestas.items():
            peso = attrs.get('peso', 1.0)
            yield u_name, v_name, peso