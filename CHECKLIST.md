# Checklist - Projeto Teoria dos Grafos

## ✅ CONCLUÍDO

### Estrutura do Projeto
- [x] Repositório Git configurado
- [x] Estrutura de pastas (`src/`, `data/`, `out/`, `tests/`)
- [x] `requirements.txt` criado e limpo (sem stdlib)
- [x] Ambiente virtual Python configurado

### Carregamento e Processamento de Dados
- [x] Função `normalizar_texto()` para padronizar nomes
- [x] Função `processar_arquivo_bairros()` para processar CSV
- [x] Função `carregar_grafo()` para criar grafo completo
- [x] Validação: 94 bairros, 245 conexões
- [x] Identificação de dados problemáticos (Aldeia, Oitenta ignorados)
- [x] Detecção de bairros isolados (Cabanga, São José)

### Estrutura de Dados (Grafo)
- [x] Classe `Vertice` com atributos personalizáveis
- [x] Classe `Grafo` não-direcionado
- [x] Armazenamento de pesos nas arestas (`grafo.arestas`)
- [x] Atributos adicionais nas arestas (logradouro, tipo, id_rua)
- [x] Propriedades: `ordem`, `tamanho`, `densidade`
- [x] Método `criar_subgrafo()` para análise de regiões
- [x] Método `obter_peso()` e `obter_vizinhos()`

### Refatoração de Código
- [x] Renomeação para português claro (sem abreviações)
- [x] Remoção de docstrings e emojis conforme solicitado
- [x] Código limpo e direto
- [x] Documentação em `REFATORACAO.md`

### Métricas e Análises (solve.py)
- [x] `calcular_metricas_globais()` - ordem, tamanho, densidade
- [x] `calcular_metricas_microrregioes()` - análise por microrregião
- [x] `calcular_metricas_ego()` - ego-network de 94 bairros
- [x] `calcular_graus_e_rankings()` - graus e top bairros
- [x] Função `orquestrar()` para execução completa
- [x] Saída JSON: `recife_global.json`
- [x] Saída JSON: `microrregioes.json`
- [x] Saída CSV: `ego_bairro.csv`
- [x] Saída CSV: `graus.csv`
- [x] Saída JSON: `rankings.json`

### Interface CLI (cli.py)
- [x] Argumentos: `--dataset`, `--alg`, `--source`, `--target`, `--out`
- [x] Argumento: `--metricas` (funcional)
- [x] Argumento: `--interactive` (estrutura criada)
- [x] Integração com `solve.py` e `io.py`
- [x] Execução via `python3 -m src.cli`
- [x] Comando testado: gera todos os arquivos de métricas

### Visualizações (Estrutura Criada)
- [x] Arquivo `src/viz.py` com 7 funções
- [x] Função: `criar_grafo_interativo_pyvis()`
- [x] Função: `visualizar_arvore_percurso_plotly()`
- [x] Função: `visualizar_metricas_microrregioes()`
- [x] Função: `visualizar_distribuicao_graus()`
- [x] Função: `visualizar_top_bairros()`
- [x] Função: `criar_mapa_calor_densidade()`
- [x] Função: `gerar_todas_visualizacoes()`
- [x] Arquivo `src/dashboard.py` com ApexCharts + Tailwind
- [x] Arquivo `src/mapa.py` com GeoJSON + Leaflet
- [x] Documentação: `GUIA_VISUALIZACOES.md`

---

## ⚠️ PARCIALMENTE IMPLEMENTADO

### CLI - Execução de Algoritmos
- [ ] Lógica para executar BFS quando `--alg BFS`
- [ ] Lógica para executar DFS quando `--alg DFS`
- [ ] Lógica para executar Dijkstra quando `--alg DIJKSTRA`
- [ ] Lógica para executar Bellman-Ford quando `--alg BELLMAN_FORD`
- [ ] Validação de `--source` e `--target` obrigatórios
- [ ] Chamada de visualizações após algoritmos

### Modo Interativo
- [ ] Menu de seleção de algoritmo
- [ ] Input dinâmico de origem/destino
- [ ] Loop de execução contínua
- [ ] Opção de sair

### Visualizações
- [ ] Testar `viz.py` com dados reais
- [ ] Debug de erros de importação (linter warnings)
- [ ] Gerar HTMLs e verificar saída
- [ ] Integrar visualizações no CLI

---

## ❌ NÃO INICIADO

### Parte 1 - Algoritmos de Percurso e Caminhos

#### BFS (Breadth-First Search)
- [ ] Implementar em `src/graphs/algorithms.py`
- [ ] Retornar níveis/distâncias de cada bairro
- [ ] Retornar árvore de percurso
- [ ] Gerar saída JSON: `percurso_bfs.json`
- [ ] Testar com origem = "nova descoberta"

