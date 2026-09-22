# Notas para la Memoria del PFE

*Este documento es un registro estructurado y acumulativo de hallazgos tÃ©cnicos, decisiones metodolÃ³gicas y resultados clave que probablemente deban incorporarse en la memoria final del Proyecto Final de Estudios. No es una bitÃ¡cora diaria.*

## 1. EvoluciÃ³n del planteo

## 2. Arquitectura general del sistema
- Se ha adoptado un enfoque de **dos pasadas** (two-pass approach).
- **Primera pasada:** Consiste en el scouting, donde el sistema de visiÃ³n artificial (YOLO) realiza la detecciÃ³n y localizaciÃ³n de enfermedades para generar el mapa de prescripciÃ³n.
- **Segunda pasada:** AplicaciÃ³n selectiva basada en el mapa.
- **Flujo:** DetecciÃ³n de sÃ­ntomas (YOLO) â†’ EvaluaciÃ³n en el Modelo de Riesgo EpidemiolÃ³gico â†’ GeneraciÃ³n del Mapa de PrescripciÃ³n â†’ ActuaciÃ³n (PulverizaciÃ³n selectiva).
- El sistema de visiÃ³n por sÃ­ solo NO ordena directamente la pulverizaciÃ³n; actÃºa como sensor del estado actual.

## 3. Sistema de visiÃ³n artificial
- **EvoluciÃ³n:** Se comenzÃ³ abordando un problema multiclase de enfermedades de vid. Posteriormente, se simplificÃ³ a un modelo **monoclase** enfocado exclusivamente en OÃ­dio (Powdery Mildew).
- **Resultados Preliminares:** El experimento monoclase mostrÃ³ mejoras evidentes en Precision, Recall, mAP50 y mAP50-95 respecto al experimento multiclase comparable (aunque no se debe exagerar la conclusiÃ³n de forma absoluta dado que los entrenamientos tuvieron cantidades de Ã©pocas diferentes).

## 4. Datasets y preparaciÃ³n de datos

### Dataset `detect_field`
- Es un dataset curado que combina dos fuentes:
  - Dataset de Roboflow ("Final Grape Leaf Disease Detection..."). Aporta ~6955 imÃ¡genes.
  - Dataset de CerdeÃ±a, Italia (Ghiani et al., "Downy Mildew and Powdery Mildew Symptoms"). Aporta ~1336 imÃ¡genes tras el filtrado estricto.
- **Filtros aplicados:** Se excluyeron explÃ­citamente todas las imÃ¡genes de macetas y viveros (`piantine`, `vaso`) del dataset italiano para asegurar que el modelo se entrene exclusivamente con contextos de campo real.
- **UnificaciÃ³n de clases:** Todas las clases de oÃ­dio se mapearon a la clase 0 (`Powdery_Mildew`), y el resto de patologÃ­as/imÃ¡genes sanas se mantuvieron como background (imÃ¡genes negativas).

### SemÃ¡ntica de las Bounding Boxes (Cajas delimitadoras)
- Las bounding boxes representan **regiones sintomÃ¡ticas visibles**, NO hojas enteras ni necesariamente "una lesiÃ³n elemental individual".
- No existe una equivalencia estricta de "1 bbox = 1 hoja afectada".
- **Discrepancia entre fuentes:** El dataset de Roboflow tiende a anotar cajas pequeÃ±as y discretas. El dataset italiano presenta variabilidad, desde regiones pequeÃ±as hasta cajas que abarcan gran parte de la canopia o tejido afectado.
- **ConclusiÃ³n metodolÃ³gica:** Debido a esta semÃ¡ntica heterogÃ©nea, **NO se debe interpretar directamente el Ã¡rea sumada o la cantidad de bboxes como una mÃ©trica directa de severidad agronÃ³mica** de la enfermedad.

### Data leakage (Fuga de datos)
- Se realizÃ³ una auditorÃ­a rigurosa mediante hashing perceptual para detectar imÃ¡genes duplicadas entre splits.
- Solo se encontrÃ³ un (1) duplicado exacto entre train y valid en el dataset italiano. No se detectÃ³ leakage significativo, asegurando la validez de las mÃ©tricas de validaciÃ³n/test.

### Test set
- El conjunto de test actual contiene exclusivamente imÃ¡genes de la fuente de Roboflow.
- El dataset italiano solo participa en los conjuntos de entrenamiento (train) y validaciÃ³n (valid).
- **Pendiente:** Queda pendiente evaluar el modelo en un test set externo independiente (por ejemplo, reservando imÃ¡genes italianas) o, preferentemente, un test set de campo propio adquirido para el proyecto.

## 5. Experimentos YOLO

## 6. Hallazgos y correcciones metodolÃ³gicas

### CorrecciÃ³n del problema de escala
- Inicialmente se formulÃ³ la hipÃ³tesis (basada en el Ã¡rea porcentual de los GT) de que las bounding boxes en imÃ¡genes de altÃ­sima resoluciÃ³n (4032x3024) colapsaban a tamaÃ±os subpÃ­xel (1â€“8 px) al escalar la imagen a `imgsz=640` para la inferencia, volviÃ©ndose indetectables.
- **CorrecciÃ³n:** Un anÃ¡lisis geomÃ©trico exacto de las 11.399 bboxes con coordenadas reales desmintiÃ³ esto. La gran mayorÃ­a de los objetos en la resoluciÃ³n de inferencia son de tamaÃ±o medio (`medium`) o grande (`large`). Incluso en las imÃ¡genes de 4032x3024, el objeto mÃ¡s pequeÃ±o medÃ­a 23 px tras el letterbox.
- **ConclusiÃ³n:** `imgsz=640` se mantiene como un baseline razonable. Aumentar a `imgsz=800` queda como un experimento de optimizaciÃ³n general, no como una soluciÃ³n obligatoria para "small-object detection". La falla de detecciÃ³n en imÃ¡genes de tan alta resoluciÃ³n probablemente se deba a la incapacidad del modelo para generalizar ante contextos visuales (textura, nivel de detalle del follaje) drÃ¡sticamente diferentes a los de su conjunto de entrenamiento dominante (256px y 720px).

