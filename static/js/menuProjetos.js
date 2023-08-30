var btnMenuTasks = document.querySelector('#menu-tarefas > h2');
var filtrosProjetos = document.querySelector('#list-task');

if (filtrosProjetos) { // Verificar se o elemento foi encontrado
  btnMenuTasks.addEventListener('click', toggleFiltrosMenu);
}

function toggleFiltrosMenu() {
  if (filtrosProjetos && filtrosProjetos.style.display === 'block') { // Verificar se o elemento foi encontrado antes de acessar a propriedade 'display'
    filtrosProjetos.style.display = 'none';
  } else if (filtrosProjetos) { // Verificar se o elemento foi encontrado antes de acessar a propriedade 'display'
    filtrosProjetos.style.display = 'block';
  }
}

var botaoBusca = document.querySelector('#buscar-pessoas-click')
var inputAmigos = document.querySelector('#busca-amigos')


botaoBusca.addEventListener('click', toggleInput);


function toggleInput() {
  if (inputAmigos.style.display === 'block') { 
    inputAmigos.style.display = 'none';
  } else  { 
    inputAmigos.style.display = 'block';
  }
}