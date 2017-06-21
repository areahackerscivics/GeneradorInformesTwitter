<!DOCTYPE html>

<html>
  <head>
    <title>ERROR</title>
    <link rel="stylesheet" type="text/css" href="/css/main.css">
    <script type="text/javascript" src="/js/error.js"></script>
  </head>
  <body>
    % mensaje = error
    % pagina = '/' + pagina
    <form name="error" action="{{pagina}}" method="GET">

      <h1>
        {{mensaje}}
      </h1>

      <input type="submit" value="Ok" />
    </form>

  </body>
</html>
