## Como Executar

### Pré-requisitos

-   Python 3.8+
-   pip

### Instalação

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd trabalho-grafos

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

### Uso da Interface de Linha de Comando (CLI)

O script `src/cli.py` é a interface principal para executar análises e algoritmos.

**Argumentos Disponíveis:**
-   `--dataset <PATH>`: (Obrigatório) Caminho para o arquivo do dataset
-   `--out <PATH>`: (Obrigatório) Diretório de saída para resultados
-   `--alg <ALGORITMO>`: Algoritmo específico a executar (BFS, DFS, DIJKSTRA, BELLMAN-FORD)
-   `--source <VERTICE>`: Vértice de origem (obrigatório para algoritmos)
-   `--target <VERTICE>`: Vértice de destino (obrigatório para Dijkstra e Bellman-Ford)
-   `--interactive`: Gera visualização interativa (apenas Parte 1)
-   `--metricas`: Gera todas as métricas do grafo
-   `--viz`: Gera todas as visualizações
-   `--parte2`: Executa análise completa da Parte 2 (benchmarks + visualizações)

---
## 🧪 Testes

### Executar Todos os Testes

```bash
pytest tests/ -v
```

**Status atual:** ✅ **46/46 testes passando**

**Breakdown:**
- `test_bfs.py` - 9 testes ✅
- `test_dfs.py` - 11 testes ✅
- `test_dijkstra.py` - 12 testes ✅
- `test_bellman_ford.py` - 14 testes ✅

### Executar Testes Específicos

```bash
# Apenas testes do BFS
pytest tests/test_bfs.py -v

# Apenas testes do DFS
pytest tests/test_dfs.py -v

# Apenas testes do Dijkstra
pytest tests/test_dijkstra.py -v

# Apenas testes do Bellman-Ford
pytest tests/test_bell_manford.py -v
```

### Cobertura de Testes

```bash
pytest tests/ --cov=src --cov-report=html
# Abre htmlcov/index.html no navegador
```

---

## Explicação dos gráficos

viz_densidade_microregiao:
o gráfico em questão, mede a densidade diante da zona administrativa do recife ou seja:

RPA 1 - Centro (Recife, Santo Antônio)
RPA 2 - Norte (Casa Amarela, Dois Unidos, etc.)
RPA 3 - Noroeste (Casa Forte, Monteiro, etc.)
RPA 4 - Oeste (Cordeiro, Torrões, etc.)
RPA 5 - Sudoeste (Afogados, Bongi, etc.)
RPA 6 - Sul (Boa Viagem, Pina, etc.)

Isso ajuda a fazer planejamento urbano, Análise de Acessibilidae e impacto socieconômico

viz_distribuicao_graus:
o gráfico mostra um histograma da distribuição de graus dos bairros do Recife, ou seja:

- Eixo X: Número de conexões (grau) que cada bairro possui
- Eixo Y: Frequência (quantos bairros têm esse número de conexões)
- Inclui estatísticas: média, mediana, mínimo e máximo

Isso revela se o grafo tem poucos "hubs" (bairros muito conectados) e muitos bairros com poucas conexões, ou se a conectividade é mais distribuída uniformemente.

viz_mapa_cores_grau:
o gráfico apresenta um gráfico de barras horizontais onde cada bairro é colorido de acordo com seu grau:

- Cor mais intensa (vermelho/laranja): bairros com mais conexões
- Cor mais clara (amarelo): bairros com menos conexões
- Bairros ordenados do menor para o maior grau
- Barra de cores lateral mostra a escala

Facilita identificar visualmente quais bairros são mais centrais na rede de conectividade urbana.

viz_subgrafo_top10:
o gráfico interativo mostra os 10 bairros com maior grau de conectividade e seus vizinhos:

- Nós vermelhos: Top 10 bairros mais conectados
- Nós azuis: Vizinhos desses bairros principais
- Tamanho dos nós: proporcional ao grau de conectividade
- Arestas brancas: conexões entre bairros do Top 10
- Permite zoom, pan e hover para ver detalhes

Útil para entender quais são os "hubs" de conectividade e como eles se relacionam.

viz_arvore_bfs:
o gráfico mostra a árvore de busca em largura (BFS) a partir de um bairro origem:

- Layout hierárquico com níveis bem definidos
- Cores diferentes para cada nível da busca
- Nível 0: bairro de origem (maior e destacado)
- Níveis crescentes: bairros alcançados em cada etapa da busca
- Setas direcionadas mostrando o caminho da busca

Demonstra como a conectividade se espalha a partir de um ponto e quais bairros são mais "próximos" em termos de saltos na rede.

## parte 2

Na parte dois usamos um dataset de voos pelos estados unidos, a primeira parte foi tratar os dados para facilitar o uso deles, por isso separamos em 2 csv e tiramos todos os dados não úteis, após isso começamos criamos os grafos com os nós,arestas,pesos e por fim testamos os algorítmos nos grafos criados, descobrimos por exemplo que o dfs por algum motivo está com o tempo muito acima enquanto o dfs sendo o mais rápido de todos, o djkstra também é muito mais rápido que o bell-man ford.

Um fato a se destacar é que não usamos pesos negativos visto que nossa medida de peso seria com base na distância, portanto não tem como se ter distâncias negativas.