import json
import time
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
import copy

from graphs.io import carregar_dataset_parte2
from graphs.graph import Grafo, Vertice, DirectedGrafo

# --- Funções Auxiliares ---


def _run_benchmark(algorithm_func, *args, **kwargs) -> (Any, float):
    """Mede o tempo de execução de uma função e retorna seu resultado e o tempo decorrido."""
    start_time = time.perf_counter()
    result = algorithm_func(*args, **kwargs)
    end_time = time.perf_counter()
    return result, end_time - start_time


# --- Lógica da Parte 2 ---


def run_part2_full_analysis(grafo: Grafo, output_dir: Path):
    import viz

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


# --- Execução de Algoritmo Específico (Adaptado para Parte 2) ---


def run_specific_algorithm(args: Any):
    """Carrega o grafo correto e executa um único algoritmo especificado."""
    grafo = carregar_dataset_parte2(str(args.dataset))

    source_node = args.source
    target_node = args.target

    print(f"\nExecutando {args.alg} de '{source_node}'"+ (f" para '{target_node}'" if target_node else ""))

    if args.alg == "BFS":
        resultado = grafo.busca_em_largura(source_node)
        print("Ordem de visita:", resultado["ordem_visita"])
        print(
            "Níveis:",
            {k: v for k, v in resultado["niveis"].items() if v != float("inf")},
        )
    elif args.alg == "DFS":
        resultado = grafo.busca_em_profundidade(source_node)
        print("Ordem de visita:", resultado["ordem_visita"])
        print("Ciclo detectado:", resultado["tem_ciclo"])
    elif args.alg == "DIJKSTRA":
        distancia, caminho = grafo.caminho_mais_curto_dijkstra(source_node, target_node)
        print(f"Distância: {distancia}")
        print(f"Caminho: {' -> '.join(caminho)}")
    elif args.alg == "BELLMAN-FORD":
        try:
            distancia, caminho = grafo.caminho_mais_curto_bellman_ford(source_node, target_node)
            print(f"Distância: {distancia}")
            print(f"Caminho: {' -> '.join(caminho)}")
        except ValueError as e:
            print(f"Erro: {e}")


# --- Orquestrador Principal (Simplificado para Parte 2) ---


def solve(args: Any):
    # Para a Parte 2, sempre carrega o dataset da Parte 2 e executa a análise/algoritmo da Parte 2
    
    if args.alg:
        run_specific_algorithm(args)
    else:
        grafo = carregar_dataset_parte2(str(args.dataset))
        run_part2_full_analysis(grafo, args.out)