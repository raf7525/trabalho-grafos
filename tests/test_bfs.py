import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.graph import Grafo, Vertice
from src.graphs.algorithms import Sorting
from tests.base import HelperTest


class TestBFS:
    
    def test_bfs_grafo_pequeno_simples(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        grafo.adicionar_aresta(vertices['d'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        assert resultado['niveis']['A'] == 0
        assert resultado['niveis']['B'] == 1
        assert resultado['niveis']['C'] == 2
        assert resultado['niveis']['D'] == 3
        assert resultado['niveis']['E'] == 4
        
        assert resultado['distancias']['A'] == 0
        assert resultado['distancias']['B'] == 1
        assert resultado['distancias']['E'] == 4
        
        assert resultado['anterior']['A'] is None
        assert resultado['anterior']['B'] == 'A'
        assert resultado['anterior']['C'] == 'B'
        
        assert resultado['ordem_visita'][0] == 'A'
        assert 'E' in resultado['ordem_visita']
    
    def test_bfs_grafo_com_ramificacoes(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['a'], vertices['d'])
        grafo.adicionar_aresta(vertices['a'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        assert resultado['niveis']['A'] == 0
        
        assert resultado['niveis']['B'] == 1
        assert resultado['niveis']['C'] == 1
        assert resultado['niveis']['D'] == 1
        assert resultado['niveis']['E'] == 1
        
        assert resultado['anterior']['B'] == 'A'
        assert resultado['anterior']['C'] == 'A'
        assert resultado['anterior']['D'] == 'A'
        assert resultado['anterior']['E'] == 'A'
        
        assert len(resultado['arvore']['A']) == 4
        assert set(resultado['arvore']['A']) == {'B', 'C', 'D', 'E'}
    
    def test_bfs_no_isolado(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        assert resultado['niveis']['A'] == 0
        assert resultado['niveis']['B'] == 1
        
        assert resultado['niveis']['C'] == float('inf')
        assert resultado['niveis']['D'] == float('inf')
        assert resultado['niveis']['E'] == float('inf')
        
        assert len(resultado['ordem_visita']) == 2
        assert 'A' in resultado['ordem_visita']
        assert 'B' in resultado['ordem_visita']
        assert 'C' not in resultado['ordem_visita']
    
    def test_bfs_arvore_de_percurso(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        grafo.adicionar_aresta(vertices['c'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        assert set(resultado['arvore']['A']) == {'B', 'C'}
        
        assert 'D' in resultado['arvore']['B']
        
        assert 'E' in resultado['arvore']['C']
        
        assert resultado['arvore']['D'] == []
        assert resultado['arvore']['E'] == []
    
    def test_bfs_distancias_corretas(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        grafo.adicionar_aresta(vertices['c'], vertices['e'])
        grafo.adicionar_aresta(vertices['d'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        assert resultado['distancias']['A'] == 0
        assert resultado['distancias']['B'] == 1
        assert resultado['distancias']['C'] == 2
        assert resultado['distancias']['D'] == 2
        assert resultado['distancias']['E'] == 3
    
    def test_bfs_grafo_real_recife(self):
        grafo = HelperTest.carregar_grafo_real()
        
        origem = 'nova descoberta'
        assert origem in grafo.vertices, f"Bairro '{origem}' não encontrado no grafo"
        
        resultado = grafo.busca_em_largura(origem)
        
        assert resultado['niveis'][origem] == 0
        assert resultado['distancias'][origem] == 0
        assert resultado['anterior'][origem] is None
        
        vizinhos = grafo.obter_vizinhos(origem)
        for vizinho in vizinhos:
            assert resultado['niveis'][vizinho] == 1
            assert resultado['anterior'][vizinho] == origem
        
        assert resultado['ordem_visita'][0] == origem
        
        alcancaveis = [v for v in resultado['ordem_visita']]
        for bairro in alcancaveis:
            assert resultado['distancias'][bairro] != float('inf')
            assert resultado['niveis'][bairro] != float('inf')
    
    def test_bfs_recife_boa_viagem_a_partir_nova_descoberta(self):
        grafo = HelperTest.carregar_grafo_real()
        
        origem = 'nova descoberta'
        destino = 'boa viagem'
        
        assert origem in grafo.vertices
        assert destino in grafo.vertices
        
        resultado = grafo.busca_em_largura(origem)
        
        assert resultado['distancias'][destino] != float('inf')
        assert resultado['distancias'][destino] > 0
        
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = resultado['anterior'].get(atual)
        caminho.reverse()
        
        assert caminho[0] == origem
        assert caminho[-1] == destino
        assert len(caminho) == resultado['distancias'][destino] + 1
    
    def test_bfs_todos_vertices_inicializados(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        for nome in ['A', 'B', 'C', 'D', 'E']:
            assert nome in resultado['niveis']
            assert nome in resultado['distancias']
            assert nome in resultado['arvore']
        
        assert resultado['niveis']['C'] == float('inf')
        assert resultado['niveis']['D'] == float('inf')
        assert resultado['niveis']['E'] == float('inf')
