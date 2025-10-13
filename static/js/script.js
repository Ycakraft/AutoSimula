// script.js
// Adiciona um manipulador de evento para o carregamento da página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página carregada com sucesso!');
    
    // Aqui você pode adicionar mais interatividade conforme necessário
    // Por exemplo, validação de formulários, animações, etc.
});

// Função para exibir mensagens de feedback
function showMessage(message, type = 'info') {
    // Remove mensagens anteriores
    const existingMessages = document.querySelectorAll('.flash-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Cria a nova mensagem
    const messageDiv = document.createElement('div');
    messageDiv.className = `flash-message ${type}`;
    messageDiv.textContent = message;
    
    // Adiciona a mensagem ao topo da página
    const header = document.querySelector('header');
    if (header) {
        header.insertAdjacentElement('afterend', messageDiv);
    } else {
        document.body.insertAdjacentElement('afterbegin', messageDiv);
    }
    
    // Remove a mensagem após 5 segundos
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}
