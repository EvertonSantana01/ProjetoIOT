function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const trimmed = cookie.trim();
      if (trimmed.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function mostrarErro(msg) {
  const area = document.getElementById('resultado-consulta');
  area.innerHTML = `<div class="alert alert-warning">${msg}</div>`;
}

// Consulta via API BRASIL
function consultaApiBrasil() {
  const placa = document.getElementById('input-placa').value.trim().toUpperCase();

  if (!placa) {
    mostrarErro('Digite uma placa para consulta.');
    return;
  }

  fetch('/consultar-placa/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ placa: placa })
  })
    .then(response => response.json())
    .then(data => {
      if (data && data.status === 'sucesso') {
        renderizarResultado(data.dados);
      } else {
        mostrarErro(data.mensagem || 'Nenhum dado retornado da API.');
      }
    })
    .catch(error => {
      console.error("Erro ao consultar API:", error);
      mostrarErro('Erro ao consultar a API.');
    });
}

// Consulta em banco de dados
function consultaCadastrados() {
  const placa = document.getElementById('input-placa').value.trim().toUpperCase();

  if (!placa) {
    mostrarErro('Digite uma placa para consulta.');
    return;
  }

  fetch(`/consultar-cadastrados/?placa=${placa}`)
    .then(response => response.json())
    .then(data => {
      if (data && data.status === 'sucesso') {
        renderizarResultado(data.dados);
      } else {
        mostrarErro(data.mensagem || 'Placa não encontrada no banco.');
      }
    })
    .catch(error => {
      console.error("Erro na consulta local:", error);
      mostrarErro('Erro ao consultar o banco de dados.');
    });
}

// Função para renderizar os dados (usada por ambas)
function renderizarResultado(info) {
  const restricoes = [
    info.restricao1, info.restricao2,
    info.restricao3, info.restricao4
  ].filter(r => r && r !== 'SEM RESTRICAO');

  const tabela = `
    <h2 class="text-primary">Resultado da Consulta</h2>
    <table class="table table-bordered table-striped bg-white text-dark">
      <tbody>
        <tr><th>Placa</th><td>${info.placa}</td></tr>
        <tr><th>Modelo</th><td>${info.modelo}</td></tr>
        <tr><th>Marca</th><td>${info.marca}</td></tr>
        <tr><th>Versão</th><td>${info.versao || ''}</td></tr>
        <tr><th>Cor</th><td>${info.cor || ''}</td></tr>
        <tr><th>Ano</th><td>${info.ano}</td></tr>
        <tr><th>Ano Modelo</th><td>${info.anoModelo || ''}</td></tr>
        <tr><th>Município</th><td>${info.municipio || ''}</td></tr>
        <tr><th>UF</th><td>${info.uf || ''}</td></tr>
        <tr><th>Chassi</th><td>${info.chassi || ''}</td></tr>
        <tr><th>Combustível</th><td>${info.combustivel || ''}</td></tr>
        <tr><th>Potência</th><td>${info.potencia || ''}</td></tr>
        <tr><th>Cilindradas</th><td>${info.cilindradas || ''}</td></tr>
        <tr><th>Situação Veículo</th><td>${info.situacao_veiculo || ''}</td></tr>
        <tr><th>Nacionalidade</th><td>${info.nacionalidade || ''}</td></tr>
        <tr><th>Quantidade Passageiros</th><td>${info.quantidade_passageiro || ''}</td></tr>
        <tr><th>Peso Bruto</th><td>${info.peso_bruto_total || ''}</td></tr>
        <tr><th>Data API</th><td>${info.data || ''}</td></tr>
        <tr><th>Última Atualização</th><td>${info.ultima_atualizacao || ''}</td></tr>
        <tr><th>Restrições</th><td>${
          restricoes.length ? restricoes.join(', ') : 'Sem restrições'
        }</td></tr>
      </tbody>
    </table>
  `;

  document.getElementById('resultado-consulta').innerHTML = tabela;
}
