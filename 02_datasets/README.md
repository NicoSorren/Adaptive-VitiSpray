# Datasets

## Origen
- Dataset original proveniente de Roboflow, basado en imágenes tomadas en campo sobre oídio en vid.

## Estructura
- `dataset_detect_field/`: Dataset principal procesado y balanceado para detección con YOLO.
- `dataset_monoclass_powdery_mildew/`: Variante monoclase (anotaciones adaptadas).

## Split
- Entrenamiento: ~70%
- Validación: ~20%
- Test: ~10%

## Preprocesamiento
- Transformación de polígonos a bounding boxes (formato YOLO).
- Eliminación de imágenes sin anotaciones.
