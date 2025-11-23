# Checklist - Projeto Teoria dos Grafos

**Data:** 23 de novembro de 2025 (Atualizado)

## 📋 STATUS GERAL DO PROJETO

**Pontuação Estimada:** 10.0/10.0 pontos + Bônus Visual/UX ✅

### Resumo Executivo
- ✅ **Todos os 4 algoritmos obrigatórios completos** (BFS, DFS, Dijkstra, Bellman-Ford)
- ✅ **46/46 testes passando** 
- ✅ **CLI funcional** com todos os algoritmos e modos integrados
- ✅ **TODOS os arquivos obrigatórios gerados**
- ✅ **Parte 1 COMPLETA** - 100% dos requisitos implementados
- ✅ **Parte 2 COMPLETA** - 100% dos requisitos implementados
- ✅ **Todas as visualizações implementadas** (Parte 1 e Parte 2)
- ❌ **Relatório PDF** (única pendência - documentação final)

### Progresso por Categoria
- **Estrutura do Projeto:** 100% ✅
- **Carregamento de Dados:** 100% ✅
- **Algoritmos:** 100% ✅ (Todos os 4 completos)
- **Testes:** 100% ✅ (46 testes passando)
- **CLI:** 100% ✅ (Todos os algoritmos e modos integrados)
- **Outputs Obrigatórios:** 100% ✅ (TODOS os arquivos gerados)
- **Parte 1:** 100% ✅
- **Parte 2:** 100% ✅
- **Visualizações:** 100% ✅
- **Relatório PDF:** 0% ❌

---

## ✅ CONCLUÍDO (100% - EXCETO PDF)

### Estrutura do Projeto Obrigatória
- [x] Repositório Git configurado (GitHub: raf7525/trabalho-grafos)
- [x] Estrutura de pastas conforme PDF (`src/`, `data/`, `out/`, `tests/`)
- [x] `requirements.txt` criado e limpo (sem stdlib, apenas libs permitidas)
- [x] Ambiente virtual Python configurado

### Carregamento e Processamento de Dados (Parte 1)
- [x] Função `normalizar_texto()` para padronizar nomes de bairros
- [x] Função `processar_arquivo_bairros()` para processar CSV de bairros
- [x] Função `carregar_grafo()` para criar grafo completo
- [x] Validação: 94 bairros, 245 conexões
- [x] `data/bairros_unique.csv` - Lista de nós normalizada (bairro, microrregiao)
- [x] `data/adjacencias_bairros.csv` - Arquivo de arestas construído (formato obrigatório)
- [x] `data/enderecos.csv` - 5 pares de endereços reais com classificação de bairros

### Estrutura de Dados (Grafo)
- [x] Classe `Vertice` com atributos personalizáveis
- [x] Classe `Grafo` não-direcionado (Parte 1)
- [x] Classe `DirectedGrafo` direcionado (Parte 2)
- [x] Armazenamento de pesos nas arestas (`grafo.arestas`)
- [x] Atributos adicionais nas arestas (logradouro, tipo, id_rua)
- [x] Propriedades: `ordem`, `tamanho`, `densidade`
- [x] Método `criar_subgrafo()` para análise de regiões
- [x] Método `obter_peso()` e `obter_vizinhos()`
- [x] Método `caminho_mais_curto_dijkstra()` para facilitar uso
- [x] Método `caminho_mais_curto_bellman_ford()` para facilitar uso

### Algoritmos Implementados (PRÓPRIOS - SEM LIBS)
- [x] **BFS (Breadth-First Search)** - Busca em largura
  - [x] Implementação completa em `src/graphs/algorithms.py`
  - [x] Retornar níveis/distâncias de cada vértice
  - [x] Retornar árvore de percurso
  - [x] Retornar ordem de visitação
  - [x] Método helper `busca_em_largura()` na classe Grafo
  - [x] 9 testes unitários passando
  - [x] Integração com CLI
  - [x] Testado em ≥ 3 fontes distintas (Parte 2)

- [x] **DFS (Depth-First Search)** - Busca em profundidade
  - [x] Implementação completa
  - [x] Classificar arestas (árvore, retorno, avanço, cruzamento)
  - [x] Detectar ciclos (grafos não-direcionados e direcionados)
  - [x] Timestamps de descoberta e finalização
  - [x] Identificar componentes conexos
  - [x] Método helper `busca_em_profundidade()` na classe Grafo
  - [x] 11 testes unitários passando
  - [x] Integração com CLI
  - [x] Testado em ≥ 3 fontes distintas (Parte 2)

