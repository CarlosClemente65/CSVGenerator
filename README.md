# CSVGenerator
## Programa para generar Codigos Seguros de Verificacion (CSV)

### Desarrollado por Carlos Clemente (10-2023) version 1.0

Instrucciones:
- Si no se pasa ningun parametro, el CSV se generara con una longitud de 20 caracteres
  que incluye una cadena aleatoria de 8 caracteres, una marca de tiempo y los ultimos
  dos caracteres seran los digitos de control para garantizar que el codigo es correcto.
- Con el parametro -c se puede pasar un codigo CSV y comprobara si es correcto, 
  devolviendo la fecha y hora de generacion.
- Con el parametro -h me muestra la ayuda de ejecucion
- Con una longitud de 8 caracteres en el codigo aleatorio, se generan alrededor de 1,5 billones
  de combinaciones posibles, por lo que aunque se generasen varios codigos en el mismo segundo,
  los caracteres aleatorios haran que sea practicamente imposible que se generen dos CSV iguales.
  
