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
- [x] Método `caminho_mais_curto_dijkstra()` para facilitar uso
- [x] Método `caminho_mais_curto_bellman_ford()` para facilitar uso

### Algoritmos Implementados
- [x] **Dijkstra** - caminho mais curto com pesos positivos
  - [x] Implementação completa e testada
  - [x] Nomenclatura padronizada (distancias, anterior, visitados)
  - [x] Validação de pesos negativos (PositiveFloat)
  - [x] Retorna (distância, caminho)
  - [x] 12 testes unitários passando
- [x] **Bellman-Ford** - caminho mais curto com suporte a pesos negativos
  - [x] Implementação completa e testada
  - [x] Detecção de ciclos negativos
  - [x] Retorna todas distâncias quando destino = None
  - [x] Nomenclatura consistente com Dijkstra
  - [x] 14 testes unitários passando
- [ ] **BFS (Breadth-First Search)** - busca em largura
  - [x] Implementação básica (retorna parent dict)
  - [ ] Adaptação completa para requisitos do projeto
  - [ ] Retornar níveis/distâncias de cada vértice
  - [ ] Retornar árvore de percurso
  - [ ] Testes unitários
- [ ] **DFS (Depth-First Search)** - busca em profundidade
  - [ ] Implementação (apenas stub vazio)
  - [ ] Classificar arestas
  - [ ] Detectar ciclos
  - [ ] Testes unitários


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
- [x] Argumento: `--interactive` (estrutura criada, não funcional)
- [x] Integração com `solve.py` e `io.py`
- [x] Execução via `python3 -m src.cli`
- [x] Comando testado: gera todos os arquivos de métricas
- [ ] Integração com algoritmos Dijkstra/Bellman-Ford
- [ ] Integração com BFS/DFS

### Visualizações
- [ ] ⚠️ **NÃO IMPLEMENTADO - REMOVIDO DO ESCOPO ATUAL**
- [ ] Arquivos criados mas não testados nem funcionais
- [ ] Será implementado posteriormente se houver tempo

---

## ❌ NÃO INICIADO

### Parte 1 - Algoritmos de Percurso e Caminhos

#### BFS (Breadth-First Search)
- [x] Implementação básica existe
- [ ] Adaptar para retornar níveis/distâncias
- [ ] Retornar árvore de percurso completa
- [ ] Gerar saída JSON: `percurso_bfs.json`
- [ ] Testar com origem específica (ex: "nova descoberta")
- [ ] Testes unitários

#### DFS (Depth-First Search)
- [ ] Implementar algoritmo completo em `src/graphs/algorithms.py`
- [ ] Classificar arestas (árvore, retorno, avanço, cruzamento)
- [ ] Detectar ciclos no grafo
- [ ] Retornar ordem de descoberta/finalização (timestamps)
- [ ] Gerar saída JSON: `percurso_dfs.json`

#### Dijkstra
- [x] Implementar em `src/graphs/algorithms.py` ✅
- [x] Validar pesos não-negativos ✅
- [x] Calcular menor caminho origem → destino ✅
- [x] Retornar distância total e caminho ✅
- [x] Método helper na classe Grafo: `caminho_mais_curto_dijkstra()` ✅
- [x] 12 testes unitários passando ✅
- [ ] Integrar no CLI com argumentos `--source` e `--target`
- [ ] Gerar saída JSON: `caminho_dijkstra.json`
- [ ] Caso de uso específico: Nova Descoberta → Boa Viagem
- [ ] Gerar `percurso_nova_descoberta_setubal.json` (OBRIGATÓRIO no PDF)

#### Bellman-Ford
- [x] Implementar em `src/graphs/algorithms.py` ✅
- [x] Suportar pesos negativos ✅
- [x] Detectar ciclos negativos ✅
- [x] Calcular menor caminho origem → destino ✅
- [x] Retornar distância e caminho ✅
- [x] Método helper na classe Grafo: `caminho_mais_curto_bellman_ford()` ✅
- [x] Retornar todas as distâncias (quando destino = None) ✅
- [x] 14 testes unitários passando ✅
- [ ] Integrar no CLI
- [ ] Gerar saída JSON: `caminho_bellman_ford.json`

#### Outputs Obrigatórios de Algoritmos (conforme PDF)
- [ ] `percurso_nova_descoberta_setubal.json` (Dijkstra - OBRIGATÓRIO)
- [ ] `distancias_enderecos.csv` (matriz de distâncias entre bairros)
- [ ] JSONs com resultados de BFS e DFS
- [ ] ⚠️ Visualizações removidas do escopo atual

### Parte 2 - Dataset Adicional
- [ ] Processar segundo dataset (se fornecido)
- [ ] Executar mesmos algoritmos
- [ ] Comparar resultados entre datasets
- [ ] Análise de performance (tempo de execução)

### Testes Unitários (2.0 pontos)

