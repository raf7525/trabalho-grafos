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

## 📦 PARTE 1: Bairros de Recife

### 1.1 Análise Completa da Parte 1 (Recomendado)

Gera **TODOS** os arquivos obrigatórios da Parte 1:

```bash
python -m src.cli --dataset data/adjacencias_bairros.csv --out out/
```

**Arquivos Gerados:**
-   ✅ `out/recife_global.json` - Métricas globais (ordem, tamanho, densidade)
-   ✅ `out/microrregioes.json` - Análise por microrregião
-   ✅ `out/ego_bairro.csv` - Métricas de ego-network por bairro
-   ✅ `out/graus.csv` - Graus dos vértices
-   ✅ `out/percurso_nova_descoberta_setubal.json` - **Caminho obrigatório** (Dijkstra)
-   ✅ `out/distancias_enderecos.csv` - Matriz de distâncias entre endereços
-   ✅ `out/grafo_dados.json` - Dados para visualização interativa
-   ✅ `out/grafo_interativo.html` - Grafo interativo completo
-   ✅ `out/viz_mapa_cores_grau.png` - Mapa de cores por grau
-   ✅ `out/viz_densidade_microrregiao.png` - Ranking de densidade
-   ✅ `out/viz_subgrafo_top10.html` - Top 10 bairros (interativo)
-   ✅ `out/viz_distribuicao_graus.png` - Histograma de distribuição
-   ✅ `out/viz_arvore_bfs_boa_vista.html` - Árvore BFS interativa

### 1.2 Gerar Apenas Visualização Interativa

```bash
python -m src.cli --dataset data/adjacencias_bairros.csv --interactive --out out/
```

**Arquivo Gerado:** `out/grafo_interativo.html` (abrir no navegador)

### 1.3 Executar Algoritmos Específicos (Parte 1)

#### BFS (Busca em Largura)
```bash
python -m src.cli --dataset data/adjacencias_bairros.csv --alg BFS --source "boa viagem" --out out/
```
**Output:** Console + `out/percurso_bfs_boa_viagem.json`

#### DFS (Busca em Profundidade)
```bash
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DFS --source "nova descoberta" --out out/
```
**Output:** Console (ordem de visitação, ciclos detectados)

#### Dijkstra (Caminho Mais Curto)
```bash
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DIJKSTRA --source "nova descoberta" --target "boa viagem" --out out/
```
**Output:** Console + `out/percurso_nova_descoberta_boa_viagem.json`

#### Bellman-Ford (Caminho com Pesos Negativos)
```bash
python -m src.cli --dataset data/adjacencias_bairros.csv --alg BELLMAN-FORD --source "nova descoberta" --target "setubal" --out out/
```
**Output:** Console + `out/bellman_nova_descoberta_para_setubal.json`

---

## 🛫 PARTE 2: Aeroportos dos EUA

### 2.1 Análise Completa da Parte 2 (Recomendado)

Executa **TODOS** os benchmarks e gera visualizações da Parte 2:

```bash
python -m src.cli --parte2 --dataset data/usa_airport_dataset.csv --out out/
```

**O que é executado:**
1. ✅ **BFS** a partir de 3 fontes (SEA, JFK, LAX)
2. ✅ **DFS** a partir de 3 fontes (SEA, JFK, LAX) + detecção de ciclos
3. ✅ **Dijkstra** com 5 pares origem-destino
4. ✅ **Bellman-Ford** com pesos positivos (2 casos)
5. ✅ **Bellman-Ford** com pesos negativos SEM ciclo (1 caso)
6. ✅ **Bellman-Ford** com ciclo negativo detectado (1 caso)

**Arquivos Gerados:**
-   ✅ `out/parte2_report.json` - **Relatório completo com tempos de execução**
-   ✅ `out/parte2_distribuicao_graus.png` - Distribuição de graus dos aeroportos
-   ✅ `out/parte2_comparacao_performance.png` - Comparação de performance dos algoritmos

**Tempo estimado:** ~60 segundos

### 2.2 Visualizar os Resultados da Parte 2

Após executar a análise completa, você pode:

1. **Ver o relatório JSON:**
```bash
cat out/parte2_report.json
```

2. **Abrir as visualizações:**
```bash
# Linux/Mac
xdg-open out/parte2_distribuicao_graus.png
xdg-open out/parte2_comparacao_performance.png

# Ou navegue até a pasta out/ e abra os arquivos PNG
```

### 2.3 Executar Algoritmos Específicos (Parte 2)

#### BFS em Aeroportos
```bash
python -m src.cli --dataset data/usa_airport_dataset.csv --alg BFS --source "SEA" --out out/
```
**Output:** Console + `out/percurso_bfs_SEA.json` (222/526 vértices alcançados)

