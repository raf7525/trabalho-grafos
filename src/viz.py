from pathlib import Path
import pandas as pd
from collections import deque
raiz = Path(__file__).parent.parent
graus = str(raiz / "out" / "graus.csv")
edges = str(raiz / "out" / "ego_bairro.csv")
            
graus = pd.read_csv(graus)
edges = pd.read_csv(edges)

# Mapa de cores por grau do bairro (mais conexões = cor mais intensa).

# Ranking de densidade de ego-subrede por microrregião (barra).

# Subgrafo dos 10 bairros com maior grau (graph view).

# Distribuição dos graus (histograma).

# Árvore BFS a partir de um polo (ex.: “Boa Vista”) para visualizar camadas