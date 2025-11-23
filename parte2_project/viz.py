import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from typing import Dict, Any

from graphs.graph import Grafo

plt.style.use('seaborn-v0_8-darkgrid')

# --- Visualizações da Parte 2 ---

def visualizar_distribuicao_graus(grafo: Grafo, output_dir: Path, is_part1: bool = False):
    """Gera um histograma da distribuição de graus do grafo."""
    filename = "parte2_distribuicao_graus.png"
    caminho_saida = output_dir / filename
    graus = [len(v.vizinhos) for v in grafo.vertices.values()]
    
    plt.figure(figsize=(10, 6))
    plt.hist(graus, bins=range(min(graus), max(graus) + 2), edgecolor='black', alpha=0.7)
    title = "Distribuição de Graus dos Aeroportos"
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel("Grau (Número de Conexões)", fontsize=12)
    plt.ylabel("Frequência", fontsize=12)
    plt.grid(axis='y', alpha=0.5)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=300)
    plt.close()
    print(f"[OK] Visualização (Distribuição de Graus) salva em: {caminho_saida}")

def gerar_comparacao_performance(report_data: Dict[str, Any], output_dir: Path):
    """Gera gráfico comparando performance dos algoritmos."""
    output_file = output_dir / "parte2_comparacao_performance.png"
    
    df = pd.DataFrame(report_data)
    
    avg_times = df[~df['algoritmo'].str.contains('Negativo')].groupby('algoritmo')['tempo_execucao_s'].mean() * 1000
    avg_times = avg_times.reindex(['BFS', 'DFS', 'Dijkstra', 'Bellman-Ford (Pesos Positivos)']).rename({'Bellman-Ford (Pesos Positivos)': 'Bellman-Ford'})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_times.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'], alpha=0.8, edgecolor='black')
    
    ax.set_ylabel('Tempo Médio de Execução (ms)', fontsize=12)
    ax.set_xlabel('Algoritmo', fontsize=12)
    ax.set_title('Comparação de Performance Média dos Algoritmos', fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=0)
    ax.grid(True, axis='y', linestyle='--', alpha=0.6)

    for i, v in enumerate(avg_times):
        ax.text(i, v + 0.01 * avg_times.max(), f"{v:.2f} ms", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Visualização (Comparação de Performance) salva em: {output_file}")

def gerar_visualizacoes_parte2(grafo: Grafo, report_path: Path, output_dir: Path):
    """Orquestra a geração de todas as visualizações para a Parte 2."""
    print("\n--- Gerando Visualizações (Parte 2) ---")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)

    visualizar_distribuicao_graus(grafo, output_dir, is_part1=False)
    gerar_comparacao_performance(report_data, output_dir)