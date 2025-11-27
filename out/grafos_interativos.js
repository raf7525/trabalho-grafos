let network = null;
let nodesDataSet = null;
let edgesDataSet = null;
let datasetAtual = 'recife';
let allNodesData = [];
let nameToIdMap = {}; 

const VISUAL_STYLE = {
    node: {
        base: { background: '#374151', border: '#6b7280' },
        highlight: { background: '#06b6d4', border: '#ffffff' },
        hover: { background: '#3b82f6', border: '#ffffff' },
        font: { face: 'Inter', color: '#ffffff', size: 14, strokeWidth: 4, strokeColor: '#020617' }
    },
    edge: {
        base: { color: '#4b5563', opacity: 0.3 },
        highlight: { color: '#22d3ee', opacity: 1.0 }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    carregarGrafo('recife');
    atualizarInputsAlgoritmo();
});

function atualizarInputsAlgoritmo() {
    const alg = document.getElementById('algoritmo').value;
    const containerDestino = document.getElementById('container-destino');
    const descAlg = document.getElementById('desc-algoritmo');
    
    const algoritmosExpansao = ['bfs', 'dfs'];
    
    if (algoritmosExpansao.includes(alg)) {
        containerDestino.style.opacity = '0';
        containerDestino.style.height = '0';
        containerDestino.style.marginTop = '0';
        document.getElementById('destino').value = '';
        
        if (alg === 'bfs') descAlg.textContent = "Expansão em camadas (Níveis).";
        if (alg === 'dfs') descAlg.textContent = "Exploração profunda (Ordem).";
    } else {
        containerDestino.style.opacity = '1';
        containerDestino.style.height = 'auto';
        containerDestino.style.marginTop = '16px';
        if (alg === 'dijkstra') descAlg.textContent = "Menor custo (pesos positivos).";
        if (alg === 'bellman') descAlg.textContent = "Caminho (suporta pesos negativos).";
    }
}

function mudarDataset() {
    const select = document.getElementById('select-dataset');
    datasetAtual = select.value;
    carregarGrafo(datasetAtual);
}

async function carregarGrafo(tipo) {
    const loading = document.getElementById('loading');
    if(loading) loading.style.display = 'flex';
    
    const arquivo = tipo === 'usa' ? 'grafo_usa.json' : 'grafo_dados.json';
    
    try {
        const response = await fetch(arquivo);
        if (!response.ok) throw new Error("Erro ao carregar JSON");
        const data = await response.json();
        data.nodes.forEach(node => {
            if (node.title) {
                const container = document.createElement('div');
                container.innerHTML = node.title;
                node.title = container;
            }
        });
        
        inicializarVis(data);
        construirIndiceBusca(data.nodes);
        atualizarDatalist(data.nodes);
        
        document.getElementById('origem').value = '';
        document.getElementById('destino').value = '';
        document.getElementById('info-panel').classList.add('hidden');
        
    } catch (error) {
        console.error(error);
        alert(`Erro ao carregar: ${error.message}`);
    } finally {
        if(loading) loading.style.display = 'none';
    }
}

function construirIndiceBusca(nodes) {
    nameToIdMap = {};
    nodes.forEach(n => {
        if (n.original_title) {
            nameToIdMap[n.original_title.toLowerCase()] = n.id;
            nameToIdMap[normalizarTexto(n.original_title)] = n.id;
        }
        nameToIdMap[n.id.toLowerCase()] = n.id;
        nameToIdMap[n.label.toLowerCase()] = n.id;
    });
}

