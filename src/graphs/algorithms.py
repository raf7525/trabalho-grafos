from collections import deque
import heapq
from typing import List, Tuple
from src.graphs.graph import Grafo, Vertice

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
            for (nome_u, nome_v), info in graph.arestas.items():
                peso_aresta = info['peso']
                
                # Relaxa em ambas as direções (grafo não direcionado)
                if distancias[nome_u] + peso_aresta < distancias[nome_v]:
                    distancias[nome_v] = distancias[nome_u] + peso_aresta
                    anterior[nome_v] = nome_u
                
                if distancias[nome_v] + peso_aresta < distancias[nome_u]:
                    distancias[nome_u] = distancias[nome_v] + peso_aresta
                    anterior[nome_u] = nome_v
        
        # Verifica se há ciclos negativos
        tem_ciclo_negativo = False
        for (nome_u, nome_v), info in graph.arestas.items():
            peso_aresta = info['peso']
            if distancias[nome_u] + peso_aresta < distancias[nome_v] or distancias[nome_v] + peso_aresta < distancias[nome_u]:
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
    def breadth_first_search(start, adjacencia):
        visitado = set([start])
        fila = deque([start])
        parent = {start: None}

        while fila:
            u = fila.popleft()
            for v in adjacencia[u]:
                if v not in visitado:
                    visitado.add(v)
                    parent[v] = u
                    fila.append(v)
        return parent


    @staticmethod
    def depth_first_search():
        pass
    