#### Infraestrutura de Testes
- [x] Classe `HelperTest` em `tests/base.py` ✅
- [x] Método `criar_grafo_com_vertices()` ✅
- [x] Método `carregar_grafo_real()` ✅
- [x] Método `assert_caminho_valido()` ✅
- [x] Método `calcular_distancia_caminho()` ✅
- [x] Método `assert_caminho_direto()` ✅
- [x] Método `assert_distancia_infinita()` ✅
- [x] Método `assert_distancia_aproximada()` ✅

#### Testes Dijkstra
- [x] Implementar `tests/test_dijkstra.py` ✅
- [x] Validar menor caminho conhecido ✅
- [x] Testar rejeição de pesos negativos ✅
- [x] Verificar caminho impossível ✅
- [x] Testar com grafo real dos bairros ✅
- [x] Validar continuidade do caminho ✅
- [x] Verificar cálculo correto de distâncias ✅
- [x] **12 testes passando** ✅

#### Testes Bellman-Ford
- [x] Implementar `tests/test_bellman_ford.py` ✅
- [x] Validar menor caminho com pesos positivos ✅
- [x] Testar detecção de ciclo negativo ✅
- [x] Comparar com Dijkstra em grafo positivo ✅
- [x] Testar retorno de todas as distâncias ✅
- [x] Testar com grafo real dos bairros ✅
- [x] Validar caminhos múltiplos ✅
- [x] **14 testes passando** ✅

#### Testes BFS
- [ ] Implementar `tests/test_bfs.py` (atualmente vazio)
- [ ] Testar em grafo pequeno conhecido
- [ ] Validar níveis corretos a partir da origem
- [ ] Testar bairro inalcançável
- [ ] Verificar árvore de percurso (predecessores)

#### Testes DFS
- [ ] Implementar `tests/test_dfs.py` (atualmente vazio)
- [ ] Validar classificação de arestas
- [ ] Testar detecção de ciclos
- [ ] Verificar ordem de descoberta e finalização
- [ ] Testar em grafo pequeno e no grafo real

#### Executar Suite de Testes
- [x] Comando: `pytest tests/` ✅
- [x] **26/26 testes passando** (Dijkstra + Bellman-Ford) ✅
- [x] Configuração pytest.ini ✅
- [ ] Adicionar testes para BFS (0 testes atualmente)
- [ ] Adicionar testes para DFS (0 testes atualmente)
- [ ] Meta: 100% de cobertura dos 4 algoritmos principais

### Visualizações Finais

⚠️ **REMOVIDO DO ESCOPO ATUAL** - Visualizações não são prioritárias e serão implementadas apenas se houver tempo após completar todos os algoritmos e testes obrigatórios.

- [ ] Arquivos em `src/viz.py` existem mas não foram testados
- [ ] Não integrado ao CLI
- [ ] Não funcional no momento

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

#### Arquivos Obrigatórios (conforme PDF do projeto)
- [x] `recife_global.json` ✅
- [x] `microrregioes.json` ✅
- [x] `ego_bairro.csv` ✅
- [x] `graus.csv` ✅
- [x] `rankings.json` ✅
- [ ] `percurso_nova_descoberta_setubal.json` ❌ (OBRIGATÓRIO)
- [ ] `distancias_enderecos.csv` ❌
- [ ] JSONs com resultados BFS/DFS ❌
- [ ] ⚠️ HTMLs de visualização removidos do escopo atual

#### Validação Final
- [x] Executar `python3 -m src.cli --metricas` → OK ✅
- [ ] Executar `python3 -m src.cli --alg BFS --source "nova descoberta"` → Pendente
- [ ] Executar `python3 -m src.cli --alg DFS --source "nova descoberta"` → Pendente
- [ ] Executar `python3 -m src.cli --alg DIJKSTRA --source "nova descoberta" --target "boa viagem"` → Pendente
- [ ] Executar `python3 -m src.cli --alg BELLMAN_FORD --source "nova descoberta" --target "boa viagem"` → Pendente
- [x] Executar `pytest tests/` → 26/26 passando ✅
- [ ] Verificar todos os JSONs/CSVs obrigatórios gerados
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
- **Algoritmos:** 50% ⚠️ (Dijkstra + Bellman-Ford completos, BFS parcial, DFS não iniciado)
- **Testes:** 50% ⚠️ (26 testes para Dijkstra + Bellman-Ford, faltam BFS e DFS)
- **CLI Básico:** 40% ⚠️ (métricas OK, falta integração com algoritmos)
- **Integração CLI + Algoritmos:** 0% ❌
- **Outputs Obrigatórios:** 60% ⚠️ (métricas OK, faltam JSONs de algoritmos)
- **Visualizações:** 0% ❌ (removido do escopo atual)
- **Relatório:** 0% ❌

### Por Pontuação (Base: 10.0 pontos - estimativa conservadora)
- **Parte 1 (5.0 pts):** ~40% (2.0/5.0) 
  - Dijkstra: OK (implementação + testes) ✅
  - Bellman-Ford: OK (implementação + testes) ✅
  - BFS: Parcial (implementação básica, sem testes) ⚠️
  - DFS: Não iniciado ❌
  - Integração CLI: Não feita ❌
  - Outputs obrigatórios: Parciais ⚠️
  
