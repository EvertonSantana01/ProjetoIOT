let paginaAtual = 1;
let dadosFiltrados = [];
const itensPorPagina = 20;

function carregarVeiculos() {
  fetch(`/api/veiculos/`)
    .then(res => res.json())
    .then(data => {
      if (data && data.dados) {
        dadosFiltrados = data.dados;
        renderizarTabela();
      } else {
        console.error("Formato de resposta inesperado:", data);
      }
    })
    .catch(err => console.error("Erro ao carregar veículos:", err));
}

function renderizarTabela() {
  const tbody = document.querySelector("#tabela-veiculos tbody");
  const paginacao = document.getElementById("paginacao");
  tbody.innerHTML = "";
  paginacao.innerHTML = "";

  const inicio = (paginaAtual - 1) * itensPorPagina;
  const fim = inicio + itensPorPagina;
  const paginaDados = dadosFiltrados.slice(inicio, fim);

  for (const item of paginaDados) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td data-coluna="placa">${item.placa}</td>
      <td data-coluna="modelo">${item.modelo}</td>
      <td data-coluna="marca">${item.marca}</td>
      <td>${item.cor}</td>
      <td>${item.ano}</td>
      <td>${item.municipio}</td>
      <td>${item.situacao}</td>
      <td>${item.data}</td>
      <td>
        <button class="btn btn-sm btn-primary me-1" onclick="abrirModalEdicao(${item.id})">Editar</button>
        <button class="btn btn-sm btn-danger" onclick="excluirVeiculo(${item.id})">Excluir</button>
      </td>
    `;
    tbody.appendChild(tr);
  }

  const totalPaginas = Math.ceil(dadosFiltrados.length / itensPorPagina);
  for (let i = 1; i <= totalPaginas; i++) {
    const li = document.createElement("li");
    li.classList.add("page-item");
    if (i === paginaAtual) li.classList.add("active");
    li.innerHTML = `<button class="page-link" onclick="irParaPagina(${i})">${i}</button>`;
    paginacao.appendChild(li);
  }
}

function irParaPagina(pagina) {
  paginaAtual = pagina;
  renderizarTabela();
}

function abrirModalEdicao(id) {
  const veiculo = dadosFiltrados.find(v => v.id === id);
  if (!veiculo) return;

  document.getElementById("editar-id").value = id;
  document.getElementById("editar-placa").value = veiculo.placa || '';
  document.getElementById("editar-modelo").value = veiculo.modelo || '';
  document.getElementById("editar-marca").value = veiculo.marca || '';
  document.getElementById("editar-versao").value = veiculo.versao || '';
  document.getElementById("editar-ano").value = veiculo.ano || '';
  document.getElementById("editar-cor").value = veiculo.cor || '';
  document.getElementById("editar-municipio").value = veiculo.municipio || '';
  document.getElementById("editar-uf").value = veiculo.uf || '';
  document.getElementById("editar-chassi").value = veiculo.chassi || '';
  document.getElementById("editar-combustivel").value = veiculo.combustivel || '';
  document.getElementById("editar-potencia").value = veiculo.potencia || '';
  document.getElementById("editar-cilindradas").value = veiculo.cilindradas || '';
  document.getElementById("editar-capacidade").value = veiculo.capacidade_carga || '';
  document.getElementById("editar-passageiros").value = veiculo.quantidade_passageiro || '';
  document.getElementById("editar-peso").value = veiculo.peso_bruto_total || '';
  document.getElementById("editar-situacao").value = veiculo.situacao || veiculo.situacao_veiculo || '';
  document.getElementById("editar-data").value = veiculo.data || '';
  document.getElementById("editar-data-api").value = veiculo.data_api || '';

  const modal = new bootstrap.Modal(document.getElementById("modal-editar"));
  modal.show();
}



document.getElementById("form-editar").addEventListener("submit", function (e) {
  e.preventDefault();
  const id = document.getElementById("editar-id").value;
  const dados = {
    placa: document.getElementById("editar-placa").value,
    modelo: document.getElementById("editar-modelo").value,
    marca: document.getElementById("editar-marca").value,
    cor: document.getElementById("editar-cor").value,
    ano: document.getElementById("editar-ano").value,
    municipio: document.getElementById("editar-municipio").value,
    situacao: document.getElementById("editar-situacao").value
  };
  fetch(`/api/veiculos/${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(dados)
  }).then(() => {
    bootstrap.Modal.getInstance(document.getElementById("modal-editar")).hide();
    carregarVeiculos();
  });
});

function excluirVeiculo(id) {
  if (!confirm("Tem certeza que deseja excluir?")) return;
  fetch(`/api/veiculos/${id}/excluir/`, {
    method: "DELETE"
  }).then(() => carregarVeiculos());
}

function aplicarFiltroInstantaneo() {
  const termo = document.getElementById("filtro-placa").value.toLowerCase();
  
  // Use os dados originais em vez de sobrescrever
  const resultado = dadosFiltrados.filter(v =>
    v.placa.toLowerCase().includes(termo) ||
    v.modelo.toLowerCase().includes(termo) ||
    v.marca.toLowerCase().includes(termo) ||
    v.municipio.toLowerCase().includes(termo)
  );

  const tbody = document.querySelector("#tabela-veiculos tbody");
  tbody.innerHTML = "";

  const inicio = 0;
  const fim = itensPorPagina;
  const paginaDados = resultado.slice(inicio, fim);

  for (const item of paginaDados) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td data-coluna="placa">${item.placa}</td>
      <td data-coluna="modelo">${item.modelo}</td>
      <td data-coluna="marca">${item.marca}</td>
      <td>${item.cor}</td>
      <td>${item.ano}</td>
      <td>${item.municipio}</td>
      <td>${item.situacao}</td>
      <td>${item.data}</td>
      <td>
        <button class="btn btn-sm btn-primary me-1" onclick="abrirModalEdicao(${item.id})">Editar</button>
        <button class="btn btn-sm btn-danger" onclick="excluirVeiculo(${item.id})">Excluir</button>
      </td>
    `;
    tbody.appendChild(tr);
  }
}


document.addEventListener("DOMContentLoaded", () => {
  carregarVeiculos();
  document.getElementById("filtro-placa").addEventListener("input", aplicarFiltroInstantaneo);
});
