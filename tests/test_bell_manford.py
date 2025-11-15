import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.algorithms import Sorting
from tests.base import HelperTest

"""
Para rodar esta outra bomba, usa:
pytest tests/test_bell_manford.py # Roda apenas esse arquivo de teste
ou
pytest # Roda todos os testes
"""


class TestBellmanFordGrafoSimples:
    """Testes do Bellman-Ford com grafos pequenos e controlados"""
    
    def setup_method(self):
        """Cria um grafo simples antes de cada teste"""
        self.grafo, self.v = HelperTest.criar_grafo_com_vertices()
    
    def test_caminho_direto(self):
        """Testa caminho direto entre dois nós"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=5.0)
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['b'])
        
        assert distancia == 5.0
        HelperTest.assert_caminho_direto(caminho, "A", "B")
    
    def test_caminho_indireto_mais_curto(self):
        """Testa quando o caminho indireto é mais curto que o direto"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=10.0)
        self.grafo.adicionar_aresta(self.v['a'], self.v['c'], peso=3.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['b'], peso=2.0)
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['b'])
        
        assert distancia == 5.0  # 3 + 2 < 10
        assert caminho == ["A", "C", "B"]
    
    def test_multiplos_caminhos(self):
        """Testa grafo com múltiplos caminhos possíveis"""
        # A -> C -> D -> E
        self.grafo.adicionar_aresta(self.v['a'], self.v['c'], peso=2.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['d'], peso=3.0)
        self.grafo.adicionar_aresta(self.v['d'], self.v['e'], peso=1.0)
        
        # A -> B -> E (caminho alternativo)
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=4.0)
        self.grafo.adicionar_aresta(self.v['b'], self.v['e'], peso=5.0)
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['e'])
        
        assert distancia == 6.0  # A->C->D->E = 2+3+1 = 6 (menor que A->B->E = 9)
        assert caminho == ["A", "C", "D", "E"]
    
    def test_no_origem_igual_destino(self):
        """Testa quando origem e destino são o mesmo nó"""
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['a'])
        
        assert distancia == 0.0
        assert caminho == ["A"]
    
    def test_caminho_inexistente(self):
        """Testa quando não há caminho entre origem e destino"""
        # A e D estão desconectados
        self.grafo.adicionar_aresta(self.v['c'], self.v['d'], peso=1.0)
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['d'])
        
        HelperTest.assert_distancia_infinita(distancia)
        assert caminho == []
    
    def test_grafo_linear(self):
        """Testa caminho em grafo linear A-B-C-D-E"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=1.0)
        self.grafo.adicionar_aresta(self.v['b'], self.v['c'], peso=2.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['d'], peso=3.0)
        self.grafo.adicionar_aresta(self.v['d'], self.v['e'], peso=4.0)
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['e'])
        
        assert distancia == 10.0  # 1+2+3+4
        assert caminho == ["A", "B", "C", "D", "E"]
    
    def test_pesos_decimais(self):
        """Testa com pesos decimais"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=1.5)
        self.grafo.adicionar_aresta(self.v['b'], self.v['c'], peso=2.3)
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['c'])
        
        HelperTest.assert_distancia_aproximada(distancia, 3.8)
        assert caminho == ["A", "B", "C"]
    
    def test_retorno_todas_distancias(self):
        """Testa quando não especifica destino - retorna todas as distâncias"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=1.0)
        self.grafo.adicionar_aresta(self.v['b'], self.v['c'], peso=2.0)
        self.grafo.adicionar_aresta(self.v['a'], self.v['c'], peso=5.0)
        
        distancias, _, tem_ciclo = Sorting.bellman_ford(self.grafo, self.v['a'])
        
        assert distancias["A"] == 0.0
        assert distancias["B"] == 1.0
        assert distancias["C"] == 3.0  # Via B: 1+2
        HelperTest.assert_distancia_infinita(distancias["D"])
        HelperTest.assert_distancia_infinita(distancias["E"])
        assert tem_ciclo == False
    
    def test_comparacao_com_dijkstra(self):
        """Compara resultados do Bellman-Ford com Dijkstra (devem ser iguais)"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=4.0)
        self.grafo.adicionar_aresta(self.v['a'], self.v['c'], peso=2.0)
        self.grafo.adicionar_aresta(self.v['b'], self.v['c'], peso=1.0)
        self.grafo.adicionar_aresta(self.v['b'], self.v['d'], peso=5.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['d'], peso=8.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['e'], peso=10.0)
        self.grafo.adicionar_aresta(self.v['d'], self.v['e'], peso=2.0)
        
        dist_bf, _ = Sorting.bellman_ford(self.grafo, self.v['a'], self.v['e'])
        dist_dj, _ = Sorting.dijkstra(self.grafo, self.v['a'], self.v['e'])
        
        assert dist_bf == dist_dj


class TestBellmanFordGrafoReal:
    """Testes do Bellman-Ford com o grafo real dos bairros do Recife"""
    
    @classmethod
    def setup_class(cls):
        """Carrega o grafo uma vez para toda a classe"""
        cls.grafo = HelperTest.carregar_grafo_real()
    
    def test_casa_forte_para_boa_viagem(self):
        """Testa caminho de Casa Forte para Boa Viagem"""
        no_origem = self.grafo.vertices["casa forte"]
        no_destino = self.grafo.vertices["boa viagem"]
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, no_origem, no_destino)
        
        assert distancia < float('inf')
        HelperTest.assert_caminho_valido(self.grafo, caminho, "casa forte", "boa viagem")
    
    def test_distancia_calculada_corretamente(self):
        """Verifica que a distância calculada corresponde à soma dos pesos"""
        no_origem = self.grafo.vertices["casa forte"]
        no_destino = self.grafo.vertices["boa viagem"]
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, no_origem, no_destino)
        
        distancia_manual = HelperTest.calcular_distancia_caminho(self.grafo, caminho)
        HelperTest.assert_distancia_aproximada(distancia, distancia_manual)
    
    def test_mesmo_bairro(self):
        """Testa quando origem e destino são o mesmo bairro"""
        no = self.grafo.vertices["casa forte"]
        
        distancia, caminho = Sorting.bellman_ford(self.grafo, no, no)
        
        assert distancia == 0.0
        assert caminho == ["casa forte"]
    
    def test_consistencia_com_dijkstra(self):
        """Verifica que Bellman-Ford e Dijkstra retornam a mesma distância"""
        no_origem = self.grafo.vertices["casa forte"]
        no_destino = self.grafo.vertices["boa viagem"]
        
        dist_bf, _ = Sorting.bellman_ford(self.grafo, no_origem, no_destino)
        dist_dj, _ = Sorting.dijkstra(self.grafo, no_origem, no_destino)
        
        HelperTest.assert_distancia_aproximada(dist_bf, dist_dj)
    
    def test_todas_distancias_positivas(self):
        """Verifica que o grafo não tem ciclos negativos"""
        no_origem = self.grafo.vertices["casa forte"]
        
        _, _, tem_ciclo_negativo = Sorting.bellman_ford(self.grafo, no_origem)
        
        assert tem_ciclo_negativo == False
