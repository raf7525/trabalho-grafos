import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.graph import Grafo, Vertice
from src.graphs.algorithms import Sorting
from tests.base import HelperTest


class TestDFS:
    """Testes para o algoritmo DFS (Depth-First Search)"""
    
    def test_dfs_grafo_pequeno_linear(self):
        """Testa DFS em grafo pequeno linear: A-B-C-D-E"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar cadeia: A - B - C - D - E
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        grafo.adicionar_aresta(vertices['d'], vertices['e'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # Verifica que todos os vértices foram visitados
        assert len(resultado['ordem_visita']) == 5
        assert resultado['ordem_visita'][0] == 'A'
        
        # Verifica timestamps
        assert resultado['descoberta']['A'] < resultado['finalizacao']['A']
        assert resultado['descoberta']['A'] == 1
        
        # Verifica predecessores (árvore DFS)
        assert resultado['anterior']['A'] is None
        assert resultado['anterior']['B'] == 'A'
        
        # Grafo linear não tem ciclos
        assert resultado['tem_ciclo'] == False
        
        # Verifica classificação de arestas - todas devem ser de árvore
        tipos_arestas = set(resultado['classificacao_arestas'].values())
        assert 'arvore' in tipos_arestas
        assert 'retorno' not in tipos_arestas  # Sem ciclos
    
    def test_dfs_grafo_com_ciclo(self):
        """Testa DFS em grafo com ciclo: A-B-C-A"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar triângulo: A - B - C - A
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        grafo.adicionar_aresta(vertices['c'], vertices['a'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # Deve detectar ciclo
        assert resultado['tem_ciclo'] == True
        
        # Deve haver pelo menos uma aresta de retorno
        tipos_arestas = list(resultado['classificacao_arestas'].values())
        assert 'retorno' in tipos_arestas
        assert tipos_arestas.count('arvore') == 2  # Duas arestas de árvore
        assert tipos_arestas.count('retorno') == 1  # Uma aresta de retorno
    
    def test_dfs_timestamps_corretos(self):
        """Verifica se os timestamps de descoberta e finalização são consistentes"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar árvore simples
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # Para cada vértice, descoberta < finalização
        for vertice in resultado['ordem_visita']:
            assert resultado['descoberta'][vertice] < resultado['finalizacao'][vertice]
        
        # Timestamps devem ser únicos e em sequência
        todas_descobertas = sorted(resultado['descoberta'].values())
        todas_finalizacoes = sorted(resultado['finalizacao'].values())
        
        # Verifica se não há duplicatas
        assert len(set(todas_descobertas)) == len(todas_descobertas)
        assert len(set(todas_finalizacoes)) == len(todas_finalizacoes)
    
    def test_dfs_classificacao_arestas_arvore(self):
        """Testa classificação de arestas em árvore"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar árvore: A como raiz, B e C como filhos, D filho de B
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        grafo.adicionar_aresta(vertices['b'], vertices['d'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # Em uma árvore, todas as arestas devem ser de árvore
        assert resultado['tem_ciclo'] == False
        tipos_arestas = list(resultado['classificacao_arestas'].values())
        assert all(tipo == 'arvore' for tipo in tipos_arestas)
        assert len(tipos_arestas) == 3  # 3 arestas
    
    def test_dfs_ordem_visita(self):
        """Verifica se a ordem de visita segue o padrão DFS"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar grafo simples
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['a'], vertices['c'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # A deve ser visitado primeiro
        assert resultado['ordem_visita'][0] == 'A'
        
        # Todos os 5 vértices devem ser visitados (DFS visita componentes desconexas)
        assert len(resultado['ordem_visita']) == 5
        assert 'B' in resultado['ordem_visita']
        assert 'C' in resultado['ordem_visita']
        assert 'D' in resultado['ordem_visita']
        assert 'E' in resultado['ordem_visita']
    
    def test_dfs_componentes_conexos(self):
        """Testa detecção de componentes conexos"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar dois componentes separados: A-B e C-D
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['c'], vertices['d'])
        # E fica isolado
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # Deve detectar múltiplos componentes
        assert len(resultado['componentes']) >= 2
        
        # Todos vértices devem ser visitados
        assert len(resultado['ordem_visita']) == 5
    
    def test_dfs_predecessor_correto(self):
        """Verifica se os predecessores formam uma árvore válida"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar caminho: A - B - C
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        
        resultado = Sorting.depth_first_search(grafo, vertices['a'])
        
        # A é a raiz
        assert resultado['anterior']['A'] is None
        
        # B deve ter A como predecessor
        assert resultado['anterior']['B'] == 'A'
        
        # C deve ter B como predecessor
        assert resultado['anterior']['C'] == 'B'
    
    def test_dfs_grafo_real_nova_descoberta(self):
        """Testa DFS no grafo real dos bairros do Recife a partir de Nova Descoberta"""
        grafo = HelperTest.carregar_grafo_real()
        
        origem_nome = 'nova descoberta'
        assert origem_nome in grafo.vertices, f"Bairro '{origem_nome}' não encontrado no grafo"
        
        origem = grafo.vertices[origem_nome]
        resultado = Sorting.depth_first_search(grafo, origem)
        
        # Verifica estrutura do resultado
        assert 'descoberta' in resultado
        assert 'finalizacao' in resultado
        assert 'anterior' in resultado
        assert 'ordem_visita' in resultado
        assert 'tem_ciclo' in resultado
        assert 'classificacao_arestas' in resultado
        
        # Origem deve ser o primeiro visitado
        assert resultado['ordem_visita'][0] == origem_nome
        
        # Deve visitar vários bairros (grafo é conexo)
        assert len(resultado['ordem_visita']) > 10
        
        # Timestamps devem ser consistentes
        for vertice in resultado['ordem_visita']:
            assert resultado['descoberta'][vertice] < resultado['finalizacao'][vertice]
        
        # Grafo de bairros deve ter ciclos (não é árvore)
        assert resultado['tem_ciclo'] == True
        
        # Deve haver arestas de retorno
        tipos_arestas = list(resultado['classificacao_arestas'].values())
        assert 'retorno' in tipos_arestas
        assert 'arvore' in tipos_arestas
    
    def test_dfs_grafo_real_boa_viagem(self):
        """Testa DFS a partir de Boa Viagem"""
        grafo = HelperTest.carregar_grafo_real()
        
        origem_nome = 'boa viagem'
        assert origem_nome in grafo.vertices
        
        origem = grafo.vertices[origem_nome]
        resultado = Sorting.depth_first_search(grafo, origem)
        
        # Origem deve ser o primeiro
        assert resultado['ordem_visita'][0] == origem_nome
        
        # Deve alcançar Nova Descoberta (grafo é conexo)
        assert 'nova descoberta' in resultado['ordem_visita']
        
        # Verifica que tem predecessor correto (exceto raiz e início de componentes)
        # O vértice inicial não tem predecessor
        assert resultado['anterior'][origem_nome] is None
        
        # Verifica que todos os outros vértices têm descoberta/finalização
        for vertice in resultado['ordem_visita']:
            assert vertice in resultado['descoberta']
            assert vertice in resultado['finalizacao']
    
    def test_dfs_metodo_helper_grafo(self):
        """Testa o método helper busca_em_profundidade() da classe Grafo"""
        grafo, vertices = HelperTest.criar_grafo_com_vertices()
        
        # Criar grafo simples
        grafo.adicionar_aresta(vertices['a'], vertices['b'])
        grafo.adicionar_aresta(vertices['b'], vertices['c'])
        
        # Testa com string
        resultado1 = grafo.busca_em_profundidade('A')
        assert resultado1['ordem_visita'][0] == 'A'
        
        # Testa com objeto Vertice
        resultado2 = grafo.busca_em_profundidade(vertices['a'])
        assert resultado2['ordem_visita'][0] == 'A'
        
        # Ambos devem produzir o mesmo resultado
        assert resultado1['ordem_visita'] == resultado2['ordem_visita']
    
    def test_dfs_comparacao_com_bfs_alcance(self):
        """Compara se DFS e BFS alcançam vértices da componente conexa"""
        grafo = HelperTest.carregar_grafo_real()
        
        origem_nome = 'nova descoberta'
        origem = grafo.vertices[origem_nome]
        
        resultado_dfs = Sorting.depth_first_search(grafo, origem)
        resultado_bfs = Sorting.breadth_first_search(grafo, origem)
        
        # DFS visita TODAS as componentes conexas, BFS só a componente da origem
        # Logo, DFS deve ter >= vertices que BFS
        assert len(resultado_dfs['ordem_visita']) >= len(resultado_bfs['ordem_visita'])
        
        # Verifica que ambos alcançam a origem
        assert origem_nome in resultado_dfs['ordem_visita']
        assert origem_nome in resultado_bfs['ordem_visita']
        
        # Todos os vértices alcançados por BFS devem estar em DFS
        vertices_bfs = set(resultado_bfs['ordem_visita'])
        vertices_dfs = set(resultado_dfs['ordem_visita'])
        assert vertices_bfs.issubset(vertices_dfs)
        
        # Verifica que DFS encontrou outras componentes (se houver)
        if len(vertices_dfs) > len(vertices_bfs):
            print(f"\nDFS encontrou {len(vertices_dfs) - len(vertices_bfs)} vértices em outras componentes conexas")
            print(f"Vértices desconectados: {vertices_dfs - vertices_bfs}")
