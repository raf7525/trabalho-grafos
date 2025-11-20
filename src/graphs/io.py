import pandas as pd
import unidecode
from src.graphs.graph import Vertice, Grafo

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
        grafo.adicionar_no(no)
    
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