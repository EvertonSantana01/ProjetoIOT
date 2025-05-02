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

function captureImage() {
  const videoElement = document.getElementById('video');
  const canvas = document.createElement('canvas');
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  const context = canvas.getContext('2d');
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/jpeg');
}

function sendImageToServer() {
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
    .then(() => {
      atualizarDashboard();
    })
    .catch(err => console.error("Erro ao enviar imagem:", err));
}

function atualizarDashboard() {
  fetch('/ultima-consulta-json')
    .then(res => res.json())
    .then(data => {
      console.log("📦 Dados recebidos:", data);
      const box = document.getElementById('placa-render');
      const conteudo = box.querySelector('.placa-conteudo');
      const etiqueta = document.querySelector('.placa-etiqueta-superior');
      if (etiqueta) etiqueta.remove();

      if (!data || !data.placa) {
        box.style.backgroundImage = "url('/static/placas/imagens/img__mercosul.png')";
        conteudo.textContent = "---";
        box.insertAdjacentHTML("afterbegin", `<div class="placa-etiqueta-superior">BRASIL MODELO MERCOSUL</div>`);
        ['modelo', 'marca', 'cor', 'ano', 'municipio', 'situacao', 'combustivel', 'potencia', 'chassi', 'versao'].forEach(id => {
          const el = document.getElementById(id);
          if (el) el.textContent = '';
        });
        document.getElementById('restricao1').innerHTML = '';
        document.querySelector('#historico-table tbody').innerHTML = '';
        return;
      }

      const tipo = /^[A-Z]{3}[0-9]{4}$/.test(data.placa) ? "velha" : "mercosul";
      const imgPath = tipo === "mercosul" ? "img__mercosul.png" : "img__velha.png";
      const etiquetaTexto = tipo === "mercosul" ? "BRASIL MODELO MERCOSUL" : "BRASIL MODELO ANTIGO";

      box.style.backgroundImage = `url('/static/placas/imagens/${imgPath}')`;
      conteudo.textContent = data.placa;
      box.insertAdjacentHTML("afterbegin", `<div class="placa-etiqueta-superior">${etiquetaTexto}</div>`);

      document.getElementById('modelo').textContent = data.modelo || '';
      document.getElementById('marca').textContent = data.marca || '';
      document.getElementById('cor').textContent = data.cor || '';
      document.getElementById('ano').textContent = data.ano || '';
      document.getElementById('municipio').textContent = data.municipio || '';
      document.getElementById('situacao').textContent = data.situacao || '';
      if (document.getElementById('combustivel')) document.getElementById('combustivel').textContent = data.combustivel || '';
      if (document.getElementById('potencia')) document.getElementById('potencia').textContent = data.potencia || '';
      if (document.getElementById('chassi')) document.getElementById('chassi').textContent = data.chassi || '';
      if (document.getElementById('versao')) document.getElementById('versao').textContent = data.versao || '';

      // 🔴🟢 Exibe restrição diretamente no campo Restrição 1
      const restricao1 = document.getElementById('restricao1');
      const temRestricao = data.restricao === true;
      if (temRestricao) {
        const motivo = data.restricao_motivo || 'Procurar DETRAN';
        restricao1.innerHTML = `<span style="color:#f44336; font-size:2rem; font-weight:bold;">🚫 Com restrição: ${motivo}</span>`;
      } else {
        restricao1.innerHTML = `<span style="color:#00cc66; font-size:1.3rem; font-weight:bold;">✅ Sem restrição</span>`;
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
    });
}

async function startVideo() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    document.getElementById('video').srcObject = stream;
    setInterval(sendImageToServer, 3000);
  } catch (err) {
    console.error("Erro ao acessar a câmera:", err);
  }
}

window.onload = () => {
  startVideo();
};
