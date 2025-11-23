from collections import deque
import heapq
from typing import List, Tuple
from graphs.graph import Grafo, Vertice

class PositiveFloat(float):
    def __new__(cls, value):
        if value < 0:
            raise ValueError("Valor deve ser um número float positivo")
        return super(PositiveFloat, cls).__new__(cls, value)

class Algorithms:
    @staticmethod
    def dijkstra(graph: Grafo, start: Vertice, end: Vertice):
        """
        Implementação do algoritmo de Dijkstra para encontrar o caminho mais curto.
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
    def bellman_ford(graph: Grafo, start: Vertice, end: Vertice = None):
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
        
        # Relaxa todas as arestas |V| - 1 vezes
        for _ in range(len(graph.vertices)):
            relaxed_in_this_pass = False
            for u_name, v_name, peso_aresta in graph.get_all_directed_edges():
                if distancias[u_name] != float('inf') and distancias[u_name] + peso_aresta < distancias[v_name]:
                    distancias[v_name] = distancias[u_name] + peso_aresta
                    anterior[v_name] = u_name
                    relaxed_in_this_pass = True
            
        # Verifica se há ciclos negativos (V-ésima passagem)
        tem_ciclo_negativo = False
        for u_name, v_name, peso_aresta in graph.get_all_directed_edges():
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
        
        Retorna dict com:
            - niveis: nível de cada vértice na árvore BFS
            - distancias: distância em número de arestas
            - anterior: predecessor de cada vértice
            - arvore: estrutura da árvore de percurso
            - ordem_visita: ordem em que os vértices foram visitados
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
            nome_vertice_atual = fila.popleft()
            vertice_atual = graph.vertices[nome_vertice_atual]
            
            # Explora todos os vizinhos
            for vizinho_obj in vertice_atual.vizinhos:
                nome_vizinho = vizinho_obj.nome
                if nome_vizinho not in visitado:
                    visitado.add(nome_vizinho)
                    anterior[nome_vizinho] = nome_vertice_atual
                    niveis[nome_vizinho] = niveis[nome_vertice_atual] + 1
                    distancias[nome_vizinho] = distancias[nome_vertice_atual] + 1
                    arvore[nome_vertice_atual].append(nome_vizinho)
                    fila.append(nome_vizinho)
                    ordem_visita.append(nome_vizinho)
        
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
        resultado = Algorithms.breadth_first_search(graph, start)
        
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
        
        def dfs_visitar(nome_vertice_atual: str, pai: str = None):
            """Função auxiliar recursiva para visitar vértices
            
            Args:
                nome_vertice_atual: Vértice atual sendo visitado
                pai: Vértice predecessor (para grafos não-direcionados)
            """
            nonlocal tem_ciclo
            
            # Marca como visitando e registra descoberta
            estado[nome_vertice_atual] = 'visitando'
            tempo[0] += 1
            descoberta[nome_vertice_atual] = tempo[0]
            ordem_visita.append(nome_vertice_atual)
            
            vertice_atual = graph.vertices[nome_vertice_atual]
            
            # Explora todos os vizinhos
            for vizinho_obj in vertice_atual.vizinhos:
                nome_vizinho = vizinho_obj.nome
                # Cria chave de aresta ordenada para grafos não-direcionados
                aresta = tuple(sorted([nome_vertice_atual, nome_vizinho]))
                
                if estado[nome_vizinho] == 'nao_visitado':
                    # Aresta de árvore
                    anterior[nome_vizinho] = nome_vertice_atual
                    classificacao_arestas[aresta] = 'arvore'
                    dfs_visitar(nome_vizinho, nome_vertice_atual)
                    
                elif estado[nome_vizinho] == 'visitando' and nome_vizinho != pai:
                    # Aresta de retorno - indica ciclo
                    # Ignora se v é o pai direto (evita falso positivo em grafos não-direcionados)
                    if aresta not in classificacao_arestas:
                        classificacao_arestas[aresta] = 'retorno'
                    tem_ciclo = True
                    
                elif estado[nome_vizinho] == 'visitado':
                    # Verifica se é aresta de avanço ou cruzamento
                    if aresta not in classificacao_arestas:
                        if descoberta[nome_vertice_atual] < descoberta[nome_vizinho]:
                            # u foi descoberto antes de v - pode ser avanço
                            if nome_vizinho in _obter_descendentes(nome_vertice_atual, anterior):
                                classificacao_arestas[aresta] = 'avanco'
                            else:
                                classificacao_arestas[aresta] = 'cruzamento'
                        else:
                            # v foi descoberto antes de u
                            classificacao_arestas[aresta] = 'cruzamento'
            
            # Marca como visitado e registra finalização
            estado[nome_vertice_atual] = 'visitado'
            tempo[0] += 1
            finalizacao[nome_vertice_atual] = tempo[0]
        
        def _obter_descendentes(nome_vertice_pai: str, anterior_dict: dict) -> set:
            """Obtém todos os descendentes de u na árvore DFS"""
            descendentes = set()
            for vertice, pai in anterior_dict.items():
                if pai == nome_vertice_pai:
                    descendentes.add(vertice)
                    descendentes.update(_obter_descendentes(vertice, anterior_dict))
            return descendentes
        
        # Executa DFS a partir do vértice inicial
        dfs_visitar(start.nome)
        componentes.append(ordem_visita.copy())
        
        # Visita vértices não alcançados (outras componentes conexas)
        for nome_vertice in graph.vertices:
            if estado[nome_vertice] == 'nao_visitado':
                componente_atual = []
                vertices_antes = len(ordem_visita)
                dfs_visitar(nome_vertice)
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
