// Cada vez que se muestra un modal, si tiene un elemento con autofocus,
// hacer foco el mismo.
// Basado en https://stackoverflow.com/a/33323836

$(document).on('shown.bs.modal', '.modal', function() {
  var e = $(this).find('[autofocus]');
  e.focus();

  // Si el elemento es no numérico, avanzar el cursor al final.
  // Basado en https://stackoverflow.com/a/19568146
  if (e.attr('type') !== 'number') {
     // Multiplicar por 2 para asegurar que el cursor siempre termine al final.
     // Algunos navegadores (ej: Opera) a veces toman un retorno de carro como 2 caracteres.
     var strLength = e.val().length * 2;
     e[0].setSelectionRange(strLength, strLength);
  }
});
