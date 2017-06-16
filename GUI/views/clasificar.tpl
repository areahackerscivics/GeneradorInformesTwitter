<!DOCTYPE html>
<html lang="es">
<head>
<title>Métricas de la Revision</title>
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
	<p>Clasificar</p>
    </header>
	<form method="post" action="/clasificar">
	%fechaini=dict['fechaini']
	%fechafin=dict['fechafin']
	<table style="estilo"align="center">
	<tr>
		<td><strong>Fecha Inicio</strong></td>
		<td><strong>Fecha Fin</strong></td>
		<td></td>	
	</tr>
	<tr>
		<td><input type="date" name="FechaInicio" value={{fechaini}}></td>
		<td><input type="date" name="FechaFin" value={{fechafin}}></td>
		<td><input type="submit" class="estilo2" value="Enviar"></td>
		</form>		
	</tr>
	</table>
    
</body>
</html>