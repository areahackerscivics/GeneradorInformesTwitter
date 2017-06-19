<!DOCTYPE html>
<html>
<head>
  <title>Administrar Clasificadores</title>
  <link rel="stylesheet" type="text/css" href="/css/main.css">
  <script type="text/javascript" src="/js/administrarClasificadores.js"></script>

  <style>
        .label {text-align: right}
        .error {color: red}
  </style>
</head>
<class="product-details-title">
  <body>


    <!-- menu -->
    <ul>
      <li class="dropdown">
        <a href="javascript:void(0)" class="dropbtn">Administrar</a>
        <div class="dropdown-content">
              <a href="/clasificar">Clasificación</a>
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

    <!-- Content izquierda. Tabla de clasificadores. -->
    <div id="ac_cont_izq">
      <table>
        <tr>
          <th>Nombre</th>
          <th>Accuracy</th>
          <th>Desviacion</th>
          <th>Entrena ini</th>
          <th>Entrena fin</th>
          <th>Fecha creacion</th>
          <th>Predeterminado</th>
        </tr>

        % for clasi in clasificadores:
        %     nombre = clasi['nombre']
        %     acc = round( ((clasi['accuracy'])*100), 2 )
        %     acc = str(acc) + ' %'
        %     desv =  round( ((clasi['desviacion'])*100), 2 )
        %     desv = '+/- ' + str(desv) + ' %'
        %     entrena_ini =  clasi['entrena_ini'].date()
        %     entrena_fin = clasi['entrena_fin'].date()
        %     fecha_creacion = clasi['fecha_creacion'].replace(microsecond=0)
        %     predeterminado = clasi['predeterminado']
        <tr onclick="seleccionarFila(this)">
          <td>
            {{nombre}}
          </td>
          <td>
            {{acc}}
          </td>
          <td>
            {{desv}}
          </td>
          <td>
            {{entrena_ini}}
          </td>
          <td>
            {{entrena_fin}}
          </td>
          <td>
            {{fecha_creacion}}
          </td>
          <td>
            {{predeterminado}}
          </td>
        </tr>
    		% end
      </table>
    </div>

    <!-- Content derecha. Botones y labels. -->
    <div id="ac_cont_der">
      <div id="menu_acciones">

         <button type="button" onclick="visibilidad('anyadir')">Añadir</button>
         <button type="button" onclick="visibilidad('borrar')">Borrar</button>
         <button type="button" onclick="visibilidad('editar')">Editar</button>
         <button type="button" onclick="visibilidad('reentrenar')">Reentrenar</button>
      </div>
      <div id="anyadir">
        <form name="anyadir" action="/Anyadir" method="POST">
          <table>
            <tr>
              <td>Nombre:</td>
              <td>
                <input type="text"  name="anyadir_nombre" >
              </td>
            </tr>
            <tr>
              <td>Fecha inicio para entrenamiento:</td>
              <td>
                <input type="text" class="input_text" name="anyadir_entrena_ini" value="AAAA-MM-DD" onfocus="eliminarValorDefault(this)" onfocusout="anyadirValorDefault(this)">
              </td>
            </tr>
            <tr>
              <td>Fecha fin para entrenamiento:</td>
              <td>
                <input type="text" class="input_text" name="anyadir_entrena_fin" value="AAAA-MM-DD" onfocus="eliminarValorDefault(this)" onfocusout="anyadirValorDefault(this)">
              </td>
            </tr>
          </table>

          <input type="submit" value="Enviar" />
        </form>
      </div>
      <div id="borrar">
        <form name="borrar" action="/Borrar" method="POST">
          <table>
            <tr>
              <td>Nombre:</td>
              <td>
                <input type="text" id="inpBorrar" name="borrar_nombre">
              </td>
            </tr>
          </table>

          <input type="submit" value="Eliminar clasificador" />
        </form>
      </div>
      <div id="editar">
        No disponible
      </div>
      <div id="reentrenar">
        No disponible
      </div>
    </div>
  </body>
</html>
