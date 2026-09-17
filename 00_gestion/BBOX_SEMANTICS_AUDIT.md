# Auditoría de Semántica de Bounding Boxes — `dataset_detect_field`

> **Metodología:** Se generaron 30 paneles comparativos (15 Roboflow + 15 Italia), cada uno con 4 subpaneles:
> - **A – Original:** sin ninguna anotación.
> - **B – Ground Truth (verde):** cajas almacenadas en los labels YOLO del dataset.
> - **C – Predicción conf≥0.50 (azul):** salida del modelo `yolo11m_detect_field_v1/weights/best.pt`.
> - **D – Predicción conf≥0.25 (cian):** misma salida con umbral relajado.
>
> **El informe NO concluye automáticamente qué representa el GT.** Primero se describe lo observado.

---

## 1. Tabla Completa de las 30 Muestras

| # | Fuente | Archivo | Resolución | GT Cajas | Áreas GT (%) | Pred≥0.50 | Confs Pred | IoU GT↔Pred |
|---|--------|---------|-----------|----------|--------------|-----------|------------|-------------|
| 01 | Roboflow | powdery324 | 256×256 | 3 | 8.6, 5.3, 7.3 | 3 | 0.95, 0.94, 0.91 | 0.99, 0.97, 0.80 |
| 02 | Roboflow | powdery495 | 256×256 | 3 | 3.8, 13.5, 1.5 | 3 | 0.91, 0.84, 0.53 | 0.95, 0.96, 0.00 |
| 03 | Roboflow | powdery344 | 256×256 | 3 | 7.8, 4.9, 5.2 | 3 | 0.93, 0.66, 0.53 | 0.96, 0.93, 0.95 |
| 04 | Roboflow | powdery201 | 720×720 | 3 | 6.3, 11.8, 11.4 | 3 | 0.94, 0.94, 0.94 | 0.97, 0.99, 0.97 |
| 05 | Roboflow | powdery539 | 720×720 | 2 | **21.7, 27.7** | 2 | 0.94, 0.94 | 0.97, 0.97 |
| 06 | Roboflow | IMG_0968 | 3024×3024 | 4 | 12.8, 13.3, 9.5, 14.2 | 4 | 0.93, 0.90, 0.90, 0.88 | 0.96, 0.98, 0.95, 0.98 |
| 07 | Roboflow | powdery302 | 720×720 | 3 | 8.2, 5.1, 5.6 | 3 | 0.96, 0.95, 0.92 | 0.96, 0.98, 0.94 |
| 08 | Roboflow | powdery560 | 720×720 | 2 | **29.3, 22.9** | 3 | 0.95, 0.93, 0.80 | 0.99, 0.94 |
| 09 | Roboflow | powdery267 | 720×720 | 3 | 5.9, 3.6, 4.0 | 3 | 0.96, 0.95, 0.91 | 0.99, 0.99, 0.96 |
| 10 | Roboflow | image4-703 | 256×256 | 1 | **18.8** | 1 | 0.70 | 0.96 |
| 11 | Roboflow | powdery231 | 720×720 | 3 | 5.0, 4.5, 6.4 | 3 | 0.96, 0.96, 0.87 | 0.97, 0.99, 0.95 |
| 12 | Roboflow | IMG_2720 | **4032×3024** | 4 | 5.2, 2.6, 4.4, 5.6 | **0** | — | 0.00, 0.00, 0.00, 0.00 |
| 13 | Roboflow | IMG_2075 | **4032×3024** | 6 | 5.9, 2.3, 1.9, **0.3**, 1.4, 1.0 | **0** | — | todos 0.00 |
| 14 | Roboflow | IMG_1654 | 1440×1440 | 5 | 3.3, 3.2, 8.0, 2.9, 4.2 | 8 | 0.92–0.53 | 0.95, 0.98, 0.98, 0.98, 0.77 |
| 15 | Roboflow | IMG_1636 | 1440×1440 | 1 | **1.7** | 5 | 0.80–0.51 | 0.86 |
| 16 | Italia | IMG_2310 | 3072×2048 | 1 | **38.9** | 1 | 0.88 | 0.97 |
| 17 | Italia | IMG_2354 | 3072×2048 | 10 | 16.8, 3.2, 7.2, 4.8, 6.7, 5.5, 3.2, 5.0, 2.3, 5.9 | 5 | 0.83–0.51 | muy variable |
| 18 | Italia | IMG_2504 | 3072×2048 | 2 | **60.2**, 5.8 | 3 | 0.89, 0.87, 0.53 | 0.95, 0.87 |
| 19 | Italia | Oidio10 | 3072×2048 | 1 | **70.2** | 1 | 0.70 | 0.97 |
| 20 | Italia | IMG_2516 | 3072×2048 | 4 | 18.0, 26.5, 6.1, 5.7 | 3 | 0.88, 0.75, 0.72 | 0.98, 0.94, 0.91, 0.09 |
| 21 | Italia | IMG_2528 | 3072×2048 | 4 | 4.2, 7.6, **14.8**, 6.2 | 3 | 0.78, 0.74, 0.74 | 0.94, 0.97, 0.92, 0.02 |
| 22 | Italia | germoglio_002 | 3072×2048 | 1 | **26.4** | 1 | 0.81 | 0.98 |
| 23 | Italia | Chardonnay_foglia | 3072×2048 | 1 | **63.0** | 1 | 0.91 | 0.96 |
| 24 | Italia | IMG_2302 | 3072×2048 | 4 | **50.0**, 4.1, 5.2, 3.7 | 4 | 0.90, 0.67, 0.57, 0.53 | 0.83, 0.02, 0.00, 0.83 |
| 25 | Italia | grappolo_merlot_02 | 3072×2048 | 1 | 7.0 | 1 | 0.79 | 0.94 |
| 26 | Italia | Oidio05 | 3072×2048 | 1 | **69.6** | 1 | 0.84 | 0.97 |
| 27 | Italia | germoglio_015d | 3072×2048 | 2 | 11.3, 1.8 | 1 | 0.70 | 0.74, 0.00 |
| 28 | Italia | IMG_2535 | 3072×2048 | 3 | **43.0**, 8.6, **26.7** | 3 | 0.89, 0.78, 0.70 | 0.96, 0.12, 0.87 |
| 29 | Italia | IMG_2321 | 3072×2048 | 2 | 14.1, 13.0 | 2 | 0.79, 0.64 | 0.93, 0.92 |
| 30 | Italia | WhatsApp 12.05.31 | 1200×1600 | 2 | **21.4**, 8.1 | 2 | 0.89, 0.85 | 0.94, 0.95 |