## 7. Modelo de riesgo epidemiolÃ³gico
- Se plantea desarrollar un Producto MÃ­nimo Viable (MVP) paramÃ©trico y simplificado.
- Existe una separaciÃ³n conceptual entre la **dispersiÃ³n espacial** (vectores) y la **favorabilidad ambiental** (clima).
- **LimitaciÃ³n declarada:** Los parÃ¡metros iniciales del modelo de riesgo NO se considerarÃ¡n constantes epidemiolÃ³gicas validadas. La futura incorporaciÃ³n o calibraciÃ³n deberÃ¡ hacerse contrastando con la literatura agronÃ³mica especÃ­fica sobre *Erysiphe necator*.

## 8. Mapa de prescripciÃ³n
- **DecisiÃ³n provisional de tratamiento:** Una detecciÃ³n visual identifica un *foco*. La estrategia de pulverizaciÃ³n no debe limitarse a asperjar Ãºnicamente la coordenada exacta del bbox detectado. Debe contemplar el tratamiento de la planta completa afectada y las zonas adyacentes potencialmente expuestas.

## 9. SimulaciÃ³n
- **Herramienta:** **Webots** ha sido elegido como el candidato principal para el entorno de simulaciÃ³n.
- **Objetivo:** Representar la segunda pasada del sistema: la navegaciÃ³n, la localizaciÃ³n del robot y la actuaciÃ³n de los pulverizadores (spray ON/OFF) basada en el mapa de prescripciÃ³n previamente generado.
- Estado: Pendiente de implementaciÃ³n.

## 10. Limitaciones conocidas

## 11. Trabajo futuro

## 12. Resultados que podrÃ­an incluirse en la memoria

### Validación Externa (Conjunto Independiente)
- Se constituyó manualmente un conjunto externo de 19 imágenes (12 de Oídio, 4 de Peronospora, 3 Sanas).
- El test demostró robustez absoluta para rechazar falsos positivos frente a enfermedades confusoras como Peronospora y frente a tejido sano (0% FP).
- Sin embargo, la tasa cualitativa de detección fue baja (50% a conf=0.25), evidenciando dificultades del modelo para generalizar ante variabilidades fenotípicas ajenas a las distribuciones de Roboflow e Italia.
- Se propone provisionalmente un umbral de \conf=0.25\ que rescata detecciones sutiles sin comprometer la especificidad.


*Nota de Actualización (EXP-YOLO-EXT-002):* Una repetición de esta validación utilizando una muestra depurada del dominio correcto de hojas de vid arrojó un leve incremento en la tasa de detección (58.3%), sin alterar el absoluto rechazo de falsos positivos en clases perjudiciales. Esto confirma definitivamente a \conf=0.25\ como la frontera de decisión recomendada para la inferencia a campo en el MVP.


### Auditoría de Nuevos Dominios (HERMOS y MD Nahid)
- **MD Nahid:** Introdujo instancias de oídio delimitadas por polígonos que representan el 1.3% del frame. Se validó su idoneidad cualitativa para aumentar la variabilidad del fondo y de ángulos de captura, elementos que provocaron falsos negativos en el modelo base.
- **HERMOS:** Se reveló como un dataset de detección de alta resolución (24 MP) centrado en lesiones extremadamente pequeñas (mediana de 0.21%). Resulta invaluable para forzar al modelo a detectar inicios incipientes de enfermedad. Curiosamente, el pHash detectó 90 near-duplicates con \dataset_detect_field\, confirmando que una fracción de nuestro dataset histórico desciende del corpus de HERMOS.

- **Portugal:** Dataset de clasificación aportando 1126 imágenes estrictamente a 1024x1024 de resolución. Es 100% independiente (cero solapamiento con los otros conjuntos). Su aporte semántico a la robustez contra falsos negativos queda pendiente de inspección visual humana.

- **Portugal (Selecci�n):** Tras confirmar que los 2252 hallazgos originales eran un fallo de lectura de Windows ('case-insensitive globbing') y que el dataset contiene exactamente 1126 capturas �nicas tomadas entre agosto y octubre de 2025, se dise�� un algoritmo para seleccionar una submuestra representativa de 299 im�genes. Este algoritmo maximiz� la diversidad temporal (proporcionalidad por fecha) y visual (agrupamiento K-Means de contraste, brillo, entrop�a y color verde) para garantizar una base robusta para la posterior anotaci�n manual, eludiendo la redundancia visual.

- **Portugal (Revisi�n Visual):** De la selecci�n algor�tmica de 299 im�genes candidatas, 94 fueron descartadas en revisi�n manual por redundancia o ambig�edad visual. Las 205 im�genes resultantes fueron separadas para su futura anotaci�n manual bajo la directriz estricta de usar la etiqueta REJECTED_AMBIGUOUS frente a casos donde la frontera sintom�tica no sea concluyente.