- [x] **Dijkstra** - Caminho mais curto com pesos positivos
  - [x] Implementação completa com heap (heapq)
  - [x] Nomenclatura padronizada (distancias, anterior, visitados)
  - [x] Validação de pesos negativos (PositiveFloat)
  - [x] Retorna (distância, caminho)
  - [x] 12 testes unitários passando
  - [x] Integração com CLI
  - [x] Testado com ≥ 5 pares origem-destino (Parte 2)

- [x] **Bellman-Ford** - Caminho mais curto com suporte a pesos negativos
  - [x] Implementação completa e testada
  - [x] Detecção de ciclos negativos
  - [x] Retorna todas distâncias quando destino = None
  - [x] Nomenclatura consistente com Dijkstra
  - [x] 14 testes unitários passando
  - [x] Integração com CLI
  - [x] Caso COM peso negativo SEM ciclo negativo (Parte 2)
  - [x] Caso COM ciclo negativo detectado (Parte 2)

### PARTE 1: Grafo dos Bairros do Recife (3.0 pontos) ✅

#### 1. Nós e Arestas
- [x] Grafo rotulado com 94 bairros como nós
- [x] Tratamento especial: "Setúbal" como sub-bairro de "Boa Viagem"
- [x] Arquivo `data/adjacencias_bairros.csv` com formato obrigatório:
  - [x] Colunas: bairro_origem, bairro_destino, logradouro, observacao, peso
  - [x] Grafo não-direcionado (245 conexões bidirecionais)
  - [x] Logradouros e observações documentados
  - [x] Pesos definidos e documentados

#### 2. Métricas Globais e por Grupo
- [x] **Cidade do Recife (grafo completo):** ordem, tamanho, densidade
  - [x] Arquivo: `out/recife_global.json` ✅
- [x] **Microrregiões (subgrafos induzidos):** métricas por microrregião
  - [x] Arquivo: `out/microrregioes.json` ✅
- [x] **Ego-subrede por bairro:** ordem_ego, tamanho_ego, densidade_ego
  - [x] Arquivo: `out/ego_bairro.csv` ✅

#### 3. Graus e Rankings
- [x] Lista de graus por bairro
  - [x] Arquivo: `out/graus.csv` ✅
- [x] Identificação do bairro mais denso (maior densidade_ego)
- [x] Identificação do bairro com maior grau

#### 4. Pesos das Arestas
- [x] Definição de régua de pesos clara e consistente
- [x] Documentação da fórmula de pesos (categoria de via + penalidades)
- [x] Pesos gravados em `data/adjacencias_bairros.csv`
- [x] Sem pesos negativos na Parte 1

#### 5. Distância entre Endereços X e Y
- [x] Arquivo `data/enderecos.csv` com 5 pares de endereços reais
- [x] Classificação manual dos bairros (bairro_X, bairro_Y)
- [x] Cálculo de custo e percurso usando Dijkstra
- [x] Arquivo: `out/distancias_enderecos.csv` ✅
  - [x] Colunas: Endereco_X, Endereco_Y, Bairro_X, Bairro_Y, Custo, Caminho
- [x] **Par obrigatório:** Nova Descoberta → Setúbal (Boa Viagem)
  - [x] Arquivo: `out/percurso_nova_descoberta_setubal.json` ✅

#### 6. Transformar Percurso em Árvore
- [x] Árvore de caminho do percurso obrigatório
- [x] Visualização interativa: `out/viz_arvore_bfs_boa_vista.html` ✅
- [x] Destaque do caminho (cor, espessura)
- [x] Rótulos dos bairros visíveis

#### 7. Explorações e Visualizações Analíticas (≥ 3)
- [x] **Visualização 1:** Mapa de cores por grau do bairro
  - [x] Arquivo: `out/viz_mapa_cores_grau.png` ✅
- [x] **Visualização 2:** Ranking de densidade de ego-subrede por microrregião
  - [x] Arquivo: `out/viz_densidade_microrregiao.png` ✅
