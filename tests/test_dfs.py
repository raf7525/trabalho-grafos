import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.graph import Grafo, Vertice
from src.graphs.algorithms import Sorting
from tests.base import HelperTest


class TestDFS:
    
    def test_dfs_grafo_pequeno_linear(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        grafo.adicionar_aresta(vertices['d'], vertices['e'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        assert len(resultado['ordem_visita']) == 5
        assert resultado['ordem_visita'][0] == 'A'
        
        assert resultado['descoberta']['A'] < resultado['finalizacao']['A']
        assert resultado['descoberta']['A'] == 1
        
        assert resultado['anterior']['A'] is None
        assert resultado['anterior']['B'] == 'A'
        
        assert resultado['tem_ciclo'] == False
        
        tipos_arestas = set(resultado['classificacao_arestas'].values())
        assert 'arvore' in tipos_arestas
        assert 'retorno' not in tipos_arestas
    
    def test_dfs_grafo_com_ciclo(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['c'], vertices['a'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        assert resultado['tem_ciclo'] == True
        
        tipos_arestas = list(resultado['classificacao_arestas'].values())
        assert 'retorno' in tipos_arestas
        assert tipos_arestas.count('arvore') == 2
        assert tipos_arestas.count('retorno') == 1
    
    def test_dfs_classificacao_arestas_arvore(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        assert resultado['tem_ciclo'] == False
        tipos_arestas = list(resultado['classificacao_arestas'].values())
        assert all(tipo == 'arvore' for tipo in tipos_arestas)
        assert len(tipos_arestas) == 3
    
    def test_dfs_ordem_visita(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        assert resultado['ordem_visita'][0] == 'A'
        
        assert len(resultado['ordem_visita']) == 5
        assert 'B' in resultado['ordem_visita']
        assert 'C' in resultado['ordem_visita']
        assert 'D' in resultado['ordem_visita']
        assert 'E' in resultado['ordem_visita']
    
    def test_dfs_componentes_conexos(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        assert len(resultado['componentes']) >= 2
        
        assert len(resultado['ordem_visita']) == 5
    
    def test_dfs_predecessor_correto(self):
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        assert resultado['anterior']['A'] is None
        
        assert resultado['anterior']['B'] == 'A'
        
        assert resultado['anterior']['C'] == 'B'
    
    def test_dfs_grafo_real_nova_descoberta(self):
        grafo = HelperTest.carregar_grafo_real()
        
        origem_nome = 'nova descoberta'
        assert origem_nome in grafo.vertices, f"Bairro '{origem_nome}' não encontrado no grafo"
        
        origem = grafo.vertices[origem_nome]
        resultado = Sorting.depth_first_search(grafo, origem)
        
        assert 'descoberta' in resultado
        assert 'finalizacao' in resultado
        assert 'anterior' in resultado
        assert 'ordem_visita' in resultado
        assert 'tem_ciclo' in resultado
        assert 'classificacao_arestas' in resultado
        
        assert resultado['ordem_visita'][0] == origem_nome
        
        assert len(resultado['ordem_visita']) > 10
        
        for vertice in resultado['ordem_visita']:
            assert resultado['descoberta'][vertice] < resultado['finalizacao'][vertice]
        
        assert resultado['tem_ciclo'] == True
        
        tipos_arestas = list(resultado['classificacao_arestas'].values())
        assert 'retorno' in tipos_arestas
        assert 'arvore' in tipos_arestas
    
    def test_dfs_grafo_real_boa_viagem(self):
        grafo = HelperTest.carregar_grafo_real()
        
        origem_nome = 'boa viagem'
        assert origem_nome in grafo.vertices
        
        origem = grafo.vertices[origem_nome]
        resultado = Sorting.depth_first_search(grafo, origem)
        
        assert resultado['ordem_visita'][0] == origem_nome
        
        assert 'nova descoberta' in resultado['ordem_visita']
        
        assert resultado['anterior'][origem_nome] is None
        
        for vertice in resultado['ordem_visita']:
            assert vertice in resultado['descoberta']
            assert vertice in resultado['finalizacao']