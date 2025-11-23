import pandas as pd
import unidecode 

from graphs.graph import Vertice, Grafo, DirectedGrafo

def carregar_dataset_parte2(caminho_csv: str = None) -> DirectedGrafo:
    grafo = DirectedGrafo()
    
    df = pd.read_csv(caminho_csv)
    
    aeroportos_origem = df[['Origin_airport', 'Origin_city']].rename(
        columns={'Origin_airport': 'aeroporto', 'Origin_city': 'cidade'}
    )
    aeroportos_destino = df[['Destination_airport', 'Destination_city']].rename(
        columns={'Destination_airport': 'aeroporto', 'Destination_city': 'cidade'}
    )
    
    aeroportos_unicos = pd.concat([aeroportos_origem, aeroportos_destino]).drop_duplicates(subset=['aeroporto'])
    
    for _, linha in aeroportos_unicos.iterrows():
        codigo = linha['aeroporto']
        vertice = Vertice(codigo)
        vertice.atributos['rotulo'] = linha['cidade']
        vertice.atributos['cidade'] = linha['cidade']
        grafo.adicionar_vertice(vertice)
    
    arestas_adicionadas = 0
    for _, linha in df.iterrows():
        origem_codigo = linha['Origin_airport']
        destino_codigo = linha['Destination_airport']
        
        vertice_origem = grafo.vertices.get(origem_codigo)
        vertice_destino = grafo.vertices.get(destino_codigo)
        
        if vertice_origem and vertice_destino:
            peso = float(linha['Distance'])
            
            atributos = {
                'passageiros': int(linha['Passengers']),
                'voos': int(linha['Flights']),
                'distancia': float(linha['Distance'])
            }
            
            # Isso agora chamará adicionar_aresta do DirectedGrafo, criando arestas direcionadas
            if grafo.adicionar_aresta(vertice_origem, vertice_destino, peso=peso, **atributos):
                arestas_adicionadas += 1
    
    return grafo