---

## 2. Casos Representativos Seleccionados

Los siguientes casos cubren los 5 tipos de comportamiento solicitados.

### Tipo 1 — GT claramente rodea lesiones/manchas pequeñas
- **#09 (Roboflow, powdery267):** 3 GT cajas del 5.9%, 3.6%, 4.0% del frame. Cada caja corresponde a una mancha blanca discreta visible en la imagen.
- **#11 (Roboflow, powdery231):** Similar patrón, 5.0%, 4.5%, 6.4%.
- **#27 (Italia, germoglio_015d):** Una caja del 11.3% sobre región clara afectada; otra de 1.8% sobre un área muy pequeña.

### Tipo 2 — GT cubre una porción considerable de una hoja
- **#04 (Roboflow, powdery201):** 3 cajas del 6.3%, 11.8%, 11.4%. El anotador parece haber marcado zonas de la hoja visiblemente blanquecinas pero no la hoja entera.
- **#29 (Italia, IMG_2321):** 2 cajas de 14.1% y 13.0%. La hoja tiene afectación extensa pero las cajas no cubren el 100%.

### Tipo 3 — GT prácticamente cubre la hoja completa o un sector mayoritario
- **#19 (Italia, Oidio10):** GT única de **70.2%** del frame. Visualmente corresponde a una hoja con infección masiva donde el anotador envolvió la región afectada completa.
- **#26 (Italia, Oidio05):** GT única de **69.6%**.
- **#23 (Italia, Chardonnay_foglia):** GT única de **63.0%**.
- **#18 (Italia, IMG_2504):** GT de **60.2%** en primera caja.

> ⚠️ **Observación crítica:** en el dataset italiano, varias anotaciones cubren más del 60% del fotograma. Esto no equivale necesariamente a "toda la hoja", pero se acerca. Ver panel para inspección visual directa.

