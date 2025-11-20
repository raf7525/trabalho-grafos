# Projeto Final - Teoria dos Grafos

Análise de grafos aplicada aos bairros de Recife utilizando algoritmos de percurso e caminho mais curto.

## 📋 Descrição

Este projeto implementa e aplica algoritmos clássicos de teoria dos grafos para análise da conectividade entre os bairros de Recife. O grafo é construído a partir de dados de conexões viárias (ruas, avenidas) entre os bairros, com pesos representando distâncias.

**Dataset:** 94 bairros, 245 conexões, densidade 0.056

## 🎯 Algoritmos Implementados

### ✅ Completos e Testados
- **BFS (Breadth-First Search)** - Busca em largura
  - Retorna níveis, distâncias, árvore de percurso e ordem de visitação
  - 9 testes unitários passando
  
- **Dijkstra** - Caminho mais curto (pesos não-negativos)
  - Implementação com heap (priority queue)
  - 12 testes unitários passando
  
- **Bellman-Ford** - Caminho mais curto (suporta pesos negativos)
  - Detecção de ciclos negativos
  - 14 testes unitários passando

### ❌ Pendente
- **DFS (Depth-First Search)** - Busca em profundidade (não implementado)

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8+
- pip

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

### Comandos Disponíveis

#### 1. Gerar Métricas do Grafo

```bash
python3 -m src.cli --dataset ./data/bairros_recife.csv --metricas --out ./out/
```

**Outputs gerados:**
- `out/recife_global.json` - Métricas globais (ordem, tamanho, densidade)
- `out/microrregioes.json` - Análise por microrregião
- `out/ego_bairro.csv` - Ego-network de cada bairro
- `out/graus.csv` - Graus dos vértices
- `out/rankings.json` - Rankings de bairros mais conectados

#### 2. Executar BFS (Busca em Largura)

```bash
# BFS a partir de um bairro de origem
python3 -m src.cli --dataset ./data/bairros_recife.csv --alg BFS --source "nova descoberta" --out ./out/

# BFS com origem e destino específicos
python3 -m src.cli --dataset ./data/bairros_recife.csv --alg BFS --source "nova descoberta" --target "boa viagem" --out ./out/
```

**Output:** `out/percurso_bfs_<origem>.json`

#### 3. Executar Dijkstra (Caminho Mais Curto)

```bash
python3 -m src.cli --dataset ./data/bairros_recife.csv --alg DIJKSTRA --source "nova descoberta" --target "boa viagem" --out ./out/
```

**Outputs:**
- `out/percurso_nova_descoberta_setubal.json` (obrigatório no projeto)
- Console: caminho e distância total

#### 4. Executar Bellman-Ford

```bash
python3 -m src.cli --dataset ./data/bairros_recife.csv --alg BELLMAN_FORD --source "nova descoberta" --target "boa viagem" --out ./out/
```

**Output:** `out/caminho_bellman_ford_<origem>_<destino>.json`

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest tests/
```

**Status atual:** 35/35 testes passando ✅

### Executar Testes Específicos

```bash
# Apenas testes do Dijkstra
pytest tests/test_dijkstra.py

# Apenas testes do Bellman-Ford
pytest tests/test_bell_manford.py

