from collections import deque
import heapq
from typing import List, Tuple, Union
from src.graphs.graph import Grafo, GrafoDirecionado, Vertice

class PositiveFloat(float):
    def __new__(cls, value):
        if value < 0:
            raise ValueError("Valor deve ser um número float positivo")
        return super(PositiveFloat, cls).__new__(cls, value)

class Sorting:
    @staticmethod
    def dijkstra(graph: Grafo, start: Vertice, end: Vertice):
        """
        Initialize the 'distances', 'previous' and 'visited' containers
        Set the distance for the starting vertex to 0
        Create a priority queue and add the start vertex and its distance
        Start a loop for as along as there's something in the queue
            Pop from the queue, saving the vertex and its distance
            Mark the removed vertex as visited
            Start a loop over all the neighbors of the removed vertex
                If the current vertex is visited, skip to the next
                Otherwise, calculate the distance to it
                If the new distance is smaller
                    Update distances table
                    Update previous table
                    Push into the queue the neighbor and its distance
        """
        distancias = {}
        visitados = set()
        anterior = {}
        fila: List[Tuple[int, str]] = []
        
        # Inicializa todos os vértices como infinito
        for nome in graph.vertices:
            distancias[nome] = float('inf')
            
        distancias.update({start.nome: 0})
        heapq.heappush(fila, (0, start.nome))
        
        while fila:
            _, nome_atual = heapq.heappop(fila)
            vertice = graph.vertices[nome_atual]
            
            visitados.add(vertice)
            
            for vizinho in vertice.vizinhos:
                if vizinho in visitados: continue
    
                peso_aresta = PositiveFloat(graph.obter_peso(nome_atual, vizinho.nome))
                nova_distancia = distancias[nome_atual] + peso_aresta
                
                if nova_distancia < distancias[vizinho.nome]:
                    distancias[vizinho.nome] = nova_distancia
                    anterior[vizinho.nome] = nome_atual
                    heapq.heappush(fila, (nova_distancia, vizinho.nome))

        caminho = []
        atual = end.nome
        
        if atual not in anterior and atual != start.nome:
            return float('inf'), []
        
        while atual is not None:
            caminho.append(atual)
            atual = anterior.get(atual)
            if atual == start.nome:
                caminho.append(atual)
                break
        
        caminho.reverse()
        
        return distancias[end.nome], caminho

    @staticmethod
    def bellman_ford(graph: Union[Grafo, GrafoDirecionado], start: Vertice, end: Vertice = None):
        """
        Encontra o caminho mais curto entre dois vértices usando o algoritmo de Bellman-Ford.
        Funciona com pesos negativos e detecta ciclos negativos.
            Se destino for None: Tupla (distancias_dict, anterior_dict, tem_ciclo_negativo)
        """
        # Inicializa distâncias e predecessores
        distancias = {}
        anterior = {}
        
        # Inicializa todos os vértices como infinito
        for nome_vertice in graph.vertices:
            distancias[nome_vertice] = float('inf')
        
        distancias[start.nome] = 0
        
        # Generator for edges
        def get_edges_to_relax():
            if isinstance(graph, GrafoDirecionado):
                yield from graph.obter_arestas_direcionadas()
            else: # Grafo (undirected)
                for u_name, vertice_u in graph.vertices.items():
                    for vizinho_v in vertice_u.vizinhos:
                        v_name = vizinho_v.nome
                        peso_aresta = graph.obter_peso(u_name, v_name)
                        yield u_name, v_name, peso_aresta

        # Relaxa todas as arestas |V| - 1 vezes
        for _ in range(len(graph.vertices)):
            relaxed_in_this_pass = False
            for u_name, v_name, peso_aresta in get_edges_to_relax():
                if distancias[u_name] != float('inf') and distancias[u_name] + peso_aresta < distancias[v_name]:
                    distancias[v_name] = distancias[u_name] + peso_aresta
                    anterior[v_name] = u_name
                    relaxed_in_this_pass = True
            
        # Verifica se há ciclos negativos (V-ésima passagem)
        tem_ciclo_negativo = False
        for u_name, v_name, peso_aresta in get_edges_to_relax():
            if distancias[u_name] != float('inf') and distancias[u_name] + peso_aresta < distancias[v_name]:
                tem_ciclo_negativo = True
                break
        
        # Se não foi especificado destino, retorna tudo
        if end is None:
            return distancias, anterior, tem_ciclo_negativo
        
        # Se há ciclo negativo, indica erro
        if tem_ciclo_negativo:
            raise ValueError("Grafo contém ciclo negativo")
        
        # Reconstrói o caminho para o destino
        caminho = []
        atual = end.nome
        
        if atual not in anterior and atual != start.nome:
            return float('inf'), [] # Caminho não encontrado
        
        path_nodes = set() # Para detectar ciclos durante a reconstrução do caminho
        while atual is not None:
            if atual in path_nodes: 
                return float('inf'), [] # Caminho inválido
            path_nodes.add(atual)
            caminho.append(atual)
            atual = anterior.get(atual)
            if atual == start.nome: # Se o início for alcançado, adiciona e para
                caminho.append(atual)
                break
        
        # Se o nó inicial não for alcançado, significa que não é acessível a partir do destino
        if caminho and caminho[-1] != start.nome:
            return float('inf'), []

        caminho.reverse()
        
        return distancias[end.nome], caminho
    
    @staticmethod
    def breadth_first_search(graph: Grafo, start: Vertice):
        """
        Executa busca em largura (BFS) a partir de um vértice inicial.
        
        Retorna:
            dict: Dicionário contendo:
                - 'niveis': dict[str, int] - nível de cada vértice na árvore BFS
                - 'distancias': dict[str, int] - distância (em número de arestas) de cada vértice
                - 'anterior': dict[str, str|None] - predecessor de cada vértice na árvore BFS
                - 'arvore': dict[str, list[str]] - árvore de percurso (cada nó -> seus filhos)
                - 'ordem_visita': list[str] - ordem em que os vértices foram visitados
        """
        visitado = set([start.nome])
        fila = deque([start.nome])
        anterior = {start.nome: None}
        niveis = {start.nome: 0}
        distancias = {start.nome: 0}
        arvore = {start.nome: []}
        ordem_visita = [start.nome]
        
        # Inicializa todos os outros vértices como não visitados
        for nome in graph.vertices:
            if nome != start.nome:
                niveis[nome] = float('inf')
                distancias[nome] = float('inf')
                arvore[nome] = []

        while fila:
            u = fila.popleft()
            vertice_atual = graph.vertices[u]
            
            # Explora todos os vizinhos
            for vizinho in vertice_atual.vizinhos:
                v = vizinho.nome
                if v not in visitado:
                    visitado.add(v)
                    anterior[v] = u
                    niveis[v] = niveis[u] + 1
                    distancias[v] = distancias[u] + 1
                    arvore[u].append(v)
                    fila.append(v)
                    ordem_visita.append(v)
        
        return {
            'niveis': niveis,
            'distancias': distancias,
            'anterior': anterior,
            'arvore': arvore,
            'ordem_visita': ordem_visita
        }

    @staticmethod
    def bfs_shortest_path(graph: Grafo, start: Vertice, end: Vertice) -> Tuple[float, List[str]]:
        """
        BFS para encontrar caminho mais curto entre dois vértices.
        Interface unificada compatível com Dijkstra e Bellman-Ford.
        
        Retorna:
            tuple: (custo, caminho) onde custo é o número de arestas e caminho é lista de nomes
        """
        resultado = Sorting.breadth_first_search(graph, start)
        
        if end.nome not in resultado['distancias'] or resultado['distancias'][end.nome] == float('inf'):
            return float('inf'), []
        
        # Reconstrói o caminho
        caminho = []
        atual = end.nome
        while atual is not None:
            caminho.append(atual)
            atual = resultado['anterior'].get(atual)
        
        return resultado['distancias'][end.nome], list(reversed(caminho))

    @staticmethod
    def depth_first_search(graph: Grafo, start: Vertice):
        """
        Executa busca em profundidade (DFS) a partir de um vértice inicial.
        
        Retorna:
            dict: Dicionário contendo:
                - 'descoberta': dict[str, int] - timestamp de descoberta de cada vértice
                - 'finalizacao': dict[str, int] - timestamp de finalização de cada vértice
                - 'anterior': dict[str, str|None] - predecessor de cada vértice na árvore DFS
                - 'classificacao_arestas': dict[tuple, str] - classificação de cada aresta
                    * 'arvore': aresta da árvore DFS
                    * 'retorno': aresta para ancestral (indica ciclo)
                    * 'avanco': aresta para descendente
                    * 'cruzamento': aresta entre subárvores diferentes
                - 'ordem_visita': list[str] - ordem de descoberta dos vértices
                - 'tem_ciclo': bool - indica se o grafo contém ciclos
                - 'componentes': list[list[str]] - componentes conexos do grafo
        """
        # Estados dos vértices: 'nao_visitado', 'visitando', 'visitado'
        estado = {nome: 'nao_visitado' for nome in graph.vertices}
        descoberta = {}
        finalizacao = {}
        anterior = {nome: None for nome in graph.vertices}
        classificacao_arestas = {}
        ordem_visita = []
        tempo = [0]  # Lista para permitir modificação dentro da função aninhada
        tem_ciclo = False
        componentes = []
        
        def dfs_visitar(u: str, pai: str = None):
            """Função auxiliar recursiva para visitar vértices
            
            Args:
                u: Vértice atual sendo visitado
                pai: Vértice predecessor (para grafos não-direcionados)
            """
            nonlocal tem_ciclo
            
            # Marca como visitando e registra descoberta
            estado[u] = 'visitando'
            tempo[0] += 1
            descoberta[u] = tempo[0]
            ordem_visita.append(u)
            
            vertice_atual = graph.vertices[u]
            
            # Explora todos os vizinhos
            for vizinho in vertice_atual.vizinhos:
                v = vizinho.nome
                # Cria chave de aresta ordenada para grafos não-direcionados
                aresta = tuple(sorted([u, v]))
                
                if estado[v] == 'nao_visitado':
                    # Aresta de árvore
                    anterior[v] = u
                    classificacao_arestas[aresta] = 'arvore'
                    dfs_visitar(v, u)
                    
                elif estado[v] == 'visitando' and v != pai:
                    # Aresta de retorno - indica ciclo
                    # Ignora se v é o pai direto (evita falso positivo em grafos não-direcionados)
                    if aresta not in classificacao_arestas:
                        classificacao_arestas[aresta] = 'retorno'
                    tem_ciclo = True
                    
                elif estado[v] == 'visitado':
                    # Verifica se é aresta de avanço ou cruzamento
                    if aresta not in classificacao_arestas:
                        if descoberta[u] < descoberta[v]:
                            # u foi descoberto antes de v - pode ser avanço
                            if v in _obter_descendentes(u, anterior):
                                classificacao_arestas[aresta] = 'avanco'
                            else:
                                classificacao_arestas[aresta] = 'cruzamento'
                        else:
                            # v foi descoberto antes de u
                            classificacao_arestas[aresta] = 'cruzamento'
            
            # Marca como visitado e registra finalização
            estado[u] = 'visitado'
            tempo[0] += 1
            finalizacao[u] = tempo[0]
        
        def _obter_descendentes(u: str, anterior_dict: dict) -> set:
            """Obtém todos os descendentes de u na árvore DFS"""
            descendentes = set()
            for vertice, pai in anterior_dict.items():
                if pai == u:
                    descendentes.add(vertice)
                    descendentes.update(_obter_descendentes(vertice, anterior_dict))
            return descendentes
        
        # Executa DFS a partir do vértice inicial
        dfs_visitar(start.nome)
        componentes.append(ordem_visita.copy())
        
        # Visita vértices não alcançados (outras componentes conexas)
        for nome in graph.vertices:
            if estado[nome] == 'nao_visitado':
                componente_atual = []
                vertices_antes = len(ordem_visita)
                dfs_visitar(nome)
                componente_atual = ordem_visita[vertices_antes:]
                componentes.append(componente_atual)
        
        return {
            'descoberta': descoberta,
            'finalizacao': finalizacao,
            'anterior': anterior,
            'classificacao_arestas': classificacao_arestas,
            'ordem_visita': ordem_visita,
            'tem_ciclo': tem_ciclo,
            'componentes': componentes
        }
    