### Tipo 4 — Imagen con múltiples lesiones/cajas
- **#17 (Italia, IMG_2354):** 10 GT boxes en el mismo frame (mayor densidad de la muestra). El modelo detectó solo 5.
- **#14 (Roboflow, IMG_1654):** 5 GT boxes, el modelo generó 8 predicciones (3 extra sin correspondencia GT).

### Tipo 5 — Casos ambiguos
- **#24 (Italia, IMG_2302):** Mezcla de 1 caja muy grande (**50.0%**) con 3 pequeñas (3.7–5.2%). Un anotador marcó una región masiva; otros marcaron manchas pequeñas. IoU bajo para los pequeños (0.02, 0.00) → el modelo no detectó las manchas pequeñas en ese contexto.
- **#12 y #13 (Roboflow, IMG_2720 / IMG_2075):** Imágenes a 4032×3024 de alta resolución, con GT boxes de 0.3%–5.9%, pero el modelo no detectó absolutamente nada. Esto sugiere que al redimensionar a 640px para inferencia, los objetos se vuelven subpíxel o casi invisibles.

---

## 3. Análisis del Criterio de Anotación por Fuente

### Roboflow — Análisis

**Origen de las anotaciones:** el dataset original de Roboflow contenía **polígonos** (formato segmentación YOLO, con decenas de coordenadas por objeto). El script `prepare_detection_dataset.py` los convirtió a bboxes aplicando `polygon_to_bbox()` = coordenadas extremas del polígono.

**¿Qué rodeaba el polígono original?**
- En las imágenes de baja resolución (256×256 y 720×720), los polígonos a juzgar por las áreas resultantes (2%–28%) parecen haber trazado el contorno de **manchas/lesiones individuales** o **regiones blanquecinas** sobre la superficie de la hoja.
- No hay evidencia de que envolvieran la hoja completa, ya que una hoja a 720px ocuparía ~40%–80% del cuadro y las áreas observadas son mucho menores.

