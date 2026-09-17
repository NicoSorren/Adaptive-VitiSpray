# Modelo de Visión - YOLO

## Arquitectura
- YOLOv11s (Ultralytics) seleccionado como modelo principal.

## Dataset Usado
- `dataset_detect_field` (Detección de hojas con síntomas de Oídio en campo).

## Métricas
- Precisión (P): ~90%
- Recall (R): ~78%
- Velocidad: ~135 FPS en hardware local.

## Comando de Entrenamiento Referencial
```bash
# Ejemplo conceptual
yolo train model=yolo11s.pt data=path/to/dataset.yaml epochs=50
```
