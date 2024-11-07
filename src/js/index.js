document.addEventListener('DOMContentLoaded', function() {
    // Define a função adicionarMensagem e expõe ao escopo global
    const mensagensDiv = document.getElementById("mensagens");
    function adicionarMensagem(texto) {
        const novaMensagem = document.createElement("div");
        novaMensagem.className = "mensagem";
        novaMensagem.innerHTML = texto;
        mensagensDiv.appendChild(novaMensagem);
        mensagensDiv.appendChild(document.createElement("br"));
    }

    // Expõe adicionarMensagem globalmente
    window.adicionarMensagem = adicionarMensagem;

    // Configura o evento para o botão "Iniciar análise" assim que ele for adicionado ao DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.id === 'btn-iniciar-analise') {
                        node.addEventListener('click', function() {
                            window.pywebview.api.iniciar_analise();
                        });
                        mensagensDiv.appendChild(document.createElement("br"));
                    }
                    if (node.id === 'btn-reiniciar-analise') {
                        node.addEventListener('click', function() {
                            window.pywebview.api.iniciar_analise();
                        });
                    }
                    if (node.id === 'btn-encerrar') {
                        node.addEventListener('click', function() {
                            window.pywebview.api.encerramento();
                        });
                    }
                    mensagensDiv.scrollTop = mensagensDiv.scrollHeight;
                });
            }
        });
    });

    // Observa mudanças no `mensagensDiv`
    observer.observe(mensagensDiv, { childList: true });
});
