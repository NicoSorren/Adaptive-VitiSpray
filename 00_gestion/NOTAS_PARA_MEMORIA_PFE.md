# Notas para la Memoria del PFE

*Este documento es un registro estructurado y acumulativo de hallazgos técnicos, decisiones metodológicas y resultados clave que probablemente deban incorporarse en la memoria final del Proyecto Final de Estudios. No es una bitácora diaria.*

## 1. Evolución del planteo

## 2. Arquitectura general del sistema
- Se ha adoptado un enfoque de **dos pasadas** (two-pass approach).
- **Primera pasada:** Consiste en el scouting, donde el sistema de visión artificial (YOLO) realiza la detección y localización de enfermedades para generar el mapa de prescripción.
- **Segunda pasada:** Aplicación selectiva basada en el mapa.
- **Flujo:** Detección de síntomas (YOLO) → Evaluación en el Modelo de Riesgo Epidemiológico → Generación del Mapa de Prescripción → Actuación (Pulverización selectiva).
- El sistema de visión por sí solo NO ordena directamente la pulverización; actúa como sensor del estado actual.

## 3. Sistema de visión artificial
- **Evolución:** Se comenzó abordando un problema multiclase de enfermedades de vid. Posteriormente, se simplificó a un modelo **monoclase** enfocado exclusivamente en Oídio (Powdery Mildew).
- **Resultados Preliminares:** El experimento monoclase mostró mejoras evidentes en Precision, Recall, mAP50 y mAP50-95 respecto al experimento multiclase comparable (aunque no se debe exagerar la conclusión de forma absoluta dado que los entrenamientos tuvieron cantidades de épocas diferentes).

## 4. Datasets y preparación de datos

### Dataset `detect_field`
- Es un dataset curado que combina dos fuentes:
  - Dataset de Roboflow ("Final Grape Leaf Disease Detection..."). Aporta ~6955 imágenes.
  - Dataset de Cerdeña, Italia (Ghiani et al., "Downy Mildew and Powdery Mildew Symptoms"). Aporta ~1336 imágenes tras el filtrado estricto.
- **Filtros aplicados:** Se excluyeron explícitamente todas las imágenes de macetas y viveros (`piantine`, `vaso`) del dataset italiano para asegurar que el modelo se entrene exclusivamente con contextos de campo real.
- **Unificación de clases:** Todas las clases de oídio se mapearon a la clase 0 (`Powdery_Mildew`), y el resto de patologías/imágenes sanas se mantuvieron como background (imágenes negativas).

### Semántica de las Bounding Boxes (Cajas delimitadoras)
- Las bounding boxes representan **regiones sintomáticas visibles**, NO hojas enteras ni necesariamente "una lesión elemental individual".
- No existe una equivalencia estricta de "1 bbox = 1 hoja afectada".
- **Discrepancia entre fuentes:** El dataset de Roboflow tiende a anotar cajas pequeñas y discretas. El dataset italiano presenta variabilidad, desde regiones pequeñas hasta cajas que abarcan gran parte de la canopia o tejido afectado.
- **Conclusión metodológica:** Debido a esta semántica heterogénea, **NO se debe interpretar directamente el área sumada o la cantidad de bboxes como una métrica directa de severidad agronómica** de la enfermedad.

### Data leakage (Fuga de datos)
- Se realizó una auditoría rigurosa mediante hashing perceptual para detectar imágenes duplicadas entre splits.
- Solo se encontró un (1) duplicado exacto entre train y valid en el dataset italiano. No se detectó leakage significativo, asegurando la validez de las métricas de validación/test.

### Test set
- El conjunto de test actual contiene exclusivamente imágenes de la fuente de Roboflow.
- El dataset italiano solo participa en los conjuntos de entrenamiento (train) y validación (valid).
- **Pendiente:** Queda pendiente evaluar el modelo en un test set externo independiente (por ejemplo, reservando imágenes italianas) o, preferentemente, un test set de campo propio adquirido para el proyecto.

## 5. Experimentos YOLO

## 6. Hallazgos y correcciones metodológicas

### Corrección del problema de escala
- Inicialmente se formuló la hipótesis (basada en el área porcentual de los GT) de que las bounding boxes en imágenes de altísima resolución (4032x3024) colapsaban a tamaños subpíxel (1–8 px) al escalar la imagen a `imgsz=640` para la inferencia, volviéndose indetectables.
- **Corrección:** Un análisis geométrico exacto de las 11.399 bboxes con coordenadas reales desmintió esto. La gran mayoría de los objetos en la resolución de inferencia son de tamaño medio (`medium`) o grande (`large`). Incluso en las imágenes de 4032x3024, el objeto más pequeño medía 23 px tras el letterbox.
- **Conclusión:** `imgsz=640` se mantiene como un baseline razonable. Aumentar a `imgsz=800` queda como un experimento de optimización general, no como una solución obligatoria para "small-object detection". La falla de detección en imágenes de tan alta resolución probablemente se deba a la incapacidad del modelo para generalizar ante contextos visuales (textura, nivel de detalle del follaje) drásticamente diferentes a los de su conjunto de entrenamiento dominante (256px y 720px).

## 7. Modelo de riesgo epidemiológico
- Se plantea desarrollar un Producto Mínimo Viable (MVP) paramétrico y simplificado.
- Existe una separación conceptual entre la **dispersión espacial** (vectores) y la **favorabilidad ambiental** (clima).
- **Limitación declarada:** Los parámetros iniciales del modelo de riesgo NO se considerarán constantes epidemiológicas validadas. La futura incorporación o calibración deberá hacerse contrastando con la literatura agronómica específica sobre *Erysiphe necator*.

## 8. Mapa de prescripción
- **Decisión provisional de tratamiento:** Una detección visual identifica un *foco*. La estrategia de pulverización no debe limitarse a asperjar únicamente la coordenada exacta del bbox detectado. Debe contemplar el tratamiento de la planta completa afectada y las zonas adyacentes potencialmente expuestas.

## 9. Simulación
- **Herramienta:** **Webots** ha sido elegido como el candidato principal para el entorno de simulación.
- **Objetivo:** Representar la segunda pasada del sistema: la navegación, la localización del robot y la actuación de los pulverizadores (spray ON/OFF) basada en el mapa de prescripción previamente generado.
- Estado: Pendiente de implementación.

## 10. Limitaciones conocidas

## 11. Trabajo futuro

## 12. Resultados que podrían incluirse en la memoria
