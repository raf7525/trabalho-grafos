import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pyvis.network import Network
import json

sys.path.insert(0, str(Path(__file__).parent))

from graphs.io import carregar_grafo
from graphs.graph import Grafo


plt.style.use('seaborn-v0_8-darkgrid')
RAIZ = Path(__file__).parent.parent 
DIRETORIO_SAIDA = RAIZ / "out"
DIRETORIO_SAIDA.mkdir(parents=True, exist_ok=True)


def exportar_grafo_para_json(grafo: Grafo, caminho_saida: str = None):
    if caminho_saida is None:
        caminho_saida = str(DIRETORIO_SAIDA / "grafo_dados.json")
    
    nodes = []
    for nome_bairro, vertice in grafo.vertices.items():
        vizinhos = grafo.obter_vizinhos(nome_bairro)
        grau = len(vizinhos)
        microrregiao = vertice.atributos.get('microrregiao', 'Desconhecida')
        
        nos_ego = {nome_bairro} | set(vizinhos)
        
        arestas_ego = 0
        for n1 in nos_ego:
            for n2 in nos_ego:
                if n1 < n2: # Evita duplicidade e laços
                    if grafo.obter_peso(n1, n2) != float('inf'):
                        arestas_ego += 1
        
        qtd_nos_ego = len(nos_ego)
        densidade_ego = 0.0
        if qtd_nos_ego > 1:
            densidade_ego = (2 * arestas_ego) / (qtd_nos_ego * (qtd_nos_ego - 1))
        
        nodes.append({
            "id": nome_bairro,
            "label": nome_bairro.title(),
            "group": microrregiao,
            "value": grau, 
            "title": (
                f"<b>{nome_bairro.title()}</b><br>"
                f"Microrregião: {microrregiao}<br>"
                f"Grau: {grau}<br>"
                f"Densidade Ego: {densidade_ego:.4f}"
            )
        })
    
    edges = []
    arestas_processadas = set()
    
    for (origem, destino), attrs in grafo.arestas.items():
        chave = tuple(sorted((origem, destino)))
        if chave in arestas_processadas:
            continue
            
        edges.append({
            "from": origem,
            "to": destino,
            "label": str(attrs.get('peso', '')),
            "title": f"Peso: {attrs.get('peso', '')}<br>Logradouro: {attrs.get('logradouro', 'N/A')}",
            "color": {"color": "#848484", "opacity": 0.2}
        })
        arestas_processadas.add(chave)
        
    dados_completos = {
        "nodes": nodes,
        "edges": edges
    }
    
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=2)
        
    print(f"✓ Dados JSON atualizados (com Densidade Ego) em: {caminho_saida}")
    return caminho_saida


