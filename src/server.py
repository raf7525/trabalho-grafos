from flask import Flask, request, jsonify, send_from_directory, render_template
import sys
import os
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
sys.path.append(str(ROOT_PATH))

from src.graphs.io import carregar_grafo
from src.graphs.algorithms import Sorting
from src.config import OUT_DIR, TEMPLATES_DIR, BAIRROS_FILE, ARESTAS_FILE, HTML_METADATA, PNG_METADATA, PORT

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))

print("Carregando grafo...")
try:
    GRAFO_GLOBAL = carregar_grafo(str(BAIRROS_FILE), str(ARESTAS_FILE))
    print(f"Grafo carregado com sucesso! {GRAFO_GLOBAL.ordem} nós.")
except Exception as e:
    print(f"ERRO: Não foi possível carregar o grafo. {e}")
    GRAFO_GLOBAL = None

ALGORITMOS = {
    'dijkstra': lambda g, o, d: Sorting.dijkstra(g, o, d),
    'bellman': lambda g, o, d: Sorting.bellman_ford(g, o, d),
    'bfs': lambda g, o, d: Sorting.bfs_shortest_path(g, o, d),
    'dfs': lambda g, o, d: Sorting.depth_first_search(g, o)
}

@app.route('/')
def index():
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    
    html_files = [
        {'name': f.name, 'title': HTML_METADATA.get(f.name, (f.stem.title(), ''))[0], 
        'desc': HTML_METADATA.get(f.name, ('', 'Visualização'))[1]} 
        for f in sorted(OUT_DIR.glob('*.html'))
    ]
    png_files = [
        {'name': f.name, 'title': PNG_METADATA.get(f.name, (f.stem.title(), ''))[0], 
        'desc': PNG_METADATA.get(f.name, ('', 'Gráfico'))[1]} 
        for f in sorted(OUT_DIR.glob('*.png'))
    ]
    
    return render_template('index.html', html_files=html_files, png_files=png_files)

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(OUT_DIR, filename)

@app.route('/api/calcular')
def calcular():
    if GRAFO_GLOBAL is None:
        return jsonify({"erro": "Grafo não carregado."}), 500

    alg = request.args.get('alg', '').lower()
    origem_nome = request.args.get('origem', '')
    destino_nome = request.args.get('destino', '')
    
    origem = GRAFO_GLOBAL.vertices.get(origem_nome)
    destino = GRAFO_GLOBAL.vertices.get(destino_nome) if destino_nome else None

    try:
        if alg not in ALGORITMOS:
            return jsonify({"erro": f"Algoritmo '{alg}' não suportado"}), 400

        if alg in ['bfs', 'dfs'] and not destino_nome:
            if alg == 'bfs':
                res = Sorting.breadth_first_search(GRAFO_GLOBAL, origem)
                niveis = {k: v for k, v in res['niveis'].items() if v != float('inf')}
                return jsonify({"tipo": "expansao", "dados_nos": niveis, "metrica": "Nível BFS", "algoritmo": "BFS"})
            elif alg == 'dfs':
                res = Sorting.depth_first_search(GRAFO_GLOBAL, origem)
                return jsonify({"tipo": "expansao", "dados_nos": res['descoberta'], "metrica": "Ordem Descoberta", "algoritmo": "DFS"})

        if not destino:
            return jsonify({"erro": "Destino é obrigatório para cálculo de caminho."}), 400

        resultado = ALGORITMOS[alg](GRAFO_GLOBAL, origem, destino)
        
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