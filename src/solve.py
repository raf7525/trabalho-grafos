import json
import pandas as pd
from pathlib import Path
from graphs.graph import Grafo
from graphs.io import carregar_grafo


def calcular_metricas_globais(grafo: Grafo) -> dict:
    metricas = {
        "ordem": grafo.ordem,
        "tamanho": grafo.tamanho,
        "densidade": round(grafo.densidade, 6)
    }
    return metricas


def calcular_metricas_microrregioes(grafo: Grafo) -> list:
    # Agrupa bairros por microrregião
    microrregioes = {}
    for nome_vertice, vertice in grafo.vertices.items():
        microrregiao = vertice.atributos.get('microrregiao', 'N/A')
        if microrregiao not in microrregioes:
            microrregioes[microrregiao] = []
        microrregioes[microrregiao].append(nome_vertice)
    
    # Calcula métricas para cada microrregião
    metricas_por_micro = []
    for micro_id in sorted(microrregioes.keys()):
        bairros = microrregioes[micro_id]
        subgrafo = grafo.criar_subgrafo(bairros)
        
        metricas_por_micro.append({
            "microrregiao": micro_id,
            "ordem": subgrafo.ordem,
            "tamanho": subgrafo.tamanho,
            "densidade": round(subgrafo.densidade, 6)
        })
    
    return metricas_por_micro


def calcular_metricas_ego(grafo: Grafo) -> pd.DataFrame:
    dados_ego = []
    
    for nome_bairro in sorted(grafo.vertices.keys()):
        # Obtém vizinhos
        vizinhos = grafo.obter_vizinhos(nome_bairro)
        grau = len(vizinhos)
        
        # Ego-rede = bairro + vizinhos
        nos_ego = {nome_bairro} | set(vizinhos)
        subgrafo_ego = grafo.criar_subgrafo(nos_ego)
        
        dados_ego.append({
            "bairro": nome_bairro,
            "grau": grau,
            "ordem_ego": subgrafo_ego.ordem,
            "tamanho_ego": subgrafo_ego.tamanho,
            "densidade_ego": round(subgrafo_ego.densidade, 6)
        })
    
    return pd.DataFrame(dados_ego)


def calcular_graus_e_rankings(grafo: Grafo, caminho_ego_csv: str) -> dict:
    graus_data = []
    for nome_bairro in sorted(grafo.vertices.keys()):
        grau = len(grafo.obter_vizinhos(nome_bairro))
        graus_data.append({
            "bairro": nome_bairro,
            "grau": grau
        })
    
    graus_df = pd.DataFrame(graus_data)
    
    ego_df = pd.read_csv(caminho_ego_csv)
    
    idx_mais_denso = ego_df['densidade_ego'].idxmax()
    bairro_mais_denso = ego_df.loc[idx_mais_denso]
    
    idx_maior_grau = graus_df['grau'].idxmax()
    bairro_maior_grau = graus_df.loc[idx_maior_grau]
    
    ranking = {
        "bairro_mais_denso": {
            "bairro": str(bairro_mais_denso['bairro']),
            "densidade_ego": float(bairro_mais_denso['densidade_ego']),
            "grau": int(bairro_mais_denso['grau'])
        },
        "bairro_maior_grau": {
            "bairro": str(bairro_maior_grau['bairro']),
            "grau": int(bairro_maior_grau['grau'])
        }
    }
    
    return graus_df, ranking


def orquestrar(caminho_nos: str, caminho_arestas: str, diretorio_saida: str = "out"):
    Path(diretorio_saida).mkdir(parents=True, exist_ok=True)
    
    grafo = carregar_grafo(caminho_nos, caminho_arestas)
    
    metricas_globais = calcular_metricas_globais(grafo)
    with open(f"{diretorio_saida}/recife_global.json", 'w', encoding='utf-8') as f:
        json.dump(metricas_globais, f, indent=2, ensure_ascii=False)
    
    metricas_micro = calcular_metricas_microrregioes(grafo)
    with open(f"{diretorio_saida}/microrregioes.json", 'w', encoding='utf-8') as f:
        json.dump(metricas_micro, f, indent=2, ensure_ascii=False)
    
    ego_df = calcular_metricas_ego(grafo)
    ego_df.to_csv(f"{diretorio_saida}/ego_bairro.csv", index=False, encoding='utf-8')
    
    graus_df, ranking = calcular_graus_e_rankings(grafo, f"{diretorio_saida}/ego_bairro.csv")
    graus_df.to_csv(f"{diretorio_saida}/graus.csv", index=False, encoding='utf-8')
    
    with open(f"{diretorio_saida}/rankings.json", 'w', encoding='utf-8') as f:
        json.dump(ranking, f, indent=2, ensure_ascii=False)
    
    print(f"\nArquivos gerados em '{diretorio_saida}/'")
