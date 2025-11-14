import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from solve import orquestrar


def main():
    parser = argparse.ArgumentParser(description="Análise de Grafos - Teoria dos Grafos")
    
    parser.add_argument('--dataset', type=str, required=True, help='Caminho para o dataset')
    parser.add_argument('--alg', type=str, choices=['BFS', 'DFS', 'DIJKSTRA', 'BELLMAN_FORD'], help='Algoritmo a executar')
    parser.add_argument('--source', type=str, help='Nó de origem')
    parser.add_argument('--target', type=str, help='Nó de destino')
    parser.add_argument('--out', type=str, default='./out/', help='Diretório de saída')
    parser.add_argument('--interactive', action='store_true', help='Modo interativo')
    parser.add_argument('--metricas', action='store_true', help='Calcular métricas do grafo')
    
    args = parser.parse_args()
    
    Path(args.out).mkdir(parents=True, exist_ok=True)
    
    if args.metricas:
        raiz = Path(__file__).parent.parent
        orquestrar(
            str(raiz / "data" / "bairros_unique.csv"),
            str(raiz / "data" / "bairros_vizinhos_tratados.csv"),
            args.out
        )
        return
    
    if args.alg:
        print(f"Executando {args.alg} de {args.source} até {args.target}")
        print(f"Dataset: {args.dataset}")
        print(f"Saída: {args.out}")
    
    if args.interactive:
        print("Modo interativo ativado")
        print(f"Dataset: {args.dataset}")
        print(f"Saída: {args.out}")

# python3 -m src.cli --dataset ./data/bairros_recife.csv --metricas --out ./out/

if __name__ == "__main__":
    main()