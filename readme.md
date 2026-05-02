# Experimento de cerillas (Knoblich et al., 1999)

Aplicación web para administrar una tarea de insight con ecuaciones romanas moviendo solo 1 cerilla por problema.

## Archivos del proyecto

- index.html: experimento completo para recogida de datos.
- demo.html: demo técnica del motor de cerillas.

## Que hace index.html

- Solicita codigo de participante.
- Presenta 8 problemas (2 bloques x 4 tipos: A, B, C y D).
- Permite mover una sola cerilla por intento.
- Cronometra cada problema (maximo 5 minutos).
- Permite comprobar, abandonar o reiniciar cerillas.
- Registra por problema:
  - participante
  - bloque
  - tipo
  - orden de presentacion
  - resuelto (S/N)
  - tiempo en segundos
  - observaciones
- Muestra resumen final en tabla y permite descargar CSV.

## Flujo basico de uso

1. Abrir index.html en el navegador.
2. Introducir el codigo del participante y pulsar Iniciar experimento.
3. En cada problema:
   - mover 1 cerilla
   - pulsar Comprobar (o Abandonar)
   - anotar observaciones cuando aparezca la ventana
   - pulsar Siguiente
4. Repetir hasta completar los 8 problemas.
5. En la pantalla de resultados, pulsar Descargar CSV.
6. Enviar el archivo CSV descargado al investigador.

## Importante para la recogida de datos

- Si se agota el tiempo (5:00), el problema se marca como no resuelto.
- Las observaciones se guardan por problema.
- El paso final obligatorio es descargar el CSV y enviarlo.

## Uso de demo.html

demo.html sirve para pruebas rapidas del motor visual y de validacion, sin flujo completo de experimento ni tabla final de resultados.
