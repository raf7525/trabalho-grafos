from flask import Flask, request, jsonify, send_from_directory, render_template
import sys
import os
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
sys.path.append(str(ROOT_PATH))

from src.graphs.io import carregar_grafo, carregar_dataset_parte2
from src.graphs.algorithms import Sorting
from src.config import OUT_DIR, TEMPLATES_DIR, BAIRROS_FILE, ARESTAS_FILE, HTML_METADATA, PNG_METADATA, PORT, DATASET_2_CSV

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))

GRAFOS = {
    'recife': None,
    'usa': None
}

print("Carregando grafos para memória...")
try:
    GRAFOS['recife'] = carregar_grafo(str(BAIRROS_FILE), str(ARESTAS_FILE))
    print(f"[OK] Grafo Recife carregado: {GRAFOS['recife'].ordem} nós.")
except Exception as e:
    print(f"[ERRO] Falha ao carregar Recife: {e}")

try:
    if os.path.exists(str(DATASET_2_CSV)):
        GRAFOS['usa'] = carregar_dataset_parte2(str(DATASET_2_CSV))
        print(f"[OK] Grafo USA carregado: {GRAFOS['usa'].ordem} nós.")
    else:
        print("[AVISO] Dataset USA não encontrado.")
except Exception as e:
    print(f"[ERRO] Falha ao carregar USA: {e}")


ALGORITMOS = {
    'dijkstra': lambda g, o, d: Sorting.dijkstra(g, g.vertices[o], g.vertices[d]),
    'bellman': lambda g, o, d: Sorting.bellman_ford(g, g.vertices[o], g.vertices[d]),
    'bfs': lambda g, o, d: Sorting.bfs_shortest_path(g, o, d),
    'dfs': lambda g, o, d: Sorting.depth_first_search(g, g.vertices[o])
}

@app.route('/')
def index():
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    
    html_files = [
        {
            'name': f.name, 
            'title': HTML_METADATA.get(f.name, (f.stem.title(), ''))[0], 
            'desc': HTML_METADATA.get(f.name, ('', 'Visualização'))[1]
        } 
        for f in sorted(OUT_DIR.glob('*.html'))
    ]
    
    pngs = sorted(OUT_DIR.glob('*.png'))
    png_data = []
    
    for f in pngs:
        meta = PNG_METADATA.get(f.name, (f.stem.replace('_', ' ').title(), 'Gráfico'))
        png_data.append({
            'name': f.name,
            'title': meta[0],
            'desc': meta[1]
        })
    
    parte1 = [item for item in png_data if not item['name'].lower().startswith('parte2')]
    parte2 = [item for item in png_data if item['name'].lower().startswith('parte2')]
    
    return render_template('index.html', html_files=html_files, parte1=parte1, parte2=parte2)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(OUT_DIR, filename)

@app.route('/api/calcular')
def calcular():
    dataset_key = request.args.get('dataset', 'recife')
    grafo_atual = GRAFOS.get(dataset_key)

    if grafo_atual is None:
        return jsonify({"erro": f"Dataset '{dataset_key}' não disponível."}), 500

    alg = request.args.get('alg', '').lower()
    origem_nome = request.args.get('origem', '')
    destino_nome = request.args.get('destino', '')
    
    if origem_nome not in grafo_atual.vertices:
        return jsonify({"erro": f"Origem '{origem_nome}' não encontrada em {dataset_key}"}), 400
    
    origem = grafo_atual.vertices.get(origem_nome)

    try:
        if alg not in ALGORITMOS:
            return jsonify({"erro": f"Algoritmo '{alg}' não suportado"}), 400

        if alg in ['bfs', 'dfs'] and not destino_nome:
            if alg == 'bfs':
                res = Sorting.breadth_first_search(grafo_atual, origem)
                niveis = {k: v for k, v in res['niveis'].items() if v != float('inf')}
                return jsonify({"tipo": "expansao", "dados_nos": niveis, "metrica": "Nível BFS", "algoritmo": "BFS"})
            elif alg == 'dfs':
                res = Sorting.depth_first_search(grafo_atual, origem)
                return jsonify({"tipo": "expansao", "dados_nos": res['descoberta'], "metrica": "Ordem Descoberta", "algoritmo": "DFS"})

        if not destino_nome:
            return jsonify({"erro": "Destino é obrigatório para cálculo de caminho."}), 400
            
        if destino_nome not in grafo_atual.vertices:
            return jsonify({"erro": f"Destino '{destino_nome}' não encontrado"}), 400

        resultado = ALGORITMOS[alg](grafo_atual, origem_nome, destino_nome)
        
        if isinstance(resultado, tuple) and len(resultado) == 2:
            custo, caminho = resultado
            if caminho and custo != float('inf'):
                return jsonify({"tipo": "caminho", "caminho": caminho, "custo": custo, "algoritmo": alg.upper()})
            return jsonify({"erro": "Caminho não encontrado"}), 404
            
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def run_server(port=None):
    port_to_use = port if port else PORT
    print(f"Iniciando Servidor Flask na porta {port_to_use}...")
    app.run(host='0.0.0.0', port=port_to_use, debug=True)

if __name__ == '__main__':
    run_server()