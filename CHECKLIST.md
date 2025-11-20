# Checklist - Projeto Teoria dos Grafos

**Data:** 20 de novembro de 2025

## 📋 STATUS GERAL DO PROJETO

**Pontuação Estimada:** 5.5-6.0/10.0 pontos (conservador)

### Resumo Executivo
- ✅ **3/4 algoritmos obrigatórios completos** (BFS, Dijkstra, Bellman-Ford)
- ❌ **DFS não implementado** (único algoritmo faltando)
- ✅ **35/35 testes passando** 
- ✅ **CLI funcional** com 3 algoritmos integrados
- ✅ **Arquivo obrigatório `percurso_nova_descoberta_setubal.json` gerado**
- ❌ **Matriz de distâncias faltando**
- ❌ **Parte 2 (dataset adicional) não iniciada**

### Progresso por Categoria
- **Estrutura do Projeto:** 100% ✅
- **Carregamento de Dados:** 100% ✅
- **Algoritmos:** 75% ⚠️ (3/4 completos - falta DFS)
- **Testes:** 75% ⚠️ (35 testes - falta DFS)
- **CLI:** 75% ⚠️ (falta integração DFS)
- **Outputs Obrigatórios:** 85% ⚠️ (faltam DFS e matriz)
- **Parte 2:** 0% ❌
- **Relatório PDF:** 0% ❌

---

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
- [x] **BFS (Breadth-First Search)** - busca em largura ✅
  - [x] Implementação completa em `src/graphs/algorithms.py` ✅
  - [x] Retornar níveis/distâncias de cada vértice ✅
  - [x] Retornar árvore de percurso ✅
  - [x] Retornar ordem de visitação ✅
  - [x] Método helper `busca_em_largura()` na classe Grafo ✅
  - [x] 9 testes unitários passando ✅
  - [x] Integração com CLI ✅
- [x] **DFS (Depth-First Search)** - busca em profundidade ✅
  - [x] Implementação completa com 106 linhas ✅
  - [x] Classificar arestas (árvore, retorno, avanço, cruzamento) ✅
  - [x] Detectar ciclos (grafos não-direcionados) ✅
  - [x] Timestamps de descoberta e finalização ✅
  - [x] Identificar componentes conexos ✅
  - [x] Método helper `busca_em_profundidade()` na classe Grafo ✅
  - [x] 11 testes unitários passando ✅
  - [x] Integração com CLI ✅
  - [x] Gerar saída JSON: `percurso_dfs_<origem>.json` ✅


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
- [x] Integração com BFS (`--alg BFS --source <origem>`) ✅
- [x] Integração com DFS (`--alg DFS --source <origem>`) ✅
- [x] Integração com algoritmos Dijkstra/Bellman-Ford ✅

### Visualizações
- [ ] ⚠️ **NÃO IMPLEMENTADO - REMOVIDO DO ESCOPO ATUAL**
- [ ] Arquivos criados mas não testados nem funcionais
- [ ] Será implementado posteriormente se houver tempo

---

## ❌ NÃO INICIADO

### Parte 1 - Algoritmos de Percurso e Caminhos

#### BFS (Breadth-First Search)
- [x] Implementação completa em `src/graphs/algorithms.py` ✅
- [x] Adaptar para retornar níveis/distâncias ✅
- [x] Retornar árvore de percurso completa ✅
- [x] Gerar saída JSON: `percurso_bfs_<origem>.json` ✅
- [x] Testar com origem específica (ex: "nova descoberta") ✅
- [x] Testes unitários (9 testes implementados) ✅
- [x] Integração com CLI (`--alg BFS --source <origem>`) ✅

#### DFS (Depth-First Search)
- [x] Implementar algoritmo completo em `src/graphs/algorithms.py` ✅
- [x] Classificar arestas (árvore, retorno, avanço, cruzamento) ✅
- [x] Detectar ciclos no grafo ✅
- [x] Retornar ordem de descoberta/finalização (timestamps) ✅
- [x] Gerar saída JSON: `percurso_dfs_<origem>.json` ✅
- [x] 11 testes unitários passando ✅
- [x] Integração com CLI (`--alg DFS --source <origem>`) ✅

