# Projeto Final - Teoria dos Grafos

Análise de grafos aplicada aos bairros de Recife e dados de aeroportos dos EUA, utilizando algoritmos de percurso e caminho mais curto.

## 📋 Descrição

Este projeto implementa e aplica algoritmos clássicos de teoria dos grafos para análise de conectividade. O projeto é dividido em duas partes principais:

### Parte 1: Grafos de Bairros de Recife
-   O grafo é construído a partir de dados de conexões viárias (ruas, avenidas) entre os bairros de Recife, com pesos representando distâncias.
-   **Dataset:** 94 bairros, 245 conexões, densidade 0.056

### Parte 2: Grafo de Aeroportos dos EUA
-   O grafo é construído a partir de dados de voos entre aeroportos dos EUA, onde vértices são aeroportos e arestas representam rotas de voo. Os pesos das arestas podem ser distâncias ou outros atributos.
-   **Dataset:** `usa_airport_dataset.csv` - Aeroportos e rotas de voo nos EUA.

## 🎯 Algoritmos Implementados

### ✅ Completos e Testados
-   **BFS (Breadth-First Search)** - Busca em largura
    -   Retorna níveis, distâncias, árvore de percurso e ordem de visitação
    -   Testes unitários passando
-   **DFS (Depth-First Search)** - Busca em profundidade
    -   Retorna tempos de descoberta/finalização, predecessores, classificação de arestas, ordem de visitação, detecção de ciclos e componentes conectados.
    -   Testes unitários passando
-   **Dijkstra** - Caminho mais curto (pesos não-negativos)
    -   Implementação com heap (priority queue)
    -   Testes unitários passando
-   **Bellman-Ford** - Caminho mais curto (suporta pesos negativos)
    -   Detecção de ciclos negativos
    -   Testes unitários passando

## 🚀 Como Executar

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

**Comandos Básicos:**
-   `--dataset <PATH>`: (Obrigatório) Caminho para o arquivo do dataset.
    -   Para a Parte 1: `data/adjacencias_bairros.csv`
    -   Para a Parte 2: `data/dataset_parte2/usa_airport_dataset.csv`
-   `--out <PATH>`: (Obrigatório) Caminho para o diretório de saída onde os resultados serão salvos.

#### 1. Executar Análise Completa (Métricas e Visualizações)

Se nenhum algoritmo (`--alg`) for especificado, o script executará uma análise completa do grafo e gerará métricas e visualizações padrão.

**Para a Parte 1 (Recife):**
```bash
venv/bin/python src/cli.py --dataset data/adjacencias_bairros.csv --out out/
```
**Outputs Gerados (Parte 1):**
-   `out/recife_global.json`: Métricas globais (ordem, tamanho, densidade).
-   `out/microrregioes.json`: Análise por microrregião.
-   `out/ego_bairro.csv`: Métricas de ego-network para cada bairro.
-   `out/graus.csv`: Graus dos vértices.
-   `out/percurso_nova_descoberta_setubal.json`: Caminho de Dijkstra obrigatório.
-   `out/grafo_dados.json`: Dados para visualização interativa.
-   Visualizações PNG e HTML (`viz_*.png`, `viz_*.html`).

**Para a Parte 2 (Aeroportos EUA):**
```bash
venv/bin/python src/cli.py --dataset data/dataset_parte2/usa_airport_dataset.csv --out out/
```
**Outputs Gerados (Parte 2):**
-   `out/parte2_report.json`: Relatório de benchmarks dos algoritmos.
-   `out/parte2_distribuicao_graus.png`: Visualização da distribuição de graus.
-   `out/parte2_comparacao_performance.png`: Visualização de comparação de performance.

#### 2. Executar Algoritmos Específicos

Use o argumento `--alg` para especificar o algoritmo a ser executado. O `--source` é obrigatório para todos os algoritmos e `--target` para `DIJKSTRA` e `BELLMAN-FORD`.

**Opções para `--alg`:** `BFS`, `DFS`, `DIJKSTRA`, `BELLMAN-FORD`

##### a. Breadth-First Search (BFS)

**Opções:** `--source <NOME_DO_VERTICE>`

**Para a Parte 1 (Recife):**
```bash
venv/bin/python src/cli.py --dataset data/adjacencias_bairros.csv --alg BFS --source "nova descoberta" --out out/
```
**Para a Parte 2 (Aeroportos EUA):**
```bash
venv/bin/python src/cli.py --dataset data/dataset_parte2/usa_airport_dataset.csv --alg BFS --source "SEA" --out out/
```
**Output:** Resultados impressos no console e, para a Parte 1, um arquivo `out/percurso_bfs_<origem>.json`.

##### b. Depth-First Search (DFS)

**Opções:** `--source <NOME_DO_VERTICE>`

**Para a Parte 1 (Recife):**
```bash
venv/bin/python src/cli.py --dataset data/adjacencias_bairros.csv --alg DFS --source "nova descoberta" --out out/
```
**Para a Parte 2 (Aeroportos EUA):**
```bash
venv/bin/python src/cli.py --dataset data/dataset_parte2/usa_airport_dataset.csv --alg DFS --source "JFK" --out out/
```
**Output:** Resultados impressos no console.

##### c. Dijkstra (Caminho Mais Curto para Pesos Não-Negativos)

**Opções:** `--source <NOME_DO_VERTICE> --target <NOME_DO_VERTICE>`