#### DFS em Aeroportos
```bash
python -m src.cli --dataset data/usa_airport_dataset.csv --alg DFS --source "JFK" --out out/
```
**Output:** Console (526 vértices visitados, ciclo detectado)

#### Dijkstra em Aeroportos
```bash
python -m src.cli --dataset data/usa_airport_dataset.csv --alg DIJKSTRA --source "SEA" --target "RDM" --out out/
```
**Output:** Console + `out/dijkstra_SEA_para_RDM.json` (distância: 228.0)

#### Bellman-Ford em Aeroportos
```bash
python -m src.cli --dataset data/usa_airport_dataset.csv --alg BELLMAN-FORD --source "LAX" --target "SFO" --out out/
```
**Output:** Console + arquivo JSON com caminho

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

## 📊 Resumo dos Arquivos Gerados

### Parte 1 (Bairros de Recife)
| Arquivo | Descrição | Como Gerar |
|---------|-----------|------------|
| `recife_global.json` | Métricas globais (ordem, tamanho, densidade) | Análise completa |
| `microrregioes.json` | Análise por microrregião | Análise completa |
| `ego_bairro.csv` | Ego-network de cada bairro | Análise completa |
| `graus.csv` | Graus de todos os vértices | Análise completa |
| `distancias_enderecos.csv` | Matriz de distâncias entre endereços | Análise completa |
| `percurso_nova_descoberta_setubal.json` | **Caminho obrigatório** | Análise completa |
| `grafo_interativo.html` | Grafo interativo (abrir no navegador) | `--interactive` |
| `viz_mapa_cores_grau.png` | Mapa de calor por grau | Análise completa |
| `viz_densidade_microrregiao.png` | Ranking de densidade | Análise completa |
| `viz_subgrafo_top10.html` | Top 10 bairros | Análise completa |
| `viz_distribuicao_graus.png` | Histograma de graus | Análise completa |
| `viz_arvore_bfs_boa_vista.html` | Árvore BFS interativa | Análise completa |

### Parte 2 (Aeroportos dos EUA)
| Arquivo | Descrição | Como Gerar |
|---------|-----------|------------|
| `parte2_report.json` | **Relatório completo com benchmarks** | `--parte2` |
| `parte2_distribuicao_graus.png` | Distribuição de graus dos aeroportos | `--parte2` |
| `parte2_comparacao_performance.png` | Comparação de performance dos algoritmos | `--parte2` |

---

## 💡 Exemplos Rápidos

### Gerar TODOS os arquivos obrigatórios do projeto

```bash
# Parte 1 (Recife) - Gera todos os 13 arquivos obrigatórios
python -m src.cli --dataset data/adjacencias_bairros.csv --out out/

# Parte 2 (Aeroportos) - Gera relatório + 2 visualizações
python -m src.cli --parte2 --dataset data/usa_airport_dataset.csv --out out/
```

### Testar um caminho específico

```bash
# Recife: Nova Descoberta → Boa Viagem (Setúbal)
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DIJKSTRA \
  --source "nova descoberta" --target "boa viagem" --out out/

# Aeroportos: Seattle → Redmond
python -m src.cli --dataset data/usa_airport_dataset.csv --alg DIJKSTRA \
  --source "SEA" --target "RDM" --out out/
```

### Visualizar o grafo interativamente

```bash
# Gera grafo_interativo.html
python -m src.cli --dataset data/adjacencias_bairros.csv --interactive --out out/

# Abrir no navegador (Linux/Mac)
xdg-open out/grafo_interativo.html

# Ou simplesmente navegue até out/ e abra o arquivo HTML
```

## 📁 Estrutura do Projeto