#### DFS (Depth-First Search)
- [ ] Implementar em `src/graphs/algorithms.py`
- [ ] Classificar arestas (árvore, retorno, avanço, cruzamento)
- [ ] Detectar ciclos
- [ ] Retornar ordem de descoberta/finalização
- [ ] Gerar saída JSON: `percurso_dfs.json`

#### Dijkstra
- [ ] Implementar em `src/graphs/algorithms.py`
- [ ] Validar pesos não-negativos
- [ ] Calcular menor caminho origem → destino
- [ ] Retornar distância total e caminho
- [ ] Gerar saída JSON: `caminho_dijkstra.json`
- [ ] Caso de uso: Nova Descoberta → Boa Viagem (Setúbal)
- [ ] Gerar `percurso_nova_descoberta_setubal.json` (OBRIGATÓRIO)

#### Bellman-Ford
- [ ] Implementar em `src/graphs/algorithms.py`
- [ ] Suportar pesos negativos (se existirem)
- [ ] Detectar ciclos negativos
- [ ] Calcular menor caminho origem → destino
- [ ] Retornar distância e caminho
- [ ] Gerar saída JSON: `caminho_bellman_ford.json`

#### Outputs Obrigatórios de Algoritmos
- [ ] `percurso_nova_descoberta_setubal.json` (Dijkstra)
- [ ] `distancias_enderecos.csv` (matriz de distâncias)
- [ ] Visualização: `arvore_percurso.html`

### Parte 2 - Dataset Adicional
- [ ] Processar segundo dataset (se fornecido)
- [ ] Executar mesmos algoritmos
- [ ] Comparar resultados entre datasets
- [ ] Análise de performance (tempo de execução)

### Testes Unitários (2.0 pontos)

#### Testes BFS
- [ ] Implementar `tests/test_bfs.py`
- [ ] Testar em grafo pequeno conhecido
- [ ] Validar níveis corretos
- [ ] Testar bairro inalcançável

#### Testes DFS
- [ ] Implementar `tests/test_dfs.py`
- [ ] Validar classificação de arestas
- [ ] Testar detecção de ciclos
- [ ] Verificar ordem de descoberta

#### Testes Dijkstra
- [ ] Implementar `tests/test_dijkstra.py`
- [ ] Validar menor caminho conhecido
- [ ] Testar rejeição de pesos negativos
- [ ] Verificar caminho impossível

#### Testes Bellman-Ford
- [ ] Implementar `tests/test_bellman_ford.py`
- [ ] Validar menor caminho com pesos negativos
- [ ] Testar detecção de ciclo negativo
- [ ] Comparar com Dijkstra em grafo positivo

#### Executar Suite de Testes
- [ ] Comando: `pytest tests/`
- [ ] Garantir 100% de cobertura dos algoritmos
- [ ] Corrigir falhas

### Visualizações Finais

#### Grafo Interativo
- [ ] Gerar `out/grafo_interativo.html` (PyVis)
- [ ] Cores por microrregião
- [ ] Tamanho de nó proporcional ao grau
- [ ] Hover com informações
- [ ] Testar em navegador

#### Árvore de Percurso
- [ ] Gerar `out/arvore_percurso.html` (Plotly)
- [ ] Visualizar BFS/DFS como árvore
- [ ] Destacar caminho encontrado
- [ ] Mostrar pesos acumulados

#### Gráficos de Análise
- [ ] Histograma de distribuição de graus
- [ ] Barras de métricas por microrregião
- [ ] Heatmap de densidade
- [ ] Rankings de bairros

#### Bônus: Dashboard Interativo (+1.0 ponto)
- [ ] Filtros por microrregião
- [ ] Busca de bairro
- [ ] Seleção de algoritmo dinâmica
- [ ] Comparação de caminhos
- [ ] Exportar para PNG/PDF

### Relatório Final (PDF)

#### Introdução
- [ ] Descrição do problema
- [ ] Objetivos do trabalho
- [ ] Estrutura do relatório

#### Metodologia
- [ ] Descrição da estrutura de dados
- [ ] Explicação de cada algoritmo
- [ ] Justificativa das escolhas de implementação

#### Resultados - Parte 1
- [ ] Métricas globais do grafo (tabela)
- [ ] Análise por microrregião
- [ ] Resultados BFS: níveis, árvore
- [ ] Resultados DFS: classificação de arestas, ciclos
- [ ] Resultados Dijkstra: caminho Nova Descoberta → Boa Viagem
- [ ] Resultados Bellman-Ford: comparação com Dijkstra
- [ ] Screenshots das visualizações

#### Resultados - Parte 2 (se aplicável)
- [ ] Métricas do segundo dataset
- [ ] Comparação com Parte 1
- [ ] Análise de performance (tempo de execução)

#### Discussão
- [ ] Interpretação dos resultados
- [ ] Insights sobre a estrutura de Recife
- [ ] Bairros mais conectados vs isolados
- [ ] Eficiência dos algoritmos

#### Conclusão
- [ ] Resumo dos achados
- [ ] Limitações do trabalho
- [ ] Trabalhos futuros

