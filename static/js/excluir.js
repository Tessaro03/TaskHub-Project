// Selecionar todos os ícones de exclusão e opções de exclusão
var btnExcluir = document.querySelectorAll('.excluir');
var filtros = document.querySelectorAll('.opcao-excluir');
var tasks = document.querySelectorAll('.task');

// Percorrer cada ícone de exclusão e adicionar os ouvintes de evento de clique
btnExcluir.forEach(function (deleteIcon, index) {
  deleteIcon.addEventListener('click', function () {
    // Obter o elemento "opcao-excluir" correspondente com base no índice
    var currentFiltros = filtros[index];
    var currentTask = tasks[index];

    // Alternar a exibição do elemento "opcao-excluir"
    if (currentFiltros.style.display === 'flex') {
      currentFiltros.style.display = 'none';
      currentTask.style.height = '380px'; // Reduz a altura para 350px quando desativado
    } else {
      currentFiltros.style.display = 'flex';
      currentTask.style.height = '430px'; // Aumenta a altura para 400px quando ativado
    }
  });
});

document.addEventListener('DOMContentLoaded', function() {
    // Selecionar todos os ícones de exclusão inline e opções de exclusão inline
    var btnExcluirInline = document.querySelectorAll('.excluir-inline');
    var filtrosInline = document.querySelectorAll('.opcao-excluir-inline');
    var tasksInline = document.querySelectorAll('.task-inline');
  
    // Percorrer cada ícone de exclusão inline e adicionar os ouvintes de evento de clique
    btnExcluirInline.forEach(function (deleteIcon, index) {
      deleteIcon.addEventListener('click', function (event) {
        event.stopPropagation(); // Impedir que o clique no ícone de exclusão "inline" afete o "task"
  
        // Obter o elemento "opcao-excluir-inline" correspondente com base no índice
        var currentFiltrosInline = filtrosInline[index];
        var currentTaskInline = tasksInline[index];
  
        // Alternar a exibição do elemento "opcao-excluir-inline"
        if (currentFiltrosInline.style.display === 'block') {
          currentFiltrosInline.style.display = 'none';
          currentTaskInline.style.height = '129px'; // Reduz a altura para 129px quando desativado
        } else {
          currentFiltrosInline.style.display = 'block';
          currentTaskInline.style.height = '150px'; // Aumenta a altura para 150px quando ativado
        }
      });
    });
  });
  