#### Dijkstra
- [x] Implementar em `src/graphs/algorithms.py` ✅
- [x] Validar pesos não-negativos ✅
- [x] Calcular menor caminho origem → destino ✅
- [x] Retornar distância total e caminho ✅
- [x] Método helper na classe Grafo: `caminho_mais_curto_dijkstra()` ✅
- [x] 12 testes unitários passando ✅
- [x] Integrar no CLI com argumentos `--source` e `--target` ✅
- [x] Gerar saída JSON: `caminho_dijkstra.json` ✅
- [x] Caso de uso específico: Nova Descoberta → Boa Viagem ✅
- [x] Gerar `percurso_nova_descoberta_setubal.json` (OBRIGATÓRIO no PDF) ✅

#### Bellman-Ford
- [x] Implementar em `src/graphs/algorithms.py` ✅
- [x] Suportar pesos negativos ✅
- [x] Detectar ciclos negativos ✅
- [x] Calcular menor caminho origem → destino ✅
- [x] Retornar distância e caminho ✅
- [x] Método helper na classe Grafo: `caminho_mais_curto_bellman_ford()` ✅
- [x] Retornar todas as distâncias (quando destino = None) ✅
- [x] 14 testes unitários passando ✅
- [x] Integrar no CLI ✅
- [x] Gerar saída JSON: `caminho_bellman_ford.json` ✅

#### Outputs Obrigatórios de Algoritmos (conforme PDF)
- [x] `percurso_nova_descoberta_setubal.json` (Dijkstra - OBRIGATÓRIO) ✅
- [ ] `distancias_enderecos.csv` (matriz de distâncias entre bairros)
- [x] JSON com resultado de BFS: `percurso_bfs_nova_descoberta.json` ✅
- [ ] JSON com resultado de DFS
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
- [x] Implementar `tests/test_bell_manford.py` ✅
- [x] Validar menor caminho com pesos positivos ✅
- [x] Testar detecção de ciclo negativo ✅
- [x] Comparar com Dijkstra em grafo positivo ✅
- [x] Testar retorno de todas as distâncias ✅
- [x] Testar com grafo real dos bairros ✅
- [x] Validar caminhos múltiplos ✅
- [x] **14 testes passando** ✅

#### Testes BFS
- [x] Implementar `tests/test_bfs.py` ✅
- [x] Testar em grafo pequeno conhecido ✅
- [x] Validar níveis corretos a partir da origem ✅
- [x] Testar bairro inalcançável ✅
- [x] Verificar árvore de percurso (predecessores) ✅
- [x] Testar com grafo real dos bairros ✅
- [x] Testar caminho Nova Descoberta → Boa Viagem ✅
- [x] **9 testes passando** ✅

#### Testes DFS
- [x] Implementar `tests/test_dfs.py` ✅
- [x] Validar classificação de arestas ✅
- [x] Testar detecção de ciclos ✅
- [x] Verificar ordem de descoberta e finalização ✅
- [x] Testar em grafo pequeno e no grafo real ✅
- [x] **11 testes passando** ✅

#### Executar Suite de Testes
- [x] Comando: `pytest tests/` ✅
- [x] **46/46 testes passando** (Dijkstra + Bellman-Ford + BFS + DFS) ✅
- [x] Configuração pytest.ini ✅
- [x] Testes para BFS (9 testes implementados e passando) ✅
- [x] Testes para DFS (11 testes implementados e passando) ✅
- [ ] Adicionar testes para DFS (0 testes atualmente)
- [ ] Meta: 100% de cobertura dos 4 algoritmos principais

### Visualizações Finais
⚠️ **REMOVIDO DO ESCOPO ATUAL**

### Relatório Final (PDF)
(Seções do relatório omitidas por brevidade)

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
- [x] `percurso_bfs_nova_descoberta.json` ✅
- [x] `percurso_nova_descoberta_setubal.json` ✅ (OBRIGATÓRIO)
- [ ] `distancias_enderecos.csv` ❌
- [ ] JSON com resultado DFS ❌
- [ ] ⚠️ HTMLs de visualização removidos do escopo atual