- **Parte 2 (3.0 pts):** 0% (0/3.0) - Dataset adicional não iniciado ❌
- **Testes (2.0 pts):** 50% (1.0/2.0) - Apenas Dijkstra + Bellman-Ford ⚠️
- **Bônus Visualizações (+1.0 pt):** 0% (0/1.0) - Removido do escopo ❌

**Total Estimado Conservador:** ~3.0/10.0 pontos
**Total Otimista (se completar BFS/DFS):** ~5.0/10.0 pontos

---

## 🎯 PRÓXIMOS PASSOS PRIORITÁRIOS

### CRÍTICO - Para Pontuação Básica (Curto Prazo)
1. ~~Implementar Dijkstra~~ ✅ COMPLETO
2. ~~Implementar Bellman-Ford~~ ✅ COMPLETO
3. ~~Testes Dijkstra~~ ✅ COMPLETO
4. ~~Testes Bellman-Ford~~ ✅ COMPLETO
5. **Completar BFS** - retornar níveis e árvore de percurso ⚠️ URGENTE
6. **Implementar DFS completo** - com classificação de arestas ⚠️ URGENTE
7. **Integrar Dijkstra no CLI** - aceitar `--source` e `--target` ⚠️ URGENTE
8. **Integrar Bellman-Ford no CLI** ⚠️ URGENTE
9. **Integrar BFS no CLI** ⚠️ URGENTE
10. **Integrar DFS no CLI** ⚠️ URGENTE
11. **Gerar `percurso_nova_descoberta_setubal.json`** ⚠️ OBRIGATÓRIO NO PDF

### IMPORTANTE - Para Completar Requisitos (Médio Prazo)
12. Criar testes unitários para BFS completo
13. Criar testes unitários para DFS completo
14. Gerar `distancias_enderecos.csv` (matriz de distâncias)
15. Gerar JSONs de resultados para todos os algoritmos
16. Executar suite completa de testes (meta: 40+ testes)
17. Processar Parte 2 (dataset adicional, se fornecido)

### OPCIONAL - Se Houver Tempo (Longo Prazo)
18. Implementar visualizações básicas
19. Escrever relatório PDF
20. Adicionar screenshots no relatório
21. Revisar código e documentação
22. Criar README.md completo
23. Push final no GitHub
24. Validação completa de todos os outputs

---

## 📝 NOTAS IMPORTANTES

### Dados do Grafo
- **Dados:** 94 bairros, 245 conexões, densidade 0.056
- **Bairros isolados:** Cabanga, São José (0 arestas)
- **Externos ignorados:** Aldeia, Oitinga (não são Recife)
- **Top bairro (grau):** Casa Amarela (11 conexões)
- **Top bairro (densidade ego):** Brasília Teimosa (1.0)

### Comandos Funcionais
- ✅ `python3 -m src.cli --dataset ./data/bairros_recife.csv --metricas --out ./out/`
- ❌ Comandos com algoritmos (--alg) ainda não funcionam

### Bibliotecas Instaladas
- pandas, matplotlib, plotly, pyvis, pytest, unidecode

### Outputs Obrigatórios Conforme PDF
1. ✅ Métricas do grafo (recife_global.json, etc.)
2. ❌ **percurso_nova_descoberta_setubal.json** (CRÍTICO - OBRIGATÓRIO)
3. ❌ distancias_enderecos.csv
4. ❌ Resultados dos 4 algoritmos em JSON

### Status dos Algoritmos
- **Dijkstra:** ✅ Implementado e testado (12 testes)
- **Bellman-Ford:** ✅ Implementado e testado (14 testes)
- **BFS:** ⚠️ Implementação básica existe, precisa completar
- **DFS:** ❌ Apenas stub vazio, precisa implementar do zero

---

## ⏰ ESTIMATIVA DE TEMPO

### Já Completo (~12-18 horas)
- ✅ Implementar Dijkstra e Bellman-Ford
- ✅ Criar testes Dijkstra + Bellman-Ford (26 testes)
- ✅ Documentação dos algoritmos

### Trabalho Restante Crítico
- Completar BFS: **2-3 horas** ⚠️ URGENTE
- Implementar DFS completo: **3-4 horas** ⚠️ URGENTE
- Integrar 4 algoritmos no CLI: **4-6 horas** ⚠️ URGENTE
- Gerar outputs obrigatórios JSON: **2-3 horas** ⚠️ URGENTE
- Criar testes BFS + DFS: **3-4 horas**
- Criar matriz de distâncias: **2-3 horas**
- **Subtotal Crítico:** ~16-23 horas

### Trabalho Restante Opcional
- Parte 2 (dataset adicional): **4-6 horas**
- Escrever relatório PDF: **6-8 horas**
- Implementar visualizações: **4-6 horas**
- Revisão final e validação: **2-3 horas**
- **Subtotal Opcional:** ~16-23 horas

**TOTAL RESTANTE (Mínimo Crítico):** ~16-23 horas
**TOTAL RESTANTE (Completo):** ~32-46 horas

---

*Última atualização: 15 de novembro de 2025 - Revisão completa baseada no PDF do projeto*
