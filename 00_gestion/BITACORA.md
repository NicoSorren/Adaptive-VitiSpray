# Bitácora de Trabajo - PFE

| Fecha | Objetivo de la Sesión | Tareas Realizadas | Problemas Encontrados | Próximos Pasos |
|---|---|---|---|---|
| 2026-09-17 | Reorganización de Repositorio (Fase 1) | Creación de estructura de directorios y archivos de gestión. | Ninguno. | Definir paths centralizados y realizar movimientos (Fase 2). |

## Registro de Reorganización (2026-09-17)

### Estructura Anterior
Scripts (entrenamiento, datasets, evaluación) mezclados en la raíz junto con resultados (`runs/`, `weights/`), carpetas de datasets y documentación (`docs/`, `.docx`). MVP de prescripción en la carpeta `viti_prescription/`.

### Nueva Estructura Base (FASE 1)
Se crearon las carpetas `00_gestion/`, `01_documentacion/`, `02_datasets/`, `03_ia_yolo/`, `04_modelo_riesgo/`, `05_mapa_prescripcion/`, y `06_webots/`.

### Archivos Movidos
(Fase 1: No se han movido archivos aún).

### Paths Modificados
(Fase 1: No se han modificado paths aún).

### Verificaciones Realizadas
(Fase 1: Carpetas y archivos de control generados correctamente).

## Registro de Reorganización (2026-09-17) - FASE 2 Bloque A
**Archivos Documentales Consolidados en `01_documentacion/`**

### Archivos Movidos
- **Origen:** `docs/Anteproyecto PFE - ... (1).pdf` -> **Destino:** `01_documentacion/anteproyecto/`
- **Origen:** `docs/Anteproyecto_PFE_Actualizado.docx` -> **Destino:** `01_documentacion/anteproyecto/`
- **Origen:** `docs/Anteproyecto_PFE_Sistema_Vision_Control_Actualizado.docx` -> **Destino:** `01_documentacion/anteproyecto/`
- **Origen:** `docs/Anteproyecto_PFE_Sorrentino.docx` -> **Destino:** `01_documentacion/anteproyecto/`
- **Origen:** `docs/Detección de Oídio en Vid.pdf` -> **Destino:** `01_documentacion/borradores/` *(Nota: Se inspeccionó y confirmó como documento propio preliminar del estado del arte).*
- **Origen:** `Propuesta_Simulacion_Modelo_Riesgo_PFE_Sorrentino.docx` -> **Destino:** `01_documentacion/metodologia/`
- **Origen:** `create_anteproyecto_pfe_final.py` -> **Destino:** `01_documentacion/generadores/`

### Cambios de Rutas Realizados
- En `01_documentacion/generadores/create_anteproyecto_pfe_final.py` se cambió la ruta rígida `Path("docs")` por `Path(__file__).resolve().parent.parent / "anteproyecto"`.

### Verificaciones
- Generador de anteproyecto modificado correctamente.
- `README.md` creado en `anteproyecto/` detallando versiones vigentes y obsoletas.

## Registro de Reorganización (2026-09-17) - FASE 2 Bloque B
**Datasets Consolidados en `02_datasets/`**

### Archivos Movidos
- **Origen:** `dataset_detect_field` -> **Destino:** `02_datasets/procesados/`
- **Origen:** `dataset_monoclass_powdery_mildew` -> **Destino:** `02_datasets/procesados/`
- **Origen:** `Final Grape Leaf Disease Detection...` -> **Destino:** `02_datasets/publicos/`
- **Origen:** `Downy Mildew and Powdery Mildew Symptoms` -> **Destino:** `02_datasets/publicos/`

### Cambios de Configuración
- Archivos `data.yaml` actualizados eliminando la clave `path` estricta para garantizar portabilidad. 
- Scripts de Python refactorizados para usar `from vitispray.paths import DETECT_FIELD_DATASET, MONOCLASS_DATASET`.

### Verificaciones
- Se verificó la integridad mediante el comando `check_det_dataset` de Ultralytics, validando la accesibilidad a imágenes y labels.
- Se generó el informe de resoluciones `DATASET_IMAGE_RESOLUTIONS.md`.
## Registro de Reorganización (2026-09-17) - FASE 2 Bloque C
**IA y YOLO Consolidados en `03_ia_yolo/`**

### Archivos Movidos
- **Scripts de Entrenamiento (`03_ia_yolo/scripts/training/`):** `train_detection.py`, `train_baseline.py`
- **Scripts de Preparación (`03_ia_yolo/scripts/preparation/`):** `prepare_detection_dataset.py`, `prepare_monoclass_dataset.py`
- **Scripts de Evaluación (`03_ia_yolo/scripts/evaluation/`):** `evaluate_test_set.py`, `verify_dataset_detect.py`
- **Scripts de Utilidades (`03_ia_yolo/scripts/utilities/`):** `visualize_samples.py`, `check_dataset_polygons.py`, `read_results.py`, `analyze_resolutions.py`, `audit_dataset.py`, `compute_bbox_sizes.py`, `extract_runs.py`, `generate_sample_preds.py`, `print_cases.py`, `visual_bbox_audit.py`
- **Carpetas de Resultados:** 
  - `runs/` -> `03_ia_yolo/runs/`
  - `inspeccion_*` -> `03_ia_yolo/inspections/`
  - `predicciones_*` y `test_visual_*` -> `03_ia_yolo/predictions/`
- **Pesos (`03_ia_yolo/weights/pretrained/`):** `yolo11m.pt`, `yolo11s.pt`, `yolo11s-seg.pt`

### Cambios de Rutas Realizados
- Se agregaron las constantes `YOLO_DIR`, `YOLO_RUNS_DIR`, `YOLO_WEIGHTS_DIR`, `YOLO_PRETRAINED_WEIGHTS_DIR`, `YOLO_SELECTED_WEIGHTS_DIR`, `YOLO_PREDICTIONS_DIR`, `YOLO_INSPECTIONS_DIR`, `YOLO_METRICS_DIR` a `src/vitispray/paths.py`.
- Se refactorizaron los scripts movidos para eliminar rutas hardcodeadas (ej. `Path(__file__)`) y utilizar las nuevas constantes de `vitispray.paths`.

### Documentación y Gestión
- Se creó `03_ia_yolo/README.md` detallando la estructura y convenciones del módulo.
- Se actualizó `00_gestion/EXPERIMENTOS.csv` reconstruyendo la historia desde los 7 runs verificables.
- Se creó `00_gestion/NOTAS_PARA_MEMORIA_PFE.md` incorporando las metodologías, decisiones técnicas (arquitectura two-pass, dataset), y la corrección metodológica del problema de escala (demostrando que imgsz=640 es viable y los objetos son de tamaño medio/grande, no de 1-8 px).

### Verificaciones
- Smoke tests completados verificando imports y acceso a datasets/pesos (`python -c "from vitispray.paths import YOLO_DIR..."`, `train_detection.py --help`, compilación sintáctica mediante `py_compile`).
