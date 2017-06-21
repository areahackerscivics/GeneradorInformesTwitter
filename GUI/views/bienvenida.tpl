<!DOCTYPE html>

<html>
  <head>
    <title>Bienvenida</title>
  	<link rel="stylesheet" type="text/css" href="/css/main.css">

    <style>
          .label {text-align: right}
          .error {color: red}
    </style>
  </head>
  <class="product-details-title">
  <body>
      Bienvenida {{username}}

      <!-- menu -->
      <ul>
        <li class="dropdown">
          <a href="javascript:void(0)" class="dropbtn">Administrar</a>
          <div class="dropdown-content">
                <a href="/clasificar">Clasificación</a>
                <a href="/ListarClasificadores">Clasificadores</a>
          </div>
        </li>
        <li class="dropdown">
          <a href="javascript:void(0)" class="dropbtn">Revisar</a>
          <div class="dropdown-content">
                <a href="/revision">Revision por Categoría</a>
                <a href="/metrica">Métricas</a>
          </div>
        </li>
        <li class="dropdown">
          <a href="javascript:void(0)" class="dropbtn">Reporte</a>
          <div class="dropdown-content">
                <a href="#">Reporte 1</a>
          </div>
        </li>
      </ul>
      <!-- fin menu -->

  </body>

</html>
