import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.graph import Grafo, Vertice
from src.graphs.algorithms import Sorting
from tests.base import HelperTest


class TestBFS:
    """Testes para o algoritmo BFS (Breadth-First Search)"""
    
    def test_bfs_grafo_pequeno_simples(self):
        """Testa BFS em grafo pequeno com caminho simples: A-B-C-D-E"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar cadeia: A - B - C - D - E
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        grafo.adicionar_aresta(vertices['d'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        # Verifica níveis
        assert resultado['niveis']['A'] == 0
        assert resultado['niveis']['B'] == 1
        assert resultado['niveis']['C'] == 2
        assert resultado['niveis']['D'] == 3
        assert resultado['niveis']['E'] == 4
        
        # Verifica distâncias (mesmo que níveis neste caso)
        assert resultado['distancias']['A'] == 0
        assert resultado['distancias']['B'] == 1
        assert resultado['distancias']['E'] == 4
        
        # Verifica predecessores
        assert resultado['anterior']['A'] is None
        assert resultado['anterior']['B'] == 'A'
        assert resultado['anterior']['C'] == 'B'
        
        # Verifica ordem de visita
        assert resultado['ordem_visita'][0] == 'A'
        assert 'E' in resultado['ordem_visita']
    
    def test_bfs_grafo_com_ramificacoes(self):
        """Testa BFS em grafo com múltiplas ramificações"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar estrela: A no centro conectado a B, C, D, E
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['a'], vertices['d'])
        grafo.adicionar_aresta(vertices['a'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        # A está no nível 0
        assert resultado['niveis']['A'] == 0
        
        # Todos os outros devem estar no nível 1 (vizinhos diretos)
        assert resultado['niveis']['B'] == 1
        assert resultado['niveis']['C'] == 1
        assert resultado['niveis']['D'] == 1
        assert resultado['niveis']['E'] == 1
        
        # Todos devem ter A como predecessor
        assert resultado['anterior']['B'] == 'A'
        assert resultado['anterior']['C'] == 'A'
        assert resultado['anterior']['D'] == 'A'
        assert resultado['anterior']['E'] == 'A'
        
        # A deve ter 4 filhos na árvore
        assert len(resultado['arvore']['A']) == 4
        assert set(resultado['arvore']['A']) == {'B', 'C', 'D', 'E'}
    
    def test_bfs_no_isolado(self):
        """Testa BFS com nó isolado (inalcançável)"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Conecta apenas A-B e C-D, E fica isolado
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        # E não tem conexões
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        # A e B devem ser alcançados
        assert resultado['niveis']['A'] == 0
        assert resultado['niveis']['B'] == 1
        
        # C, D, E devem ser inalcançáveis (infinito)
        assert resultado['niveis']['C'] == float('inf')
        assert resultado['niveis']['D'] == float('inf')
        assert resultado['niveis']['E'] == float('inf')
        
        # Apenas A e B na ordem de visita
        assert len(resultado['ordem_visita']) == 2
        assert 'A' in resultado['ordem_visita']
        assert 'B' in resultado['ordem_visita']
        assert 'C' not in resultado['ordem_visita']
    
    def test_bfs_arvore_de_percurso(self):
        """Testa construção da árvore de percurso BFS"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar árvore: A -> B, C; B -> D; C -> E
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        grafo.adicionar_aresta(vertices['c'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        # A deve ter B e C como filhos
        assert set(resultado['arvore']['A']) == {'B', 'C'}
        
        # B deve ter D como filho
        assert 'D' in resultado['arvore']['B']
        
        # C deve ter E como filho
        assert 'E' in resultado['arvore']['C']
        
        # D e E não têm filhos
        assert resultado['arvore']['D'] == []
        assert resultado['arvore']['E'] == []
    
    def test_bfs_distancias_corretas(self):
        """Testa se as distâncias (em arestas) estão corretas"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # A - B - C
        #     |   |
        #     D - E
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        grafo.adicionar_aresta(vertices['c'], vertices['e'])
        grafo.adicionar_aresta(vertices['d'], vertices['e'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        # Distâncias de A
        assert resultado['distancias']['A'] == 0
        assert resultado['distancias']['B'] == 1  # A -> B
        assert resultado['distancias']['C'] == 2  # A -> B -> C
        assert resultado['distancias']['D'] == 2  # A -> B -> D
        assert resultado['distancias']['E'] == 3  # A -> B -> C -> E ou A -> B -> D -> E
    
    def test_bfs_helper_method_grafo(self):
        """Testa o método helper busca_em_largura() da classe Grafo"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        
        # Testa com objeto Vertice
        resultado1 = grafo.busca_em_largura(vertices['a'])
        assert resultado1['niveis']['A'] == 0
        assert resultado1['niveis']['B'] == 1
        assert resultado1['niveis']['C'] == 2
        
        # Testa com string
        resultado2 = grafo.busca_em_largura('A')
        assert resultado2['niveis']['A'] == 0
        assert resultado2['niveis']['B'] == 1
        assert resultado2['niveis']['C'] == 2
    
    def test_bfs_grafo_real_recife(self):
        """Testa BFS no grafo real dos bairros do Recife"""
        grafo = HelperTest.carregar_grafo_real()
        
        # Testa a partir de Nova Descoberta
        origem = 'nova descoberta'
        assert origem in grafo.vertices, f"Bairro '{origem}' não encontrado no grafo"
        
        resultado = grafo.busca_em_largura(origem)
        
        # Verifica que a origem está no nível 0
        assert resultado['niveis'][origem] == 0
        assert resultado['distancias'][origem] == 0
        assert resultado['anterior'][origem] is None
        
        # Verifica que há vizinhos no nível 1
        vizinhos = grafo.obter_vizinhos(origem)
        for vizinho in vizinhos:
            assert resultado['niveis'][vizinho] == 1
            assert resultado['anterior'][vizinho] == origem
        
        # Verifica que a ordem de visita começa com a origem
        assert resultado['ordem_visita'][0] == origem
        
        # Verifica que bairros alcançáveis têm distância finita
        alcancaveis = [v for v in resultado['ordem_visita']]
        for bairro in alcancaveis:
            assert resultado['distancias'][bairro] != float('inf')
            assert resultado['niveis'][bairro] != float('inf')
    
    def test_bfs_recife_boa_viagem_a_partir_nova_descoberta(self):
        """Testa se Boa Viagem é alcançável a partir de Nova Descoberta via BFS"""
        grafo = HelperTest.carregar_grafo_real()
        
        origem = 'nova descoberta'
        destino = 'boa viagem'
        
        assert origem in grafo.vertices
        assert destino in grafo.vertices
        # tocaram na minha porta
        resultado = grafo.busca_em_largura(origem)
        
        # Boa Viagem deve ser alcançável (distância finita)
        assert resultado['distancias'][destino] != float('inf')
        assert resultado['distancias'][destino] > 0
        
        # Reconstrói o caminho
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = resultado['anterior'].get(atual)
        caminho.reverse()
        
        # Verifica caminho
        assert caminho[0] == origem
        assert caminho[-1] == destino
        assert len(caminho) == resultado['distancias'][destino] + 1
    
    def test_bfs_todos_vertices_inicializados(self):
        """Testa se todos os vértices são inicializados, mesmo os não alcançáveis"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Conecta apenas A-B
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        
        resultado = Sorting.breadth_first_search(grafo, vertices['a'])
        
        # Todos os vértices devem estar presentes nos dicionários
        for nome in ['A', 'B', 'C', 'D', 'E']:
            assert nome in resultado['niveis']
            assert nome in resultado['distancias']
            assert nome in resultado['arvore']
        
        # C, D, E devem ter distância infinita
        assert resultado['niveis']['C'] == float('inf')
        assert resultado['niveis']['D'] == float('inf')
        assert resultado['niveis']['E'] == float('inf')
