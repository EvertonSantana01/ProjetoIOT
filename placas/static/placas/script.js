// Função para capturar a imagem da câmera
function captureImage() {
    const videoElement = document.getElementById('video');
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    // Converte a imagem para Base64
    return canvas.toDataURL('image/jpeg'); // Ou 'image/png', dependendo do tipo de imagem desejado
}

// Função para obter o valor do cookie CSRF
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

// Captura o CSRF Token
const csrftoken = getCookie('csrftoken');

// Função para enviar a imagem para o servidor
function sendImageToServer() {
    const imageBase64 = captureImage();  // Captura a imagem em Base64

    fetch('/detectar-placa/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ imagem: imageBase64 })  // Envia a imagem como parte do corpo da requisição
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Exibe os dados retornados pelo servidor
        document.getElementById('placa').textContent = data.placa;  // Exibe a placa detectada
    })
    .catch(error => {
        console.error('Erro ao enviar a imagem:', error);
    });
}

// Função para iniciar o vídeo da câmera
async function startVideo() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        const video = document.getElementById('video');
        video.srcObject = stream;

        // Chama a função de detecção a cada 2 segundos
        setInterval(sendImageToServer, 2000);  // 2000ms = 2 segundos
    } catch (error) {
        console.error("Erro ao acessar a câmera: ", error);
    }
}

// Começa o vídeo automaticamente quando a página é carregada
window.onload = startVideo;
