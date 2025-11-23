# Exemplos de Uso do CLI

## 🎯 Parte 1 - Bairros do Recife

### Calcular Métricas
```bash
python -m src.cli --dataset data/bairros_vizinhos_tratados.csv --metricas
```

### Gerar Visualizações
```bash
python -m src.cli --dataset data/bairros_vizinhos_tratados.csv --viz
```

### Executar Algoritmos

**BFS:**
```bash
python -m src.cli --dataset data/bairros_vizinhos_tratados.csv --alg BFS --source "Boa Viagem"
```

**DFS:**
```bash
python -m src.cli --dataset data/bairros_vizinhos_tratados.csv --alg DFS --source "Boa Vista"
```

**Dijkstra:**
```bash
python -m src.cli --dataset data/bairros_vizinhos_tratados.csv --alg DIJKSTRA --source "Nova Descoberta" --target "Boa Viagem"
```

**Bellman-Ford:**
```bash
python -m src.cli --dataset data/bairros_vizinhos_tratados.csv --alg BELLMAN_FORD --source "Nova Descoberta" --target "Boa Viagem"
```

---

## ✈️ Parte 2 - Aeroportos

### Análise Completa (Recomendado)
Executa todos os benchmarks e gera visualizações automaticamente:
```bash
python -m src.cli --parte2 --dataset data/dataset_parte2/Airports_2008_2009_200k.csv --out out/
```

Ou usando o caminho padrão:
```bash
python -m src.cli --parte2 --out out/
```

### Executar Algoritmo Específico

**BFS:**
```bash
python -m src.cli --dataset data/dataset_parte2/Airports_2008_2009_200k.csv --alg BFS --source ATL --out out/
```

**DFS:**
```bash
python -m src.cli --dataset data/dataset_parte2/Airports_2008_2009_200k.csv --alg DFS --source JFK --out out/
```

**Dijkstra:**
```bash
python -m src.cli --dataset data/dataset_parte2/Airports_2008_2009_200k.csv --alg DIJKSTRA --source SEA --target RDM --out out/
```

**Bellman-Ford:**
```bash
python -m src.cli --dataset data/dataset_parte2/Airports_2008_2009_200k.csv --alg BELLMAN_FORD --source JFK --target LAX --out out/
```

---

## 📊 Outputs Gerados

### Parte 1
- `out/recife_global.json` - Métricas globais
- `out/microrregioes.json` - Métricas por microrregião
- `out/ego_bairro.csv` - Métricas de ego-rede
- `out/graus.csv` - Graus de cada bairro
- `out/rankings.json` - Rankings (mais denso, maior grau)
- `out/percurso_*.json` - Resultados de algoritmos
- `out/viz_*.png` - Visualizações estáticas
- `out/viz_*.html` - Visualizações interativas

### Parte 2
- `out/parte2_report.json` - Relatório completo de benchmarks
- `out/parte2_distribuicao_graus.png` - Histograma de graus
- `out/parte2_comparacao_performance.png` - Comparação de performance

---

## 🔍 Detecção Automática

O CLI detecta automaticamente se você está usando Parte 1 ou Parte 2 baseado no nome do dataset:

- Se contiver **"airport"** ou **"aeroporto"** → Parte 2 (não normaliza nomes)
- Caso contrário → Parte 1 (normaliza nomes de bairros)

---

## 💡 Dicas

1. **Sempre especifique `--out`** para controlar onde os arquivos são salvos
2. **Use `--parte2`** para executar a análise completa da Parte 2 (inclui testes de ciclos negativos)
3. **Use `--alg`** para executar algoritmos individuais (mais rápido para testes)
4. **Para Parte 1**, os nomes são normalizados automaticamente (ex: "Boa Viagem" → "boa viagem")
5. **Para Parte 2**, use códigos IATA exatos (ex: "ATL", "JFK", "LAX")
