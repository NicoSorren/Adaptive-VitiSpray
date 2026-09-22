# Reporte de Generalización Externa V2 (EXP-YOLO-EXT-002)

Este informe detalla los resultados de la validación externa utilizando la muestra actualizada (dominio correcto de hojas de vid), preservando el mismo modelo candidato (`yolo11m_detect_field_v1`) y los mismos umbrales.

## 1. Verificación de Integridad (Data Leakage)
Se calcularon hashes criptográficos exactos (MD5) y hashes perceptuales (pHash) contra el dataset de entrenamiento y validación.
**Resultado:** **0 duplicados encontrados**. Se certifica que las 19 imágenes son estrictamente un conjunto independiente out-of-sample.

## 2. Descripción del Conjunto Externo (Dominio Corregido)
Total de imágenes: **19**
- **Oídio (Powdery Mildew - PM):** 12 imágenes.
- **Peronospora (Downy Mildew):** 4 imágenes.
- **Sanas (Healthy):** 3 imágenes.

## 3. Resultados Cuantitativos por Threshold (Umbral)

### A. Tasa de Detección en Imágenes Positivas (Oídio)
*Condición: Al menos 1 bounding box detectada.*

| Threshold | Detecciones Exitosas | Imágenes Fallidas | Tasa de Detección Cualitativa |
|:---:|:---:|:---:|:---:|
| **conf=0.25** | 7 | 5 | **58.3%** (7/12) |
| **conf=0.50** | 6 | 6 | **50.0%** (6/12) |
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

| Nombre de Archivo | Categoría | Detecciones (0.25) | Detecciones (0.50) | Detecciones (0.70) | Max Conf | Observación Cualitativa |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| images (1).jpg | PM | 1 | 1 | 0 | 0.67 | Exitoso en 0.25 y 0.50. |
| images (2).jpg | PM | 1 | 1 | 1 | 0.80 | Muy alta confianza, detecta en todos los umbrales. |
| images (3).jpg | PM | 2 | 1 | 0 | 0.52 | Detección múltiple en 0.25. Límite de confianza 0.52. |
| images (4).jpg | PM | 1 | 0 | 0 | 0.29 | **Solo detectado a conf=0.25**. Síntoma sutil o difícil. |
| images (6).jpg | PM | 2 | 1 | 1 | 0.90 | Excelente detección, altísima confianza. |
| images (10).jpg| PM | 1 | 1 | 1 | 0.74 | Buena detección en un rango amplio de confianza. |
| images(14).jpg | PM | 1 | 1 | 0 | 0.62 | Exitoso en 0.25 y 0.50. |
| images(5).jpg  | PM | 0 | 0 | 0 | - | **FN**. Falla completa. |
| images (7).jpg | PM | 0 | 0 | 0 | - | **FN**. Falla completa. |
| images (8).jpg | PM | 0 | 0 | 0 | - | **FN**. Falla completa. |
| images (9).jpg | PM | 0 | 0 | 0 | - | **FN**. Falla completa. |
| images (11).jpg| PM | 0 | 0 | 0 | - | **FN**. Falla completa. |
| images (12)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |
| images (13)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |
| images (14)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |
| images (15)_p.jpg | DOWNY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |
| images (12)_s.jpg | HEALTHY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |
| images (13)_s.jpg | HEALTHY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |
| images (14)_s.jpg | HEALTHY | 0 | 0 | 0 | - | **Exitoso**. Sin FP. |

---

## 5. Comparativa (EXP-001 vs EXP-002)

### ¿El cambio al "dominio correcto" alteró significativamente los resultados?
- **Falsos Positivos:** El modelo demostró idéntica resiliencia frente a clases confusoras. En ambos experimentos **los falsos positivos se mantuvieron estrictamente en 0%**, validando que el entrenamiento de "una clase vs fondo variable" es sumamente robusto para discriminar otras patologías (Peronospora) y hojas sanas, incluso ante cambios de dominio.
- **Tasa de Detección:** Hubo una **leve mejoría** cualitativa. La capacidad de detectar al menos una lesión de oídio subió de 50.0% (6/12 en EXP-001) a **58.3% (7/12 en EXP-002)** usando el umbral 0.25.
- **Conclusión General:** El cambio al dominio correcto confirmó que el modelo es conservador (no inventa lesiones en follaje sano/enfermo por otras causas). Las fallas sistemáticas (5 falsos negativos) sugieren que existen patrones fenotípicos o estadios fenológicos en este nuevo dominio externo que no están debidamente representados en los datasets públicos de entrenamiento, constituyendo el principal límite del MVP.

### Recomendación de Threshold
Se reafirma contundentemente la recomendación de **`conf=0.25`**. Al no existir falsos positivos ni en el set inicial ni en el corregido, un umbral de 0.25 maximiza la recuperación de síntomas débiles (e.g. `images (4).jpg` detectada con 0.29) que se perderían totalmente con el umbral por defecto (0.50), sin penalizar la especificidad del diagnóstico en el campo.