- [x] **Visualização 3:** Subgrafo dos 10 bairros com maior grau
  - [x] Arquivo: `out/viz_subgrafo_top10.html` ✅
- [x] **Visualização 4:** Distribuição dos graus (histograma)
  - [x] Arquivo: `out/viz_distribuicao_graus.png` ✅
- [x] **Visualização 5:** Árvore BFS a partir de "Boa Vista"
  - [x] Arquivo: `out/viz_arvore_bfs_boa_vista.html` ✅

#### 8. Apresentação Interativa do Grafo
- [x] HTML interativo com pyvis
- [x] Tooltip por bairro (grau, microrregião, densidade_ego)
- [x] Caixa de busca por bairro
- [x] Realce do caminho obrigatório
- [x] Arquivo: `out/grafo_interativo.html` ✅

### PARTE 2: Dataset Maior e Comparação (3.0 pontos) ✅

#### Dataset Escolhido: Aeroportos dos EUA
- [x] Arquivo: `data/usa_airport_dataset.csv`
- [x] Descrição completa do dataset:
  - [x] |V| = 526 aeroportos (vértices)
  - [x] |E| = 8524 rotas de voo (arestas)
  - [x] Tipo: Grafo direcionado e ponderado
  - [x] Distribuição de graus: variável (hubs vs aeroportos regionais)

#### Implementação e Execução dos Algoritmos
- [x] **BFS/DFS** a partir de ≥ 3 fontes distintas
  - [x] Testado: SEA, JFK, LAX
  - [x] Relatório de ordem/camadas/ciclos gerado
- [x] **Dijkstra** com pesos ≥ 0 (≥ 5 pares origem-destino)
  - [x] Testado: SEA→RDM, MHK→AMW, GEG→RDM, AZA→RDM, JFK→LAX
- [x] **Bellman-Ford** com casos especiais:
  - [x] Caso COM peso negativo SEM ciclo negativo
  - [x] Caso COM ciclo negativo (detectado corretamente)

#### Métricas de Desempenho
- [x] Tempo de execução por algoritmo/tarefa
- [x] Arquivo: `out/parte2_report.json` ✅
- [x] Inclui todos os benchmarks (BFS, DFS, Dijkstra, Bellman-Ford)

#### Visualizações (≥ 1)
- [x] **Visualização 1:** Distribuição de graus do grafo de aeroportos
  - [x] Arquivo: `out/parte2_distribuicao_graus.png` ✅
- [x] **Visualização 2:** Comparação de performance dos algoritmos
  - [x] Arquivo: `out/parte2_comparacao_performance.png` ✅

#### Discussão Crítica
- [x] Quando/por que cada algoritmo é mais adequado
- [x] Limites do design de pesos
- [x] Documentado no código e no `parte2_report.json`

### TESTES UNITÁRIOS (2.0 pontos) ✅

#### Testes Obrigatórios (pytest)
- [x] **BFS:** Níveis corretos em grafo pequeno
  - [x] 9 testes passando ✅
- [x] **DFS:** Detecção de ciclo e classificação de arestas
  - [x] 11 testes passando ✅
- [x] **Dijkstra:** Caminhos corretos com pesos ≥ 0; recusar peso negativo
  - [x] 12 testes passando ✅
- [x] **Bellman-Ford:** 
  - [x] Pesos negativos SEM ciclo negativo → distâncias corretas
  - [x] COM ciclo negativo → flag/detecção
  - [x] 14 testes passando ✅

#### Status Total
- [x] **46/46 testes passando** ✅
- [x] Cobertura completa dos 4 algoritmos principais

### INTERFACE CLI (src/cli.py) ✅

#### Argumentos Implementados
- [x] `--dataset <PATH>` - Caminho para o dataset
- [x] `--alg <ALG>` - Algoritmo (BFS, DFS, DIJKSTRA, BELLMAN-FORD)
- [x] `--source <VERTICE>` - Vértice de origem
- [x] `--target <VERTICE>` - Vértice de destino
- [x] `--out <PATH>` - Diretório de saída
- [x] `--interactive` - Modo interativo (Parte 1)
- [x] `--metricas` - Gerar métricas completas
- [x] `--viz` - Gerar visualizações
- [x] `--parte2` - Análise completa da Parte 2

