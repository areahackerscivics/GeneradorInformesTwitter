<!DOCTYPE html>
<html lang="es">
<head>
<title>Revisar Tweet</title>
<link rel="stylesheet" type="text/css" href="/css/main.css">
<meta charset="utf-8" />
</head>
<body>

<p>
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
    <header>
    </header>
	<form method="post" action="/revision">
	%catsel=dict['catsel']
	%reentre=dict['reentre']
	%ntwets=dict['ntwets']
	%fechaini=dict['fechaini']
	%fechafin=dict['fechafin']
	<table style="estilo"align="center">
	<tr>
		<td><strong>Revisados </strong></td>
		<td><strong>Categoria</strong></td>
		<td><strong>Fecha Inicio</strong></td>
		<td><strong>Fecha Fin</strong></td>
		<td><strong>Nro Tweets</strong></td>
		<td></td>
	</tr>
	<tr>
	<td><input class="estilo1" type="text" name="reentre" value="{{reentre}}" readonly></td>
		<td>
				<select name="catlistar">
					<option value="Ninguna">--Selecciona--</option>
					<option value="{{catsel}}"selected>{{catsel}}</option>
					<option value="Ciencia y tecnología">Ciencia y tecnología</option>
					<option value="Comercio">Comercio</option>
					<option value="Cultura y ocio">Cultura y ocio</option>
					<option value="Demografía">Demografía</option>
					<option value="Deporte">Deporte</option>
					<option value="Economía">Economía</option>
					<option value="Educación">Educación</option>
					<option value="Empleo">Empleo</option>
					<option value="Energía">Energía</option>
					<option value="Hacienda">Hacienda</option>
					<option value="Industria">Industria</option>
					<option value="Legislación y justicia">Legislación y justicia</option>
					<option value="Medio ambiente">Medio ambiente</option>
					<option value="Medio Rural">Medio Rural</option>
					<option value="Salud">Salud</option>
					<option value="Sector público">Sector público</option>
					<option value="Seguridad">Seguridad</option>
					<option value="Sociedad y bienestar">Sociedad y bienestar</option>
					<option value="Transporte">Transporte</option>
					<option value="Turismo">Turismo</option>
					<option value="Urbanismo e infraestructuras">Urbanismo e infraestructuras</option>
					<option value="Vivienda">Vivienda</option>
				</select>
			</td>
		<td><input type="date" name="FechaInicio" value={{fechaini}}></td>
		<td><input type="date" name="FechaFin" value={{fechafin}}></td>
		<td><select name="nlistwets">
			<option value="10">10</option>
			<option value={{ntwets}} selected>{{ntwets}}</option>
			<option value="20">20</option>
			<option value="50">50</option>
			<option value="100">100</option>
			</select>
		</td>
		<td><input type="submit" class="estilo2" value="Listar"></td>
		</form>
		<form name="actualizar" action="/Actualizar" method="POST">
		<td><input type="submit" class="estilo2" onclick="return confirm('¿Esta seguro que desea enviar el formulario?');" name="dict"></td>

	</tr>
	</table>


	<table align="center">
	<tr>
		<!-- <td><strong>Categoria</strong></td> -->
		<td style="background-color:Transparent"></td>
		<td><strong>Tweet</strong></td>
		<td><strong>Nueva Categoria</strong></td>
		<td></td>
	</tr>
	% count=0
	% for i in range(len(dict['tweet'])):
	%catsel=dict['catsel']
	%catnewn='catnew'+str(i)
	%idtn='idt'+str(i)
	%catoldn='catold'+str(i)
	%texton='texto'+str(i)
		<tr>
		<td style="background-color:white"><input type="text" name={{idtn}} style="visibility:hidden" value="{{dict['idt'][i]}}"></td>
		<td><textarea class="estilo" rows="3" name={{texton}}  cols="90" readonly>{{dict['tweet'][i]}}</textarea> </td>
			</td>
			<td valign="top">
				<select name={{catnewn}}>
					<option value="Correcta">--CORRECTA--</option>
					<option value="Desechado">--DESECHADO--</option>
					<option value="Ciencia y tecnología">Ciencia y tecnología</option>
					<option value="Comercio">Comercio</option>
					<option value="Cultura y ocio">Cultura y ocio</option>
					<option value="Demografía">Demografía</option>
					<option value="Deporte">Deporte</option>
					<option value="Economía">Economía</option>
					<option value="Educación">Educación</option>
					<option value="Empleo">Empleo</option>
					<option value="Energía">Energía</option>
					<option value="Hacienda">Hacienda</option>
					<option value="Industria">Industria</option>
					<option value="Legislación y justicia">Legislación y justicia</option>
					<option value="Medio ambiente">Medio ambiente</option>
					<option value="Medio Rural">Medio Rural</option>
					<option value="Salud">Salud</option>
					<option value="Sector público">Sector público</option>
					<option value="Seguridad">Seguridad</option>
					<option value="Sociedad y bienestar">Sociedad y bienestar</option>
					<option value="Transporte">Transporte</option>
					<option value="Turismo">Turismo</option>
					<option value="Urbanismo e infraestructuras">Urbanismo e infraestructuras</option>
					<option value="Vivienda">Vivienda</option>
				</select>
			</td>
			<td style="background-color:white"><input type="text" name={{catoldn}} style="visibility:hidden" value="{{dict['catold'][i]}}"></td>
		</tr>

		%count=count+1
		% end
</table>
<div class="bottomOfThePage">
        <div class="centerOfThePage">
		<input type="text" name="contar" style="visibility:hidden" value="{{count}}">

	 </div>
</div>
	</form>

</body>
</html>