#### Validação Final
- [x] Executar `python3 -m src.cli --metricas` → OK ✅
- [x] Executar `python3 -m src.cli --alg BFS --source "nova descoberta"` → OK ✅
- [x] Executar `python3 -m src.cli --alg BFS --source "nova descoberta" --target "boa viagem"` → OK ✅
- [ ] Executar `python3 -m src.cli --alg DFS --source "nova descoberta"` → Pendente
- [x] Executar `python3 -m src.cli --alg DIJKSTRA --source "nova descoberta" --target "boa viagem"` → OK ✅
- [x] Executar `python3 -m src.cli --alg BELLMAN_FORD --source "nova descoberta" --target "boa viagem"` → OK ✅
- [x] Executar `pytest tests/` → 35/35 passando ✅
- [ ] Verificar todos os JSONs/CSVs obrigatórios gerados
- [ ] Ler PDF do relatório

#### GitHub
- [ ] Push final do código
- [ ] Tag de versão: `v1.0`
- [ ] README.md atualizado
- [ ] .gitignore configurado (venv/, __pycache__, *.pyc)

---

## 📊 ANÁLISE DETALHADA POR REQUISITO DO PDF

### Parte 1: Implementação dos Algoritmos (5.0 pontos)

| Algoritmo | Status | Implementação | Testes | CLI | Output JSON | Pontos Estimados |
|-----------|--------|---------------|--------|-----|-------------|------------------|
| **BFS** | ✅ Completo | ✅ | ✅ 9 testes | ✅ | ✅ | 1.25/1.25 |
| **DFS** | ❌ Não feito | ❌ | ❌ 0 testes | ❌ | ❌ | 0.0/1.25 |
| **Dijkstra** | ✅ Completo | ✅ | ✅ 12 testes | ✅ | ✅ | 1.25/1.25 |
| **Bellman-Ford** | ✅ Completo | ✅ | ✅ 14 testes | ✅ | ✅ | 1.25/1.25 |
| **Integração** | ⚠️ Parcial | ✅ | - | ✅ | ⚠️ | 0.5/0.75 |

**Subtotal Parte 1:** ~4.25/5.0 pontos

### Parte 2: Dataset Adicional (3.0 pontos)

| Item | Status | Pontos |
|------|--------|--------|
| Processar segundo dataset | ❌ | 0.0/1.0 |
| Executar algoritmos | ❌ | 0.0/1.0 |
| Comparar resultados | ❌ | 0.0/0.5 |
| Análise de performance | ❌ | 0.0/0.5 |

**Subtotal Parte 2:** 0.0/3.0 pontos

### Parte 3: Testes Unitários (2.0 pontos)

| Item | Status | Pontos |
|------|--------|--------|
| Infraestrutura de testes | ✅ | 0.3/0.3 |
| Testes BFS | ✅ 9 testes | 0.4/0.4 |
| Testes DFS | ❌ 0 testes | 0.0/0.4 |
| Testes Dijkstra | ✅ 12 testes | 0.5/0.5 |
| Testes Bellman-Ford | ✅ 14 testes | 0.5/0.5 |
| Coverage > 80% | ⚠️ ~75% | 0.0/0.4 |

**Subtotal Parte 3:** 1.7/2.0 pontos

### 📁 Arquivos Obrigatórios (Conforme PDF)

**Gerados ✅:**
- ✅ `recife_global.json`
- ✅ `microrregioes.json`
- ✅ `ego_bairro.csv`
- ✅ `graus.csv`
- ✅ `rankings.json`
- ✅ `percurso_bfs_nova_descoberta.json`
- ✅ `percurso_nova_descoberta_setubal.json` **(OBRIGATÓRIO)**
- ✅ `caminho_bellman_ford_*.json`

**Faltando ❌:**
- ❌ `percurso_dfs_*.json`
- ❌ `distancias_enderecos.csv`
- ❌ Relatório final (PDF)

### 🎯 Prioridades para Atingir Cada Nota

