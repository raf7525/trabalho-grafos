import pytest
from src.graphs.graph import Grafo, Vertice
from src.graphs.io import carregar_grafo


class HelperTest:
    """Classe auxiliar para testes com métodos reutilizáveis"""
    
    @staticmethod
    def criar_grafo_com_vertices():
        """Cria um grafo com 5 vértices (A, B, C, D, E)"""
        grafo = Grafo()
        
        vertices = {
            'a': Vertice("A"),
            'b': Vertice("B"),
            'c': Vertice("C"),
            'd': Vertice("D"),
            'e': Vertice("E")
        }
        
        for vertice in vertices.values():
            grafo.adicionar_no(vertice)
        
        return grafo, vertices
        
    @staticmethod
    def carregar_grafo_real():
        """Carrega o grafo real dos bairros do Recife"""
        return carregar_grafo(
            "data/bairros_unique.csv",
            "data/bairros_vizinhos_tratados.csv"
        )
    
    @staticmethod
    def assert_caminho_valido(grafo: Grafo, caminho: list[str], origem_esperada: str, destino_esperado: str):
        """Verifica se um caminho é válido e contínuo"""
        assert len(caminho) > 0, "Caminho não pode estar vazio"
        assert caminho[0] == origem_esperada, f"Origem esperada: {origem_esperada}, obtida: {caminho[0]}"
        assert caminho[-1] == destino_esperado, f"Destino esperado: {destino_esperado}, obtido: {caminho[-1]}"
        
        # Verifica que o caminho é contínuo (cada par consecutivo é vizinho)
        for i in range(len(caminho) - 1):
            vizinhos = grafo.obter_vizinhos(caminho[i])
            assert caminho[i + 1] in vizinhos, \
                f"{caminho[i+1]} não é vizinho de {caminho[i]}"
    
    @staticmethod
    def calcular_distancia_caminho(grafo: Grafo, caminho: list[str]) -> float:
        """Calcula a distância total de um caminho somando os pesos das arestas"""
        distancia_total = 0
        for i in range(len(caminho) - 1):
            peso = grafo.obter_peso(caminho[i], caminho[i + 1])
            distancia_total += peso
        return distancia_total
    
    @staticmethod
    def assert_distancia_infinita(distancia: float):
        """Verifica se a distância é infinita"""
        assert distancia == float('inf'), f"Esperado inf, obtido {distancia}"
        
    @staticmethod
    def assert_distancia_aproximada(distancia: float, valor_esperado: float):
        """Verifica se a distância está próxima do valor esperado"""
        assert distancia == pytest.approx(valor_esperado), \
            f"Esperado {valor_esperado}, obtido {distancia}"
    
    @staticmethod
    def assert_caminho_direto(caminho: list[str], origem: str, destino: str):
        """Verifica se o caminho é direto (apenas 2 nós)"""
        assert len(caminho) == 2, f"Caminho direto deve ter 2 nós, obteve {len(caminho)}"
        assert caminho == [origem, destino], f"Caminho esperado: [{origem}, {destino}], obtido: {caminho}"
