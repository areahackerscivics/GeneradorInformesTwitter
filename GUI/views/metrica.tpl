<!DOCTYPE html>
<html lang="es">
<head>
<title>Métricas de la Revision</title>
<style type="text/css">
div#paginacion {
  border: 1px solid #CCC;
  padding: .5em;
}
.derecha {
  float: right;
}
.izquierda {
  float: left;
}
div.clear {
  clear: both;
}
</style>
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
	<form method="post" action="/metrica">
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
		<td><input type="submit" class="estilo2" value="Listar"></td>
		</form>
	</tr>
	</table>
<script src="/js/Chart.js"></script>
<div id="paginacion">
<div id="pieChart" class="derecha"></div>

<script src="/js/d3.min.js"></script>
<script src="/js/d3pie.js"></script>
<script>
var pie = new d3pie("pieChart", {
	"header": {
		"title": {
			"text": "Clasificación",
			"fontSize": 23,
			"font": "open sans"
		},
		"subtitle": {
			"text": "Muestra en porcentaje los estados de "+{{dict['Total'][0]}}+" tweets revisados",
			"color": "#999999",
			"fontSize": 15,
			"font": "open sans"
		},
		"titleSubtitlePadding": 6
	},
	"footer": {
		"color": "#999999",
		"fontSize": 10,
		"font": "open sans",
		"location": "bottom-left"
	},
	"size": {
		"canvasWidth": 590,
		"pieOuterRadius": "53%"
	},
	"data": {
		"sortOrder": "value-desc",
		"content": [
			{
				"label": "Modificados",
				"value": {{dict['TotalR'][0]}},
				"color": "#2484c1"
			},
			{
				"label": "Descartados",
				"value": {{dict['TotalD'][0]}},
				"color": "#cb2121"
			},
			{
				"label": "Correctos",
				"value": {{dict['TotalC'][0]}},
				"color": "#86f71a"
			}
		]
	},
	"labels": {
		"outer": {
			"pieDistance": 10
		},
		"inner": {
			"hideWhenLessThanPercentage": 3
		},
		"mainLabel": {
			"fontSize": 11
		},
		"percentage": {
			"color": "#ffffff",
			"decimalPlaces": 0
		},
		"value": {
			"color": "#adadad",
			"fontSize": 11
		},
		"lines": {
			"enabled": true
		},
		"truncation": {
			"enabled": true
		}
	},
	"effects": {
		"pullOutSegmentOnClick": {
			"effect": "linear",
			"speed": 400,
			"size": 8
		}
	},
	"misc": {
		"gradient": {
			"enabled": true,
			"percentage": 100
		},
		"canvasPadding": {
			"top": 2,
			"left": 5
		}
	}
});
</script>

<div id="left">
	<table align="center">
	<tr>

		<td><strong>Categoría</strong></td>
		<td><strong>Descartados (%)</strong></td>
		<td><strong>Modificados(%)</strong></td>
		<td><strong>Correctos(%)</strong></td>
		<td><strong>Total</strong></td>
	</tr>
	% for i in range(len(dict['cat'])):
		<tr>
		<td>{{dict['cat'][i]}}</td>
		<td>{{dict['D'][i]}}</td>
		<td>{{dict['R'][i]}}</td>
		<td>{{dict['C'][i]}}</td>
		<td>{{dict['SubTC'][i]}}</td>
		</tr>
	% end
</table>
 </div>
 </div>
</body>
</html>