**Para 6.0 (Nota Mínima):**
- Implementar DFS básico sem classificação de arestas
- Adicionar 5-6 testes simples
- Gerar JSON de saída
- **Tempo:** 4-5 horas

**Para 7.0-7.5 (Nota Boa):**
- Implementar DFS completo com classificação
- Adicionar 8-10 testes robustos
- Gerar matriz de distâncias
- **Tempo:** 8-11 horas

**Para 9.0-10.0 (Nota Excelente):**
- Todo o anterior +
- Processar Parte 2 (dataset adicional)
- Escrever relatório PDF
- Adicionar análises comparativas
- **Tempo:** 20-30 horas

---

## 📊 PROGRESSO GERAL (ATUALIZADO E CORRIGIDO)

### Por Categoria
- **Estrutura do Projeto:** 100% ✅
- **Carregamento de Dados:** 100% ✅
- **Grafo e Métricas:** 100% ✅
- **Algoritmos:** 100% ✅ (Dijkstra + Bellman-Ford + BFS + DFS completos)
- **Testes:** 90% ✅ (46 testes: 12 Dijkstra + 14 Bellman-Ford + 9 BFS + 11 DFS)
- **CLI Básico:** 100% ✅
- **Integração CLI + Algoritmos:** 100% ✅ (Dijkstra/Bellman-Ford/BFS/DFS integrados e funcionando)
- **Outputs Obrigatórios:** 90% ✅ (métricas + BFS + Dijkstra + Bellman-Ford + DFS OK, falta apenas matriz)
- **Visualizações:** 0% ❌ (removido do escopo atual)
- **Relatório:** 0% ❌

### Por Pontuação (Base: 10.0 pontos - estimativa conservadora)
- **Parte 1 (5.0 pts):** ~95% (4.75/5.0)
  - Dijkstra: OK (implementação + testes + CLI + output) ✅
  - Bellman-Ford: OK (implementação + testes + CLI) ✅
  - BFS: OK (implementação + testes + CLI + output) ✅
  - DFS: OK (implementação + testes + CLI + output) ✅
  - Integração CLI: Completa ✅
  - Outputs obrigatórios: Completos (falta apenas matriz de distâncias) ⚠️

- **Parte 2 (3.0 pts):** 0% (0/3.0) - Dataset adicional não iniciado ❌
- **Testes (2.0 pts):** 90% (1.8/2.0) - Dijkstra + Bellman-Ford + BFS + DFS completos ✅
- **Bônus Visualizações (+1.0 pt):** 0% (0/1.0) - Removido do escopo ❌

**Total Estimado Conservador:** ~6.5/10.0 pontos
**Total Otimista (se completar matriz):** ~7.0/10.0 pontos

---

## 🎯 PRÓXIMOS PASSOS PRIORITÁRIOS

### CRÍTICO - Para Pontuação Básica (Curto Prazo)
1. ~~Implementar Dijkstra~~ ✅ COMPLETO
2. ~~Implementar Bellman-Ford~~ ✅ COMPLETO
3. ~~Testes Dijkstra~~ ✅ COMPLETO
4. ~~Testes Bellman-Ford~~ ✅ COMPLETO
5. ~~Completar BFS~~ ✅ COMPLETO
6. ~~Testes BFS~~ ✅ COMPLETO
7. ~~Integrar BFS no CLI~~ ✅ COMPLETO
8. **Implementar DFS completo** - com classificação de arestas ⚠️ URGENTE
9. ~~Integrar Dijkstra no CLI~~ ✅ CONCLUÍDO
10. ~~Integrar Bellman-Ford no CLI~~ ✅ CONCLUÍDO
11. **Integrar DFS no CLI** ⚠️ URGENTE
12. ~~Gerar `percurso_nova_descoberta_setubal.json`~~ ✅ CONCLUÍDO

### IMPORTANTE - Para Completar Requisitos (Médio Prazo)
13. Criar testes unitários para DFS completo
14. Gerar `distancias_enderecos.csv` (matriz de distâncias)
15. Gerar JSONs de resultados para Bellman-Ford (Dijkstra já está feito)
16. Executar suite completa de testes (meta: 40+ testes)
17. Processar Parte 2 (dataset adicional, se fornecido)

