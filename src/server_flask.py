from flask import Flask, request, jsonify, send_from_directory, render_template
from src.graphs.io import carregar_grafo
from src.graphs.algorithms import Sorting
from src.config import OUT_DIR, TEMPLATES_DIR, BAIRROS_FILE, ARESTAS_FILE, HTML_METADATA, PNG_METADATA

app = Flask(__name__, template_folder=str(TEMPLATES_DIR))

GRAFO_GLOBAL = carregar_grafo(str(BAIRROS_FILE), str(ARESTAS_FILE))

ALGORITMOS = {
    'dijkstra': lambda g, o, d: Sorting.dijkstra(g, o, d),
    'bellman': lambda g, o, d: Sorting.bellman_ford(g, o, d),
    'bfs': lambda g, o, d: Sorting.bfs_shortest_path(g, o, d),
    'dfs': lambda g, o, d: Sorting.depth_first_search(g, o)
}

@app.route('/')
def index():
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
    alg = request.args.get('alg', '').lower()
    origem_nome = request.args.get('origem', '')
    destino_nome = request.args.get('destino', '')
    
    origem = GRAFO_GLOBAL.vertices.get(origem_nome)
    destino = GRAFO_GLOBAL.vertices.get(destino_nome)

    try:
        custo, caminho = ALGORITMOS[alg](GRAFO_GLOBAL, origem, destino)
        
        if caminho and custo != float('inf'):
            return jsonify({"caminho": caminho, "custo": custo, "algoritmo": alg.upper()})
        return jsonify({"erro": "Caminho não encontrado"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
