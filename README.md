# Clasificador PLN de mensajes estudiantiles

Este proyecto implementa una aplicación local de procesamiento de lenguaje natural orientada a la clasificación de mensajes estudiantiles. Permite escribir o cargar mensajes, limpiar el texto, extraer tokens útiles, identificar la intención del mensaje, estimar el sentimiento y sugerir una prioridad de atención desde una interfaz gráfica ejecutable en VSCode.

Python se encarga de normalizar el texto, aplicar una representación TF-IDF, entrenar clasificadores con ejemplos internos y complementar la decisión con reglas lingüísticas simples. La salida se muestra en pantalla y también puede exportarse a CSV cuando se analizan varios mensajes.

## Propósito

La app está pensada para convertir mensajes breves de estudiantes en una señal operativa útil. En lugar de revisar manualmente cada comentario, solicitud o queja, el usuario puede procesar el texto y obtener una clasificación inicial que ayude a decidir si el caso corresponde a apoyo académico, trámite administrativo, bienestar estudiantil, problema técnico, felicitación, queja de servicio o consulta general.

No sustituye la revisión humana, la atención psicológica, el seguimiento administrativo ni un sistema institucional formal. Su valor está en mostrar un flujo completo y funcional de PLN clásico: limpieza textual, tokenización, vectorización, clasificación, interpretación básica y exportación de resultados.

## Qué hace

- limpia y normaliza texto en español
- elimina ruido básico como enlaces, correos y signos innecesarios
- tokeniza mensajes y filtra palabras vacías
- clasifica la intención del mensaje
- estima sentimiento positivo, neutral o negativo
- calcula prioridad baja, media o alta
- recomienda una acción inicial de seguimiento
- permite análisis individual desde una interfaz gráfica
- permite análisis masivo con archivos TXT o CSV
- exporta resultados a CSV
- muestra métricas internas del prototipo

## Categorías compatibles

El clasificador trabaja con siete categorías principales:

- `apoyo_academico`
- `tramite_administrativo`
- `bienestar_estudiantil`
- `problema_tecnico`
- `felicitacion`
- `queja_servicio`
- `consulta_general`

El sentimiento se clasifica como:

- `positivo`
- `neutral`
- `negativo`

## Arquitectura general

La solución está organizada en cuatro capas funcionales.

### Interfaz

La interfaz está construida con Tkinter y concentra en una sola ventana:

- análisis individual
- análisis por archivo
- tabla de resultados
- exportación a CSV
- panel de evaluación interna
- sección de ayuda

### Procesamiento textual

La lógica de PLN está implementada en Python. Esta capa resuelve:

- conversión a minúsculas
- eliminación de acentos
- eliminación de URLs y correos
- limpieza de caracteres no relevantes
- tokenización
- filtrado de palabras vacías
- conteo de palabras útiles y palabras únicas

### Modelo de clasificación

El sistema usa un enfoque híbrido:

- TF-IDF por palabras y n-gramas
- TF-IDF por caracteres para tolerar variaciones pequeñas de escritura
- clasificador Complement Naive Bayes
- reglas lingüísticas de apoyo para términos críticos y categorías frecuentes

Este diseño mantiene el programa ligero, ejecutable en una computadora común y adecuado para una práctica académica de PLN sin requerir modelos grandes ni conexión a servicios externos.

### Interpretación y priorización

Después de clasificar el mensaje, el sistema estima prioridad con base en intención, sentimiento y términos urgentes. También muestra palabras relevantes y una acción recomendada para orientar el seguimiento.

## Estructura del proyecto

    clasificador-pln-mensajes-estudiantiles/
    ├─ app.py
    ├─ README.md
    ├─ LICENSE.md
    ├─ requirements.txt
    ├─ .gitignore
    ├─ examples/
    │  ├─ mensajes_demo.csv
    │  └─ mensajes_demo.txt
    ├─ scripts/
    │  └─ prueba_rapida.py
    └─ src/
       ├─ __init__.py
       ├─ datos_entrenamiento.py
       ├─ interfaz.py
       ├─ modelo_pln.py
       └─ procesamiento_texto.py

## Responsabilidades por módulo

- `app.py`: punto de entrada de la aplicación
- `src/interfaz.py`: construcción de la interfaz gráfica y eventos de usuario
- `src/modelo_pln.py`: entrenamiento, clasificación, priorización y métricas internas
- `src/procesamiento_texto.py`: limpieza, normalización y tokenización
- `src/datos_entrenamiento.py`: ejemplos internos para entrenar el prototipo
- `examples/`: archivos de prueba para análisis masivo
- `scripts/prueba_rapida.py`: validación rápida por terminal

## Dependencias principales

- Python 3.11 o superior
- Tkinter
- scikit-learn

Tkinter suele venir incluido con Python en Windows. La única dependencia externa requerida por el proyecto es `scikit-learn`.

