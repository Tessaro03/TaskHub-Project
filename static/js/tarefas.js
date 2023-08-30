var cardTarefas = document.querySelectorAll('.card-tarefa');

cardTarefas.forEach(function (card) {
    card.addEventListener('click', function () {
        var tarefaCard = card.querySelector('.tarefa-card-content');
        if (tarefaCard.style.display === 'none') {
            tarefaCard.style.display = 'block';
        } else {
            tarefaCard.style.display = 'none';
        }
    });
})