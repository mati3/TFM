### <div style="text-align: center">Trabajo Fin de Máster <div/>

### <div style="text-align: center">En el Máster de Ingeniería Informática <div/>

# <div style="text-align: center">Consultas Biomédicas mediante Minería de Textos <div/>

## <div style="text-align: center">***Desarrollo de una herramienta experimental para crear consultas biomédicas mediante minería de textos.*** <div/>

- Esta aplicación evalua la calidad de un conjunto de documentos. Tenemos tres tipos de archivos:

        FVS. Conjuntos de validación.
        FDS. Conjuntos de test.
        TIS. Conjuntos de identificación de terminos.

- En el espacio de trabajo de un usuario se pueden incluir tantos conjuntos de documentos como se quiera. Cada conjunto contiene un archivo positivo y otro negativo. 

- Primero se incluye el positivo. Una vez que los archivos se suban al servidor serán indexados.

- Para que la aplicación pueda indexar los archivos han estar escritos en texto plano (.txt), se guardará el título, abstract y palabras claves de cada documento, han de tener el siguiente formato:

        El título empieza por 'ST  -'
        La linea del abstract comienza por 'AB -'
        La linea de las palabras clave comienza con 'KW  -'

- Si existe una de las partes del documento que hemos nombrado, se indexará.

- Para evaluar un conjunto de documentos (FDS o FVS), tendremos que seleccionar un par de archivos TIS, decidir cuantos términos formará nuestra consulta y elegír uno de los filtros.

- Una vez tengamos formada la consulta podremos evaluar el conjunto de documentos que seleccionemos. Tendremos la posivilidad de incluir a la consulta el operador booleano AND, en tal caso, todos los terminos tendran que estar en el mismo documento. 

- Si no se puede calcular alguna medida de rendimiento, la aplicación devolverá el valor 0.

- Independientemente se pueden hacer busquedas de texto en pares de archivos FVS y FDS.