def visualizar_mapa_cores_grau(grafo: Grafo, caminho_saida: str = None):
    if caminho_saida is None:
        caminho_saida = str(DIRETORIO_SAIDA / "viz_mapa_cores_grau.png")
    
    dados_graus = []
    for nome_bairro, vertice in grafo.vertices.items():
        grau = len(vertice.vizinhos)
        dados_graus.append({"bairro": nome_bairro, "grau": grau})
    
    df = pd.DataFrame(dados_graus).sort_values("grau", ascending=True)
    
    norm = mcolors.Normalize(vmin=df["grau"].min(), vmax=df["grau"].max())
    cores = plt.cm.YlOrRd(norm(df["grau"]))
    
    resultado = plt.subplots(figsize=(12, max(8, len(df) * 0.15)))
    fig = resultado[0]  
    ax = resultado[1]   
    barras = ax.barh(df["bairro"], df["grau"], color=cores, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel("Grau (Número de Conexões)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Bairro", fontsize=12, fontweight='bold')
    ax.set_title("Mapa de Cores por Grau dos Bairros\n(Cor mais intensa = mais conexões)", 
                fontsize=14, fontweight='bold', pad=20)
    
    sm = plt.cm.ScalarMappable(cmap=plt.cm.YlOrRd, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.01)
    cbar.set_label('Grau', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Visualização 1 salva em: {caminho_saida}")
    return caminho_saida


def visualizar_densidade_por_microrregiao(grafo: Grafo, caminho_saida: str = None):
    if caminho_saida is None:
        caminho_saida = str(DIRETORIO_SAIDA / "viz_densidade_microrregiao.png")
    
    microrregioes_densidades = {}
    
    for nome_bairro, vertice in grafo.vertices.items():
        microrregiao = vertice.atributos.get('microrregiao', 'N/A')
        
        vizinhos = grafo.obter_vizinhos(nome_bairro)
        nos_ego = {nome_bairro} | set(vizinhos)
        subgrafo_ego = grafo.criar_subgrafo(nos_ego)
        
        if microrregiao not in microrregioes_densidades:
            microrregioes_densidades[microrregiao] = []
        microrregioes_densidades[microrregiao].append(subgrafo_ego.densidade)
    
    dados_ranking = []
    for micro, densidades in microrregioes_densidades.items():
        dados_ranking.append({
            "microrregiao": f"RPA {micro}",
            "densidade_media": sum(densidades) / len(densidades)
        })
    
    df = pd.DataFrame(dados_ranking).sort_values("densidade_media", ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    cores = plt.cm.viridis(range(len(df)))
    barras = ax.bar(df["microrregiao"], df["densidade_media"], color=cores, 
                    edgecolor='black', linewidth=1.2)
    
    ax.set_xlabel("Microrregião (RPA)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Densidade Média de Ego-Subrede", fontsize=12, fontweight='bold')
    ax.set_title("Ranking de Densidade de Ego-Subrede por Microrregião", 
                fontsize=14, fontweight='bold', pad=20)
    
    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., altura,
                f'{altura:.4f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Visualização 2 salva em: {caminho_saida}")
    return caminho_saida


def visualizar_subgrafo_top10(grafo: Grafo, caminho_saida: str = None):
    if caminho_saida is None:
        caminho_saida = str(DIRETORIO_SAIDA / "viz_subgrafo_top10.html")
    
    dados_graus = []
    for nome_bairro, vertice in grafo.vertices.items():
        grau = len(vertice.vizinhos)
        dados_graus.append({"bairro": nome_bairro, "grau": grau})
    
    df = pd.DataFrame(dados_graus).sort_values("grau", ascending=False)
    top10_bairros = df.head(10)["bairro"].tolist()
    
    nos_incluir = set(top10_bairros)
    for bairro in top10_bairros:
        vizinhos = grafo.obter_vizinhos(bairro)
        nos_incluir.update(vizinhos)
    
    subgrafo = grafo.criar_subgrafo(nos_incluir)
    
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=200)
    
    for nome_no, vertice in subgrafo.vertices.items():
        grau = len(vertice.vizinhos)
        eh_top10 = nome_no in top10_bairros
        
        tamanho = 30 + (grau * 3) if eh_top10 else 15 + (grau * 2)
        cor = "#ff6b6b" if eh_top10 else "#4ecdc4"
        
        net.add_node(nome_no, 
                    label=nome_no.title(),
                    size=tamanho,
                    color=cor,
                    title=f"Bairro: {nome_no.title()}<br>Grau: {grau}<br>{'★ TOP 10' if eh_top10 else ''}",
                    font={'size': 14 if eh_top10 else 10})
    
    arestas_adicionadas = set()
    for origem, destino in subgrafo.arestas.keys():
        if (origem, destino) not in arestas_adicionadas and (destino, origem) not in arestas_adicionadas:
            peso = subgrafo.obter_peso(origem, destino)
            net.add_edge(origem, destino, 
                        value=peso,
                        title=f"Peso: {peso}",
                        color="#ffffff" if origem in top10_bairros and destino in top10_bairros else "#888888")
            arestas_adicionadas.add((origem, destino))
    
    net.save_graph(caminho_saida)
    
    print(f"✓ Visualização 3 salva em: {caminho_saida}")
    print(f"  Top 10 bairros: {', '.join([b.title() for b in top10_bairros])}")
    return caminho_saida


def visualizar_distribuicao_graus(grafo: Grafo, caminho_saida: str = None):
    if caminho_saida is None:
        caminho_saida = str(DIRETORIO_SAIDA / "viz_distribuicao_graus.png")
    
    graus = [len(vertice.vizinhos) for vertice in grafo.vertices.values()]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    n, bins, patches = ax.hist(graus, bins=range(min(graus), max(graus) + 2), 
                                edgecolor='black', linewidth=1.2, alpha=0.7)
    
    norm = mcolors.Normalize(vmin=min(graus), vmax=max(graus))
    for bin_val, patch in zip(bins, patches):
        patch.set_facecolor(plt.cm.Blues(norm(bin_val)))
    
    ax.set_xlabel("Grau (Número de Conexões)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Frequência (Número de Bairros)", fontsize=12, fontweight='bold')
    ax.set_title("Distribuição dos Graus dos Bairros", fontsize=14, fontweight='bold', pad=20)
    
    media = sum(graus) / len(graus)
    mediana = sorted(graus)[len(graus)//2]
    
    texto_stats = f"Estatísticas:\nMédia: {media:.2f}\nMediana: {mediana}\nMín: {min(graus)}\nMáx: {max(graus)}"
    ax.text(0.95, 0.95, texto_stats,
            transform=ax.transAxes,
            fontsize=11,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Visualização 4 salva em: {caminho_saida}")
    return caminho_saida


def visualizar_arvore_bfs(grafo: Grafo, origem: str = "boa vista", caminho_saida: str = None):
    if caminho_saida is None:
        caminho_saida = str(DIRETORIO_SAIDA / f"viz_arvore_bfs_{origem.replace(' ', '_')}.html")
    
    resultado_bfs = grafo.busca_em_largura(origem)
    niveis = resultado_bfs['niveis']
    arvore = resultado_bfs['arvore']
    
    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    net.barnes_hut(gravity=-5000, central_gravity=0.5, spring_length=150)
    
    max_nivel = max([v for v in niveis.values() if v != float('inf')])
    cores_niveis = plt.cm.rainbow([i/max_nivel for i in range(max_nivel + 1)])
    
    for nome_no, nivel in niveis.items():
        if nivel == float('inf'):
            continue
        
        eh_origem = nome_no == origem
        tamanho = 40 if eh_origem else 20 + (5 * (max_nivel - nivel))
        
        cor_rgb = cores_niveis[nivel]
        cor_hex = mcolors.rgb2hex(cor_rgb[:3])
        
        net.add_node(nome_no,
                    label=f"{nome_no.title()}\nNível {nivel}",
                    size=tamanho,
                    color=cor_hex,
                    title=f"Bairro: {nome_no.title()}<br>Nível BFS: {nivel}<br>{'★ ORIGEM' if eh_origem else ''}",
                    level=nivel,
                    font={'size': 16 if eh_origem else 12})
    
    for pai, filhos in arvore.items():
        if niveis[pai] == float('inf'):
            continue
        for filho in filhos:
            net.add_edge(pai, filho, 
                        color="#ffffff",
                        arrows="to",
                        title=f"{pai.title()} → {filho.title()}")
    
    net.set_options("""
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",
          "sortMethod": "directed",
          "levelSeparation": 150,
          "nodeSpacing": 200
        }
      },
      "physics": {
        "hierarchicalRepulsion": {
          "centralGravity": 0.0,
          "springLength": 200,
          "springConstant": 0.01,
          "nodeDistance": 150
        }
      }
    }
    """)
    
    net.save_graph(caminho_saida)
    
    print(f"✓ Visualização 5 salva em: {caminho_saida}")
    print(f"  Origem: {origem.title()}")
    print(f"  Níveis encontrados: {max_nivel + 1}")
    print(f"  Vértices alcançados: {len([v for v in niveis.values() if v != float('inf')])}/{len(niveis)}")
    return caminho_saida


def gerar_todas_visualizacoes(caminho_nos: str = None, caminho_arestas: str = None):
    print("\n" + "="*70)
    print("GERANDO VISUALIZAÇÕES ANALÍTICAS")
    print("="*70 + "\n")
    
    if caminho_nos is None:
        caminho_nos = str(RAIZ / "data" / "bairros_unique.csv")
    if caminho_arestas is None:
        caminho_arestas = str(RAIZ / "data" / "bairros_vizinhos_tratados.csv")
    
    print("Carregando grafo...")
    try:
        grafo = carregar_grafo(caminho_nos, caminho_arestas)
        print(f"Grafo carregado: {grafo.ordem} vértices, {grafo.tamanho} arestas\n")
    except Exception as e:
        print(f"Erro fatal ao carregar grafo: {e}")
        return
    
    print("Gerando visualizações...\n")
    
    try:
        exportar_grafo_para_json(grafo) # FUNCAO NOVA
        visualizar_mapa_cores_grau(grafo)
        visualizar_densidade_por_microrregiao(grafo)
        visualizar_subgrafo_top10(grafo)
        visualizar_distribuicao_graus(grafo)
        visualizar_arvore_bfs(grafo, origem="boa vista")
    except Exception as e:
        print(f"Erro ao gerar visualizações: {e}")
    
    print("\n" + "="*70)
    print("TODAS AS VISUALIZAÇÕES FORAM GERADAS COM SUCESSO!")
    print(f"Arquivos salvos em: {DIRETORIO_SAIDA}")
    print("="*70 + "\n")


if __name__ == "__main__":
    gerar_todas_visualizacoes()