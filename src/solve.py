import copy
import json
import time
import csv
from typing import Any, Dict, List
import pandas as pd
from pathlib import Path
from src.graphs.graph import Grafo, Vertice
from src.graphs.io import carregar_grafo
from src.config import ENDERECOS_FILE

def calcular_metricas_globais(grafo: Grafo) -> dict:
    metricas = {
        "ordem": grafo.ordem,
        "tamanho": grafo.tamanho,
        "densidade": round(grafo.densidade, 6)
    }
    return metricas

def calcular_metricas_microrregioes(grafo: Grafo) -> list:
    microrregioes = {}
    for nome_vertice, vertice in grafo.vertices.items():
        microrregiao = vertice.atributos.get('microrregiao', 'N/A')
        if microrregiao not in microrregioes:
            microrregioes[microrregiao] = []
        microrregioes[microrregiao].append(nome_vertice)
    
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
        vizinhos = grafo.obter_vizinhos(nome_bairro)
        grau = len(vizinhos)
        
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

def gerar_tabela_distancias_enderecos(grafo: Grafo, output_dir: Path):
    if not ENDERECOS_FILE.exists():
        print(f"[AVISO] Arquivo {ENDERECOS_FILE} não encontrado. Pulando matriz de endereços.")
        return

    print(f"\n--- Gerando Matriz de Endereços (Seção 6) ---")
    resultados = []
    try:
        with open(ENDERECOS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                b_origem = row['bairro_origem'].strip().lower()
                b_destino = row['bairro_destino'].strip().lower()
                custo, caminho_str = "N/A", "Bairro não encontrado"
                
                if b_origem in grafo.vertices and b_destino in grafo.vertices:
                    dist, path = grafo.caminho_mais_curto_dijkstra(b_origem, b_destino)
                    custo = f"{dist:.2f}" if dist != float('inf') else "INF"
                    caminho_str = " -> ".join(path)
                
                resultados.append({
                    "Endereco_X": row['endereco_origem'],
                    "Endereco_Y": row['endereco_destino'],
                    "Bairro_X": b_origem,
                    "Bairro_Y": b_destino,
                    "Custo": custo,
                    "Caminho": caminho_str
                })

        if resultados:
            df = pd.DataFrame(resultados)
            df.to_csv(output_dir / "distancias_enderecos.csv", index=False)
            print(f"[OK] Matriz salva em: {output_dir / 'distancias_enderecos.csv'}")
    except Exception as e:
        print(f"[ERRO] Falha ao processar endereços: {e}")

def orquestrar(caminho_nos: str, caminho_arestas: str, diretorio_saida: str = "out"):
    Path(diretorio_saida).mkdir(parents=True, exist_ok=True)
    
    grafo = carregar_grafo(caminho_nos, caminho_arestas)
    
    metricas_globais = calcular_metricas_globais(grafo)
    with open(f"{diretorio_saida}/recife_global.json", 'w', encoding='utf-8') as f:
        json.dump(metricas_globais, f, indent=2, ensure_ascii=False)
    
    metricas_micro = calcular_metricas_microrregioes(grafo)
    with open(f"{diretorio_saida}/microrregioes.json", 'w', encoding='utf-8') as f:
        json.dump(metricas_micro, f, indent=2, ensure_ascii=False)
    
    gerar_tabela_distancias_enderecos(grafo, Path(diretorio_saida))
    
    ego_df = calcular_metricas_ego(grafo)
    ego_df.to_csv(f"{diretorio_saida}/ego_bairro.csv", index=False, encoding='utf-8')
    
    graus_df, ranking = calcular_graus_e_rankings(grafo, f"{diretorio_saida}/ego_bairro.csv")
    graus_df.to_csv(f"{diretorio_saida}/graus.csv", index=False, encoding='utf-8')
    
    with open(f"{diretorio_saida}/rankings.json", 'w', encoding='utf-8') as f:
        json.dump(ranking, f, indent=2, ensure_ascii=False)
    
    print(f"\nArquivos gerados em '{diretorio_saida}/'")


# ------------------- PARTE 2 -------------------


def _run_benchmark(algorithm_func, *args, **kwargs) -> tuple[Any, float]:
    """Mede o tempo de execução de uma função e retorna seu resultado e o tempo decorrido."""
    start_time = time.perf_counter()
    result = algorithm_func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time

# --- Lógica da Parte 2 ---


def run_part2_full_analysis(grafo: Grafo, output_dir: Path):
    from src import viz

    print("\n" + "=" * 70 + "\nEXECUTANDO ANÁLISE COMPLETA - PARTE 2\n" + "=" * 70 + "\n")
    print(f"Grafo Carregado: {grafo.ordem} vértices e {grafo.tamanho} arestas. Densidade: {grafo.densidade:.6f}")

    bfs_dfs_sources = ["SEA", "JFK", "LAX"]
    
    # 5 pares prof ;)
    dijkstra_pairs = [
        ("SEA", "RDM"),
        ("MHK", "AMW"),
        ("GEG", "RDM"),
        ("AZA", "RDM"),
        ("JFK", "LAX"),
    ]
    benchmark_results: List[Dict[str, Any]] = []

    print("\n--- Executando Benchmarks: BFS e DFS ---")
    for source in bfs_dfs_sources:
        result_bfs, time_bfs = _run_benchmark(grafo.busca_em_largura, source)
        benchmark_results.append({
                "algoritmo": "BFS",
                "origem": source,
                "destino": None,
                "tempo_execucao_s": time_bfs,
                "vertices_alcancados": len(
                    [n for n in result_bfs["niveis"].values() if n != float("inf")]
                ),
            })

        print(f"BFS a partir de {source} concluído em {time_bfs:.6f}s.")

        result_dfs, time_dfs = _run_benchmark(grafo.busca_em_profundidade, source)
        benchmark_results.append({
                "algoritmo": "DFS",
                "origem": source,
                "destino": None,
                "tempo_execucao_s": time_dfs,
                "vertices_visitados": len(result_dfs["ordem_visita"]),
                "tem_ciclo": result_dfs["tem_ciclo"],
            })
        print(f"DFS a partir de {source} concluído em {time_dfs:.6f}s.")

    print("\n--- Executando Benchmarks: Dijkstra ---")
    for source, target in dijkstra_pairs:
        (cost, path), time_dijkstra = _run_benchmark(grafo.caminho_mais_curto_dijkstra, source, target)
        benchmark_results.append({
                "algoritmo": "Dijkstra",
                "origem": source,
                "destino": target,
                "tempo_execucao_s": time_dijkstra,
                "custo": cost,
                "tamanho_caminho": len(path),
            })
        print(f"Dijkstra de {source} para {target} concluído em {time_dijkstra:.6f}s.")

    print("\n--- Executando Benchmarks: Bellman-Ford (Pesos Positivos) ---")
    for source, target in dijkstra_pairs[:2]: # Usando os dois primeiros pares para pesos positivos
        (cost, path), time_bf = _run_benchmark(grafo.caminho_mais_curto_bellman_ford, source, target)
        benchmark_results.append({
                "algoritmo": "Bellman-Ford (Pesos Positivos)",
                "origem": source,
                "destino": target,
                "tempo_execucao_s": time_bf,
                "custo": cost,
                "tamanho_caminho": len(path),
            })
        print(f"Bellman-Ford de {source} para {target} (pesos positivos) concluído em {time_bf:.6f}s.")

    # --- NOVO: Teste de Bellman-Ford com Pesos Negativos e SEM Ciclo Negativo (Usando Grafo do Dataset) ---
    print("\n--- Testando Bellman-Ford com pesos negativos (SEM ciclo) - Usando Grafo do Dataset ---")
    grafo_neg_weights_no_cycle = copy.deepcopy(grafo)
    
    # Tenta encontrar uma aresta que não forme um ciclo negativo quando seu peso for negativo.
    # Vamos tentar JFK -> CLT (Charlotte)
    source_node_nw = "JFK"
    target_node_nw = "CLT"
    neg_weight_value = -10.0 # Peso negativo pequeno

    # Garante que os nós existem no grafo para modificação
    if (grafo_neg_weights_no_cycle.contem_vertice(Vertice(source_node_nw)) and 
        grafo_neg_weights_no_cycle.contem_vertice(Vertice(target_node_nw))):
        
        # Atributos originais da aresta, se houver
        original_edge_info = grafo_neg_weights_no_cycle.obter_informacoes_aresta(source_node_nw, target_node_nw)
        
        # Remove aresta original e adiciona uma nova com peso negativo
        grafo_neg_weights_no_cycle.remover_aresta(
            grafo_neg_weights_no_cycle.vertices[source_node_nw],
            grafo_neg_weights_no_cycle.vertices[target_node_nw]
        )
        grafo_neg_weights_no_cycle.adicionar_aresta(
            grafo_neg_weights_no_cycle.vertices[source_node_nw],
            grafo_neg_weights_no_cycle.vertices[target_node_nw],
            peso=neg_weight_value,
            **original_edge_info # Preserva outros atributos
        )
        print(f"Modificada aresta {source_node_nw} -> {target_node_nw} para peso {neg_weight_value}.")
        
        try:
            (cost_nw, path_nw), time_bf_nw = _run_benchmark(
                grafo_neg_weights_no_cycle.caminho_mais_curto_bellman_ford, 
                source_node_nw, 
                target_node_nw
            )
            benchmark_results.append({
                    "algoritmo": "Bellman-Ford (Pesos Negativos, SEM Ciclo - Dataset)",
                    "origem": source_node_nw,
                    "destino": target_node_nw,
                    "tempo_execucao_s": time_bf_nw,
                    "custo": cost_nw,
                    "tamanho_caminho": len(path_nw) if path_nw else 0,
                })
            print(f"Bellman-Ford de {source_node_nw} para {target_node_nw} (pesos negativos, sem ciclo) concluído em {time_bf_nw:.6f}s. Custo: {cost_nw}")
            print(f"Caminho: {' -> '.join(path_nw)}")
        except ValueError as e:
            benchmark_results.append({
                    "algoritmo": "Bellman-Ford (Pesos Negativos, SEM Ciclo - Dataset)",
                    "origem": source_node_nw,
                    "destino": target_node_nw,
                    "resultado": f"Erro: {str(e)} - Ciclo negativo detectado inesperadamente.",
                })
            print(f"Erro: {e} - Ciclo negativo detectado inesperadamente ao testar pesos negativos sem ciclo no dataset.")
    else:
        benchmark_results.append({
                "algoritmo": "Bellman-Ford (Pesos Negativos, SEM Ciclo - Dataset)",
                "resultado": f"Não executado - Vértices {source_node_nw} ou {target_node_nw} não encontrados no grafo.",
            })
        print(f"Não foi possível executar teste de Bellman-Ford (pesos negativos, sem ciclo): vértices {source_node_nw} ou {target_node_nw} não encontrados no grafo.")


    # --- Teste de Bellman-Ford com Pesos Negativos E COM Ciclo Negativo ---
    print("\n--- Testando Bellman-Ford com pesos negativos (COM ciclo) ---")
    grafo_neg_cycle = copy.deepcopy(grafo)
    
    cycle_nodes = ["SEA", "RDM", "GEG"]
    # Garante que todos os nós do ciclo existam no grafo
    for node_name in cycle_nodes:
        if not grafo_neg_cycle.contem_vertice(Vertice(node_name)):
            grafo_neg_cycle.adicionar_vertice(Vertice(node_name))

    # Define arestas para o ciclo negativo
    edges_to_create = [
        ("SEA", "RDM", 100),
        ("RDM", "GEG", 100),
        ("GEG", "SEA", -300)
    ]
    
    # Remove arestas existentes e adiciona novas com pesos especificados
    for u_name, v_name, weight in edges_to_create:
        u = grafo_neg_cycle.vertices[u_name]
        v = grafo_neg_cycle.vertices[v_name]
        
        # Remove aresta direcionada existente (u, v) se houver
        grafo_neg_cycle.remover_aresta(u, v)
        
        # Adiciona nova aresta direcionada
        grafo_neg_cycle.adicionar_aresta(u, v, peso=weight)

    try:
        start_time_cycle_new = time.perf_counter()
        # Chama Bellman-Ford a partir de um nó DENTRO do ciclo
        grafo_neg_cycle.caminho_mais_curto_bellman_ford("SEA", "LAX") 
    except ValueError as e:
        end_time_cycle_new = time.perf_counter()
        benchmark_results.append({
                "algoritmo": "Bellman-Ford (Pesos Negativos, COM Ciclo)",
                "origem": "SEA",
                "destino": "LAX",
                "tempo_execucao_s": end_time_cycle_new - start_time_cycle_new,
                "resultado": str(e),
            })
        print(f"Bellman-Ford detectou corretamente o ciclo negativo. ({e})")
    else:
        benchmark_results.append({
                "algoritmo": "Bellman-Ford (Pesos Negativos, COM Ciclo)",
                "origem": "SEA",
                "destino": "LAX",
                "resultado": "Ciclo negativo não detectado (INESPERADO!).",
            })
        print("Ciclo negativo esperado, mas não detectado (INESPERADO!).")


    report_path = output_dir / "parte2_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Relatório de benchmark da Parte 2 salvo em: {report_path}")

    print("\n--- Gerando Visualizações da Parte 2 ---")
    viz.gerar_visualizacoes_parte2(grafo, report_path, output_dir)
    print("\n" + "=" * 70 + "\nANÁLISE - PARTE 2 CONCLUÍDA\n" + "=" * 70 + "\n")