#### Funcionalidades
- [x] Detecção automática do tipo de dataset (Parte 1 vs Parte 2)
- [x] Execução de algoritmos individuais
- [x] Execução de análise completa
- [x] Geração de métricas e visualizações
- [x] Orquestração com `solve.py` e `viz.py`

#### Exemplos de Uso Funcionais (Conforme PDF)
```bash
# PARTE 1 - Análise Completa
python -m src.cli --dataset data/adjacencias_bairros.csv --out out/

# PARTE 1 - BFS
python -m src.cli --dataset data/adjacencias_bairros.csv --alg BFS --source "Boa Viagem" --out out/

# PARTE 1 - Dijkstra
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DIJKSTRA --source "Nova Descoberta" --target "Boa Viagem" --out out/

# PARTE 1 - Interativo
python -m src.cli --dataset data/adjacencias_bairros.csv --interactive --out out/

# PARTE 2 - Análise Completa
python -m src.cli --parte2 --dataset data/usa_airport_dataset.csv --out out/

# PARTE 2 - Dijkstra
python -m src.cli --dataset data/usa_airport_dataset.csv --alg DIJKSTRA --source "SEA" --target "RDM" --out out/
```

### QUALIDADE DO CÓDIGO E ORGANIZAÇÃO (2.0 pontos) ✅

#### Qualidade do Código
- [x] Código limpo e bem comentado
- [x] Separação de responsabilidades (cli, solve, viz, graphs)
- [x] Uso adequado de classes e funções
- [x] Type hints onde apropriado
- [x] Tratamento de erros adequado

#### Organização
- [x] Estrutura de pastas conforme especificação do PDF
- [x] Arquivos organizados por funcionalidade
- [x] Nomenclatura clara e consistente
- [x] Remoção de arquivos desnecessários (.pyc, __pycache__)

#### README.md
- [x] Instruções completas de instalação
- [x] Exemplos de uso do CLI
- [x] Descrição dos algoritmos
- [x] Estrutura do projeto documentada
- [x] Tecnologias utilizadas listadas

#### PDF (PENDENTE)
- [ ] ❌ Documentação completa (manual + técnica)
- [ ] ❌ Fontes/justificativas das interconexões
- [ ] ❌ Fórmula de peso documentada
- [ ] ❌ Limitações e discussão crítica
- [ ] ❌ Notas analíticas das visualizações

### BÔNUS VISUAL/UX (+1.0 ponto) ✅

- [x] Experiência interativa caprichada
- [x] Filtros e busca no grafo interativo
- [x] Destaque de caminhos
- [x] Camadas por microrregião
- [x] Tooltips informativos
- [x] Visualizações diversificadas e informativas
- [x] Interface CLI amigável e bem documentada

---

## 📊 ANÁLISE DETALHADA POR REQUISITO DO PDF

### Parte 1: Implementação dos Algoritmos (3.0 pontos) ✅

| Requisito | Status | Arquivo de Saída |
|-----------|--------|------------------|
| Nós/arestas | ✅ | `data/adjacencias_bairros.csv` |
| Métricas globais | ✅ | `out/recife_global.json` |
| Métricas microrregiões | ✅ | `out/microrregioes.json` |
| Métricas ego-subrede | ✅ | `out/ego_bairro.csv` |
| Graus e rankings | ✅ | `out/graus.csv` |
| Distâncias endereços | ✅ | `out/distancias_enderecos.csv` |
| Percurso obrigatório | ✅ | `out/percurso_nova_descoberta_setubal.json` |
| Árvore do percurso | ✅ | `out/viz_arvore_bfs_boa_vista.html` |
| Visualizações (≥3) | ✅ | `out/viz_*.png`, `out/viz_*.html` |
| Grafo interativo | ✅ | `out/grafo_interativo.html` |

**Pontuação Estimada:** 3.0/3.0 ✅

### Parte 2: Dataset Maior e Comparação (3.0 pontos) ✅

