from collections import deque
import heapq
from typing import List, Tuple
from graphs.graph import Grafo, Vertice

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
    def bellman_ford(graph: Grafo, start: Vertice, end: Vertice = None):
        """
        Initialize the 'distances' and 'previous' containers
        Set the distance for the starting vertex to 0
        Relax all edges |V| - 1 times
            For each edge in the graph
                If the distance to the destination can be shortened
                    Update the distance and previous vertex
        Check for negative cycles
        If end is specified, reconstruct the path
        """
        # Inicializa distâncias e predecessores
        distancias = {}
        anterior = {}
        
        # Inicializa todos os vértices como infinito
        for nome in graph.vertices:
            distancias[nome] = float('inf')
        
        distancias[start.nome] = 0
        
        # Relaxa todas as arestas |V| - 1 vezes
        
        for _ in range( len(graph.vertices) - 1):
            # Para cada aresta no grafo
            for (origem, destino), info in graph.arestas.items():
                peso_aresta = info['peso']
                
                # Relaxa em ambas as direções (grafo não direcionado)
                pode_relaxar_ida = distancias[origem] + peso_aresta < distancias[destino]
                if pode_relaxar_ida:
                    distancias[destino] = distancias[origem] + peso_aresta
                    anterior[destino] = origem
                
                pode_relaxar_volta = distancias[destino] + peso_aresta < distancias[origem]
                if pode_relaxar_volta:
                    distancias[origem] = distancias[destino] + peso_aresta
                    anterior[origem] = destino
        
        # Verifica se há ciclos negativos
        tem_ciclo_negativo = False
        for (origem, destino), info in graph.arestas.items():
            peso_aresta = info['peso']
            pode_relaxar_ida = distancias[origem] + peso_aresta < distancias[destino]
            pode_relaxar_volta = distancias[destino] + peso_aresta < distancias[origem]
            if pode_relaxar_ida or pode_relaxar_volta:
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
    def depth_first_search():
        pass
    