```
trabalho-grafos/
├── README.md                        # Este arquivo
├── requirements.txt                 # Dependências Python
├── CHECKLIST.md                     # Checklist detalhado do projeto
├── STATUS_PROJETO.md                # Status e pontuação estimada
├── data/                            # Datasets de entrada
│   ├── bairros_recife.csv           # Dados dos bairros (fornecido)
│   ├── bairros_unique.csv           # Bairros únicos processados
│   ├── adjacencias_bairros.csv      # Arestas entre bairros (construído)
│   ├── enderecos.csv                # 5 pares de endereços (construído)
│   └── usa_airport_dataset.csv      # Dataset Parte 2 (aeroportos EUA)
├── out/                             # Saídas geradas (criar pasta se não existir)
│   ├── recife_global.json           # Métricas globais
│   ├── microrregioes.json           # Análise por microrregião
│   ├── ego_bairro.csv               # Ego-network por bairro
│   ├── graus.csv                    # Graus dos vértices
│   ├── distancias_enderecos.csv     # Matriz de distâncias
│   ├── percurso_nova_descoberta_setubal.json  # Caminho obrigatório
│   ├── grafo_interativo.html        # Grafo interativo
│   ├── viz_*.png                    # Visualizações estáticas (5 arquivos)
│   ├── viz_*.html                   # Visualizações interativas (2 arquivos)
│   ├── parte2_report.json           # Relatório benchmarks Parte 2
│   ├── parte2_distribuicao_graus.png      # Visualização Parte 2
│   └── parte2_comparacao_performance.png  # Visualização Parte 2
├── src/                             # Código fonte
│   ├── __init__.py
│   ├── cli.py                       # Interface de linha de comando
│   ├── solve.py                     # Orquestração e métricas
│   ├── viz.py                       # Geração de visualizações
│   ├── config.py                    # Configurações e constantes
│   └── graphs/                      # Pacote de grafos
│       ├── __init__.py
│       ├── io.py                    # Carregamento de datasets
│       ├── graph.py                 # Classes Vertice, Grafo, DirectedGrafo
│       └── algorithms.py            # BFS, DFS, Dijkstra, Bellman-Ford
└── tests/                           # Testes unitários (pytest)
    ├── base.py                      # Classe base para testes
    ├── test_bfs.py                  # 9 testes BFS
    ├── test_dfs.py                  # 11 testes DFS
    ├── test_dijkstra.py             # 12 testes Dijkstra
    └── test_bell_manford.py         # 14 testes Bellman-Ford
```

## 📈 Visualizações Geradas

### Parte 1 (Recife) - 7 Visualizações

1. **`grafo_interativo.html`** (Interativo)
   - Grafo completo dos bairros de Recife
   - Tooltip com informações (grau, microrregião, densidade_ego)
   - Busca por bairro
   - Destaque do caminho obrigatório (Nova Descoberta → Boa Viagem)
   - **Como abrir:** Navegue até `out/` e abra no navegador

2. **`viz_mapa_cores_grau.png`** (Estático)
   - Mapa de calor: cor mais intensa = mais conexões
   - Identifica bairros com maior conectividade

3. **`viz_densidade_microrregiao.png`** (Estático)
   - Gráfico de barras comparando densidade de ego-subrede
   - Agrupado por microrregião

4. **`viz_subgrafo_top10.html`** (Interativo)
   - Subgrafo dos 10 bairros com maior grau
   - Visualização de rede focada nos "hubs"

5. **`viz_distribuicao_graus.png`** (Estático)
   - Histograma da distribuição de graus
   - Mostra padrão de conectividade

6. **`viz_arvore_bfs_boa_vista.html`** (Interativo)
   - Árvore BFS a partir de "Boa Vista"
   - Visualiza camadas/níveis de percurso

7. **Arquivos de Percurso** (JSON)
   - `percurso_nova_descoberta_setubal.json` - Caminho obrigatório
   - `percurso_bfs_*.json` - Resultados de BFS
   - Outros caminhos calculados

### Parte 2 (Aeroportos EUA) - 2 Visualizações

1. **`parte2_distribuicao_graus.png`** (Estático)
   - Histograma da distribuição de graus dos aeroportos
   - Mostra hubs (aeroportos com muitas conexões) vs aeroportos regionais
   - **Gerado por:** `--parte2`

2. **`parte2_comparacao_performance.png`** (Estático)
   - Gráficos comparativos de tempo de execução
   - Compara BFS, DFS, Dijkstra e Bellman-Ford
   - Mostra qual algoritmo é mais eficiente em cada caso
   - **Gerado por:** `--parte2`

### Como Visualizar

```bash
# Linux/Mac - Abrir visualizações PNG
xdg-open out/parte2_distribuicao_graus.png
xdg-open out/parte2_comparacao_performance.png
xdg-open out/viz_mapa_cores_grau.png

# Windows
start out/parte2_distribuicao_graus.png

# Ou simplesmente navegue até a pasta out/ no explorador de arquivos
```

### Visualizações Interativas (HTML)

Abra no navegador:
- `out/grafo_interativo.html`
- `out/viz_subgrafo_top10.html`
- `out/viz_arvore_bfs_boa_vista.html`

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

**Última atualização:** 23 de novembro de 2025

## 🎯 Status do Projeto

✅ **Parte 1:** 100% completa (13 arquivos gerados)  
✅ **Parte 2:** 100% completa (3 arquivos gerados)  
✅ **Testes:** 46/46 passando  
✅ **CLI:** Totalmente funcional  
❌ **Relatório PDF:** Pendente

**Pontuação Estimada:** 10.0/10.0 + Bônus Visual/UX

Para mais detalhes, consulte:
- `CHECKLIST.md` - Checklist completo do projeto
- `STATUS_PROJETO.md` - Resumo executivo e pontuação