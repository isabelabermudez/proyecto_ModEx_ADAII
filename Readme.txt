ModEx - Interfaz gráfica
=======================

Este proyecto contiene la interfaz gráfica para el problema ModEx, creada en Python con Tkinter
sin dependencias externas.

Archivos importantes
--------------------
- red_social.py: modelos Agente y RedSocial; carga de entrada.
- calculos.py: funciones de costo, aporte, esfuerzo, extremismo y validación.
- soluciones.py: funciones modexFB y modexV. El punto modexPD queda preparado pero aún no implementado.
- gui.py: interfaz gráfica principal con Tkinter.
- generador.py: generador de casos.
- io_salida.py: lectura/escritura de archivos de entrada y salida.
- verificacion.py: comprobación de esfuerzo y validación del costo.
- main.py: lanzador de la aplicación.

Requisitos
----------
- Python 3.9 o superior.
- Solo usa la librería estándar de Python.

Ejecución
---------
1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta:
   python run_interface.py

Qué hace la interfaz
--------------------
- Cargar una red desde un archivo .txt.
- Abrir cualquiera de las pruebas de la carpeta "Bateria de pruebas".
- Ver la tabla de agentes con opinión, receptividad, influencia, costo y aporte.
- Ejecutar fuerza bruta y voraz.
- Mostrar resumen, tiempo de ejecución y validación del costo.
- Guardar salida en formato ModEx.
- Verificar una salida existente.
- Generar casos aleatorios, difíciles y fáciles.
- Exportar comparación a CSV.

Formato de entrada
------------------
La entrada debe ser así:

n
op_0, recep_0, inf_0
...
op_(n-1), recep_(n-1), inf_(n-1)
R_max

Ejemplo:
3
100, 0.5, 1
100, 0.1, 1
-10, 0.1, 1
55

Formato de salida
-----------------
La salida debe ser:

Ext
Esf
mod_0
mod_1
...
mod_(n-1)

Prueba de validación
--------------------
1. Carga la prueba Prueba1.txt.
2. Ejecuta el algoritmo Voraz.
3. Verifica que el esfuerzo y el extremismo coinciden con la lógica de calculos.py.
4. Guarda la salida y vuelve a cargarla para comprobar que la verificación detecta consistencia.

Nota
----
La programación dinámica quedará preparada para que tú la implementes después; la interfaz ya está diseñada para integrarla sin reescribir la estructura general.
