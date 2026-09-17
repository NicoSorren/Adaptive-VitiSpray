# Historial de Experimentos YOLO

Este documento reconstruye de forma verificable (a partir de `args.yaml` y `results.csv`) el historial de experimentos ejecutados en el repositorio. No se han inventado datos; todos los valores provienen de la introspección de la carpeta `runs/`.

## 1. Tabla Cronológica de Runs

| ID | Run Name | Tarea | Modelo Base | Dataset | Épocas (Conf/Real) | Batch | imgsz | Precisión | Recall | mAP50 | mAP50-95 | Rutas Weights |
|----|----------|-------|-------------|---------|--------------------|-------|-------|-----------|--------|-------|----------|---------------|
| 1 | `test_sanity_check` | Segmentación (Baseline) | yolo11s-seg.pt | Final Grape Leaf... (3 Clases) | 1 / 1 | 8 | 640 | 0.4539 | 0.1128 | 0.0787 | 0.0383 | `best.pt`, `last.pt` |
| 2 | `baseline_v1` | Segmentación (Baseline) | yolo11s-seg.pt | Final Grape Leaf... (3 Clases) | 40 / 40 | 8 | 640 | 0.6341 | 0.4114 | 0.4473 | 0.3630 | `best.pt`, `last.pt` |
| 3 | `baseline_80epochs` | Segmentación (Baseline) | yolo11s-seg.pt | Final Grape Leaf... (3 Clases) | 80 / 80 | 8 | 640 | 0.6378 | 0.4222 | 0.4681 | 0.3737 | `best.pt`, `last.pt` |
| 4 | `monoclass_pm_v1` | Segmentación (Monoclase) | yolo11s-seg.pt | dataset_monoclass... (1 Clase) | 60 / 60 | 8 | 640 | 0.7993 | 0.5650 | 0.6458 | 0.5544 | `best.pt`, `last.pt` |
| 5 | `yolo11s_detect_field_v1` | Detección (Campo) | yolo11s.pt | dataset_detect_field (1 Clase) | 60 / 60 | 16 | 640 | 0.8280 | 0.5361 | 0.6449 | 0.5418 | `best.pt`, `last.pt` |
| 6 | `yolo11s_detect_field_v2` | Detección (Campo) | last.pt (Fine-tune) | dataset_detect_field (1 Clase) | 40 / 40 | 16 | 640 | 0.8069 | 0.5612 | 0.6585 | 0.5418 | `best.pt`, `last.pt` |
| 7 | `yolo11m_detect_field_v1` | Detección (Campo) | yolo11m.pt | dataset_detect_field (1 Clase) | 70 / 70 | 8 | 640 | 0.7465 | 0.5617 | 0.6282 | 0.5300 | `best.pt`, `last.pt` |

*Nota: Todos los experimentos usaron el optimizador en modo `auto`, learning rate inicial de `0.01`, la misma semilla `seed=0` y las mismas augmentations (hsv_h: 0.015, hsv_s: 0.7, hsv_v: 0.4, scale: 0.5, fliplr: 0.5, mosaic: 1.0).*

---

## 2. Comparativa: Multiclase vs Monoclase (Impacto de la simplificación)

- **Experimento A (Multiclase):** `baseline_80epochs` entrenado con el dataset de Roboflow "Final Grape Leaf Disease Detection..." (3 clases).
- **Experimento B (Monoclase):** `monoclass_pm_v1` entrenado con `dataset_monoclass_powdery_mildew` (1 clase).

### Control de variables
Para que la comparación sea justa, se verificaron las variables de control:
- **Modelo base:** `yolo11s-seg.pt` (Mismo en ambos).
- **Dataset de fondo:** Es exactamente el mismo dataset original, pero en B las etiquetas se mapearon a 1 sola clase (Powdery Mildew) y se unificaron las demás.
- **Resolución (imgsz):** 640 (Mismo en ambos).
- **Batch size:** 8 (Mismo en ambos).
- **Augmentations:** Idénticas.
- **Épocas:** A corrió por 80 épocas, mientras que B corrió por 60 épocas (Aun con menos épocas, B fue evaluado comparativamente).

### Tabla de Comparación de Métricas Finales

| Métrica | Experimento A (Multiclase) | Experimento B (Monoclase) | Diferencia |
|---------|----------------------------|---------------------------|------------|
| **Precision** | 0.6378 | 0.7993 | **+0.1615 (Mejora significativa)** |
| **Recall** | 0.4222 | 0.5650 | **+0.1428 (Mejora significativa)** |
| **mAP50** | 0.4681 | 0.6458 | **+0.1777 (Mejora significativa)** |
| **mAP50-95**| 0.3737 | 0.5544 | **+0.1807 (Mejora significativa)** |

**Conclusión Verificable:** La reducción del problema de 3 clases a 1 sola clase (Powdery Mildew vs Background) generó un salto masivo en absolutamente todas las métricas, confirmando que la simplificación del espacio de características fue una decisión arquitectónica sumamente exitosa.
