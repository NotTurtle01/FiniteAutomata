# FiniteAutomata
A quick script to read and process finite automata.

-- INSTRUCCIONES DE EJECUCIÓN --

-----------------------------------------------------------------------------------------------------
1 - Lectura de ficheros con el formato de Autómata de Estados Finitos (Determinista o No Determinista).

Ejecutar <class_automata.py> por línea de comandos y/o IDE y seguir las instrucciones del menú principal del programa. 

Para facilitar la lectura de archivos de texto plano se emplea el módulo "os" de Python. 
Se recomienda instalar dicho módulo mediante el comando <pip install os> para que el programa 
pueda agregar rápidamente la ruta al camino relativo que el usuario escribirá por pantalla.

El archivo <aut_cajero.txt> sirve como ejemplo para comprobar que el programa carga bien los ficheros. Recuerde tenerlo en el mismo directorio que
<class_automata.py>, o por el contrario tendrá que especificar la ruta desde el directorio en el que se encuentre en terminal. También puede contar 
con ejDefinicion.txt como archivo de prueba.

Recuerde que los archivos a ser leídos deberán mantener el siguiente formato de autómata para que se puedan leer y procesar:

    #número total de estados estado1 estado2 …
    #número de estados finales estadoFinal1 estadoFinal2 …
    #número total de símbolos del alfabeto simbolo1 simbolo2 … símbolo n
    --TABLA DE TRANSICIONES--
    TANTAS FILAS COMO ESTADOS
    TANTAS COLUMNAS COMO SÍMBOLOS DEL ALFABETO + 1 (cadena vacía). 
    Cada columna finaliza con el símbolo #

-----------------------------------------------------------------------------------------------------
2 - Escritura de cadenas.

Respecto al resto de símbolos del alfabeto, recuerde respetar lo especificado en la línea 3 del archivo leído. En cualquier otro caso, obtendrá
un error como respuesta. 
