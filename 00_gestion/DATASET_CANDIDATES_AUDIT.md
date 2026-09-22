# Auditoría de Datasets Candidatos

Este documento resume la auditoría de los datasets públicos propuestos para ampliar la generalización del detector de Oídio en hojas de vid.

## 1. Inventario por Dataset

### A. MD Nahid (Powdery Mildew.v1i.yolov11)
* **Cantidad total de imágenes:** 566
* **Positivas (Oídio):** 565
* **Negativas:** 1
* **Resolución:** Mínima 256x256, Máxima 800x1000, Mediana 256x256
* **Tipo de Tarea Original:** Segmentación (Instance Segmentation)
* **Formato de Anotación:** YOLO Polygon (polígonos de múltiples vértices normalizados).
* **Nombres de Clases:** `Powdery-Mildew`
* **Splits:** `train`, `valid`, `test` disponibles.

### B. HERMOS (j4xs3kh3fd-2)
* **Cantidad total de imágenes:** 982
* **Positivas (Oídio):** 522
* **Negativas (Otras clases/Fondo):** 460
* **Resolución:** Mínima 395x710, Máxima 6000x4000, Mediana 6000x4000 (Alta Resolución / 24 Megapíxeles)
* **Tipo de Tarea Original:** Object Detection
* **Formato de Anotación:** Pascal VOC XML
* **Nombres de Clases:** `powdery mildew`, `downy mildew`, `dead arm`, `healthy`, `dog`
* **Splits:** Única carpeta `Images`, sin particiones predefinidas.

### C. Portugal
* **Cantidad total de imágenes:** 1126 (solo clase Powdery Mildew auditada)
* **Resolución:** Constante en 1024x1024 (Mediana 1024x1024)
* **Tamaño de archivo:** Mínimo 75.8 KB, Máximo 191.1 KB, Mediana 129.1 KB
* **Tipo de Tarea Original:** Clasificación (organizado en carpetas por patología)
* **Formato de Anotación:** Solo a nivel de imagen (sin bounding boxes/polígonos nativos)
* **Nombres de Clases Disponibles:** `Powdery Mildew`, `Downy Mildew`, `Erineum Mite`, `Esca Complex`, `Healthy`
* **Splits:** Todo agrupado en la carpeta `resized/Powdery Mildew`, sin particiones predefinidas.

---

## 2. Duplicados y Linaje (Data Leakage Check)
Se ejecutó un análisis de `hash exacto` (MD5) y `perceptual hash` (pHash, distancia máxima = 3) comparando los candidatos contra las 8.207 imágenes del `dataset_detect_field` actual, y entre sí:

* **MD Nahid vs dataset_detect_field:** 0 exactos, 0 near-duplicates.
* **HERMOS vs dataset_detect_field:** 0 exactos, **90 near-duplicates**. (Evidencia de que una porción de imágenes de HERMOS fue utilizada para componer el dataset base en el pasado, probablemente aplicándoles transformaciones o compresión).
* **MD Nahid vs HERMOS:** 0 exactos, 0 near-duplicates.
* **Portugal vs (dataset_detect_field, HERMOS, MD Nahid):** 0 exactos, 0 near-duplicates. (100% independiente).

---

## 3. Semántica de Anotación (Inspección Visual)

### MD Nahid
* **Geometría:** Polígonos convertibles a Bounding Boxes. Mediana de área envolvente: **1.39%** de la imagen (p75 = 2.57%).
* **Observación Visual:**
  - Las imágenes corresponden efectivamente a hojas de vid reales (muchas de ellas sostenidas por la mano del operario o fotografiadas de cerca en el campo).
  - Los polígonos **rodean regiones sintomáticas extensas/difusas**, no la hoja completa.
  - **Conversión:** Es 100% seguro y matemáticamente trivial convertirlos a Bounding Boxes envolventes (tomando min/max de las coordenadas X e Y) para nuestro pipeline de detección.

### HERMOS
* **Geometría:** Bounding Boxes. Mediana de área: **0.21%** de la imagen (p75 = 0.26%). El 0% de las anotaciones supera el 40% del frame.
* **Observación Visual:**
  - La clase es explícitamente `powdery mildew`.
  - Las cajas rodean **lesiones extremadamente puntuales, diminutas o tenues** sobre la superficie de la hoja, fotografiadas desde lejos (a nivel de canopia).
  - **No hay hojas completas anotadas**, el criterio es puramente la mancha sintomática fina, lo cual es altamente consistente con nuestro `dataset_detect_field` pero a una escala mucho menor.

---

## 4. Valor Añadido (Diagnóstico Potencial)

¿Qué aporta cada dataset que no esté bien representado y cómo ayuda con los Falsos Negativos del EXP-YOLO-EXT-002?

**1. MD Nahid:**
* **Valor:** *Fondos complejos y diversidad de dominio (manos, ángulos).*
* **Impacto en Falsos Negativos:** Muchas de nuestras fallas externas ocurrieron por diferencias de iluminación o texturas atípicas del fondo. MD Nahid introduce mucha variabilidad de capturas con celular/cámara manual, ayudando al modelo a desvincular el síntoma de oídio del "fondo de viñedo estándar" que ya memorizó.

**2. HERMOS:**
* **Valor:** *Síntomas tenues, difusos y resolución masiva.*
* **Impacto en Falsos Negativos:** Aporta la capacidad de detectar los inicios sutiles de la enfermedad ("polvillo" incipiente), algo que el modelo actual falló en percibir (e.g., la imagen 4 requirió bajar a conf=0.25 para ser apenas intuida). Incorporar cajas tan pequeñas forzará a la red a no depender exclusivamente de la gran mancha blanca y densa, mejorando la sensibilidad (Recall).

**3. Portugal:**
* **Valor:** *[PENDIENTE DE REVISIÓN VISUAL]* (Dataset masivo de clasificación a 1024x1024).
* **Impacto en Falsos Negativos:** *[PENDIENTE DE REVISIÓN VISUAL]*

---

## 5. Salidas Generadas
Las subcarpetas en `00_gestion/dataset_candidates_audit/` contienen un muestreo aleatorio de 25 imágenes (`sample_0.jpg` a `sample_24.jpg`) procesadas con las cajas superpuestas (Ground Truth) para verificación cualitativa offline.
