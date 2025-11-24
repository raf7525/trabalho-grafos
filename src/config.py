from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / "src"
DATA_DIR = ROOT_DIR / "data"
OUT_DIR = ROOT_DIR / "out"
TEMPLATES_DIR = SRC_DIR / "templates"

BAIRROS_FILE = DATA_DIR / "bairros_unique.csv"
ARESTAS_FILE = DATA_DIR / "adjacencias_bairros.csv"
ENDERECOS_FILE = DATA_DIR / "enderecos.csv"

DATASET_2_CSV = DATA_DIR / "usa_airport_dataset.csv"

HTML_METADATA = {
    'grafo_interativo.html': ('Grafo Interativo Completo', 'Explore todos os bairros com algoritmos de busca'),
    'viz_arvore_bfs_boa_vista.html': ('Árvore BFS - Boa Vista', 'Visualização hierárquica da busca em largura'),
    'viz_subgrafo_top10.html': ('TOP 10 Bairros Conectados', 'Subgrafo dos bairros com maior grau')
}

PNG_METADATA = {
    'viz_mapa_cores_grau.png': ('Mapa de Cores por Grau', 'Ranking de bairros por número de conexões'),
    'viz_densidade_microrregiao.png': ('Densidade por Microrregião', 'Análise de densidade local'),
    'viz_distribuicao_graus.png': ('Distribuição de Graus', 'Histograma da conectividade')
}

PORT = 8000