function normalizarTexto(texto) {
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

function resolverId(inputVal) {
    if (!inputVal) return null;
    const valLower = inputVal.toLowerCase().trim();
    const valNorm = normalizarTexto(inputVal);
    return nameToIdMap[valLower] || nameToIdMap[valNorm] || (allNodesData.find(n => n.id === inputVal) ? inputVal : null);
}

function inicializarVis(data) {
    const container = document.getElementById('mynetwork');
    
    nodesDataSet = new vis.DataSet(data.nodes);
    edgesDataSet = new vis.DataSet(data.edges);
    allNodesData = data.nodes;

    const options = {
        nodes: {
            shape: 'dot',
            font: VISUAL_STYLE.node.font,
            borderWidth: 2,
            color: {
                background: VISUAL_STYLE.node.base.background,
                border: VISUAL_STYLE.node.base.border,
                highlight: VISUAL_STYLE.node.highlight,
                hover: VISUAL_STYLE.node.hover
            },
            shadow: { enabled: true, color: 'rgba(0,0,0,0.5)' }
        },
        edges: {
            color: { 
                color: VISUAL_STYLE.edge.base.color, 
                opacity: VISUAL_STYLE.edge.base.opacity,
                highlight: VISUAL_STYLE.edge.highlight.color 
            },
            smooth: { type: 'continuous', roundness: 0.5 },
            arrows: datasetAtual === 'usa' ? 'to' : undefined,
            width: 1,
            selectionWidth: 3
        },
        physics: {
            stabilization: true,
            barnesHut: {
                gravitationalConstant: -8000,
                centralGravity: 0.3,
                springLength: 200,
                springConstant: 0.01,
                damping: 0.09
            }
        },
        interaction: { hover: true, tooltipDelay: 100, hideEdgesOnDrag: true }
    };

    if (network) network.destroy();
    network = new vis.Network(container, { nodes: nodesDataSet, edges: edgesDataSet }, options);
    
    network.on("click", function (params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const nodeObj = allNodesData.find(n => n.id === nodeId);
            const nomeBonito = nodeObj.original_title || nodeObj.label; 

            const origemInput = document.getElementById('origem');
            const destinoInput = document.getElementById('destino');
            const alg = document.getElementById('algoritmo').value;
            
            if (!origemInput.value) {
                origemInput.value = nomeBonito;
            } else {
                if (['bfs', 'dfs'].includes(alg)) {
                    origemInput.value = nomeBonito;
                } else {
                    if (!destinoInput.value && origemInput.value !== nomeBonito) {
                        destinoInput.value = nomeBonito;
                    } else {
                        origemInput.value = nomeBonito;
                        destinoInput.value = '';
                    }
                }
            }
        }
    });
}

function atualizarDatalist(nodes) {
    const datalist = document.getElementById('lista-bairros');
    if(!datalist) return;
    datalist.innerHTML = '';
    const sortedNodes = [...nodes].sort((a, b) => {
        const nomeA = a.original_title || a.label;
        const nomeB = b.original_title || b.label;
        return nomeA.localeCompare(nomeB);
    });
    
    sortedNodes.forEach(node => {
        const option = document.createElement('option');
        option.value = node.original_title || node.label; 
        datalist.appendChild(option);
    });
}

async function NovaDescobertaAteSetubal() {
    const origem = 'Nova Descoberta'
    const destino = 'Boa Viagem'
    const alg = 'dijkstra'

    const origemId = resolverId(origem);
    const destinoId = resolverId(destino);

    const url = `/api/calcular?alg=${alg}&origem=${encodeURIComponent(origemId)}&destino=${encodeURIComponent(destinoId || '')}&dataset=${datasetAtual}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        if (data.erro) return alert(data.erro);

        nodesDataSet.update(allNodesData.map(n => ({
            id: n.id, 
            color: { 
                background: '#1f2937', border: '#374151',
                highlight: VISUAL_STYLE.node.highlight,
                hover: VISUAL_STYLE.node.hover
            },
            size: n.value ? 15 : 10,
            font: { color: '#4b5563', strokeWidth: 0 }
        })));
        
        edgesDataSet.update(edgesDataSet.getIds().map(id => ({
            id: id, 
            color: {color: '#1f2937', opacity: 0.05}, 
            width: 1
        })));

        const panel = document.getElementById('info-panel');
        const content = document.getElementById('result-content');
        
        if (data.tipo === 'caminho') {
            destacarCaminho(data.caminho);
            content.innerHTML = `
                <div class="flex justify-between items-end mb-2">
                    <span class="text-gray-400 text-xs uppercase tracking-wide">Algoritmo</span>
                    <span class="font-mono text-indigo-400 font-bold text-sm">${data.algoritmo}</span>
                </div>
                <div class="grid grid-cols-2 gap-2 mb-3">
                    <div class="bg-gray-800 p-2 rounded border border-gray-700 text-center">
                        <div class="text-xs text-gray-500">Custo</div>
                        <div class="font-bold text-green-400 text-lg">${Number(data.custo).toFixed(1)}</div>
                    </div>
                    <div class="bg-gray-800 p-2 rounded border border-gray-700 text-center">
                        <div class="text-xs text-gray-500">Saltos</div>
                        <div class="font-bold text-white text-lg">${data.caminho.length - 1}</div>
                    </div>
                </div>
                <div class="pt-3 border-t border-gray-700">
                    <p class="text-xs text-gray-500 mb-2">Trajeto:</p>
                    <div class="max-h-40 overflow-y-auto text-xs text-indigo-200 leading-loose custom-scrollbar bg-gray-800/50 p-2 rounded border border-gray-700">
                        ${data.caminho.join(' <br><i class="fas fa-arrow-down text-gray-600 mx-auto block w-min my-1"></i> ')}
                    </div>
                </div>
            `;
        } else if (data.tipo === 'expansao') {
            colorirExpansao(data.dados_nos, data.metrica);
            const nomeMetrica = data.metrica || 'Níveis';
            
            content.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <span class="font-bold text-white uppercase text-sm tracking-wider">${data.algoritmo}</span>
                    <span class="text-xs bg-indigo-900 text-indigo-200 px-2 py-1 rounded-full border border-indigo-700 font-mono">
                        ${Object.keys(data.dados_nos).length} nós
                    </span>
                </div>
                
                <div class="bg-gray-800 p-3 rounded-lg border border-gray-700">
                    <div class="flex justify-between text-[10px] text-gray-400 mb-1 uppercase font-bold tracking-wider">
                        <span>Início</span>
                        <span>Fim</span>
                    </div>
                    <div class="gradient-bar"></div>
                    <div class="flex justify-between text-[10px] text-gray-500 font-mono">
                        <span>0</span>
                        <span>Max</span>
                    </div>
                </div>
                
                <div class="mt-4 pt-3 border-t border-gray-700 text-xs text-gray-400 space-y-2">
                    <div class="flex items-center gap-2">
                        <div style="width: 12px; height: 12px; background: #3b82f6; border: 2px solid white; border-radius: 50%;"></div> 
                        <span>Origem da Busca</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <div style="width: 12px; height: 12px; background: #ef4444; border-radius: 50%;"></div> 
                        <span>Últimos Visitados</span>
                    </div>
                </div>
                
                <div class="mt-3 text-center">
                    <span class="text-[10px] text-gray-600 uppercase tracking-widest">Métrica: ${nomeMetrica}</span>
                </div>
            `;
        }
        if(panel) panel.classList.remove('hidden');

    } catch (e) {
        console.error(e);
        alert("Erro na API.");
    }
}

