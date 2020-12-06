### <div style="text-align: center">Trabajo Fin de Máster <div/>

### <div style="text-align: center">En el Máster de Ingeniería Informática <div/>

# <div style="text-align: center">Consultas Biomédicas mediante Minería de Textos <div/>

## <div style="text-align: center">***Desarrollo de una herramienta experimental para crear consultas biomédicas mediante minería de textos.*** <div/>

- Esta aplicación evalúa la calidad de una serie de consultas que se generan a partir del método se selección de términos. Tenemos tres tipos de archivos:

        FVS. Conjuntos de validación.
        FDS. Conjuntos de test.
        TIS. Conjuntos de identificación de términos.

- En el espacio de trabajo de un usuario se pueden incluir tantos conjuntos de documentos como se quiera. Cada conjunto contiene un archivo positivo y otro negativo. 

- Primero se incluye el positivo. Una vez que los archivos se suban al servidor serán indexados.

- Para que la aplicación pueda indexar los archivos han estar escritos en texto plano (.txt), se guardará el título, abstract y palabras claves de cada documento, han de tener el siguiente formato:

        El título empieza por 'ST  -'
        La linea del abstract comienza por 'AB -'
        La linea de las palabras clave comienza con 'KW  -'

- Si existe una de las partes del documento que hemos nombrado, se indexará.

- Para evaluar un conjunto de documentos (FDS o FVS), tendremos que seleccionar un par de archivos TIS, decidir cuantos términos formará nuestra consulta y elegir uno de los filtros.

- Una vez tengamos formada la consulta podremos evaluar el conjunto de documentos que seleccionemos. Tendremos la posibilidad de incluir a la consulta el operador booleano AND, en tal caso, todos los términos tendrán que estar en el mismo documento. 

- Si no se puede calcular alguna medida de rendimiento, la aplicación devolverá el valor 0.

- Independientemente se pueden hacer búsquedas de texto en pares de archivos FVS y FDS.

- ***Autor:*** Matilde Cabrera González
- ***Tutor:*** Juan Manuel Fernandez Luna


- Documentación 

        Angular en ruta: frontend/documentation/index.html
        Filtros en ruta: backendfile/pdoc/filtros.m.html
        Pylucene en ruta: backendfile/pdoc/recuperacionInformacion.m.html
        Medidas de rendimiento en ruta: backendfile/pdoc/rendimiento.m.html


### <div style="text-align: center">Master's thesis <div/>

### <div style="text-align: center">In the Master of Computer Engineering <div/>

# <div style="text-align: center">Biomedical Consultation through Text Mining

## <div style="text-align: center">***Development of an experimental tool to create biomedical consultations through text mining.*** <div/>

- This application evaluates the quality of a set of documents. We have three types of files:

        FVS. Validation sets.
        SDS. Test sets.
        TIS. Term identification sets.

- A user's workspace can include as many sets of documents as desired. Each set contains one positive and one negative file. 

- The positive is included first. Once the files are uploaded to the server they will be indexed.

- For the application to index the files have to be written in plain text (.txt), the title, abstract and keywords of each document will be saved, they have to have the following format:

        The title starts with 'ST -'.
        The line of the abstract begins with 'AB -'.
        The keyword line begins with 'KW -'.

- If one of the parts of the document we have named exists, it will be indexed.

- To evaluate a set of documents (SDS or FVS), we will have to select a couple of TIS files, decide how many terms will form our query and choose one of the filters.

- Once the query has been formed we can evaluate the set of documents we have selected. It is possible to include the Boolean operator AND in the query, in which case all the terms must be in the same document. 

- If any performance measure cannot be calculated, the application will return the value 0.

- Independently, text searches can be made on pairs of FVS and FDS files.
