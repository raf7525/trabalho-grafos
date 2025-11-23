let network = null;
let nodesDataset = null;
let edgesDataset = null;
let originalData = null;

document.addEventListener('DOMContentLoaded', () => {
    init();
    const selectAlg = document.getElementById('algoritmo');
    if (selectAlg) selectAlg.addEventListener('change', handleAlgChange);
});

function limparVisualizacao() {
    if (!nodesDataset || !edgesDataset) return;

    const resetNodes = nodesDataset.get().map(n => ({
        id: n.id,
        color: null,
        size: 16,
        font: { color: '#ffffff' },
        label: n.label
    }));

    const resetEdges = edgesDataset.get().map(e => ({
        id: e.id,
        color: { inherit: 'from', opacity: 0.3 },
        width: 1,
        dashes: false
    }));

    nodesDataset.update(resetNodes);
    edgesDataset.update(resetEdges);
}

async function init() {
    try {
        const response = await fetch('grafo_dados.json');
        if (!response.ok) throw new Error('Arquivo grafo_dados.json não encontrado.');

        const data = await response.json();

        const datalist = document.getElementById('lista-bairros');
        if (datalist) {
            datalist.innerHTML = '';
            data.nodes.forEach(node => {
                const option = document.createElement('option');
                option.value = node.id;
                datalist.appendChild(option);
            });
        }

        originalData = {
            nodes: JSON.parse(JSON.stringify(data.nodes)),
            edges: JSON.parse(JSON.stringify(data.edges))
        };

        const nodesProcessed = data.nodes.map(n => ({
            ...n,
            title: n.title ? createHtmlElement(n.title) : undefined
        }));

        const edgesProcessed = data.edges.map(e => ({
            ...e,
            title: e.title ? createHtmlElement(e.title) : undefined
        }));

        nodesDataset = new vis.DataSet(nodesProcessed);
        edgesDataset = new vis.DataSet(edgesProcessed);

        const container = document.getElementById('network');
        const options = {
            nodes: {
                shape: 'dot',
                size: 16,
                font: { size: 14, color: '#ffffff', face: 'sans-serif' },
                borderWidth: 2,
                shadow: true
            },
            edges: {
                width: 1,
                color: { inherit: 'from', opacity: 0.3 },
                smooth: { type: 'continuous', roundness: 0.5 }
            },
            physics: {
                stabilization: false,
                barnesHut: {
                    gravitationalConstant: -8000,
                    springConstant: 0.04,
                    springLength: 95
                }
            },
            interaction: { hover: true, tooltipDelay: 200, zoomView: true }
        };

        network = new vis.Network(container, { nodes: nodesDataset, edges: edgesDataset }, options);

        network.on('stabilizationIterationsDone', () => network.fit());

        resetLegendPadrao();
        handleAlgChange();

    } catch (error) {
        mostrarErro('Erro ao carregar grafo: ' + error.message);
    }
}

function createHtmlElement(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString;
    return div;
}

function handleAlgChange() {
    const alg = document.getElementById('algoritmo').value;
    const divDestino = document.getElementById('grupo-destino');
    const inputDestino = document.getElementById('destino');

    if (alg === 'bfs' || alg === 'dfs') {
        if (divDestino) divDestino.classList.add('hidden');
        if (inputDestino) inputDestino.value = '';
    } else {
        if (divDestino) divDestino.classList.remove('hidden');
    }

    limparVisualizacao();
    resetLegendPadrao();
}

function resetGrafo() {
    if (!originalData || !nodesDataset || !edgesDataset) return;

    const nodesRestore = originalData.nodes.map(n => ({
        ...n,
        title: n.title ? createHtmlElement(n.title) : undefined
    }));

    const edgesRestore = originalData.edges.map(e => ({
        ...e,
        title: e.title ? createHtmlElement(e.title) : undefined
    }));

    nodesDataset.update(nodesRestore);
    edgesDataset.update(edgesRestore);

    esconderErro();
    resetLegendPadrao();
}

async function calcular() {
    resetGrafo();

    const alg = document.getElementById('algoritmo').value;
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;

    if (!origem) {
        mostrarErro('Por favor, selecione uma origem.');
        return;
    }

    try {
        const params = new URLSearchParams({ alg, origem, destino });
        const res = await fetch(`/api/calcular?${params.toString()}`);
        const text = await res.text();
        const data = text ? JSON.parse(text) : {};

        if (!res.ok) {
            throw new Error(data.erro || 'Erro desconhecido no servidor');
        }

        if (data.tipo === 'caminho') processarCaminho(data);
        else if (data.tipo === 'expansao') processarExpansao(data);
        else mostrarErro('Resposta do servidor desconhecida');

    } catch (e) {
        mostrarErro(e.message || String(e));
    }
}

