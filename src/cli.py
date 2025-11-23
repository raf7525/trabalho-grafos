import argparse
import sys
import json
from pathlib import Path

from src.solve import orquestrar, run_part2_full_analysis
from src.graphs.io import carregar_grafo, normalizar_texto, carregar_dataset_parte2
from src.config import ARESTAS_FILE, OUT_DIR, BAIRROS_FILE, ROOT_DIR, DATASET_2_CSV


def executar_bfs(grafo, origem, destino, diretorio_saida, normalizar=True):
    """Executa BFS e gera arquivo JSON com resultados"""
    origem_normalizada = normalizar_texto(origem) if normalizar else origem
    
    if origem_normalizada not in grafo.vertices:
        print(f"Erro: Vértice de origem '{origem}' não encontrado no grafo.")
        print(f"Vértices disponíveis: {sorted(list(grafo.vertices.keys())[:10])}...")
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
        destino_normalizado = normalizar_texto(destino) if normalizar else destino
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
    arquivo_saida = OUT_DIR / f"percurso_bfs_{origem_normalizada.replace(' ', '_')}.json"
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_saida, f, ensure_ascii=False, indent=2)
    
    print(f"Resultado salvo em: {arquivo_saida}")
    print(f"Vértices alcançados: {dados_saida['estatisticas']['vertices_alcancados']}/{dados_saida['estatisticas']['vertices_totais']}")


def executar_dfs(grafo, origem, destino, diretorio_saida, normalizar=True):
    """Executa DFS e gera arquivo JSON com resultados"""
    origem_normalizada = normalizar_texto(origem) if normalizar else origem
    
    if origem_normalizada not in grafo.vertices:
        print(f"Erro: Vértice de origem '{origem}' não encontrado no grafo.")
        print(f"Vértices disponíveis: {sorted(list(grafo.vertices.keys())[:10])}...")
        return
    
    print(f"Executando DFS a partir de '{origem_normalizada}'...")
    resultado = grafo.busca_em_profundidade(origem_normalizada)
    
    # Converte classificação de arestas para formato JSON-friendly
    classificacao_json = {f"{u}-{v}": tipo for (u, v), tipo in resultado['classificacao_arestas'].items()}
    
    # Prepara dados para JSON
    dados_saida = {
        "algoritmo": "DFS",
        "origem": origem_normalizada,
        "descoberta": resultado['descoberta'],
        "finalizacao": resultado['finalizacao'],
        "anterior": resultado['anterior'],
        "classificacao_arestas": classificacao_json,
        "ordem_visita": resultado['ordem_visita'],
        "tem_ciclo": resultado['tem_ciclo'],
        "componentes": resultado['componentes'],
        "estatisticas": {
            "vertices_alcancados": len(resultado['ordem_visita']),
            "vertices_totais": len(grafo.vertices),
            "numero_componentes": len(resultado['componentes']),
            "arestas_arvore": sum(1 for t in classificacao_json.values() if t == 'arvore'),
            "arestas_retorno": sum(1 for t in classificacao_json.values() if t == 'retorno'),
            "arestas_avanco": sum(1 for t in classificacao_json.values() if t == 'avanco'),
            "arestas_cruzamento": sum(1 for t in classificacao_json.values() if t == 'cruzamento')
        }
    }
    
    # Se destino foi especificado, adiciona informações do caminho
    if destino:
        destino_normalizado = normalizar_texto(destino) if normalizar else destino
        if destino_normalizado in grafo.vertices:
            if destino_normalizado in resultado['descoberta']:
                # Reconstrói caminho usando predecessores
                caminho = []
                atual = destino_normalizado
                while atual is not None:
                    caminho.append(atual)
                    atual = resultado['anterior'].get(atual)
                caminho.reverse()
                
                dados_saida["destino"] = destino_normalizado
                dados_saida["caminho"] = caminho
                dados_saida["distancia_arestas"] = len(caminho) - 1
                print(f"Caminho encontrado: {' -> '.join(caminho)}")
                print(f"Distância (arestas): {len(caminho) - 1}")
            else:
                dados_saida["destino"] = destino_normalizado
                dados_saida["caminho"] = []
                dados_saida["distancia_arestas"] = "inf"
                print(f"Destino '{destino_normalizado}' não é alcançável a partir de '{origem_normalizada}'")
    
    # Informações sobre ciclos
    if resultado['tem_ciclo']:
        print(f"[AVISO] Grafo contém ciclos! Arestas de retorno: {dados_saida['estatisticas']['arestas_retorno']}")
    else:
        print("[OK] Grafo é acíclico (floresta/árvore)")
    
    print(f"Componentes conexos: {dados_saida['estatisticas']['numero_componentes']}")
    
    # Salva arquivo JSON
    arquivo_saida = OUT_DIR / f"percurso_dfs_{origem_normalizada.replace(' ', '_')}.json"
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_saida, f, ensure_ascii=False, indent=2)
    
    print(f"Resultado salvo em: {arquivo_saida}")
    print(f"Vértices alcançados: {dados_saida['estatisticas']['vertices_alcancados']}/{dados_saida['estatisticas']['vertices_totais']}")


