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
        
        distancias = {}
        visitados = set()
        anterior = {}
        fila: List[Tuple[int, str]] = []
        
        
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
        
       
        distancias = {}
        anterior = {}
        
        
        for nome_vertice in graph.vertices:
            distancias[nome_vertice] = float('inf')
        
        distancias[start.nome] = 0
        
       
        def get_edges_to_relax():
            if isinstance(graph, GrafoDirecionado):
                yield from graph.obter_arestas_direcionadas()
            else: 
                for u_name, vertice_u in graph.vertices.items():
                    for vizinho_v in vertice_u.vizinhos:
                        v_name = vizinho_v.nome
                        peso_aresta = graph.obter_peso(u_name, v_name)
                        yield u_name, v_name, peso_aresta

        
        for _ in range(len(graph.vertices)):
            relaxed_in_this_pass = False
            for u_name, v_name, peso_aresta in get_edges_to_relax():
                if distancias[u_name] != float('inf') and distancias[u_name] + peso_aresta < distancias[v_name]:
                    distancias[v_name] = distancias[u_name] + peso_aresta
                    anterior[v_name] = u_name
                    relaxed_in_this_pass = True
            
        
        tem_ciclo_negativo = False
        for u_name, v_name, peso_aresta in get_edges_to_relax():
            if distancias[u_name] != float('inf') and distancias[u_name] + peso_aresta < distancias[v_name]:
                tem_ciclo_negativo = True
                break
        
       
        if end is None:
            return distancias, anterior, tem_ciclo_negativo
        
        
        if tem_ciclo_negativo:
            raise ValueError("Grafo contém ciclo negativo")
        
        
        caminho = []
        atual = end.nome
        
        if atual not in anterior and atual != start.nome:
            return float('inf'), [] 
        
        path_nodes = set() 
        while atual is not None:
            if atual in path_nodes: 
                return float('inf'), [] 
            path_nodes.add(atual)
            caminho.append(atual)
            atual = anterior.get(atual)
            if atual == start.nome: 
                caminho.append(atual)
                break
        
        
        if caminho and caminho[-1] != start.nome:
            return float('inf'), []

        caminho.reverse()
        
        return distancias[end.nome], caminho
    
    @staticmethod
    def breadth_first_search(graph: Grafo, start: Vertice):
        
        visitado = set([start.nome])
        fila = deque([start.nome])
        anterior = {start.nome: None}
        niveis = {start.nome: 0}
        distancias = {start.nome: 0}
        arvore = {start.nome: []}
        ordem_visita = [start.nome]
        
        
        for nome in graph.vertices:
            if nome != start.nome:
                niveis[nome] = float('inf')
                distancias[nome] = float('inf')
                arvore[nome] = []

        while fila:
            u = fila.popleft()
            vertice_atual = graph.vertices[u]
            
            
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
        
        resultado = Sorting.breadth_first_search(graph, start)
        
        if end.nome not in resultado['distancias'] or resultado['distancias'][end.nome] == float('inf'):
            return float('inf'), []
        
        
        caminho = []
        atual = end.nome
        while atual is not None:
            caminho.append(atual)
            atual = resultado['anterior'].get(atual)
        
        return resultado['distancias'][end.nome], list(reversed(caminho))

    @staticmethod
    def depth_first_search(graph: Grafo, start: Vertice):
        
        
        estado = {nome: 'nao_visitado' for nome in graph.vertices}
        descoberta = {}
        finalizacao = {}
        anterior = {nome: None for nome in graph.vertices}
        classificacao_arestas = {}
        ordem_visita = []
        tempo = [0]  
        tem_ciclo = False
        componentes = []
        
        def dfs_visitar(u: str, pai: str = None):
            
            nonlocal tem_ciclo
            
           
            estado[u] = 'visitando'
            tempo[0] += 1
            descoberta[u] = tempo[0]
            ordem_visita.append(u)
            
            vertice_atual = graph.vertices[u]
            
            
            for vizinho in vertice_atual.vizinhos:
                v = vizinho.nome
                
                aresta = tuple(sorted([u, v]))
                
                if estado[v] == 'nao_visitado':
                    
                    anterior[v] = u
                    classificacao_arestas[aresta] = 'arvore'
                    dfs_visitar(v, u)
                    
                elif estado[v] == 'visitando' and v != pai:
                    
                    if aresta not in classificacao_arestas:
                        classificacao_arestas[aresta] = 'retorno'
                    tem_ciclo = True
                    
                elif estado[v] == 'visitado':
                    
                    if aresta not in classificacao_arestas:
                        if descoberta[u] < descoberta[v]:
                            
                            if v in _obter_descendentes(u, anterior):
                                classificacao_arestas[aresta] = 'avanco'
                            else:
                                classificacao_arestas[aresta] = 'cruzamento'
                        else:
                            
                            classificacao_arestas[aresta] = 'cruzamento'
            
            
            estado[u] = 'visitado'
            tempo[0] += 1
            finalizacao[u] = tempo[0]
        
        def _obter_descendentes(u: str, anterior_dict: dict) -> set:
            
            descendentes = set()
            for vertice, pai in anterior_dict.items():
                if pai == u:
                    descendentes.add(vertice)
                    descendentes.update(_obter_descendentes(vertice, anterior_dict))
            return descendentes
        
       
        dfs_visitar(start.nome)
        componentes.append(ordem_visita.copy())
        
        
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
    