document.addEventListener('DOMContentLoaded', function() {
    function adicionarMensagem(texto) {
        const mensagensDiv = document.getElementById("mensagens");
        const novaMensagem = document.createElement("div");
        novaMensagem.className = "mensagem";
        novaMensagem.innerHTML = texto;
        mensagensDiv.appendChild(novaMensagem);
        mensagensDiv.appendChild(document.createElement("br"));
        mensagensDiv.scrollTop = mensagensDiv.scrollHeight;
    }

    // Expõe adicionarMensagem globalmente
    window.adicionarMensagem = adicionarMensagem;
});
function showTelaConfirmacao() {
    document.getElementById("dialogo-confirmacao").style.display = "flex";
}

function closeTelaConfirmacao() {
    document.getElementById("dialogo-confirmacao").style.display = "none";
}

document.getElementById("botao-confirmar").onclick = function () {
    var btnIniciar = document.getElementById("btn-iniciar-analise");
    if (btnIniciar) {
        btnIniciar.disabled = true;
    };
    var btnReiniciar = document.getElementById("btn-reiniciar-analise");
    if (btnReiniciar) {
        btnReiniciar.disabled = true;
    };
    pywebview.api.encerramento();
    closeTelaConfirmacao();
};

document.getElementById("botao-cancelar").onclick = function () {
    closeTelaConfirmacao();
};