**Para a Parte 1 (Recife):**
```bash
venv/bin/python src/cli.py --dataset data/adjacencias_bairros.csv --alg DIJKSTRA --source "nova descoberta" --target "boa viagem" --out out/
```
**Para a Parte 2 (Aeroportos EUA):**
```bash
venv/bin/python src/cli.py --dataset data/dataset_parte2/usa_airport_dataset.csv --alg DIJKSTRA --source "LAX" --target "JFK" --out out/
```
**Output:** Caminho e distância total impressos no console. Para a Parte 1, também é gerado `out/percurso_<origem>_<destino>.json`.

##### d. Bellman-Ford (Caminho Mais Curto com Suporte a Pesos Negativos)

**Opções:** `--source <NOME_DO_VERTICE> --target <NOME_DO_VERTICE>`

**Para a Parte 1 (Recife):**
```bash
venv/bin/python src/cli.py --dataset data/adjacencias_bairros.csv --alg BELLMAN-FORD --source "nova descoberta" --target "boa viagem" --out out/
```
**Para a Parte 2 (Aeroportos EUA):**
```bash
venv/bin/python src/cli.py --dataset data/dataset_parte2/usa_airport_dataset.csv --alg BELLMAN-FORD --source "JFK" --target "SFO" --out out/
```
**Output:** Caminho e distância total impressos no console. Para a Parte 1, também é gerado `out/caminho_bellman_ford_<origem>_<destino>.json`.

#### 3. Gerar Visualização Interativa (Apenas Parte 1)

Use o argumento `--interactive` para gerar uma visualização interativa do grafo da Parte 1. Esta opção executa a análise completa da Parte 1.

```bash
venv/bin/python src/cli.py --dataset data/adjacencias_bairros.csv --interactive --out out/
```
**Output:** `out/grafo_interativo.html` e outras visualizações HTML/PNG.

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest tests/
```

**Status atual:** Todos os testes passando ✅

### Executar Testes Específicos

```bash
# Apenas testes do Dijkstra
pytest tests/test_dijkstra.py

# Apenas testes do Bellman-Ford
pytest tests/test_bell_manford.py

# Apenas testes do BFS
pytest tests/test_bfs.py

# Apenas testes do DFS
pytest tests/test_dfs.py

# Com verbose para ver detalhes
pytest tests/ -v
```

### Cobertura de Testes

```bash
pytest tests/ --cov=src --cov-report=html
```

## 📁 Estrutura do Projeto

```
trabalho-grafos/
├── data/
│   ├── adjacencias_bairros.csv      # Dataset de arestas de Recife (Parte 1)
│   ├── bairros_recife.csv           # Dados adicionais de bairros de Recife
│   ├── bairros_unique.csv           # Bairros únicos processados
│   └── dataset_parte2/
│       └── usa_airport_dataset.csv  # Dataset de aeroportos dos EUA (Parte 2)
├── src/
│   ├── cli.py                       # Interface de linha de comando
│   ├── solve.py                     # Lógica principal de resolução e orquestração
│   ├── viz.py                       # Funções para geração de visualizações
│   └── graphs/
│       ├── algorithms.py            # Implementação dos algoritmos de grafos (BFS, DFS, Dijkstra, Bellman-Ford)
│       ├── graph.py                 # Definição das classes Vertice e Grafo
│       └── io.py                    # Funções para carregamento e processamento de datasets
├── tests/
│   ├── base.py                      # Classe base para testes
│   ├── test_bell_manford.py         # Testes para o algoritmo Bellman-Ford
│   ├── test_bfs.py                  # Testes para o algoritmo BFS
│   ├── test_dfs.py                  # Testes para o algoritmo DFS
│   ├── test_dijkstra.py             # Testes para o algoritmo Dijkstra
├── out/                             # Diretório de saída para resultados e visualizações
├── requirements.txt                 # Dependências Python do projeto
└── README.md                        # Este arquivo
```

## 📈 Visualizações Geradas

O projeto gera diversas visualizações para ajudar na compreensão da estrutura e dos resultados dos algoritmos:

### Parte 1 (Recife):
-   **Grafo Interativo:** Um arquivo HTML interativo (`grafo_interativo.html`) que permite explorar o grafo dos bairros, visualizar conexões e atributos.
-   **Árvore de Percurso BFS/DFS:** Visualizações HTML da árvore gerada por BFS ou DFS a partir de um ponto de origem.
-   **Mapas de Cores de Graus:** Mapas de calor representando o grau de cada bairro.
-   **Distribuição de Graus:** Gráficos da distribuição dos graus dos vértices.

### Parte 2 (Aeroportos EUA):
-   **Distribuição de Graus:** Gráfico da distribuição dos graus dos aeroportos.
-   **Comparação de Performance:** Gráficos comparando o tempo de execução dos diferentes algoritmos (BFS, DFS, Dijkstra, Bellman-Ford) para os datasets.

## 🛠️ Tecnologias Utilizadas

-   **Python 3.12+**
-   **pandas**: Manipulação e análise de dados.
-   **numpy**: Suporte a operações numéricas.
-   **matplotlib**: Geração de gráficos estáticos.
-   **seaborn**: Melhoria da estética dos gráficos.
-   **plotly**: Geração de gráficos interativos.
-   **networkx**: Utilitários para grafos (usado principalmente para validação e testes).
-   **unidecode**: Normalização de texto.
-   **pytest**: Framework de testes.

## 👥 Autores

Projeto desenvolvido para a disciplina de Teoria dos Grafos.

## 📄 Licença

Este projeto é acadêmico e desenvolvido para fins educacionais.

---

**Última atualização:** 22 de novembro de 2025