import json
import pandas as pd
from graphs.graph import Graph

def calculate_density(order: int, size: int) -> float:
    
    if order < 2:
        return 0.0
    return (2 * size) / (order * (order - 1))

def calculate_all_metrics(graph: Graph, output_dir: str):
    
    print("Calculando métricas globais...")
    global_order = graph.get_order()
    global_size = graph.get_size()
    global_density = calculate_density(global_order, global_size)
    
    global_metrics = {
        "ordem": global_order,
        "tamanho": global_size,
        "densidade": round(global_density, 6)
    }
    with open(f"{output_dir}/recife_global.json", 'w', encoding='utf-8') as f:
        json.dump(global_metrics, f, indent=4, ensure_ascii=False)
    print(f"Salvo em {output_dir}/recife_global.json")

   
    print("\nCalculando métricas por microrregião...")
    microrregioes_metrics = []
    
    
    micros = {}
    for bairro, attrs in graph.nodes_attr.items():
        microrregiao = attrs.get('microrregiao', 'N/A')
        if microrregiao not in micros:
            micros[microrregiao] = []
        micros[microrregiao].append(bairro)

    for mr_id, bairros in sorted(micros.items()):
        subgraph = graph.create_subgraph(bairros)
        order = subgraph.get_order()
        size = subgraph.get_size()
        density = calculate_density(order, size)
        
        microrregioes_metrics.append({
            "microrregiao": mr_id,
            "ordem": order,
            "tamanho": size,
            "densidade": round(density, 6)
        })

    with open(f"{output_dir}/microrregioes.json", 'w', encoding='utf-8') as f:
        json.dump(microrregioes_metrics, f, indent=4, ensure_ascii=False)
    print(f"Salvo em {output_dir}/microrregioes.json")
    
   
    print("\nCalculando métricas de ego-rede...")
    ego_metrics = []
    for bairro in sorted(graph.adj.keys()):
        vizinhos = graph.get_neighbors(bairro)
       
        ego_nodes = {bairro} | set(vizinhos)
        
        ego_subgraph = graph.create_subgraph(ego_nodes)
        
        ego_metrics.append({
            "bairro": bairro,
            "grau": len(vizinhos),
            "ordem_ego": ego_subgraph.get_order(),
            "tamanho_ego": ego_subgraph.get_size(),
            "densidade_ego": round(calculate_density(ego_subgraph.get_order(), ego_subgraph.get_size()), 6)
        })

    ego_df = pd.DataFrame(ego_metrics)
    ego_df.to_csv(f"{output_dir}/ego_bairro.csv", index=False, encoding='utf-8')
    print(f"Salvo em {output_dir}/ego_bairro.csv")
