# Módulo IA / YOLO (`03_ia_yolo`)

Este directorio centraliza todo el trabajo relacionado con los modelos de percepción basados en Ultralytics YOLOv11 para el proyecto Adaptive-VitiSpray.

## Estructura de Directorios

- `scripts/`: Contiene todo el código Python ejecutable relacionado con YOLO, organizado en subcategorías:
  - `training/`: Scripts para iniciar entrenamientos (ej. `train_detection.py`).
  - `preparation/`: Scripts para preparar y transformar datasets.
  - `evaluation/`: Scripts para calcular métricas sobre conjuntos de test.
  - `utilities/`: Herramientas misceláneas (visualización, análisis, auditoría).
- `runs/`: Directorio donde Ultralytics almacena automáticamente los resultados de los entrenamientos (`train/`, `detect/`). Cada experimento tiene su propia subcarpeta con métricas, curvas y pesos iterativos (`best.pt`, `last.pt`). **No modificar manualmente su estructura interna.**
- `weights/`: Almacenamiento de pesos de modelos.
  - `pretrained/`: Pesos base descargados de Ultralytics (ej. `yolo11m.pt`).
  - `selected/`: Pesos finales seleccionados para su uso en inferencia de producción o simulación.
- `configs/`: Archivos de configuración adicionales para los entrenamientos (hiperparámetros, etc.).
- `inspections/`: Resultados de auditorías visuales e inspecciones sobre los datos y predicciones.
- `predictions/`: Predicciones visuales generadas para evaluación cualitativa.
- `metrics/`: Análisis cuantitativos adicionales fuera de los proporcionados por Ultralytics.

## Datasets

Los datasets no se almacenan aquí. Se encuentran en `02_datasets/` y se referencian a través del módulo centralizado `vitispray.paths`.

## Cómo Ejecutar

Para asegurar que las importaciones (como `vitispray.paths`) funcionen correctamente, los scripts deben ejecutarse teniendo la raíz del repositorio en el `PYTHONPATH`, lo cual está garantizado si el entorno está activado y el paquete instalado con `pip install -e .`.

Ejemplo de entrenamiento:
```bash
python 03_ia_yolo/scripts/training/train_detection.py --epochs 60 --batch 16 --name yolo11s_detect_field_v3
```

## Registro de Experimentos

Cada experimento importante debe ser registrado en:
- `00_gestion/EXPERIMENTOS.csv`
- `00_gestion/YOLO_HISTORICAL_EXPERIMENTS.md`

### Política de Nomenclatura

Para nuevos experimentos, utilizar identificadores secuenciales coherentes (ej. `EXP-YOLO-008`), o bien nombres descriptivos que indiquen el propósito y la versión, por ejemplo:
- `yolo11s_detect_field_v2` (Detección a campo, modelo small, versión 2)
- `monoclass_pm_v1` (Modelo monoclase, Powdery Mildew, versión 1)