**Inconsistencia de resolución:**
- En las imágenes a 4032×3024 (casos #12, #13), los GT boxes son del 0.3%–5.9%. Al escalar a 640px, el objeto anotado mide apenas 2–14 píxeles, que es prácticamente invisible para el modelo. Esto indica un **problema de escala entre la resolución de anotación y la resolución de entrenamiento**.

### Italia — Análisis

**Origen de las anotaciones:** las anotaciones están en formato YOLO-bbox nativo (sin pasar por polígonos). El archivo ZIP `annot_powdery_downy_mildew_2021.zip` contiene los `.txt` originales distribuidos en subcarpetas por sesión/ubicación (Fenosu, Atlantide, Misto, etc.).

**¿Qué rodea el GT en Italia?**

Las áreas del GT italiano varían drásticamente:

| Rango de área | Interpretación posible |
|--------------|------------------------|
| 1–10% | Manchas localizadas o brotes iniciales |
| 10–30% | Regiones extendidas afectadas o brotes medianos |
| 30–70% | Potencialmente: hoja parcialmente afectada encuadrada; o hoja cubierta completamente por ceniza blanca |

Los archivos originales muestran nombres como `IMG_2310.txt`, `Oidio10.txt`, `Chardonnay_foglia_Lamon_01.txt`. La subcarpeta `Oidio_piantine` fue excluida del entrenamiento por el script (macetas), lo que es correcto.

**Criterio de anotación italiano:** No existe un manual de anotación público disponible. Lo que los datos sugieren es que el anotador italiano tendió a trazar una caja que envuelve toda la **región visible de la enfermedad**, que puede ser:
- Una mancha aislada → caja pequeña
- Una hoja fuertemente infectada → caja grande que coincide con la forma de la hoja
- Un racimo con síntomas → caja sobre el racimo

---

## 4. ¿Existe inconsistencia de semántica entre fuentes?

**Sí, existe variación semántica entre e intra-fuentes.** Los datos cuantitativos son claros:

| Fuente | Área mediana GT | Rango GT | Comentario |
|--------|----------------|----------|-----------|
| Roboflow (256/720px) | ~5–8% | 1–30% | Manchas sobre hoja, múltiples por imagen |
| Roboflow (4032/1440px) | ~3–8% | 0.3–8% | Manchas muy pequeñas en imagen grande → riesgo resolución |
| Italia | ~20–25% | 2–70% | Amplio rango; GT grandes corresponden a hojas o porciones |

> ⚠️ **Esto NO invalida el dataset, pero tiene consecuencias concretas:**
> 1. El modelo aprende a detectar tanto manchas pequeñas como regiones afectadas extensas bajo la misma clase `Powdery_Mildew`.
> 2. La interpretación cuantitativa de "número de detecciones" en una imagen nueva dependerá del criterio del anotador original.
> 3. Las imágenes de alta resolución de Roboflow (4032px) con objetos subpíxel a 640px representan GT no detectables con el pipeline actual.

---

## 5. Rendimiento del Modelo por Tipo de GT

| Tipo de GT | IoU Típico | Observación |
|------------|-----------|-------------|
| GT pequeño (< 5%), imagen 256–720px | 0.93–0.99 | Modelo funciona muy bien |
| GT mediano (5–20%), imagen cualquier resolución | 0.86–0.98 | Buen ajuste |
| GT grande (> 40%), imagen italiana | 0.94–0.97 | Modelo ajusta bien el contorno general |
| GT múltiple (> 5 cajas por imagen) | Variable (0.0–0.98) | Algunas cajas no detectadas, especialmente las más pequeñas |
| GT en imagen 4032px (alta resolución) | **0.00** | Modelo falla completamente — problema de escala |

---

## 6. Conclusión de la Auditoría (Descripción, No Interpretación)

Los ground truths del `dataset_detect_field` presentan **dos patrones de anotación diferenciables**:

1. **Patrón A (dominante en Roboflow):** Múltiples cajas por imagen, cada una encerrando una región blanquecina discreta. Área típica: 2–15% del frame.

2. **Patrón B (dominante en Italia):** Pocas cajas por imagen (1–4), con área variable: desde 2% hasta 70%. Las cajas grandes parecen envolver una hoja o sector completo de canopia con síntomas visibles.

**Lo que NO puede determinarse sin ver cada imagen directamente:** si el contenido de las cajas grandes italianas corresponde a una lesión extensa en la superficie de la hoja, a toda la hoja, o a la presencia de polvo blanco sobre múltiples tejidos superpuestos.

> **Acción recomendada:** Revisar los paneles generados en `00_gestion/auditoria_semantica_bbox/` —en particular los casos #16, #18, #19, #23, #24, #26— para determinar visualmente qué representa cada GT grande.

---

## 7. Corrección Verificada: Escala en Imágenes 4032×3024

> ⚠️ **CORRECCIÓN:** Una versión anterior de este informe afirmaba que los objetos se comprimen a "1–8 px" al escalar a imgsz=640. Esto era **incorrecto**. Los cálculos exactos con las coordenadas YOLO reales demuestran lo contrario.

### Cálculo exacto — IMG_2720 (4032×3024)

```
scale@640 = 640 / max(4032, 3024) = 640 / 4032 = 0.15873
canvas@640: 640×480 px
scale@800 = 800 / 4032 = 0.198413
canvas@800: 800×600 px
```

| Caja | orig (px) | área GT | @imgsz=640 | clase@640 | @imgsz=800 | clase@800 |
|------|-----------|---------|-----------|-----------|-----------|-----------|
| box[0] | 1312×484 | 5.21% | **208×77 px** | medium | 260×96 px | large |
| box[1] | 861×372 | 2.63% | **137×59 px** | medium | 171×74 px | medium |
| box[2] | 808×667 | 4.43% | **128×106 px** | large | 160×132 px | large |
| box[3] | 956×709 | 5.55% | **152×113 px** | large | 190×141 px | large |

### Cálculo exacto — IMG_2075 (4032×3024)

| Caja | orig (px) | área GT | @imgsz=640 | clase@640 | @imgsz=800 | clase@800 |
|------|-----------|---------|-----------|-----------|-----------|-----------|
| box[0] | 1060×679 | 5.91% | **168×108 px** | large | 210×135 px | large |
| box[1] | 682×408 | 2.28% | **108×65 px** | medium | 135×81 px | medium |
| box[2] | 704×337 | 1.94% | **112×53 px** | medium | 140×67 px | medium |
| box[3] | 273×142 | **0.32%** | **43×23 px** | small | 54×28 px | small |
| box[4] | 514×331 | 1.40% | **82×53 px** | medium | 102×66 px | medium |
| box[5] | 672×177 | 0.98% | **107×28 px** | small | 133×35 px | medium |

### Conclusión Revisada

Los objetos en las imágenes de 4032px **NO se vuelven subpíxel ni invisibles** a imgsz=640. El tamaño mínimo resizeado es de **23 px** (box[3] de IMG_2075 — el más pequeño del dataset, área original 0.32%). Los demás oscilan entre 53 px y 208 px, todos perfectamente dentro del rango detectable.

La causa real del **fallo de detección en #12 y #13** no es el tamaño de los objetos, sino probablemente alguna de estas razones:
1. **Contraste/textura:** Las anotaciones en esas imágenes podrían cubrir regiones donde el síntoma visual es sutil comparado con las imágenes de entrenamiento.
2. **Distribución de resoluciones en entrenamiento:** La mayoría de imágenes de Roboflow en el dataset están a 256px o 720px. El modelo puede haber aprendido features a esas escalas y no generalizar bien a 4032px aunque el objeto escalado sea del mismo tamaño.
3. **Contexto visual:** Una imagen a 4032px tiene mucho más contexto visual (más canopia, más hojas, fondo más complejo) que una imagen a 256px. Esto puede confundir al detector.

**El punto anterior sobre tiling/slicing sigue siendo válido como recomendación técnica, pero la razón no es tamaño subpíxel sino generalización a contextos visuales diferentes.**

---

## 8. Distribución Global de Tamaños por Fuente, Split e imgsz

Calculado sobre las **11,399 bboxes** del dataset completo usando coordenadas YOLO reales.

**Clasificación:** tiny (<8px), very_small (<16px), small (16–32px), medium (32–96px), large (>96px) — basado en el lado mínimo del bbox resizeado.

| Segmento | imgsz | tiny | very_small | small | medium | large |
|----------|-------|------|------------|-------|--------|-------|
| **Roboflow** | 640 | 31 (0.3%) | 39 (0.4%) | 288 (2.6%) | 3826 (35.2%) | 6700 (61.6%) |
| **Roboflow** | 800 | 25 (0.2%) | 20 (0.2%) | 167 (1.5%) | 2917 (26.8%) | 7755 (71.3%) |
| **Italia** | 640 | 0 (0.0%) | 0 (0.0%) | 1 (0.2%) | 124 (24.1%) | 390 (75.7%) |
| **Italia** | 800 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 74 (14.4%) | 441 (85.6%) |
| **train** | 640 | 24 (0.3%) | 27 (0.4%) | 205 (2.7%) | 2773 (36.4%) | 4587 (60.2%) |
| **train** | 800 | 19 (0.2%) | 16 (0.2%) | 114 (1.5%) | 2106 (27.7%) | 5361 (70.4%) |
| **valid** | 640 | 7 (0.4%) | 9 (0.5%) | 56 (2.9%) | 766 (40.1%) | 1072 (56.1%) |
| **valid** | 800 | 6 (0.3%) | 4 (0.2%) | 35 (1.8%) | 567 (29.7%) | 1298 (68.0%) |
| **test** | 640 | 0 (0.0%) | 3 (0.2%) | 28 (1.5%) | 411 (21.9%) | 1431 (76.4%) |
| **test** | 800 | 0 (0.0%) | 0 (0.0%) | 18 (1.0%) | 318 (17.0%) | 1537 (82.1%) |

**Observaciones:**
- La **inmensa mayoría** de las bboxes son `medium` o `large` tras el escalado — el dataset NO es fundamentalmente un dataset de detección de objetos pequeños.
- El área normalizada mediocre (~4.7%) fue engañosa: corresponde a dimensiones lineales de 30–100px, no a objetos minúsculos.
- Solo hay **31 bboxes tiny** en todo Roboflow a imgsz=640, y **ninguna en el dataset italiano**.
- Subir a imgsz=800 prácticamente elimina la categoría tiny/very_small, a costa de mayor costo computacional.

---

*Generado a partir de 30 paneles comparativos (Original | GT | Pred≥0.50 | Pred≥0.25) y análisis de 11,399 bboxes reales. Ningún archivo del dataset fue modificado.*