# Apenas testes do BFS
pytest tests/test_bfs.py

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
│   ├── bairros_recife.csv           # Dataset principal
│   ├── bairros_unique.csv           # Bairros únicos processados
│   ├── bairros_vizinhos_tratados.csv
│   └── cache/                        # Cache de geocodificação
├── src/
│   ├── __init__.py
│   ├── cli.py                        # Interface de linha de comando
│   ├── solve.py                      # Cálculo de métricas
│   ├── viz.py                        # Visualizações (não implementado)
│   └── graphs/
│       ├── __init__.py
│       ├── algorithms.py             # Implementação dos algoritmos
│       ├── graph.py                  # Classes Grafo e Vertice
│       └── io.py                     # Carregamento de dados
├── tests/
│   ├── base.py                       # HelperTest - classe base
│   ├── test_bfs.py                   # 9 testes BFS
│   ├── test_dijkstra.py              # 12 testes Dijkstra
│   ├── test_bell_manford.py          # 14 testes Bellman-Ford
│   └── test_dfs.py                   # (vazio - não implementado)
├── out/                              # Diretório de saída
├── requirements.txt                  # Dependências Python
├── pytest.ini                        # Configuração do pytest
├── CHECKLIST.md                      # Acompanhamento do progresso
└── README.md                         # Este arquivo
```

## 📊 Arquivos de Saída

### Métricas Globais
- ✅ `recife_global.json` - Ordem, tamanho, densidade do grafo
- ✅ `microrregioes.json` - Análise por microrregião
- ✅ `ego_bairro.csv` - Estatísticas de ego-network
- ✅ `graus.csv` - Grau de cada vértice
- ✅ `rankings.json` - Top bairros mais conectados

### Algoritmos de Percurso
- ✅ `percurso_bfs_<origem>.json` - Resultado da busca em largura
- ❌ `percurso_dfs_<origem>.json` - (não implementado)

### Caminhos Mais Curtos
- ✅ `percurso_nova_descoberta_setubal.json` - **Obrigatório no PDF**
- ✅ `caminho_bellman_ford_<origem>_<destino>.json`
- ❌ `distancias_enderecos.csv` - Matriz de distâncias (pendente)

## 🔍 Exemplos de Uso Interativo

### Carregar Grafo e Executar Algoritmos Manualmente

```python
from src.graphs.io import carregar_grafo

# Carregar o grafo
grafo = carregar_grafo('./data/bairros_recife.csv')

# BFS
resultado_bfs = grafo.busca_em_largura('nova descoberta')
print(f"Níveis: {resultado_bfs['niveis']}")
print(f"Ordem de visita: {resultado_bfs['ordem_visita']}")

# Dijkstra
distancia, caminho = grafo.caminho_mais_curto_dijkstra('nova descoberta', 'boa viagem')
print(f"Distância: {distancia} km")
print(f"Caminho: {' → '.join(caminho)}")

# Bellman-Ford
distancia, caminho = grafo.caminho_mais_curto_bellman_ford('nova descoberta', 'boa viagem')
print(f"Distância: {distancia} km")
print(f"Caminho: {' → '.join(caminho)}")
```

## 📈 Status do Projeto

### Progresso Geral: ~5.5/10.0 pontos

#### Por Categoria
- **Estrutura do Projeto:** 100% ✅
- **Carregamento de Dados:** 100% ✅
- **Grafo e Métricas:** 100% ✅
- **Algoritmos:** 75% ✅ (3/4 completos - falta DFS)
- **Testes:** 75% ✅ (35 testes - falta DFS)
- **CLI:** 100% ✅
- **Integração CLI + Algoritmos:** 75% ✅ (falta DFS)
- **Outputs Obrigatórios:** 85% ⚠️ (faltam DFS e matriz)

#### Próximos Passos Críticos
1. ⚠️ **Implementar DFS** - com classificação de arestas
2. ⚠️ **Testes DFS** - adicionar suite completa
3. ⚠️ **Integrar DFS no CLI**
4. ⚠️ **Gerar matriz de distâncias** - `distancias_enderecos.csv`

## 🛠️ Tecnologias Utilizadas

- **Python 3.12.3**
- **pandas** - Manipulação de dados
- **pytest** - Framework de testes
- **unidecode** - Normalização de texto
- **matplotlib, plotly, pyvis** - Visualizações (planejado)
- **networkx** - Utilitários de grafos

## 📝 Notas Importantes

### Bairros Especiais
- **Isolados:** Cabanga, São José (0 conexões)
- **Mais conectado:** Casa Amarela (11 conexões)
- **Maior densidade ego:** Brasília Teimosa (1.0)

### Dados Ignorados
- **Aldeia** e **Oitinga** - Não pertencem a Recife

### Validações Implementadas
- ✅ Detecção de pesos negativos (Dijkstra rejeita, Bellman-Ford aceita)
- ✅ Validação de vértices existentes
- ✅ Tratamento de caminhos impossíveis (retorna infinito)
- ✅ Detecção de ciclos negativos (Bellman-Ford)

## 👥 Autores

Projeto desenvolvido para a disciplina de Teoria dos Grafos.

## 📄 Licença

Este projeto é acadêmico e desenvolvido para fins educacionais.

---

**Última atualização:** 20 de novembro de 2025
