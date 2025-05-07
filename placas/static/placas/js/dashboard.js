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
let ultimaPlacaProcessada = null;

function captureImage() {
  const videoElement = document.getElementById('video');
  const canvas = document.createElement('canvas');
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  const context = canvas.getContext('2d');
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/jpeg');
}

function exibirBarraDeProgresso() {
  const campos = [
    'placa', 'modelo', 'marca', 'cor', 'ano', 'municipio', 'situacao',
    'versao', 'combustivel', 'potencia', 'chassi', 'restricao1'
  ];
  campos.forEach(id => {
    const td = document.getElementById(id);
    if (td) {
      td.innerHTML = `<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div></div>`;
    }
  });
}

function exibirPlacaDetectadaNaTela(placaDetectada) {
  const box = document.getElementById('placa-render');
  const conteudo = box.querySelector('.placa-conteudo');
  const etiqueta = box.querySelector('.placa-etiqueta-superior');
  if (etiqueta) etiqueta.remove();

  const tipo = /^[A-Z]{3}[0-9]{4}$/.test(placaDetectada) ? "velha" : "mercosul";
  const imgPath = tipo === "mercosul" ? "img__mercosul.png" : "img__velha.png";
  const etiquetaTexto = tipo === "mercosul" ? "BRASIL MODELO MERCOSUL" : "BRASIL MODELO ANTIGO";

  box.style.backgroundImage = `url('/static/placas/imagens/${imgPath}')`;
  conteudo.textContent = placaDetectada;
  box.insertAdjacentHTML("afterbegin", `<div class="placa-etiqueta-superior">${etiquetaTexto}</div>`);
}

function atualizarDashboard() {
  fetch('/ultima-consulta-json')
    .then(res => res.json())
    .then(data => {
      if (!data || !data.placa) return;  // Se a API não trouxe nova placa, não apaga a atual

      // Se for a mesma da última exibida, evita reprocessar
      if (data.placa === ultimaPlacaProcessada) return;

      ultimaPlacaProcessada = data.placa;
      exibirPlacaDetectadaNaTela(data.placa);
      exibirBarraDeProgresso();

      setTimeout(() => {
        document.getElementById('placa').textContent = data.placa || '';
        document.getElementById('modelo').textContent = data.modelo || '';
        document.getElementById('marca').textContent = data.marca || '';
        document.getElementById('cor').textContent = data.cor || '';
        document.getElementById('ano').textContent = data.ano || '';
        document.getElementById('municipio').textContent = data.municipio || '';
        document.getElementById('situacao').textContent = data.situacao || '';
        document.getElementById('versao').textContent = data.versao || '';
        document.getElementById('combustivel').textContent = data.combustivel || '';
        document.getElementById('potencia').textContent = data.potencia || '';
        document.getElementById('chassi').textContent = data.chassi || '';

        const restricao1 = document.getElementById('restricao1');
        if (data.restricao) {
          restricao1.innerHTML = `<span class="text-danger fw-bold">🚫 Com restrição</span>`;
        } else {
          restricao1.innerHTML = `<span class="text-success fw-bold">✅ Sem restrição</span>`;
        }

        const tbody = document.querySelector('#historico-table tbody');
        tbody.innerHTML = (data.historico || []).map(item => `
          <tr>
            <td>${item.placa}</td>
            <td>${item.modelo}</td>
            <td>${item.cor}</td>
            <td>${item.municipio}</td>
            <td>${item.situacao}</td>
            <td>${item.data}</td>
          </tr>
        `).join('');
      }, 1000); // tempo para simular carregamento da API
    });
}

function atualizarSemaforo(cor) {
  const verde = document.getElementById("sinal-verde");
  const amarelo = document.getElementById("sinal-amarelo");
  const vermelho = document.getElementById("sinal-vermelho");

  verde.classList.add("d-none");
  amarelo.classList.add("d-none");
  vermelho.classList.add("d-none");

  if (cor === "verde") verde.classList.remove("d-none");
  else if (cor === "vermelho") vermelho.classList.remove("d-none");
  else amarelo.classList.remove("d-none");  // padrão
}


function sendImageToServer() {
  atualizarSemaforo("amarelo"); // inicia como lendo

  const imageBase64 = captureImage();

  fetch('/detectar-placa/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ imagem: imageBase64 })
  })
    .then(response => response.json())
    .then(data => {
      const placaDetectada = data.placa;

      if (
        placaDetectada &&
        (/^[A-Z]{3}[0-9]{4}$/.test(placaDetectada) || /^[A-Z]{3}[0-9][A-Z][0-9]{2}$/.test(placaDetectada))
      ) {
        exibirPlacaDetectadaNaTela(placaDetectada);
        atualizarSemaforo("verde"); // detectou
      } else {
        atualizarSemaforo("vermelho"); // não detectou
      }

      atualizarDashboard();
    })
    .catch(err => {
      console.error("Erro ao enviar imagem:", err);
      atualizarSemaforo("vermelho");
    });
}

async function startVideo() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    document.getElementById('video').srcObject = stream;
    setInterval(sendImageToServer, 4000);
  } catch (err) {
    console.error("Erro ao acessar a câmera:", err);
  }
}

window.onload = () => {
  startVideo();
};
