import sys
from pathlib import Path
import pytest
import math

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.graphs.graph import Grafo, Vertice
from src.graphs.io import carregar_grafo
from src.config import BAIRROS_FILE, ARESTAS_FILE

class HelperTest:

    @staticmethod
    def criar_grafo_com_vertices():
        """Cria um grafo com 5 vértices (A, B, C, D, E)"""
        grafo = Grafo()
        
        nomes_upper = ['A', 'B', 'C', 'D', 'E']
        nomes_lower = ['a', 'b', 'c', 'd', 'e']
        vertices = {}
        
        for i in range(len(nomes_upper)):
            nome_maiúsculo = nomes_upper[i]
            chave_minúscula = nomes_lower[i]
            
            vertice = Vertice(nome_maiúsculo)
            vertices[chave_minúscula] = vertice

            grafo.adicionar_no(vertice)
        
        return grafo, vertices

    @staticmethod
    def carregar_grafo_real():
        """Carrega o grafo real dos bairros do Recife"""
        path_nos = str(BAIRROS_FILE)
        path_arestas = str(ARESTAS_FILE)
        
        return carregar_grafo(path_nos, path_arestas)
    
    @staticmethod
    def assert_caminho_valido(grafo, caminho, origem_esperada, destino_esperado):
        """Verifica se um caminho é válido e contínuo"""
        assert caminho is not None, "Caminho não pode ser nulo"
        assert len(caminho) > 0, "Caminho não pode estar vazio"
        assert caminho[0] == origem_esperada, f"Origem esperada: {origem_esperada}, obtida: {caminho[0]}"
        assert caminho[-1] == destino_esperado, f"Destino esperado: {destino_esperado}, obtido: {caminho[-1]}"
        
        # Verifica que o caminho é contínuo (cada par consecutivo é vizinho)
        for i in range(len(caminho) - 1):
            vizinhos = grafo.obter_vizinhos(caminho[i])
            assert caminho[i + 1] in vizinhos, \
                f"{caminho[i+1]} não é vizinho de {caminho[i]}"

    @staticmethod
    def calcular_distancia_caminho(grafo, caminho):
        """Calcula o peso total de um caminho."""
        distancia = 0.0
        if len(caminho) < 2:
            return 0.0
            
        for i in range(len(caminho) - 1):
            peso = grafo.obter_peso(caminho[i], caminho[i+1])
            if peso == math.inf:
                raise ValueError(f"Caminho inválido: Aresta {caminho[i]}-{caminho[i+1]} não existe")
            distancia += peso
        return distancia

    @staticmethod
    def assert_caminho_direto(caminho, u, v):
        """Helper para testar caminhos diretos simples."""
        assert len(caminho) == 2
        assert caminho[0] == u
        assert caminho[-1] == v

    @staticmethod
    def assert_distancia_infinita(dist):
        """Verifica se um caminho é inalcançável."""
        assert dist == math.inf, "Distância deveria ser infinita"

    @staticmethod
    def assert_distancia_aproximada(dist, val, precisao=4):
        """Compara floats com uma margem de aproximação."""
        assert round(dist, precisao) == round(val, precisao)