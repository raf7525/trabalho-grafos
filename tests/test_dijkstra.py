import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.graphs.algorithms import Sorting
from tests.base import HelperTest

"""
Pra rodar essa bomba eh so ir no terminal e digitar:
pytest # Procura todos os testes na pasta atual e subpastas
ou
pytest tests/test_dijkstra.py # Roda apenas esse arquivo de teste
"""

    
class TestDijkstraGrafoSimples:
    """Testes do Dijkstra com grafos pequenos e controlados"""
    
    def setup_method(self):
        """Cria um grafo simples antes de cada teste"""
        self.grafo, self.v = HelperTest.criar_grafo_com_vertices()
        
    def test_caminho_direto(self):
        """Testa caminho direto entre dois nós"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=5.0)
        
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['b'])
        
        assert distancia == 5.0
        HelperTest.assert_caminho_direto(caminho, "A", "B")
    
    def test_caminho_indireto_mais_curto(self):
        """Testa quando o caminho indireto é mais curto que o direto"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=10.0)
        self.grafo.adicionar_aresta(self.v['a'], self.v['c'], peso=3.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['b'], peso=2.0)
        
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['b'])
        
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
        
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['e'])
        
        assert distancia == 6.0  # A->C->D->E = 2+3+1 = 6 (menor que A->B->E = 9)
        assert caminho == ["A", "C", "D", "E"]
    
    def test_no_origem_igual_destino(self):
        """Testa quando origem e destino são o mesmo nó"""
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['a'])
        
        assert distancia == 0.0
        assert caminho == ["A"]
    
    def test_caminho_inexistente(self):
        """Testa quando não há caminho entre origem e destino"""
        # A e D estão desconectados
        self.grafo.adicionar_aresta(self.v['c'], self.v['d'], peso=1.0)
        
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['d'])
        
        HelperTest.assert_distancia_infinita(distancia)
        assert caminho == []
    
    def test_peso_negativo(self):
        """Testa que pesos negativos geram erro"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=-5.0)
        
        with pytest.raises(ValueError):
            Sorting.dijkstra(self.grafo, self.v['a'], self.v['b'])
    
    def test_grafo_linear(self):
        """Testa caminho em grafo linear A-B-C-D-E"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=1.0)
        self.grafo.adicionar_aresta(self.v['b'], self.v['c'], peso=2.0)
        self.grafo.adicionar_aresta(self.v['c'], self.v['d'], peso=3.0)
        self.grafo.adicionar_aresta(self.v['d'], self.v['e'], peso=4.0)
        
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['e'])
        
        assert distancia == 10.0  # 1+2+3+4
        assert caminho == ["A", "B", "C", "D", "E"]
    
    def test_pesos_decimais(self):
        """Testa com pesos decimais"""
        self.grafo.adicionar_aresta(self.v['a'], self.v['b'], peso=1.5)
        self.grafo.adicionar_aresta(self.v['b'], self.v['c'], peso=2.3)
        
        distancia, caminho = Sorting.dijkstra(self.grafo, self.v['a'], self.v['c'])
        
        HelperTest.assert_distancia_aproximada(distancia, 3.8)
        assert caminho == ["A", "B", "C"]


class TestDijkstraGrafoReal:
    """Testes do Dijkstra com o grafo real dos bairros do Recife"""
    
    @classmethod
    def setup_class(cls):
        """Carrega o grafo uma vez para toda a classe"""
        cls.grafo = HelperTest.carregar_grafo_real()

    def test_casa_forte_para_boa_viagem(self):
        """Testa caminho de Casa Forte para Boa Viagem"""
        no_origem = self.grafo.vertices["casa forte"]
        no_destino = self.grafo.vertices["boa viagem"]
        
        distancia, caminho = Sorting.dijkstra(self.grafo, no_origem, no_destino)
        
        assert distancia < float('inf')
        HelperTest.assert_caminho_valido(self.grafo, caminho, "casa forte", "boa viagem")
    
    def test_distancia_calculada_corretamente(self):
        """Verifica que a distância calculada corresponde à soma dos pesos"""
        no_origem = self.grafo.vertices["casa forte"]
        no_destino = self.grafo.vertices["boa viagem"]
        
        distancia, caminho = Sorting.dijkstra(self.grafo, no_origem, no_destino)
        
        distancia_manual = HelperTest.calcular_distancia_caminho(self.grafo, caminho)
        HelperTest.assert_distancia_aproximada(distancia, distancia_manual)
    
    def test_mesmo_bairro(self):
        """Testa quando origem e destino são o mesmo bairro"""
        no = self.grafo.vertices["casa forte"]
        
        distancia, caminho = Sorting.dijkstra(self.grafo, no, no)
        
        assert distancia == 0.0
        assert caminho == ["casa forte"]
    
    def test_bairros_vizinhos(self):
        """Testa caminho entre bairros vizinhos diretos"""
        bairro1 = "casa forte"
        vizinhos = self.grafo.obter_vizinhos(bairro1)
        
        if len(vizinhos) > 0:
            bairro2 = vizinhos[0]
            no1 = self.grafo.vertices[bairro1]
            no2 = self.grafo.vertices[bairro2]
            
            distancia, caminho = Sorting.dijkstra(self.grafo, no1, no2)
            
            # Entre vizinhos, o caminho deve ser direto
            HelperTest.assert_caminho_direto(caminho, bairro1, bairro2)
            
            # A distância deve ser igual ao peso da aresta
            peso_aresta = self.grafo.obter_peso(bairro1, bairro2)
            assert distancia == peso_aresta
