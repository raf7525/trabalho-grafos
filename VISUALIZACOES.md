# Visualizações Analíticas - Projeto de Grafos

Este documento descreve as 5 visualizações analíticas geradas para o projeto de análise de grafos dos bairros de Recife.

## Como Gerar as Visualizações

### Opção 1: Via CLI (Recomendado)
```bash
python src/cli.py --viz
```

### Opção 2: Executar diretamente o módulo viz.py
```bash
python src/viz.py
```

## Visualizações Geradas

### 1. Mapa de Cores por Grau dos Bairros
**Arquivo:** `out/viz_mapa_cores_grau.png`

Gráfico de barras horizontal onde cada bairro é colorido de acordo com seu grau (número de conexões). 
- **Cores mais intensas** (vermelho/laranja) = mais conexões
- **Cores mais claras** (amarelo) = menos conexões

**Função:** `visualizar_mapa_cores_grau()`

### 2. Ranking de Densidade por Microrregião
**Arquivo:** `out/viz_densidade_microrregiao.png`

Gráfico de barras mostrando a densidade média de ego-subrede para cada microrregião (RPA).
- Cada barra representa uma RPA (Região Político-Administrativa)
- A altura indica a densidade média das ego-redes dos bairros daquela região
- Cores diferenciadas para melhor visualização

**Função:** `visualizar_densidade_por_microrregiao()`

### 3. Subgrafo dos Top 10 Bairros
**Arquivo:** `out/viz_subgrafo_top10.html` (Visualização Interativa)

Visualização interativa em HTML dos 10 bairros com maior grau e seus vizinhos.
- **Nós vermelhos** = Top 10 bairros com maior grau
- **Nós azuis** = Vizinhos diretos
- **Tamanho dos nós** = Proporcional ao grau
- **Interativo:** Permite zoom, arrastar nós, e visualizar informações ao passar o mouse

**Função:** `visualizar_subgrafo_top10()`

**Como abrir:** Clique duas vezes no arquivo HTML ou abra no navegador

### 4. Distribuição dos Graus (Histograma)
**Arquivo:** `out/viz_distribuicao_graus.png`

Histograma mostrando a distribuição de frequência dos graus dos bairros.
- **Eixo X:** Grau (número de conexões)
- **Eixo Y:** Frequência (quantos bairros têm aquele grau)
- Inclui estatísticas: média, mediana, mínimo e máximo
- Cores gradientes do azul claro ao escuro

**Função:** `visualizar_distribuicao_graus()`

### 5. Árvore BFS a partir de Boa Vista
**Arquivo:** `out/viz_arvore_bfs_boa_vista.html` (Visualização Interativa)

Visualização hierárquica da árvore de busca em largura (BFS) partindo do bairro "Boa Vista".
- **Layout hierárquico** com níveis bem definidos
- **Cores do arco-íris** representam diferentes níveis da árvore
- **Setas direcionadas** mostram a direção do percurso
- Mostra claramente as "camadas" de distância a partir da origem

**Função:** `visualizar_arvore_bfs()`

**Como abrir:** Clique duas vezes no arquivo HTML ou abra no navegador

## Dependências Necessárias

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

As principais bibliotecas usadas:
- `matplotlib` - Para gráficos estáticos (1, 2, 4)
- `pyvis` - Para visualizações interativas de grafos (3, 5)
- `pandas` - Para manipulação de dados
- `numpy` - Para operações numéricas

## Estrutura de Saída

Todos os arquivos serão salvos no diretório `out/`:

```
out/
├── viz_mapa_cores_grau.png              # Visualização 1
├── viz_densidade_microrregiao.png       # Visualização 2
├── viz_subgrafo_top10.html              # Visualização 3
├── viz_distribuicao_graus.png           # Visualização 4
└── viz_arvore_bfs_boa_vista.html        # Visualização 5
```

## Personalização

Você pode modificar os parâmetros das visualizações editando o arquivo `src/viz.py`:

### Exemplo: Mudar a origem da árvore BFS
```python
# No final do arquivo viz.py, linha ~332
visualizar_arvore_bfs(grafo, origem="recife")  # Mude para qualquer bairro
```

### Exemplo: Mudar o número de bairros no subgrafo
```python
# Na função visualizar_subgrafo_top10(), linha ~130
top10_bairros = df.head(15)["bairro"].tolist()  # Mude 10 para 15
```

## Análises Possíveis

Com essas visualizações você pode:

1. **Identificar hubs** - Bairros com maior conectividade (visualização 1 e 3)
2. **Comparar regiões** - Qual RPA tem bairros mais conectados (visualização 2)
3. **Entender a topologia** - Como o grafo está estruturado (visualização 3 e 5)
4. **Análise estatística** - Distribuição das conexões segue algum padrão? (visualização 4)
5. **Distâncias e alcance** - Quantos "saltos" para chegar a todos os bairros (visualização 5)

## Troubleshooting

### Erro: "Module 'pyvis' not found"
```bash
pip install pyvis
```

### Erro: "Module 'matplotlib' not found"
```bash
pip install matplotlib
```

### Arquivos HTML não abrem corretamente
- Certifique-se de que está abrindo no navegador (Chrome, Firefox, Edge)
- Verifique se os arquivos foram gerados sem erros
- Tente dar refresh (F5) na página

### Gráficos aparecem vazios
- Verifique se os dados foram carregados corretamente
- Confira se os arquivos CSV estão no diretório `data/`
- Execute primeiro `python src/cli.py --metricas` para gerar os dados base

## Contato e Suporte

Para dúvidas ou problemas, verifique:
1. Os logs de execução no terminal
2. Se todos os arquivos de dados estão presentes
3. Se as dependências estão instaladas corretamente