#### Anexos
- [ ] Código-fonte (link GitHub)
- [ ] Instruções de execução
- [ ] Requisitos (requirements.txt)

### Entrega Final

#### Organização
- [ ] Código limpo e comentado (mínimo)
- [ ] README.md com instruções completas
- [ ] Estrutura de pastas organizada
- [ ] Remover arquivos desnecessários (.pyc, __pycache__)

#### Arquivos Obrigatórios
- [ ] `recife_global.json` ✅
- [ ] `microrregioes.json` ✅
- [ ] `ego_bairro.csv` ✅
- [ ] `graus.csv` ✅
- [ ] `rankings.json` ✅
- [ ] `percurso_nova_descoberta_setubal.json` ❌
- [ ] `distancias_enderecos.csv` ❌
- [ ] `grafo_interativo.html` ❌
- [ ] `arvore_percurso.html` ❌
- [ ] Relatório PDF ❌

#### Validação Final
- [ ] Executar `python3 -m src.cli --metricas` → OK
- [ ] Executar `python3 -m src.cli --alg BFS --source "nova descoberta"` → Pendente
- [ ] Executar `python3 -m src.cli --alg DIJKSTRA --source "nova descoberta" --target "boa viagem"` → Pendente
- [ ] Executar `pytest tests/` → Pendente
- [ ] Abrir todas as visualizações HTML → Pendente
- [ ] Verificar todos os JSONs/CSVs gerados
- [ ] Ler PDF do relatório

#### GitHub
- [ ] Push final do código
- [ ] Tag de versão: `v1.0`
- [ ] README.md atualizado
- [ ] .gitignore configurado (venv/, __pycache__, *.pyc)

---

## 📊 PROGRESSO GERAL

### Por Categoria
- **Estrutura do Projeto:** 100% ✅
- **Carregamento de Dados:** 100% ✅
- **Grafo e Métricas:** 100% ✅
- **CLI Básico:** 70% ⚠️
- **Algoritmos:** 0% ❌
- **Testes:** 0% ❌
- **Visualizações:** 30% ⚠️ (código pronto, não testado)
- **Relatório:** 0% ❌

### Por Pontuação (Base: 10.0 pontos)
- **Parte 1 (5.0 pts):** ~30% (1.5/5.0) - Métricas OK, algoritmos pendentes
- **Parte 2 (3.0 pts):** 0% (0/3.0) - Não iniciado
- **Testes (2.0 pts):** 0% (0/2.0) - Arquivos vazios
- **Bônus Viz (+1.0 pt):** 30% (~0.3/1.0) - Código existe, não funcional

**Total Estimado:** ~1.8/10.0 pontos

---

## 🎯 PRÓXIMOS PASSOS PRIORITÁRIOS

### Curto Prazo (Esta Semana)
1. Implementar BFS em `algorithms.py`
2. Implementar DFS em `algorithms.py`
3. Implementar Dijkstra em `algorithms.py`
4. Implementar Bellman-Ford em `algorithms.py`
5. Integrar algoritmos no `cli.py`
6. Gerar `percurso_nova_descoberta_setubal.json`
7. Testar visualizações (`python3 src/viz.py`)

### Médio Prazo (Próxima Semana)
8. Criar testes unitários para cada algoritmo
9. Executar suite de testes (`pytest`)
10. Gerar todas as visualizações HTML
11. Criar matriz de distâncias (`distancias_enderecos.csv`)
12. Processar Parte 2 (se dataset disponível)

### Longo Prazo (Antes da Entrega)
13. Escrever relatório PDF
14. Adicionar screenshots no relatório
15. Revisar código e documentação
16. Criar README.md completo
17. Push final no GitHub
18. Validação completa de todos os outputs

---

## 📝 NOTAS IMPORTANTES

- **Dados:** 94 bairros, 245 conexões, densidade 0.056
- **Bairros isolados:** Cabanga, São José (0 arestas)
- **Externos ignorados:** Aldeia, Oitinga (não são Recife)
- **Top bairro (grau):** Casa Amarela (11 conexões)
- **Top bairro (densidade ego):** Brasília Teimosa (1.0)
- **Comando CLI funcional:** `python3 -m src.cli --dataset ./data/bairros_recife.csv --metricas --out ./out/`
- **Bibliotecas instaladas:** pandas, matplotlib, plotly, pyvis, pytest, unidecode

---

## ⏰ ESTIMATIVA DE TEMPO

- Implementar 4 algoritmos: **8-12 horas**
- Criar testes unitários: **4-6 horas**
- Corrigir e testar visualizações: **2-3 horas**
- Escrever relatório PDF: **6-8 horas**
- Parte 2 (dataset adicional): **4-6 horas**
- Revisão final e validação: **2-3 horas**

**TOTAL:** 26-38 horas de trabalho

---

*Última atualização: 13 de novembro de 2025*
