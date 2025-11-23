import argparse
from pathlib import Path
import sys

# Adiciona o diretório atual ao sys.path para permitir importações absolutas dentro do projeto
sys.path.insert(0, str(Path(__file__).parent))

import solve

def main():
    """
    Ponto de entrada principal para a interface de linha de comando da Parte 2.
    Analisa os argumentos e os passa para o solver.
    """
    parser = argparse.ArgumentParser(
        description="Projeto de Teoria dos Grafos - Análise de Redes (Parte 2: Aeroportos EUA)",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "--dataset",
        required=True,
        type=Path,
        help="Caminho para o arquivo de dataset da Parte 2 (ex: data/usa_airport_dataset.csv)."
    )
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Caminho para o diretório de saída (ex: out/)."
    )
    parser.add_argument(
        "--alg",
        choices=["BFS", "DFS", "DIJKSTRA", "BELLMAN-FORD"],
        help="O algoritmo a ser executado."
    )
    parser.add_argument(
        "--source",
        help="O nó de origem para o algoritmo."
    )
    parser.add_argument(
        "--target",
        help="O nó de destino (para DIJKSTRA e BELLMAN-FORD)."
    )
    
    args = parser.parse_args()

    # Validação básica
    if not args.out.is_dir():
        print(f"Erro: Diretório de saída não encontrado em '{args.out}'")
        sys.exit(1) 

    if args.alg and not args.source:
        parser.error("--source é obrigatório quando --alg é especificado.")

    if args.alg in ["DIJKSTRA", "BELLMAN-FORD"] and not args.target:
        parser.error("--target é obrigatório para DIJKSTRA e BELLMAN-FORD.")

    solve.solve(args)

if __name__ == "__main__":
    main()