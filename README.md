# Teoria dos Grafos - Projeto Final

Este projeto implementa uma biblioteca de manipulação de grafos em Python, aplicada a dois cenários distintos:
1.  **Análise de Bairros de Recife**: Modelagem da malha urbana para análise de conectividade e rotas.
2.  **Malha Aérea dos EUA**: Análise de rotas de voos e performance de algoritmos em grafos de maior escala.

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/raf7525/trabalho-grafos
cd trabalho-grafos

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

## Uso da Interface de Linha de Comando (CLI)

O script `src/cli.py` é a interface principal para executar análises e algoritmos.

### Exemplos de Uso

A seguir, exemplos de como usar os principais comandos da CLI.

#### Parte 1: Análise dos Bairros de Recife

O dataset padrão (`data/adjacencias_bairros.csv`) já é carregado se nenhum for especificado.

**1. Calcular Métricas e Gerar Relatórios**

Este comando calcula métricas como densidade, grau dos vértices, e gera rankings e outras análises.

```bash
python3 -m src.cli --metricas
```
*Os resultados serão salvos no diretório `out/`.*

**2. Gerar Todas as Visualizações**

Cria gráficos como o mapa de calor de graus, densidade por microrregião, e a distribuição de graus.

```bash
python3 -m src.cli --viz
```
*As imagens e arquivos HTML serão salvos em `out/`.*

**3. Executar Algoritmos de Travessia e Caminho Mínimo**

-   **Busca em Largura (BFS)**: Encontra o caminho mais curto em número de arestas.

    ```bash
    # De "Boa Viagem" para "Casa Amarela"
    python3 -m src.cli --alg BFS --source "boa viagem" --target "casa amarela"
    ```

-   **Busca em Profundidade (DFS)**: Acha um caminho e identifica ciclos.

    ```bash
    # De "Boa Viagem" para "Casa Amarela"
    python3 -m src.cli --alg DFS --source "boa viagem" --target "casa amarela"
    ```

-   **Dijkstra**: Encontra o caminho de menor custo (considerando peso 1 para cada aresta).

    ```bash
    # De "Nova Descoberta" para "Boa Viagem"
    python3 -m src.cli --alg DIJKSTRA --source "nova descoberta" --target "boa viagem"
    ```

-   **Bellman-Ford**: Alternativa ao Dijkstra, também funcional em grafos sem pesos negativos.

    ```bash
    # De "Nova Descoberta" para "Boa Viagem"
    python3 -m src.cli --alg BELLMAN_FORD --source "nova descoberta" --target "boa viagem"
    ```

#### Parte 2: Análise da Malha Aérea dos EUA

Para a parte 2, é preciso especificar o dataset de aeroportos.

**1. Executar Análise Completa da Parte 2**

Este comando executa benchmarks de performance com todos os algoritmos (BFS, DFS, Dijkstra, Bellman-Ford com e sem pesos negativos) e gera as visualizações comparativas.

```bash
python3 -m src.cli --parte2
```
*O relatório `parte2_report.json` e os gráficos de performance serão salvos em `out/`.*

**2. Executar Algoritmos Específicos no Grafo de Aeroportos**

-   **Dijkstra**: Encontra a rota de menor custo entre dois aeroportos.

    ```bash
    # De Los Angeles (LAX) para Nova York (JFK)
    python3 -m src.cli --alg DIJKSTRA --source LAX --target JFK --dataset data/usa_airport_dataset.csv
    ```

-   **Bellman-Ford**: Alternativa ao Dijkstra.

    ```bash
    # De Seattle (SEA) para Redmond (RDM)
    python3 -m src.cli --alg BELLMAN_FORD --source SEA --target RDM --dataset data/usa_airport_dataset.csv
    ```

## Testes

### Executar Todos os Testes

```bash
pytest tests/ -v
```

**Status atual:** 46/46 testes passando

**Detalhamento:**
- `test_bfs.py` - 9 testes
- `test_dfs.py` - 11 testes
- `test_dijkstra.py` - 12 testes
- `test_bellman_ford.py` - 14 testes

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

## Visualizações e Análises

Abaixo, a descrição das visualizações geradas pelo sistema:

### 1. Densidade por Microrregião (`viz_densidade_microregiao`)
Este gráfico mede a densidade de conexões dentro de cada zona administrativa (RPA) do Recife:
- RPA 1 - Centro (Recife, Santo Antônio)
- RPA 2 - Norte (Casa Amarela, Dois Unidos, etc.)
- RPA 3 - Noroeste (Casa Forte, Monteiro, etc.)
- RPA 4 - Oeste (Cordeiro, Torrões, etc.)
- RPA 5 - Sudoeste (Afogados, Bongi, etc.)
- RPA 6 - Sul (Boa Viagem, Pina, etc.)

**Utilidade:** Auxilia no planejamento urbano, análise de acessibilidade e impacto socioeconômico.

### 2. Distribuição de Graus (`viz_distribuicao_graus`)
Histograma que mostra a frequência de conexões por bairro:
- **Eixo X:** Número de conexões (grau).
- **Eixo Y:** Quantidade de bairros com aquele grau.
- Inclui estatísticas como média, mediana, mínimo e máximo.

**Utilidade:** Revela se a rede possui poucos "hubs" (bairros muito conectados) ou se a conectividade é distribuída uniformemente.

### 3. Mapa de Calor de Graus (`viz_mapa_cores_grau`)
Gráfico de barras horizontais onde cada bairro é colorido conforme seu grau:
- **Cores Quentes (Vermelho/Laranja):** Bairros com mais conexões.
- **Cores Frias (Amarelo/Claro):** Bairros com menos conexões.

**Utilidade:** Facilita a identificação visual dos bairros centrais na rede de conectividade.

### 4. Subgrafo Top 10 (`viz_subgrafo_top10`)
Visualização interativa dos 10 bairros com maior conectividade e seus vizinhos diretos:
- **Nós Vermelhos:** Top 10 bairros mais conectados.
- **Nós Azuis:** Vizinhos desses bairros.
- **Tamanho dos Nós:** Proporcional ao grau.

**Utilidade:** Permite explorar os principais "hubs" de conectividade e suas relações.

### 5. Árvore BFS (`viz_arvore_bfs`)
Representação visual da execução do algoritmo de Busca em Largura:
- Layout hierárquico com níveis definidos.
- Cores distintas para cada nível de profundidade a partir da origem.
- Setas indicando o caminho da descoberta.

**Utilidade:** Demonstra como a conectividade se propaga a partir de um ponto inicial.

## Sobre a Parte 2 (Malha Aérea)

Na segunda etapa do projeto, utilizamos um dataset de voos dos Estados Unidos. O processo envolveu:

1.  **Tratamento de Dados:** Limpeza e separação dos dados em arquivos CSV otimizados, removendo informações irrelevantes.
2.  **Modelagem:** Criação do grafo com aeroportos como vértices e rotas como arestas ponderadas pela distância.
3.  **Análise de Performance:** Execução e benchmark dos algoritmos implementados.

**Observações:**
- O algoritmo DFS apresentou tempos de execução superiores em comparação ao BFS neste cenário específico.
- O algoritmo Dijkstra demonstrou performance superior ao Bellman-Ford, como esperado pela complexidade assintótica.
- Não foram utilizados pesos negativos, pois a métrica de custo é baseada na distância física entre aeroportos.