function processarCaminho(data) {
    if (!data || !Array.isArray(data.caminho) || !nodesDataset || !edgesDataset) return;

    limparVisualizacao();

    const caminho = data.caminho;

    const nodeUpdates = caminho.map((no, index) => ({
        id: no,
        color: { background: '#FACC15', border: '#CA8A04' },
        size: 25,
        label: `${index + 1}. ${no}`,
        title: createHtmlElement(`<div style="padding:4px;"><strong>Passo ${index + 1}</strong><br>Bairro: ${no}</div>`)
    }));

    nodesDataset.update(nodeUpdates);

    const edgeUpdates = [];
    for (let i = 0; i < caminho.length - 1; i++) {
        const u = caminho[i];
        const v = caminho[i + 1];

        const found = edgesDataset.get({ filter: e => (e.from === u && e.to === v) || (e.from === v && e.to === u) });
        if (found.length > 0) {
            const e = found[0];
            edgeUpdates.push({
                id: e.id,
                color: { color: '#EF4444', opacity: 1 },
                width: 6,
                dashes: false,
                title: createHtmlElement(`<div style="padding:4px;"><strong>Aresta do Caminho</strong><br>Peso: ${e.label || '?'} </div>`)
            });
        }
    }

    if (edgeUpdates.length) edgesDataset.update(edgeUpdates);

    updateLegend('caminho', data.custo);
}

function processarExpansao(data) {
    if (!data || !data.dados_nos || !nodesDataset) return;

    const valores = data.dados_nos;
    const maxVal = Math.max(...Object.values(valores)) || 1;

    const updates = Object.entries(valores).map(([bairro, valor]) => ({
        id: bairro,
        color: {
            background: getColorByValue(valor, maxVal),
            border: '#1F2937'
        },
        size: 22,
        title: createHtmlElement(`<div style="padding:4px;"><strong>${bairro}</strong><br>${data.metrica}: <b>${valor}</b></div>`)
    }));

    nodesDataset.update(updates);

    updateLegend('expansao', null, data.metrica);
}

function getColorByValue(value, max) {
    const pct = (value || 0) / (max || 1);
    const hue = Math.floor(pct * 300);
    return `hsl(${hue}, 100%, 50%)`;
}

function mostrarErro(msg) {
    const el = document.getElementById('msg-erro');
    if (!el) return;
    el.textContent = msg;
    el.classList.remove('hidden');
}

function esconderErro() {
    const el = document.getElementById('msg-erro');
    if (!el) return;
    el.classList.add('hidden');
}

function resetLegendPadrao() {
    const div = document.getElementById('legend-content');
    if (!div) return;

    div.innerHTML = `
        <div class="flex items-center text-sm text-gray-600 mb-1">
            <span class="dot bg-blue-300 mr-2"></span>
            <span>Padrão</span>
        </div>
        <div class="flex items-center text-sm text-gray-600">
            <span class="dot bg-yellow-400 mr-2"></span>
            <span>Selecionado</span>
        </div>
    `;
}

function updateLegend(tipo, custo, metricaNome) {
    const div = document.getElementById('legend-content');
    if (!div) return;

    if (tipo === 'caminho') {
        div.innerHTML = `
            <div class="flex items-center mb-1 text-sm text-gray-700">
                <span class="dot bg-yellow-400 border-2 border-yellow-600 mr-2"></span>
                <span>Nó do Caminho</span>
            </div>
            <div class="flex items-center mb-3 text-sm text-gray-700">
                <span class="line bg-red-500 mr-2"></span>
                <span>Aresta Percorrida</span>
            </div>
            <div class="pt-2 border-t border-gray-200">
                <div class="text-xs text-gray-500 uppercase tracking-wide">Custo Total</div>
                <div class="text-lg font-bold text-blue-600">${custo !== undefined && custo !== null ? custo : '-'}</div>
            </div>
        `;
    } else if (tipo === 'expansao') {
        const gradientStyle = `background: linear-gradient(to right, \
            hsl(0, 100%, 50%), \
            hsl(60, 100%, 50%), \
            hsl(120, 100%, 50%), \
            hsl(180, 100%, 50%), \
            hsl(240, 100%, 50%), \
            hsl(300, 100%, 50%)); height: 10px; width: 100%; border-radius: 5px; margin-top: 5px;`;

        div.innerHTML = `
            <div class="text-sm font-bold text-gray-800 mb-1">${metricaNome || 'Métrica'}</div>
            <div style="${gradientStyle}"></div>
            <div class="flex justify-between text-xs text-gray-500 font-medium mt-1">
                <span>Baixo</span>
                <span>Alto</span>
            </div>
        `;
    } else {
        resetLegendPadrao();
    }
}
