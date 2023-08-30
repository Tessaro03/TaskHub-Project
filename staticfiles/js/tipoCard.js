var cardBlock = document.querySelector('#tasks-incard');
var cardLine = document.querySelector('#tasks-inline');
var inline = document.querySelector('#inline');
var inblock = document.querySelector('#inblock');
var listagens = document.querySelector('#listagens');

listagens.addEventListener('click', listagem);


function listagem() {
    if (inline.style.display == 'none') {
      inline.style.display = 'block';
      inblock.style.display = 'none';
      cardBlock.style.display = 'block';
      cardLine.style.display = 'none';
  
    } else {
      inblock.style.display = 'block';
      inline.style.display = 'none';
      cardBlock.style.display = 'none';
      cardLine.style.display = 'block';
    }
  }