---

## 📝 NOTAS IMPORTANTES

### Pontos Fortes do Projeto
1. ✅ **Código bem estruturado** - Classes, separação de responsabilidades
2. ✅ **Testes abrangentes** - 35 testes para 3 algoritmos  
3. ✅ **CLI funcional** - Interface completa e bem documentada
4. ✅ **Output obrigatório principal** - `percurso_nova_descoberta_setubal.json` presente
5. ✅ **Documentação completa** - README.md criado

### Pontos Fracos / Bloqueadores
1. ❌ **DFS ausente** - Único algoritmo obrigatório não implementado (~1.5 pontos perdidos)
2. ❌ **Parte 2 não iniciada** - Dataset adicional (~3.0 pontos perdidos)
3. ❌ **Matriz de distâncias faltando** - Output importante ausente
4. ❌ **Sem relatório PDF** - Documentação final não escrita

### Dados do Grafo
- **Dados:** 94 bairros, 245 conexões, densidade 0.056
- **Bairros isolados:** Cabanga, São José (0 arestas)
- **Externos ignorados:** Aldeia, Oitinga (não são Recife)
- **Top bairro (grau):** Casa Amarela (11 conexões)
- **Top bairro (densidade ego):** Brasília Teimosa (1.0)

### Comandos Funcionais
- ✅ `python3 -m src.cli --dataset ./data/bairros_recife.csv --metricas --out ./out/`
- ✅ `python3 -m src.cli --alg BFS --source "nova descoberta" --out ./out/`
- ✅ `python3 -m src.cli --alg DIJKSTRA --source "nova descoberta" --target "boa viagem" --out ./out/`
- ✅ `python3 -m src.cli --alg BELLMAN_FORD --source "nova descoberta" --target "boa viagem" --out ./out/`
- ❌ Comandos com DFS ainda não funcionam

### Status dos Algoritmos (Conforme PDF)
- **Dijkstra:** ✅ Completo (implementação + 12 testes + CLI + JSON)
- **Bellman-Ford:** ✅ Completo (implementação + 14 testes + CLI + JSON)
- **BFS:** ✅ Completo (implementação + 9 testes + CLI + JSON)
- **DFS:** ❌ Apenas stub vazio (precisa implementar do zero)

---

## ⏰ ESTIMATIVA DE TEMPO (ATUALIZADO)

### Já Completo (~20-26 horas)
- ✅ Implementar Dijkstra, Bellman-Ford e BFS
- ✅ Criar testes (35 testes no total)
- ✅ Integrar Dijkstra, Bellman-Ford e BFS ao CLI
- ✅ Gerar outputs obrigatórios de Dijkstra e BFS
- ✅ Corrigir todos os bugs de carregamento de dados e testes

### Trabalho Restante Crítico
- Implementar DFS completo: **3-4 horas** ⚠️ URGENTE
- Integrar DFS no CLI: **1 hora** ⚠️ URGENTE
- Criar testes DFS: **2-3 horas**
- Criar matriz de distâncias (`distancias_enderecos.csv`): **2-3 horas**
- Gerar JSON de saída para Bellman-Ford (o CLI já funciona, só falta o arquivo): **0.5 horas**
- **Subtotal Crítico:** ~8.5-14.5 horas

### Trabalho Restante Opcional
- Parte 2 (dataset adicional): **4-6 horas**
- Escrever relatório PDF: **6-8 horas**
- Implementar visualizações: **4-6 horas**
- Revisão final e validação: **2-3 horas**
- **Subtotal Opcional:** ~16-23 horas

**TOTAL RESTANTE (Mínimo Crítico):** ~8.5-14.5 horas
**TOTAL RESTANTE (Completo):** ~24.5-37.5 horas

---

**Última atualização:** 17 de novembro de 2025 - Pull do amigo integrado com sucesso! Dijkstra/Bellman-Ford agora totalmente integrados ao CLI. Todos testes (35/35) passando sem conflitos ✅