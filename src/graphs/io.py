import pandas as pd
import unidecode
from src.graphs.graph import GrafoDirecionado, Vertice, Grafo

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return texto
    texto = unidecode.unidecode(texto)
    return texto.lower().strip()


def processar_arquivo_bairros(caminho_entrada: str, caminho_saida: str) -> None:
    dados = pd.read_csv(caminho_entrada)
    df = dados.melt(var_name='microrregiao_cod', value_name='bairro')
    
    df.dropna(subset=['bairro'], inplace=True)
    
    df = df[df['bairro'].str.strip() != '']
    
    df['microrregiao'] = df['microrregiao_cod'].str.split('.').str[0]
    df['bairro'] = df['bairro'].apply(normalizar_texto)
    
    dados_finais = df[['bairro', 'microrregiao']].drop_duplicates(subset=['bairro']).sort_values(by='bairro')
    
    dados_finais.to_csv(caminho_saida, index=False)
    

def carregar_grafo(caminho_arquivo_nos: str, caminho_arquivo_arestas: str) -> Grafo:
    grafo = Grafo()
    try:
        dados_nos = pd.read_csv(caminho_arquivo_nos, encoding='utf-8', header=0)
    except UnicodeDecodeError:
        dados_nos = pd.read_csv(caminho_arquivo_nos, encoding='latin-1', header=0)
        
    for _, linha in dados_nos.iterrows():
        nome_bairro = linha['bairro']
        no = Vertice(nome_bairro)
        no.atributos['microrregiao'] = linha['microrregiao']
        grafo.adicionar_vertice(no)
    
    try:
        dados_arestas = pd.read_csv(caminho_arquivo_arestas, encoding='utf-8', header=0)
    except UnicodeDecodeError:
        dados_arestas = pd.read_csv(caminho_arquivo_arestas, encoding='latin-1', header=0)
    
    for _, linha in dados_arestas.iterrows():
        nome_origem = normalizar_texto(linha['Bairro'])
        nome_destino = normalizar_texto(linha['Vizinho'])
        peso = float(linha['Peso'])
        
        no_origem = grafo.vertices.get(nome_origem)
        no_destino = grafo.vertices.get(nome_destino)
        
        if no_origem and no_destino:
            atributos = {
                'logradouro': linha['Logradouro'],
                'tipo': linha['Tipo'],
                'tipo_normalizado': linha['Tipo Normalizado'],
                'id_rua': linha['Id Rua']
            }
            grafo.adicionar_aresta(no_origem, no_destino, peso=peso, **atributos)
    
    return grafo


def carregar_dataset_parte2(caminho_csv: str = None) -> GrafoDirecionado:
    grafo = GrafoDirecionado()
    
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