# Catálogo de Datasets

Este directorio contiene todos los conjuntos de datos de imágenes, anotaciones y splits utilizados para el entrenamiento, validación y prueba de los modelos de visión artificial del PFE.

## Política de Datasets
- Los datasets públicos originales deben conservarse sin modificaciones siempre que sea posible.
- Las transformaciones deben generar una versión procesada separada.
- No mezclar datasets con políticas de anotación incompatibles sin revisión.
- Registrar versión y procedencia de cada dataset usado en un experimento.

---

## 1. Datasets Públicos (`publicos/`)

### Final Grape Leaf Disease Detection and Classification.v1i.yolov11
* **Tipo:** Público
* **Origen:** Roboflow Universe
* **URL:** [Roboflow Universe](https://universe.roboflow.com/nsorrentino2001-gmail-com/final-grape-leaf-disease-detection-and-classification-zjgha/dataset/1)
* **Licencia:** CC BY 4.0
* **Propósito:** Dataset de origen multi-enfermedad en espaldera y laboratorio.
* **Clases originales:** 3 (`Birds_Eye_Rot`, `Healthy`, `Powdery_Mildew`)
* **Cantidad de imágenes:** ~6,950
* **Formato de anotación:** YOLO (Bounding Boxes)
* **Resolución:** Mixta
* **Transformaciones:** Ninguna (Original)
* **Ubicación Actual:** `02_datasets/publicos/Final Grape Leaf Disease Detection...`

### Downy Mildew and Powdery Mildew Symptoms
* **Tipo:** Público
* **Origen:** *Pendiente de reconstruir*
* **URL:** *Pendiente de reconstruir*
* **Licencia:** *Pendiente de reconstruir*
* **Propósito:** Imágenes en campo abierto en Italia.
* **Clases:** *Pendiente de reconstruir*
* **Cantidad de imágenes:** *Pendiente de reconstruir*
* **Formato de anotación:** *Pendiente de reconstruir*
* **Resolución:** Alta
* **Transformaciones:** Ninguna (Original, formato ZIP)
* **Ubicación Actual:** `02_datasets/publicos/Downy Mildew and Powdery Mildew Symptoms`

---

## 2. Datasets Procesados (`procesados/`)

### dataset_detect_field
* **Tipo:** Procesado
* **Origen:** Mezcla de "Final Grape Leaf..." y "Downy Mildew...". Generado por `prepare_detection_dataset.py`.
* **Propósito:** Dataset principal balanceado y estandarizado para entrenar detección (bboxes) en campo.
* **Clases:** 1 (`Powdery_Mildew`)
* **Cantidad de imágenes:** ~8,290
* **Formato de anotación:** YOLO (Bounding Boxes)
* **Resolución:** Estandarizada
* **Transformaciones:** Filtrado de imágenes de laboratorio, mapeo a mono-clase, limpieza de polígonos a bboxes.
* **Relación:** Derivado de los datasets públicos.
* **Ubicación Actual:** `02_datasets/procesados/dataset_detect_field`

### dataset_monoclass_powdery_mildew
* **Tipo:** Procesado
* **Origen:** Derivado de "Final Grape Leaf Disease Detection...". Generado por `prepare_monoclass_dataset.py`.
* **Propósito:** Variante mono-clase estricta.
* **Clases:** 1 (`Powdery_Mildew`)
* **Cantidad de imágenes:** ~6,950
* **Formato de anotación:** YOLO (Bounding Boxes)
* **Resolución:** Mixta
* **Transformaciones:** Mapeo de IDs de clase a 0 unificando o descartando las demás.
* **Relación:** Subconjunto mapeado de "Final Grape Leaf...".
* **Ubicación Actual:** `02_datasets/procesados/dataset_monoclass_powdery_mildew`

---

## 3. Datasets Propios (`propios/`)
*(Actualmente vacío)*

## 4. Splits Especiales (`splits/`)
*(Actualmente vacío)*
