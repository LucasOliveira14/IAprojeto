document.addEventListener('DOMContentLoaded', function () {
    // Função para validar o formulário antes de enviar
    document.querySelector('form').addEventListener('submit', function (event) {
        const userId = document.querySelector('#user_id').value.trim();
        if (!userId || isNaN(userId)) {
            alert('Por favor, insira um ID de usuário válido.');
            event.preventDefault(); // Impede o envio do formulário
        }
    });
});
