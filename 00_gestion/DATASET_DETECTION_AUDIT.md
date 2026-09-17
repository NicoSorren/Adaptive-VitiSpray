# Auditoría Técnica: `dataset_detect_field` y Entrenamiento Actual

Este informe detalla la composición, criterios de anotación y potenciales problemas de fuga de datos (data leakage) en el dataset unificado, así como la configuración exacta del entrenamiento actual.

## 1. Composición por Fuente y Split

El `dataset_detect_field` fue construido combinando:
- **Fuente A:** "Final Grape Leaf Disease Detection" (Roboflow)
- **Fuente B:** "Downy Mildew and Powdery Mildew Symptoms" (Italia)

| Split | A (Roboflow) | B (Italia) | Positivas (Con Oídio) | Negativas (Background) | Total Imágenes |
|-------|-------------:|-----------:|----------------------:|-----------------------:|---------------:|
| **Train** | 4,042 | 1,068 | 2,163 | 2,947 | 5,110 |
| **Valid** | 1,455 | 268 | 531 | 1,192 | 1,723 |
| **Test** | 1,458 | 0 | 571 | 887 | 1,458 |

**Observación:** El dataset italiano NO tiene representación en el conjunto de Test.

## 2. Distribución de Anotaciones y Tamaños

| Split | Total BBoxes | Promedio por Img | Mediana BBoxes | Área Mediana | Pequeñas (< 5% área) |
|-------|--------------|------------------|----------------|--------------|----------------------|
| **Train** | 7,616 | 1.49 | 0.0 | 4.70% | 52.27% |
| **Valid** | 1,910 | 1.11 | 0.0 | 4.36% | 56.49% |
| **Test** | 1,873 | 1.28 | 0.0 | 5.38% | 42.71% |

**Conclusión:** Más de la mitad de las instancias de oídio (cajas delimitadoras) ocupan **menos del 5% del área total de la imagen**. El modelo está detectando regiones/lesiones pequeñas de enfermedad, no hojas enteras. 

## 3. Diferencia de Criterio de Anotación entre Fuentes

Al inspeccionar los scripts y resultados visuales:
- **Roboflow (Fuente A):** Anotaba originalmente con **polígonos** que delineaban con precisión las manchas o lesiones de oídio sobre la hoja. Estos fueron convertidos a bounding boxes usando las coordenadas extremas del polígono (vía `polygon_to_bbox()`).
- **Italia (Fuente B):** También anota **lesiones/manchas** dentro de la canopia.
- **Semántica:** Ambas fuentes son semánticamente compatibles. Ambas buscan identificar la **región específica afectada** por el hongo dentro del cuadro, no clasificar la imagen entera o enmarcar la hoja completa.

## 4. Data Leakage en el Dataset Italiano

Se realizó un escaneo mediante Hashing Perceptual (Difference Hashing - dHash) para identificar imágenes idénticas o casi idénticas que hayan caído tanto en Train como en Valid debido al split aleatorio:

- **Duplicados Exactos (Train vs Valid):** 1 (Ej: `italy_2021_WhatsApp_Image_2021-05-12_at_12.05.31_(2).jpeg` es idéntica a `italy_2021_photo_2021-05-13_08-28-17.jpg`).
- **Near-Duplicates (Distancia de Hamming <= 4):** 0.
- **Leakage Estimado:** **~0.37%** sobre el set de validación italiano.
- **Conclusión:** Afortunadamente, no hay un leakage masivo. Las imágenes italianas no parecen ser fotogramas consecutivos de video muy apretados en el tiempo que hayan contaminado significativamente la validación.

## 5. Análisis del Test Set

El set de Test actual (1,458 imágenes) **proviene 100% de Roboflow (Fuente A)**. 
- La fuente italiana (Fuente B) no reservó ningún split para test durante el script de preparación (se dividió 80/20 en train/valid). 
- Esto significa que el modelo está siendo evaluado en un entorno puramente Roboflow, y su capacidad de generalización a la "textura visual italiana" no está medida objetivamente al final, sólo en validación.

## 6. Aclaración del Experimento Histórico Monoclase

Al revisar el script `prepare_monoclass_dataset.py`, la unificación de "las demás clases" significó **la opción A**:
- **Se mantuvieron las etiquetas de Oídio (Target ID 2).**
- **Se eliminaron por completo las etiquetas de las otras enfermedades (Birds_Eye_Rot, etc.)**, convirtiendo esas imágenes en negativos/background puro si no tenían también oídio.
No se mapearon como oídio, se volvieron fondo.

## 7. Sobre el Optimizador Real

En los archivos `args.yaml` históricos, el parámetro indica `optimizer: auto`. 
Ultralytics no guarda el nombre del optimizador resuelto en texto plano. En modo `auto`, YOLOv8/11 elige:
- **SGD** si `epochs > 50` y hay más de 10,000 imágenes.
- **AdamW** en cualquier otro caso.
Dado que nuestro dataset tiene ~5,100 imágenes en Train, Ultralytics **utilizó AdamW**.

## 8. Configuración Exacta del Entrenamiento Actual

Basado en `train_detection.py` y los parámetros del último modelo (`yolo11m_detect_field_v1`):

- **Modelo Arquitectura:** YOLOv11m (`yolo11m.pt`).
- **Pesos Iniciales:** Pre-entrenados de Ultralytics (COCO).
- **Dataset:** `02_datasets/procesados/dataset_detect_field/data.yaml`
- **Resolución (imgsz):** 640
- **Épocas Configuradas:** 70 (completó 70).
- **Batch Size:** 8 (para el modelo m).
- **Early Stopping (patience):** 20.
- **Semilla (seed):** 0.
- **Optimizador Configurado:** `auto` (Resultó en AdamW).
- **Augmentations Relevantes:** scale: 0.5, fliplr: 0.5, mosaic: 1.0, HSV variaciones leves.
- **Nombre del Run:** `yolo11m_detect_field_v1`.
- **Estado Actual:** Finalizado con éxito (guardó best.pt y last.pt).
