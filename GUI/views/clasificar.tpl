<!DOCTYPE html>
<html lang="es">
% include('menu.tpl', title='Clasificar')
	<form method="post" action="/clasificar">
	%fechaini=dict['fechaini']
	%fechafin=dict['fechafin']
<div id="paginacion">
	<div id="left">
	<table align="center">
	<tr>

		<td><strong>Fecha</strong></td>
		<td><strong>Total</strong></td>
		<td><strong>pendientes</strong></td>
		<td><strong>Fecha Clasificación</strong></td>
		<td><input type="submit" class="estilo2" value="Clasificar"></td>
	</tr>
	% count=0
	% for i in range(len(dict['fechaTweet'])):
	% fechatn='fechat'+str(i)
	%print dict['faltaTweet'][i]
	<tr>
	<td>{{dict['fechaTweet'][i]}}</td>
	<td>{{dict['totalTweet'][i]}}</td>
	<td>{{dict['faltaTweet'][i]}}</td>
	<td>{{dict['fechaClas'][i]}}</td>
	<td><input type="checkbox" name={{fechatn}} value="{{dict['fechaTweet'][i]}}"></td>
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
 </div>
 </div>


</body>
</html>
