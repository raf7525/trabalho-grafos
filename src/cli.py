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
    
    parser.add_argument(
        '--dataset', 
        type=str, 
        required=False,
        default='./data/bairros_vizinhos_tratados.csv',
        help='Caminho para o dataset'
    )
    parser.add_argument('--alg', type=str, choices=['BFS', 'DFS', 'DIJKSTRA', 'BELLMAN_FORD'], help='Algoritmo a executar')
    parser.add_argument('--source', type=str, help='Nó de origem')
    parser.add_argument('--target', type=str, help='Nó de destino')
    parser.add_argument('--out', type=str, default='./out/', help='Diretório de saída')
    parser.add_argument('--interactive', action='store_true', help='Modo interativo')
    parser.add_argument('--metricas', action='store_true', help='Calcular métricas do grafo')
    
    args = parser.parse_args()
    
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    raiz = Path(__file__).parent.parent
    path_nos = str(raiz / "data" / "bairros_unique.csv")
    path_arestas = args.dataset

    if not Path(path_arestas).exists():
        print(f"Erro: Arquivo de dataset não encontrado em {path_arestas}")
        return
    
    if args.metricas:
        print("Calculando métricas do grafo...")
        path_nos_metricas = str(raiz / "data" / "bairros_unique.csv")
        path_arestas_metricas = path_arestas

        if not Path(path_nos_metricas).exists():
            print(f"Erro: Arquivo de nós não encontrado em {path_nos_metricas}")
            return
        
        orquestrar(
            path_nos_metricas,
            path_arestas_metricas,
            str(out_dir)
        )
        print("Métricas calculadas com sucesso.")
        return
    
    if args.alg:
        print(f"Executando {args.alg}...")

        if not args.source:
            print(f"Erro: --source é obrigatório para executar {args.alg}.")
            return

        if args.alg in ['DIJKSTRA', 'BELLMAN_FORD'] and not args.target:
            print(f"Erro: --target é obrigatório para {args.alg}.")
            return

        try:
            grafo = carregar_grafo(path_nos, path_arestas) 
            print(f"Grafo carregado: {grafo.ordem} vértices, {grafo.tamanho} arestas.")
        except FileNotFoundError as e:
            print(f"Erro ao carregar arquivos do grafo: {e}")
            return
        except Exception as e:
            print(f"Erro inesperado ao carregar o grafo: {e}")
            return

        try:
            origem_nome = normalizar_texto(args.source)
            if origem_nome not in grafo.vertices:
                raise KeyError(f"Vértice de origem '{args.source}' (normalizado para '{origem_nome}') não encontrado.")
            
            destino_nome = None
            if args.target:
                destino_nome = normalizar_texto(args.target)
                if destino_nome not in grafo.vertices:

                    if args.alg != 'BFS':
                        raise KeyError(f"Vértice de destino '{args.target}' (normalizado para '{destino_nome}') não encontrado.")

        except KeyError as e:
            print(f"Erro: {e}")
            return

        resultado = {}
        nome_arquivo = f"resultado_{args.alg.lower()}.json"
        
        try:
            if args.alg == 'DIJKSTRA':
                dist, caminho = grafo.caminho_mais_curto_dijkstra(origem_nome, destino_nome)
                resultado = {
                    "algoritmo": "Dijkstra",
                    "origem": origem_nome,
                    "destino": destino_nome,
                    "distancia_total": dist,
                    "caminho": caminho
                }
                
                if origem_nome == "nova descoberta" and (destino_nome == "boa viagem" or destino_nome == "setubal"):
                    nome_arquivo = "percurso_nova_descoberta_setubal.json"
                else:
                    nome_arquivo = f"dijkstra_{origem_nome}_para_{destino_nome}.json"

            elif args.alg == 'BELLMAN_FORD':
                dist, caminho = grafo.caminho_mais_curto_bellman_ford(origem_nome, destino_nome)
                resultado = {
                    "algoritmo": "Bellman-Ford",
                    "origem": origem_nome,
                    "destino": destino_nome,
                    "distancia_total": dist,
                    "caminho": caminho
                }
                nome_arquivo = f"bellman_{origem_nome}_para_{destino_nome}.json"

            elif args.alg == 'BFS':
                executar_bfs(grafo, origem_nome, destino_nome, args.out)
                resultado = None

            elif args.alg == 'DFS':
                print(f"Executando DFS a partir de {origem_nome}...")
                print("Lógica do DFS ainda não implementada no cli.py.")
                resultado = None
        
        except ValueError as e:
            print(f"Erro ao executar {args.alg}: {e}")
            return

        if resultado:
            caminho_saida = out_dir / nome_arquivo
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            print(f"Resultado salvo em: {caminho_saida}")
        
        return
    
    if args.interactive:
        print("Modo interativo ativado (não implementado)")
        return

    if not args.metricas and not args.alg and not args.interactive:
        print("Nenhuma ação especificada. Use --metricas ou --alg.")
        parser.print_help()


if __name__ == "__main__":
    main()