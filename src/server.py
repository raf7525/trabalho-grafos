import http.server
import socketserver
import json
import urllib.parse
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
ROOT_DIR = CURRENT_DIR.parent
OUT_DIR = ROOT_DIR / "out"
sys.path.insert(0, str(CURRENT_DIR))

from graphs.io import carregar_grafo
from graphs.graph import Grafo
from graphs.algorithms import Sorting

print("Carregando grafo do Recife...")
path_nos = str(ROOT_DIR / "data" / "bairros_unique.csv")
path_arestas = str(ROOT_DIR / "data" / "bairros_vizinhos_tratados.csv")
GRAFO_GLOBAL = carregar_grafo(path_nos, path_arestas)
print(f"Grafo carregado! {GRAFO_GLOBAL.ordem} nós.")

class GraphHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        if path == "/api/calcular":
            self.handle_algorithm(query)
        else:
            if path == "/" or path == "/index.html":
                path = "/grafo_interativo.html"
            
            self.directory = str(OUT_DIR)
            super().do_GET()

    def handle_algorithm(self, query):
        try:
            alg = query.get('alg', [''])[0]
            origem_nome = query.get('origem', [''])[0]
            destino_nome = query.get('destino', [''])[0]

            if not alg or not origem_nome or not destino_nome:
                self.send_error_json(400, "Parâmetros faltando.")
                return

            origem = GRAFO_GLOBAL.vertices.get(origem_nome)
            destino = GRAFO_GLOBAL.vertices.get(destino_nome)

            if not origem or not destino:
                self.send_error_json(404, "Bairro não encontrado no grafo.")
                return

            result_path = []
            custo = 0

            if alg == 'dijkstra':
                custo, result_path = Sorting.dijkstra(GRAFO_GLOBAL, origem, destino)
                if result_path == [] and custo == float('inf'):
                    result_path = None

            elif alg == 'bellman':
                try:
                    custo, result_path = Sorting.bellman_ford(GRAFO_GLOBAL, origem, destino)
                except Exception as e:
                    self.send_error_json(500, f"Erro no Bellman-Ford: {str(e)}")
                    return

            elif alg == 'bfs':
                resultado = Sorting.breadth_first_search(GRAFO_GLOBAL, origem)
                anterior = resultado['anterior']
                
                if destino_nome in resultado['distancias'] and resultado['distancias'][destino_nome] != float('inf'):
                    path = []
                    curr = destino_nome
                    while curr is not None:
                        path.append(curr)
                        curr = anterior.get(curr)
                    result_path = list(reversed(path))
                    custo = resultado['distancias'][destino_nome]
                else:
                    result_path = None

            elif alg == 'dfs':
                resultado = Sorting.depth_first_search(GRAFO_GLOBAL, origem, destino)
                
                if resultado is None:
                    self.send_error_json(404, "Caminho não encontrado via DFS.")
                    return
                else:
                    custo, result_path = resultado
            else:
                self.send_error_json(400, f"Algoritmo '{alg}' desconhecido.")
                return

            if result_path:
                response = {
                    "caminho": result_path,
                    "custo": custo if custo != float('inf') else "Infinito",
                    "algoritmo": alg.upper()
                }
                self.send_json(200, response)
            else:
                self.send_error_json(404, "Caminho não encontrado entre estes bairros.")

        except Exception as e:
            print(f"Erro interno: {e}")
            self.send_error_json(500, str(e))

    def send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_error_json(self, code, message):
        self.send_json(code, {"erro": message})

PORT = 8000
with socketserver.TCPServer(("", PORT), GraphHandler) as httpd:
    print(f"\nSERVIDOR PYTHON RODANDO EM: http://127.0.0.1:{PORT}")
    print("Use Ctrl+C para parar.")
    httpd.serve_forever()