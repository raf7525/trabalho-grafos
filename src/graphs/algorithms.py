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
    def dijkstra(grafo: Grafo, inicio: Vertice, fim: Vertice):
        distancias = {}
        visitados = set()
        anterior = {}
        fila: List[Tuple[int, str]] = []
        
        for nome in grafo.vertices:
            distancias[nome] = float('inf')
            
        distancias[inicio.nome] = 0
        heapq.heappush(fila, (0, inicio.nome))
        
        while fila:
            _, nome_atual = heapq.heappop(fila)
            vertice = grafo.vertices[nome_atual]
            
            visitados.add(vertice)
            
            for vizinho in vertice.vizinhos:
                if vizinho in visitados: continue
    
                peso_aresta = PositiveFloat(grafo.obter_peso(nome_atual, vizinho.nome))
                nova_distancia = distancias[nome_atual] + peso_aresta
                
                if nova_distancia < distancias[vizinho.nome]:
                    distancias[vizinho.nome] = nova_distancia
                    anterior[vizinho.nome] = nome_atual
                    heapq.heappush(fila, (nova_distancia, vizinho.nome))

        caminho = []
        atual = fim.nome
        
        if atual not in anterior and atual != inicio.nome:
            return float('inf'), []
        
        while atual is not None:
            caminho.append(atual)
            atual = anterior.get(atual)
            if atual == inicio.nome:
                caminho.append(atual)
                break
        
        caminho.reverse()
        
        return distancias[fim.nome], caminho

    @staticmethod
    def bellman_ford(grafo: Union[Grafo, GrafoDirecionado], inicio: Vertice, fim: Vertice = None):
        distancias = {}
        anterior = {}
        
        for nome_vertice in grafo.vertices:
            distancias[nome_vertice] = float('inf')
        
        distancias[inicio.nome] = 0
        
       
        def obter_arestas_para_relaxar():
            if isinstance(grafo, GrafoDirecionado):
                yield from grafo.obter_arestas_direcionadas()
            else: 
                for nome_u, vertice_u in grafo.vertices.items():
                    for vizinho_v in vertice_u.vizinhos:
                        nome_v = vizinho_v.nome
                        peso_aresta = grafo.obter_peso(nome_u, nome_v)
                        yield nome_u, nome_v, peso_aresta

        
        for _ in range(len(grafo.vertices)):
            relaxou_nesta_passada = False
            for nome_u, nome_v, peso_aresta in obter_arestas_para_relaxar():
                if distancias[nome_u] != float('inf') and distancias[nome_u] + peso_aresta < distancias[nome_v]:
                    distancias[nome_v] = distancias[nome_u] + peso_aresta
                    anterior[nome_v] = nome_u
                    relaxou_nesta_passada = True
            
        
        tem_ciclo_negativo = False
        for nome_u, nome_v, peso_aresta in obter_arestas_para_relaxar():
            if distancias[nome_u] != float('inf') and distancias[nome_u] + peso_aresta < distancias[nome_v]:
                tem_ciclo_negativo = True
                break
        
       
        if fim is None:
            return distancias, anterior, tem_ciclo_negativo
        
        
        if tem_ciclo_negativo:
            raise ValueError("Grafo contém ciclo negativo")
        
        caminho = []
        atual = fim.nome
        
        if atual not in anterior and atual != inicio.nome:
            return float('inf'), []
        
        nos_caminho = set() 
        while atual is not None:
            if atual in nos_caminho: 
                return float('inf'), [] 
            nos_caminho.add(atual)
            caminho.append(atual)
            atual = anterior.get(atual)
            if atual == inicio.nome: 
                caminho.append(atual)
                break
        
        if caminho and caminho[-1] != inicio.nome:
            return float('inf'), []

        caminho.reverse()
        
        return distancias[fim.nome], caminho
    
    @staticmethod
    def breadth_first_search(grafo: Grafo, inicio: Vertice):
        visitado = set([inicio.nome])
        fila = deque([inicio.nome])
        anterior = {inicio.nome: None}
        niveis = {inicio.nome: 0}
        distancias = {inicio.nome: 0}
        arvore = {inicio.nome: []}
        ordem_visita = [inicio.nome]
        
        for nome in grafo.vertices:
            if nome != inicio.nome:
                niveis[nome] = float('inf')
                distancias[nome] = float('inf')
                arvore[nome] = []

        while fila:
            u = fila.popleft()
            vertice_atual = grafo.vertices[u]
            
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
    def bfs_shortest_path(grafo: Grafo, inicio: str, fim: str) -> Tuple[float, List[str]]:
        
        vertice_inicio = grafo.vertices.get(inicio)
        if not vertice_inicio:
            return float('inf'), []
        
        resultado = Sorting.breadth_first_search(grafo, vertice_inicio)
        
        if fim not in resultado['distancias'] or resultado['distancias'][fim] == float('inf'):
            return float('inf'), []
        
        
        caminho = []
        atual = fim
        while atual is not None:
            caminho.append(atual)
            atual = resultado['anterior'].get(atual)
        
        return resultado['distancias'][fim], list(reversed(caminho))

    @staticmethod
    def depth_first_search(grafo: Grafo, inicio: Vertice):
        estado = {nome: 'nao_visitado' for nome in grafo.vertices}
        descoberta = {}
        finalizacao = {}
        anterior = {nome: None for nome in grafo.vertices}
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
            
            vertice_atual = grafo.vertices[u]
            
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
        
        dfs_visitar(inicio.nome)
        componentes.append(ordem_visita.copy())
        
        for nome in grafo.vertices:
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
    