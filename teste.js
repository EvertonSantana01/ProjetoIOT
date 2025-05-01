// dashboard.js ajustado para IDs do HTML novo

function atualizarDashboard(dados) {
  document.getElementById('campo-placa').textContent = dados.placa || '-';
  document.getElementById('campo-marca').textContent = dados.marca || '-';
  document.getElementById('campo-modelo').textContent = dados.modelo || '-';
  document.getElementById('campo-versao').textContent = dados.versao || '-';
  document.getElementById('campo-ano').textContent = dados.ano || '-';
  document.getElementById('campo-cor').textContent = dados.cor || '-';
  document.getElementById('campo-municipio').textContent = dados.municipio || '-';
  document.getElementById('campo-uf').textContent = dados.uf || '-';
  document.getElementById('campo-combustivel').textContent = dados.combustivel || '-';
  document.getElementById('campo-potencia').textContent = dados.potencia || '-';
  document.getElementById('campo-chassi').textContent = dados.chassi || '-';
  document.getElementById('campo-situacao').textContent = dados.situacao || '-';

  const restricoes = [dados.restricao1, dados.restricao2, dados.restricao3, dados.restricao4]
    .filter(r => r && r !== 'SEM RESTRICAO')
    .join(', ');
  document.getElementById('campo-restricoes').textContent = restricoes || 'SEM RESTRICAO';

  if (dados.logo) {
    const logoEl = document.getElementById('logo-marca');
    if (logoEl) logoEl.src = dados.logo;
  }
}

// Histórico da sessão
function adicionarAoHistorico(dado) {
  const tabela = document.querySelector('#historico-table tbody');
  const linha = document.createElement('tr');
  linha.innerHTML = `
    <td>${dado.placa}</td>
    <td>${dado.modelo}</td>
    <td>${dado.cor}</td>
    <td>${dado.municipio}</td>
    <td>${dado.situacao}</td>
    <td>${dado.data}</td>
  `;
  tabela.prepend(linha);
}

// Consulta inicial
fetch('/ultima-consulta-json')
  .then(res => res.json())
  .then(dados => {
    if (dados && dados.placa) {
      atualizarDashboard(dados);
      dados.historico?.forEach(adicionarAoHistorico);
    }
  });
