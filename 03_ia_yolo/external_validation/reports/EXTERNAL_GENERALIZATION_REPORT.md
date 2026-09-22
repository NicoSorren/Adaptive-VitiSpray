# Reporte de Generalización Externa (EXP-YOLO-EXT-001)

Este informe detalla los resultados de evaluar el mejor modelo candidato actual (`yolo11m_detect_field_v1`) sobre un conjunto de validación externa curado manualmente, que **no participó** en ninguna fase del entrenamiento (train/valid/test del modelo).

## 1. Verificación de Integridad (Data Leakage)
Se calcularon hashes criptográficos exactos (MD5) y hashes perceptuales (pHash) para las 19 imágenes contra todo el dataset de entrenamiento y validación.
**Resultado:** **0 duplicados encontrados**. La fuga de datos (data leakage) queda descartada.

## 2. Descripción del Conjunto Externo
Total de imágenes: **19**
- **Oídio (Powdery Mildew - PM):** 12 imágenes.
- **Peronospora (Downy Mildew):** 4 imágenes.
- **Sanas (Healthy):** 3 imágenes.

## 3. Resultados Cuantitativos por Threshold (Umbral)

### A. Tasa de Detección en Imágenes Positivas (Oídio)
*Condición: Al menos 1 bounding box detectada correctamente.*

| Threshold | Detecciones Exitosas | Imágenes Fallidas | Tasa de Detección Cualitativa |
|:---:|:---:|:---:|:---:|
| **conf=0.25** | 6 | 6 | **50.0%** (6/12) |
| **conf=0.50** | 5 | 7 | **41.6%** (5/12) |
| **conf=0.70** | 3 | 9 | **25.0%** (3/12) |

### B. Falsos Positivos en Peronospora (Confusión Inter-clase)
*Condición: Falsa alarma de Oídio sobre síntomas de Peronospora.*

| Threshold | Falsos Positivos | Tasa de Falsos Positivos |
|:---:|:---:|:---:|
| **conf=0.25** | 0 | **0.0%** (0/4) |
| **conf=0.50** | 0 | **0.0%** (0/4) |
| **conf=0.70** | 0 | **0.0%** (0/4) |

### C. Falsos Positivos en Hojas Sanas
*Condición: Falsa alarma de Oídio sobre tejido sano.*

| Threshold | Falsos Positivos | Tasa de Falsos Positivos |
|:---:|:---:|:---:|
| **conf=0.25** | 0 | **0.0%** (0/3) |
| **conf=0.50** | 0 | **0.0%** (0/3) |
| **conf=0.70** | 0 | **0.0%** (0/3) |

---

## 4. Análisis Detallado (Tabla Imagen a Imagen)

| Nombre de Archivo | Categoría Real | Detecciones (0.25) | Detecciones (0.50) | Detecciones (0.70) | Max Conf | Observación Cualitativa |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| images (1).jpg | PM | 1 | 1 | 0 | 0.67 | Detección estable hasta umbrales medios. Falla en 0.70. |
| images (2).jpg | PM | 1 | 1 | 1 | 0.80 | Muy alta confianza, detecta en todos los umbrales. |
| images (3).jpg | PM | 2 | 1 | 0 | 0.52 | Detección múltiple en 0.25. Límite de confianza en 0.52. |
| images (4).jpg | PM | 1 | 0 | 0 | 0.29 | Síntoma leve/difícil. Sólo detectable a baja confianza. |
| images (5).jpg | PM | 0 | 0 | 0 | - | **Falso Negativo (Falla completa)**. Síntoma no reconocido. |
| images (6).jpg | PM | 2 | 1 | 1 | 0.90 | Excelente detección, altísima confianza. |
| images (7).jpg | PM | 0 | 0 | 0 | - | **Falso Negativo (Falla completa)**. Síntoma no reconocido. |
| images (8).jpg | PM | 0 | 0 | 0 | - | **Falso Negativo (Falla completa)**. Síntoma no reconocido. |
| images (9).jpg | PM | 0 | 0 | 0 | - | **Falso Negativo (Falla completa)**. Síntoma no reconocido. |
| images (10).jpg | PM | 1 | 1 | 1 | 0.74 | Buena detección en un rango amplio de confianza. |
| images (11).jpg | PM | 0 | 0 | 0 | - | **Falso Negativo (Falla completa)**. Síntoma no reconocido. |
| images.jpg | PM | 0 | 0 | 0 | - | **Falso Negativo (Falla completa)**. Síntoma no reconocido. |
| images (12)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en Peronospora. |
| images (13)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en Peronospora. |
| images (14)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en Peronospora. |
| images (15)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en Peronospora. |
| images (12)_s.jpg | HEALTHY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en tejido sano. |
| images (13)_s.jpg | HEALTHY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en tejido sano. |
| images (14)_s.jpg | HEALTHY | 0 | 0 | 0 | - | **Exitoso**. Sin falsos positivos en tejido sano. |

---

## 5. Discusión y Recomendación Provisional

### A. Casos Exitosos
- El modelo muestra una robustez absoluta frente a clases confusas (Peronospora) y hojas sanas. Incluso bajando el umbral a `conf=0.25`, no se activó **ningún falso positivo**, lo que indica que el mapeo de características aprendió exitosamente a ignorar lesiones no relacionadas al oídio.
- Las imágenes de oídio detectadas lograron buenas confianzas en general (hasta 0.90), y la localización de la caja en esas muestras se observa correcta.

### B. Falsos Negativos (El Problema Principal)
- Se evidencia una dificultad severa para generalizar en la mitad del set de validación (6 de 12 imágenes fallaron en todos los umbrales).
- Esto puede deberse a que las imágenes externas contienen patrones de iluminación, texturas del follaje (variedades de vid), o estadios de infección diferentes a la distribución de las fuentes `Roboflow` o `Italia` empleadas en el entrenamiento.

### C. Recomendación de Threshold
- Al no presentarse NINGÚN falso positivo a `conf=0.25` en el set de control (Peronospora + Sanas), y al ser el umbral de 0.25 el único capaz de detectar la imagen 4 (max conf = 0.29), **se recomienda provisionalmente emplear `conf=0.25` para la inferencia a campo**.
- Un umbral mayor (como el default 0.50) sacrificaría un 16% relativo de las detecciones posibles (de 6 a 5 imágenes) sin aportar beneficio comprobado en la reducción de falsos positivos en este lote.

*Nota: Esta recomendación es cualitativa y provisional. Debe calibrarse nuevamente si se incorporan estas imágenes al dominio de entrenamiento.*