## Requisitos de ejecución

Para ejecutar el proyecto se recomienda:

- tener Python instalado
- abrir la carpeta en VSCode
- crear un entorno virtual
- instalar dependencias desde `requirements.txt`

## Instalación

### 1. Crear y activar el entorno virtual

En PowerShell, desde la carpeta del proyecto:

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1

Si PowerShell bloquea la activación, ejecutar una vez:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Después volver a activar el entorno.

### 2. Actualizar pip

    python -m pip install --upgrade pip

### 3. Instalar dependencias

    pip install -r requirements.txt

### 4. Ejecutar la aplicación

    python app.py

## Uso de la aplicación

### Análisis individual

1. Abrir la aplicación.
2. Escribir o pegar un mensaje estudiantil.
3. Presionar `Analizar texto`.
4. Revisar intención, sentimiento, prioridad, tokens y acción recomendada.

### Análisis por archivo

1. Ir a la pestaña `Análisis por archivo`.
2. Cargar un archivo `.txt` con un mensaje por línea o un archivo `.csv` con columna `texto`.
3. Revisar la tabla de resultados.
4. Guardar los resultados en CSV si se requiere evidencia.

## Formato de archivo CSV

El archivo CSV recomendado debe tener una columna llamada `texto`.

Ejemplo:

    texto
    No puedo subir mi tarea a la plataforma.
    La explicación de la clase fue excelente.
    Quisiera saber la fecha de entrega.

## Flujo técnico de extremo a extremo

1. el usuario escribe o carga un mensaje
2. el sistema normaliza el texto
3. se eliminan acentos, enlaces, correos y caracteres no relevantes
4. el texto se tokeniza y se filtran palabras vacías
5. el vectorizador TF-IDF convierte el texto en variables numéricas
6. el clasificador estima intención y sentimiento
7. las reglas lingüísticas refuerzan casos críticos o muy evidentes
8. el sistema calcula prioridad
9. se genera una acción recomendada
10. la interfaz muestra los resultados o los exporta a CSV

## Archivos de ejemplo

La carpeta `examples/` incluye archivos listos para validar la app:

- `mensajes_demo.txt`
- `mensajes_demo.csv`

Estos ejemplos permiten probar tanto el análisis individual como el análisis por lote.

## Pruebas y validación

Para ejecutar una prueba rápida desde terminal:

    python scripts\prueba_rapida.py

La pestaña `Evaluación` muestra una validación funcional interna sobre los ejemplos incluidos. Esta métrica sirve para verificar que el prototipo está procesando correctamente los casos de demostración, pero no debe confundirse con una validación externa sobre datos reales no vistos.

## Notas importantes

- el programa funciona de forma local
- no requiere conexión a internet después de instalar dependencias
- no usa APIs externas
- no procesa datos sensibles de forma remota
- los datos reales deben anonimizarse antes de usarse
- las predicciones deben revisarse por una persona cuando la prioridad sea alta

## Consideraciones de rendimiento

El programa es ligero. En una computadora común, el entrenamiento inicial y la clasificación de mensajes cortos deben ejecutarse en pocos segundos. Para archivos muy grandes, conviene analizarlos por lotes moderados y guardar resultados progresivamente.

## Limitaciones conocidas

- el conjunto de entrenamiento interno es pequeño
- el prototipo no comprende ironía ni contexto institucional profundo
- las reglas pueden favorecer términos explícitos sobre mensajes ambiguos
- la precisión real depende de recolectar mensajes auténticos y anonimizados
- no sustituye atención humana ni decisiones institucionales formales

## Casos de uso recomendados

- clasificación inicial de comentarios estudiantiles
- práctica académica de PLN clásico
- demostración de TF-IDF y clasificación de texto
- priorización básica de solicitudes
- análisis rápido de encuestas abiertas
- prototipado de herramientas de atención estudiantil

## Resultado esperado

El resultado esperado es una herramienta local, sencilla y funcional que permite pasar de texto libre a una clasificación interpretable, con intención, sentimiento, prioridad y acción recomendada. El proyecto cumple como producto mínimo viable de procesamiento de lenguaje natural porque integra limpieza textual, vectorización, modelo de clasificación, reglas de apoyo, interfaz gráfica y exportación de resultados.

## About

Aplicación local de procesamiento de lenguaje natural en Python para clasificar mensajes estudiantiles, estimar sentimiento, priorizar atención y exportar resultados desde una interfaz gráfica con Tkinter.

## Topics

`python` `nlp` `pln` `text-classification` `sentiment-analysis` `tf-idf` `scikit-learn` `tkinter` `machine-learning` `spanish-nlp` `student-support` `desktop-app`

## Licencia

Este proyecto se distribuye bajo licencia GPL-3.0. Consulta `LICENSE.md`.
