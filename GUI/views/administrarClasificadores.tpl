<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
  <head>
  <body>

    <!-- Content izquierda. Tabla de clasificadores. -->
    <div id="cont_izq">
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
        %     acc = clasi['acc']
        %     desv = clasi['desviacion']
        %     entrena_ini = clasi['entrena_ini']
        %     entrena_fin = clasi['entrena_fin']
        %     fecha_creacion = clasi['fecha_creacion']
        %     predeterminado = clasi['predeterminado']
        <tr>
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
    <div id="cont_der">
      <div id="anyadir">
        <form name="anyadir" action="/Anyadir" method="POST">
          <table>
            <tr>
              <td>Nombre:</td>
              <td>
                <input type="text" name="anyadir_nombre">
              </td>
            </tr>
            <tr>
              <td>Fecha inicio para entrenamiento:</td>
              <td>
                <input type="text" name="anyadir_entrena_ini">
              </td>
            </tr>
            <tr>
              <td>Fecha fin para entrenamiento:</td>
              <td>
                <input type="text" name="anyadir_entrena_fin">
              </td>
            </tr>
          </table>

          <input type="submit" value="Añadir" />
        </form>
      </div>
      <div id="borrar">
      </div>
      <div id="editar">
      </div>
      <div id="actualizar">
      </div>
    </div>
  </body>
</html>
