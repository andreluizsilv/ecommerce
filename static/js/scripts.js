// Scripts do cabeçalho
var eleCabecalhoMenu = document.querySelector(".cabecalho__menu");
var eleCabecalho = document.querySelector(".cabecalho");
var elemsItemLista = document.querySelectorAll(".cabecalho__item-lista");

eleCabecalhoMenu.addEventListener("click", function () {
  eleCabecalho.classList.toggle("cabecalho--aberto");

  elemsItemLista.forEach(function (ele) {
    ele.querySelector(".cabecalho__link").href = "javascript: void(0)";
  });
});

elemsItemLista.forEach(function (ele) {
  ele.addEventListener("click", function () {
    ele.classList.toggle("cabecalho__item-lista--aberto");
  });
});

var eleCabecalhoLogin = document.querySelector(".cabecalho__icone-login");
var eleInfosPerfil = document.querySelector(".cabecalho__informacoes-perfil");

eleCabecalhoLogin.addEventListener("click", function () {
  eleInfosPerfil.classList.toggle("cabecalho__informacoes-perfil--aberto");
});
 // Get the modal
var modal = document.getElementById("avisoModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}