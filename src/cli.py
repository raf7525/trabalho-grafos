import argparse
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from solve import orquestrar
from graphs.io import carregar_grafo, normalizar_texto


def executar_bfs(grafo, origem, destino, diretorio_saida):
    """Executa BFS e gera arquivo JSON com resultados"""
    origem_normalizada = normalizar_texto(origem)
    
    if origem_normalizada not in grafo.vertices:
        print(f"Erro: Bairro de origem '{origem}' não encontrado no grafo.")
        print(f"Bairros disponíveis: {sorted(list(grafo.vertices.keys())[:10])}...")
        return
    
    print(f"Executando BFS a partir de '{origem_normalizada}'...")
    resultado = grafo.busca_em_largura(origem_normalizada)
    
    # Converte valores infinitos para string "inf" para JSON
    niveis_json = {k: ("inf" if v == float('inf') else v) for k, v in resultado['niveis'].items()}
    distancias_json = {k: ("inf" if v == float('inf') else v) for k, v in resultado['distancias'].items()}
    
    # Prepara dados para JSON
    dados_saida = {
        "algoritmo": "BFS",
        "origem": origem_normalizada,
        "niveis": niveis_json,
        "distancias": distancias_json,
        "anterior": resultado['anterior'],
        "arvore": resultado['arvore'],
        "ordem_visita": resultado['ordem_visita'],
        "estatisticas": {
            "vertices_alcancados": len(resultado['ordem_visita']),
            "vertices_totais": len(grafo.vertices),
            "maior_nivel": max([v for v in resultado['niveis'].values() if v != float('inf')], default=0)
        }
    }
    
    # Se destino foi especificado, adiciona informações do caminho
    if destino:
        destino_normalizado = normalizar_texto(destino)
        if destino_normalizado in grafo.vertices:
            if resultado['distancias'][destino_normalizado] != float('inf'):
                # Reconstrói caminho
                caminho = []
                atual = destino_normalizado
                while atual is not None:
                    caminho.append(atual)
                    atual = resultado['anterior'].get(atual)
                caminho.reverse()
                
                dados_saida["destino"] = destino_normalizado
                dados_saida["caminho"] = caminho
                dados_saida["distancia_arestas"] = resultado['distancias'][destino_normalizado]
                print(f"Caminho encontrado: {' -> '.join(caminho)}")
                print(f"Distância (arestas): {resultado['distancias'][destino_normalizado]}")
            else:
                dados_saida["destino"] = destino_normalizado
                dados_saida["caminho"] = []
                dados_saida["distancia_arestas"] = "inf"
                print(f"Destino '{destino_normalizado}' não é alcançável a partir de '{origem_normalizada}'")
    
    # Salva arquivo JSON
    arquivo_saida = Path(diretorio_saida) / f"percurso_bfs_{origem_normalizada.replace(' ', '_')}.json"
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_saida, f, ensure_ascii=False, indent=2)
    
    print(f"Resultado salvo em: {arquivo_saida}")
    print(f"Vértices alcançados: {dados_saida['estatisticas']['vertices_alcancados']}/{dados_saida['estatisticas']['vertices_totais']}")


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
        # Carrega o grafo
        raiz = Path(__file__).parent.parent
        grafo = carregar_grafo(
            str(raiz / "data" / "bairros_unique.csv"),
            str(raiz / "data" / "bairros_vizinhos_tratados.csv")
        )
        
        if args.alg == 'BFS':
            if not args.source:
                print("Erro: --source é obrigatório para BFS")
                return
            executar_bfs(grafo, args.source, args.target, args.out)
        
        elif args.alg in ['DFS', 'DIJKSTRA', 'BELLMAN_FORD']:
            print(f"Algoritmo {args.alg} ainda não integrado ao CLI")
            print(f"Origem: {args.source}, Destino: {args.target}")
        
        return
    
    if args.interactive:
        print("Modo interativo ativado")
        print(f"Dataset: {args.dataset}")
        print(f"Saída: {args.out}")

# python3 -m src.cli --dataset ./data/bairros_recife.csv --metricas --out ./out/

if __name__ == "__main__":
    main()