| Requisito | Status | Pontos | Evidência |
|-----------|--------|--------|-----------|
| Descrever o dataset | ✅ | 0.5/0.5 | 526 vértices, 8524 arestas, direcionado |
| Execução correta dos 4 algoritmos | ✅ | 1.0/1.0 | BFS/DFS (3 fontes), Dijkstra (5 pares) |
| Casos BF (pesos negativos e ciclo) | ✅ | 0.5/0.5 | `parte2_report.json` |
| Métricas de desempenho | ✅ | 0.5/0.5 | `out/parte2_report.json` |
| Visualização (≥1) | ✅ | 0.25/0.25 | 2 visualizações geradas |
| Discussão crítica | ✅ | 0.25/0.25 | Documentada no código e report |

**Pontuação Estimada:** 3.0/3.0 ✅

### Apresentação: Participação e Comprometimento (2.0 pontos)

**Status:** A ser avaliado durante as apresentações ⏳

### Qualidade do Código, Organização, Testes, README e PDF (2.0 pontos)

| Item | Status | Pontos |
|------|--------|--------|
| Qualidade do código | ✅ | 0.5/0.5 |
| Organização | ✅ | 0.5/0.5 |
| Testes Unitários (46 passando) | ✅ | 0.5/0.5 |
| README | ✅ | 0.25/0.25 |
| PDF | ❌ | 0.0/0.25 |

**Pontuação Estimada:** 1.75/2.0 (pendente PDF)

### Bônus Visual/UX (+1.0 ponto) ✅

- ✅ Experiência interativa completa e caprichada
- ✅ Múltiplas visualizações informativas
- ✅ Interface CLI amigável

**Pontuação Bônus:** +1.0 ✅

---

## 📁 ARQUIVOS OBRIGATÓRIOS (CHECKLIST COMPLETO)

### Dados de Entrada
- [x] `data/bairros_recife.csv` (fornecido)
- [x] `data/bairros_unique.csv` (construído - lista de nós normalizada)
- [x] `data/adjacencias_bairros.csv` (construído - formato obrigatório)
- [x] `data/enderecos.csv` (construído - 5 pares)
- [x] `data/usa_airport_dataset.csv` (dataset Parte 2)

### Saídas Obrigatórias (Parte 1)
- [x] `out/recife_global.json` ✅
- [x] `out/microrregioes.json` ✅
- [x] `out/ego_bairro.csv` ✅
- [x] `out/graus.csv` ✅
- [x] `out/distancias_enderecos.csv` ✅
- [x] `out/percurso_nova_descoberta_setubal.json` ✅ **(OBRIGATÓRIO)**
- [x] `out/arvore_percurso.html|png` ✅ (HTML implementado)
- [x] `out/grafo_interativo.html` ✅

### Saídas Obrigatórias (Parte 2)
- [x] `out/parte2_report.json` ✅

### Visualizações Adicionais
- [x] `out/viz_mapa_cores_grau.png` ✅
- [x] `out/viz_densidade_microrregiao.png` ✅
- [x] `out/viz_subgrafo_top10.html` ✅
- [x] `out/viz_distribuicao_graus.png` ✅
- [x] `out/viz_arvore_bfs_boa_vista.html` ✅
- [x] `out/parte2_comparacao_performance.png` ✅
- [x] `out/parte2_distribuicao_graus.png` ✅

### Código Fonte
- [x] `src/cli.py` ✅
- [x] `src/solve.py` ✅
- [x] `src/viz.py` ✅
- [x] `src/config.py` ✅
- [x] `src/graphs/io.py` ✅
- [x] `src/graphs/graph.py` ✅
- [x] `src/graphs/algorithms.py` ✅

### Testes
- [x] `tests/test_bfs.py` ✅
- [x] `tests/test_dfs.py` ✅
- [x] `tests/test_dijkstra.py` ✅
- [x] `tests/test_bellman_ford.py` ✅

### Documentação
- [x] `README.md` ✅
- [x] `requirements.txt` ✅
- [ ] **Relatório PDF** ❌ **(ÚNICA PENDÊNCIA)**

---

## 🎯 PRÓXIMOS PASSOS

### CRÍTICO - Para Entrega Final
1. ❌ **Escrever Relatório PDF completo**
   - Documentação técnica (como foi implementado)
   - Manual de uso (já coberto no README)
   - Fontes e justificativas das interconexões entre bairros
   - Fórmula de peso documentada e justificada
   - Limitações do projeto
   - Discussão crítica sobre os algoritmos
   - Notas analíticas sobre as visualizações

---

## 📊 PONTUAÇÃO FINAL ESTIMADA

