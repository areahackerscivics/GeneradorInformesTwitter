<!DOCTYPE html>
<html lang="es">
% include('menu.tpl', title='Clasificar')
	<form method="post" action="/clasificar">
	%fechaini=dict['fechaini']
	%fechafin=dict['fechafin']
<div id="paginacion">
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

	</tr>
	</table>
	
	<div id="left">
	<table align="center">
	<tr>

		<td><strong>Fecha Descarga de Tweet</strong></td>
		<td><strong>Nro de Tweets</strong></td>
		<td><strong>Tweets No clasificados</strong></td>
		<td><strong>Fecha Clasificación</strong></td>
	</tr>
	% for i in range(len(dict['fechaTweet'])):
		<tr>
		<td>{{dict['fechaTweet'][i]}}</td> 
		<td>{{dict['totalTweet'][i]}}</td>
		<td>{{dict['faltaTweet'][i]}}</td>
		<td>{{dict['fechaClas'][i]}}</td>
		</tr>		
	% end
</table>
</form>		
 </div> 
 </div> 
	
    
</body>
</html>