async function calcularRota() {
    const origemRaw = document.getElementById('origem').value;
    const destinoRaw = document.getElementById('destino').value;
    const alg = document.getElementById('algoritmo').value;

    const origemId = resolverId(origemRaw);
    const destinoId = resolverId(destinoRaw);

    if (!origemId) return alert("Ponto de origem não encontrado!");
    if (!['bfs', 'dfs'].includes(alg) && !destinoId) return alert("Ponto de destino não encontrado!");

    const url = `/api/calcular?alg=${alg}&origem=${encodeURIComponent(origemId)}&destino=${encodeURIComponent(destinoId || '')}&dataset=${datasetAtual}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        if (data.erro) return alert(data.erro);

        nodesDataSet.update(allNodesData.map(n => ({
            id: n.id, 
            color: { 
                background: '#1f2937', border: '#374151',
                highlight: VISUAL_STYLE.node.highlight,
                hover: VISUAL_STYLE.node.hover
            },
            size: n.value ? 15 : 10,
            font: { color: '#4b5563', strokeWidth: 0 }
        })));
        
        edgesDataSet.update(edgesDataSet.getIds().map(id => ({
            id: id, 
            color: {color: '#1f2937', opacity: 0.05}, 
            width: 1
        })));

        const panel = document.getElementById('info-panel');
        const content = document.getElementById('result-content');
        
        if (data.tipo === 'caminho') {
            destacarCaminho(data.caminho);
            content.innerHTML = `
                <div class="flex justify-between items-end mb-2">
                    <span class="text-gray-400 text-xs uppercase tracking-wide">Algoritmo</span>
                    <span class="font-mono text-indigo-400 font-bold text-sm">${data.algoritmo}</span>
                </div>
                <div class="grid grid-cols-2 gap-2 mb-3">
                    <div class="bg-gray-800 p-2 rounded border border-gray-700 text-center">
                        <div class="text-xs text-gray-500">Custo</div>
                        <div class="font-bold text-green-400 text-lg">${Number(data.custo).toFixed(1)}</div>
                    </div>
                    <div class="bg-gray-800 p-2 rounded border border-gray-700 text-center">
                        <div class="text-xs text-gray-500">Saltos</div>
                        <div class="font-bold text-white text-lg">${data.caminho.length - 1}</div>
                    </div>
                </div>
                <div class="pt-3 border-t border-gray-700">
                    <p class="text-xs text-gray-500 mb-2">Trajeto:</p>
                    <div class="max-h-40 overflow-y-auto text-xs text-indigo-200 leading-loose custom-scrollbar bg-gray-800/50 p-2 rounded border border-gray-700">
                        ${data.caminho.join(' <br><i class="fas fa-arrow-down text-gray-600 mx-auto block w-min my-1"></i> ')}
                    </div>
                </div>
            `;
        } else if (data.tipo === 'expansao') {
            colorirExpansao(data.dados_nos, data.metrica);
            const nomeMetrica = data.metrica || 'Níveis';
            
            content.innerHTML = `
                <div class="flex justify-between items-center mb-4">
                    <span class="font-bold text-white uppercase text-sm tracking-wider">${data.algoritmo}</span>
                    <span class="text-xs bg-indigo-900 text-indigo-200 px-2 py-1 rounded-full border border-indigo-700 font-mono">
                        ${Object.keys(data.dados_nos).length} nós
                    </span>
                </div>
                
                <div class="bg-gray-800 p-3 rounded-lg border border-gray-700">
                    <div class="flex justify-between text-[10px] text-gray-400 mb-1 uppercase font-bold tracking-wider">
                        <span>Início</span>
                        <span>Fim</span>
                    </div>
                    <div class="gradient-bar"></div>
                    <div class="flex justify-between text-[10px] text-gray-500 font-mono">
                        <span>0</span>
                        <span>Max</span>
                    </div>
                </div>
                
                <div class="mt-4 pt-3 border-t border-gray-700 text-xs text-gray-400 space-y-2">
                    <div class="flex items-center gap-2">
                        <div style="width: 12px; height: 12px; background: #3b82f6; border: 2px solid white; border-radius: 50%;"></div> 
                        <span>Origem da Busca</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <div style="width: 12px; height: 12px; background: #ef4444; border-radius: 50%;"></div> 
                        <span>Últimos Visitados</span>
                    </div>
                </div>
                
                <div class="mt-3 text-center">
                    <span class="text-[10px] text-gray-600 uppercase tracking-widest">Métrica: ${nomeMetrica}</span>
                </div>
            `;
        }
        if(panel) panel.classList.remove('hidden');

    } catch (e) {
        console.error(e);
        alert("Erro na API.");
    }
}

function destacarCaminho(caminho) {
    const updates = caminho.map((id, index) => ({
        id: id,
        color: { 
            background: index === 0 ? '#10b981' : (index === caminho.length - 1 ? '#ef4444' : '#fbbf24'),
            border: '#ffffff',
            highlight: VISUAL_STYLE.node.highlight,
            hover: VISUAL_STYLE.node.hover
        },
        size: 45,
        font: { color: '#ffffff', size: 16, strokeWidth: 4 },
        borderWidth: 3
    }));
    nodesDataSet.update(updates);

    for (let i = 0; i < caminho.length - 1; i++) {
        const u = caminho[i];
        const v = caminho[i+1];
        const edges = edgesDataSet.get({
            filter: item => (item.from === u && item.to === v) || (datasetAtual === 'recife' && item.from === v && item.to === u)
        });
        if (edges.length > 0) {
            edgesDataSet.update({id: edges[0].id, color: {color: '#fbbf24', opacity: 1}, width: 5});
        }
    }
}

function getHeatmapColor(ratio) {
    const palette = [
        { r: 59,  g: 130, b: 246 }, 
        { r: 6,   g: 182, b: 212 }, 
        { r: 34,  g: 197, b: 94  }, 
        { r: 234, b: 8,   g: 179 }, 
        { r: 239, g: 68,  b: 68  }  
    ];
    const scaled = ratio * (palette.length - 1);
    const idx = Math.floor(scaled);
    const nextIdx = Math.min(idx + 1, palette.length - 1);
    const t = scaled - idx;
    const c1 = palette[idx];
    const c2 = palette[nextIdx];
    const r = Math.floor(c1.r + t * (c2.r - c1.r));
    const g = Math.floor(c1.g + t * (c2.g - c1.g));
    const b = Math.floor(c1.b + t * (c2.b - c1.b));
    return `rgb(${r}, ${g}, ${b})`;
}

function colorirExpansao(dados, tipoMetrica) {
    const valores = Object.entries(dados).filter(([_, v]) => v !== 'inf').map(([id, v]) => ({ id, val: v }));
    if (valores.length === 0) return;

    const vals = valores.map(x => x.val);
    const maxVal = Math.max(...vals);
    const minVal = Math.min(...vals);
    const updates = [];
    
    valores.forEach(item => {
        let ratio = 0;
        if (maxVal !== minVal) {
            ratio = (item.val - minVal) / (maxVal - minVal);
        }
        const color = getHeatmapColor(ratio);
        const isStart = ratio === 0;
        
        updates.push({
            id: item.id,
            color: { 
                background: color, 
                border: isStart ? '#ffffff' : color,
                highlight: VISUAL_STYLE.node.highlight, 
                hover: VISUAL_STYLE.node.hover
            },
            size: isStart ? 50 : 25,
            borderWidth: isStart ? 4 : 1,
            font: { color: '#ffffff', size: 14, strokeWidth: 3 } 
        });
    });
    nodesDataSet.update(updates);
}

function limparRota() {
    carregarGrafo(datasetAtual);
    document.getElementById('info-panel').classList.add('hidden');
    document.getElementById('origem').value = '';
    document.getElementById('destino').value = '';
}