| Categoria | Pontos Possíveis | Pontos Obtidos | Status |
|-----------|------------------|----------------|--------|
| Parte 1: Grafo dos Bairros | 3.0 | 3.0 | ✅ |
| Parte 2: Dataset Maior | 3.0 | 3.0 | ✅ |
| Apresentação | 2.0 | - | ⏳ |
| Qualidade/Testes/Docs | 2.0 | 1.75 | 🟨 (falta PDF) |
| **Subtotal** | **10.0** | **7.75** | - |
| Bônus Visual/UX | +1.0 | +1.0 | ✅ |
| **TOTAL** | **10.0** | **8.75** | 🟨 |

**Com PDF completo:** 10.0/10.0 pontos + Bônus ✅

---

## 📝 NOTAS IMPORTANTES

### Pontos Fortes do Projeto
1. ✅ **Implementação completa e correta** - Todos os 4 algoritmos funcionando perfeitamente
2. ✅ **Testes abrangentes** - 46 testes unitários cobrindo todos os algoritmos
3. ✅ **CLI robusto e amigável** - Interface completa com detecção automática
4. ✅ **TODOS os outputs obrigatórios gerados** - 100% dos arquivos exigidos
5. ✅ **Visualizações ricas e informativas** - Múltiplas visualizações interativas e estáticas
6. ✅ **Código bem estruturado** - Separação clara de responsabilidades
7. ✅ **Parte 2 completa** - Dataset adicional totalmente implementado com benchmarks

### Única Pendência
1. ❌ **Relatório PDF** - Documentação final necessária para completar os 10 pontos

### Conformidade com o PDF do Projeto
- ✅ Estrutura de pastas **100% conforme especificado**
- ✅ Nomenclatura de arquivos **100% conforme obrigatório**
- ✅ Todos os algoritmos **implementados SEM libs prontas** (própria implementação)
- ✅ Libs permitidas usadas corretamente (pandas, matplotlib, pyvis, heapq)
- ✅ Formato de `adjacencias_bairros.csv` **exatamente como especificado**
- ✅ Tratamento de "Setúbal" como sub-bairro de Boa Viagem **conforme instruções**

### Comandos de Teste Validados
Todos os comandos especificados no PDF foram testados e funcionam corretamente:
```bash
# PARTE 1 - Análise completa
python -m src.cli --dataset data/adjacencias_bairros.csv --out out/

# PARTE 1 - Algoritmos específicos
python -m src.cli --dataset data/adjacencias_bairros.csv --alg BFS --source "Boa Viagem" --out out/
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DIJKSTRA --source "Nova Descoberta" --target "Boa Viagem" --out out/
python -m src.cli --dataset data/adjacencias_bairros.csv --interactive --out out/

# PARTE 2 - Análise completa
python -m src.cli --parte2 --dataset data/usa_airport_dataset.csv --out out/

# PARTE 2 - Algoritmos específicos
python -m src.cli --dataset data/usa_airport_dataset.csv --alg DIJKSTRA --source "SEA" --target "RDM" --out out/
```

---

**Última atualização:** 23 de novembro de 2025 - Projeto 100% completo (exceto PDF)
**Status:** ✅ PRONTO PARA ENTREGA (adicionar PDF)



# Final do final

COMO CONSEGUIMOS OS DADOS ?
- conseguiu malha geometrica dos bairros usando QGIS gerando uma lista de adjecencia dos bairros
- a partir dessa lista usamos osmnx para conseguir os logradouros que ligavam esses bairros
- calculando dijkstra para os dois bairros e pagando a primeira aresta do resultado que seria a rua
- para os pesos usamos o tipo de rua (rua local, avenida etc...)
- pegamos o ID de cada logradouro para criar um link que liga a rua real e pode ser acessado :)

PARTE 2
- opcionalmente fazer uma visualização extra para parte 2 com o grafo a partir do dataset para ficar bonito
- discussão critica

README?
- fazer README e PDF (como obtiveram as interconexões (fontes/justificativas), fórmula de peso, limitações)
- pode falar na parte 2 que n fazia mt sentido usar peso negativo

REFACTOR
- limpada nos comentarios
- colocar todas as variaveis em portugues

DUVIDAS?
- pq dfs ta demorando muito mais pra rodar?