def main():
    parser = argparse.ArgumentParser(description="Análise de Grafos - Teoria dos Grafos")
    
    dataset_padrao = str(ARESTAS_FILE)
    
    parser.add_argument(
        '--dataset', 
        type=str, 
        required=False,
        default=dataset_padrao,
        help='Caminho para o dataset'
    )
    parser.add_argument('--alg', type=str, choices=['BFS', 'DFS', 'DIJKSTRA', 'BELLMAN_FORD'], help='Algoritmo a executar')
    parser.add_argument('--source', type=str, help='Nó de origem')
    parser.add_argument('--target', type=str, help='Nó de destino')
    parser.add_argument('--out', type=str, default=str(OUT_DIR), help='Diretório de saída')
    parser.add_argument('--interactive', action='store_true', help='Modo interativo')
    parser.add_argument('--metricas', action='store_true', help='Calcular métricas do grafo')
    parser.add_argument('--viz', action='store_true', help='Gerar todas as visualizações analíticas')
    parser.add_argument('--parte2', action='store_true', help='Executar análise completa da Parte 2 (Aeroportos)')
    
    args = parser.parse_args()
    
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    path_nos = str(BAIRROS_FILE)
    path_arestas = args.dataset

    if not Path(path_arestas).exists():
        print(f"Erro: Arquivo de dataset não encontrado em {path_arestas}")
        return
    
    # Parte 2: Análise completa de aeroportos
    if args.parte2:
        print("\n🛫 Executando análise completa da Parte 2 (Aeroportos)...")
        dataset_parte2 = args.dataset if args.dataset != dataset_padrao else str(DATASET_2_CSV)
        
        if not Path(dataset_parte2).exists():
            print(f"Erro: Dataset da Parte 2 não encontrado em {dataset_parte2}")
            print(f"Usando caminho padrão: {DATASET_2_CSV}")
            dataset_parte2 = str(DATASET_2_CSV)
        
        try:
            grafo_parte2 = carregar_dataset_parte2(dataset_parte2)
            run_part2_full_analysis(grafo_parte2, out_dir)
        except Exception as e:
            print(f"Erro ao executar análise da Parte 2: {e}")
            import traceback
            traceback.print_exc()
        return
    
    if args.metricas:
        print("Calculando métricas do grafo...")
        path_nos_metricas = str(BAIRROS_FILE)
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
    
    if args.viz:
        print("\nGerando visualizações analíticas...")
        from src.viz import gerar_todas_visualizacoes
        gerar_todas_visualizacoes(path_nos, path_arestas)
        return
    
    if args.alg:
        print(f"Executando {args.alg}...")

        if not args.source:
            print(f"Erro: --source é obrigatório para executar {args.alg}.")
            return

        if args.alg in ['DIJKSTRA', 'BELLMAN_FORD'] and not args.target:
            print(f"Erro: --target é obrigatório para {args.alg}.")
            return

        # Detecta se é Parte 2 baseado no dataset
        eh_parte2 = 'airport' in args.dataset.lower() or 'aeroporto' in args.dataset.lower()
        
        try:
            if eh_parte2:
                print("[PARTE 2] Carregando grafo de aeroportos...")
                grafo = carregar_dataset_parte2(args.dataset)
                usar_normalizacao = False
            else:
                print("[PARTE 1] Carregando grafo de bairros...")
                grafo = carregar_grafo(path_nos, path_arestas)
                usar_normalizacao = True
            
            print(f"Grafo carregado: {grafo.ordem} vértices, {grafo.tamanho} arestas.")
        except FileNotFoundError as e:
            print(f"Erro ao carregar arquivos do grafo: {e}")
            return
        except Exception as e:
            print(f"Erro inesperado ao carregar o grafo: {e}")
            return

        try:
            # Normaliza apenas para Parte 1 (bairros)
            if usar_normalizacao:
                origem_nome = normalizar_texto(args.source)
                destino_nome = normalizar_texto(args.target) if args.target else None
            else:
                origem_nome = args.source
                destino_nome = args.target
            
            if origem_nome not in grafo.vertices:
                raise KeyError(f"Vértice de origem '{args.source}' não encontrado no grafo.")
            
            if destino_nome and destino_nome not in grafo.vertices:
                if args.alg != 'BFS':
                    raise KeyError(f"Vértice de destino '{args.target}' não encontrado no grafo.")

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
                executar_bfs(grafo, origem_nome, destino_nome, args.out, normalizar=usar_normalizacao)
                resultado = None

            elif args.alg == 'DFS':
                executar_dfs(grafo, origem_nome, destino_nome, args.out, normalizar=usar_normalizacao)
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

    if not args.metricas and not args.alg and not args.interactive and not args.viz and not args.parte2:
        print("Nenhuma ação especificada. Use --metricas, --alg, --viz ou --parte2.")
        parser.print_help()


if __name__ == "__main__":
    main()