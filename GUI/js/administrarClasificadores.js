

function visibilidad(id){

  document.getElementById('anyadir').style.display = 'none';
  document.getElementById('borrar').style.display = 'none';
  document.getElementById('editar').style.display = 'none';
  document.getElementById('reentrenar').style.display = 'none';

  document.getElementById(id).style.display = 'block';

}


function eliminarValorDefault(elem){
  elem.value = "";
}

function anyadirValorDefault(elem){
    var valor = elem.value;

    if( valor == "" ){
      elem.value = "AAAA-MM-DD";
    }
}

function seleccionarFila(elem){
  var nombre = elem.cells[0].innerHTML;
  nombre = nombre.replace(/\s+/g,"")
  document.getElementById('inpBorrar').value = nombre;
  document.getElementById('inpReentrenar').value = nombre;
}
