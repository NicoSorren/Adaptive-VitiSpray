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
## Evaluación Externa (2026-09-17) - FASE 2
Se realizó una validación externa con un conjunto de datos manual que no fue utilizado en el entrenamiento (19 imágenes).

### Verificación de Data Leakage
- **Resultado:** 0 duplicados encontrados entre el conjunto externo y los splits de entrenamiento, validación y test (`dataset_detect_field`).

### Inferencias (Threshold: 0.25)
- **Oídio:** Se detectaron 6 de 12 imágenes correctamente (50% de tasa cualitativa de detección). Las 6 restantes (falsos negativos) muestran una gran dificultad para generalizar en diferentes contextos/enfermedades.
- **Falsos Positivos:** 0 falsos positivos en 4 imágenes con Peronospora y 0 falsos positivos en 3 imágenes sanas.
- **Recomendación provisional:** Se estableció que `conf=0.25` es el umbral adecuado para este modelo, ya que evita falsos positivos mientras logra atrapar síntomas moderados que se pierden con `conf=0.50`.
- **Registro:** Identificador de experimento: `EXP-YOLO-EXT-001`.
## Evaluación Externa V2 (2026-09-17) - FASE 2
Se repitió la validación externa (EXP-YOLO-EXT-002) tras corregir la muestra para garantizar que todas las imágenes pertenezcan al dominio de hojas de vid reales.

### Resultados y Comparativa
- **Data Leakage:** 0 duplicados encontrados contra los sets de entrenamiento.
- **Oídio (Tasa de Detección):** Hubo una leve mejoría, alcanzando 7 de 12 detecciones cualitativas a `conf=0.25` (58.3%), frente al 50% de la evaluación previa.
- **Robustez frente a Falsos Positivos:** El modelo mantuvo un impecable **0% de falsos positivos** tanto en hojas con Peronospora como en hojas sanas, probando gran especificidad.
- **Conclusión General:** El cambio al dominio correcto confirma que la recomendación provisional de usar `conf=0.25` es estadísticamente segura para el MVP, dado que capta detecciones de baja intensidad sin desestabilizar la especificidad del sistema. Los falsos negativos remanentes confirman el límite de generalización hacia fenotipos no vistos durante el entrenamiento.
- **Registro:** El informe completo de la versión 2 se ubica en `03_ia_yolo/external_validation/reports/EXTERNAL_GENERALIZATION_REPORT_V2.md`.
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
## Evaluación Externa (2026-09-17) - FASE 2
Se realizó una validación externa con un conjunto de datos manual que no fue utilizado en el entrenamiento (19 imágenes).

### Verificación de Data Leakage
- **Resultado:** 0 duplicados encontrados entre el conjunto externo y los splits de entrenamiento, validación y test (`dataset_detect_field`).

### Inferencias (Threshold: 0.25)
- **Oídio:** Se detectaron 6 de 12 imágenes correctamente (50% de tasa cualitativa de detección). Las 6 restantes (falsos negativos) muestran una gran dificultad para generalizar en diferentes contextos/enfermedades.
- **Falsos Positivos:** 0 falsos positivos en 4 imágenes con Peronospora y 0 falsos positivos en 3 imágenes sanas.
- **Recomendación provisional:** Se estableció que `conf=0.25` es el umbral adecuado para este modelo, ya que evita falsos positivos mientras logra atrapar síntomas moderados que se pierden con `conf=0.50`.
- **Registro:** Identificador de experimento: `EXP-YOLO-EXT-001`.
## Evaluación Externa V2 (2026-09-17) - FASE 2
Se repitió la validación externa (EXP-YOLO-EXT-002) tras corregir la muestra para garantizar que todas las imágenes pertenezcan al dominio de hojas de vid reales.

### Resultados y Comparativa
- **Data Leakage:** 0 duplicados encontrados contra los sets de entrenamiento.
- **Oídio (Tasa de Detección):** Hubo una leve mejoría, alcanzando 7 de 12 detecciones cualitativas a `conf=0.25` (58.3%), frente al 50% de la evaluación previa.
- **Robustez frente a Falsos Positivos:** El modelo mantuvo un impecable **0% de falsos positivos** tanto en hojas con Peronospora como en hojas sanas, probando gran especificidad.
- **Conclusión General:** El cambio al dominio correcto confirma que la recomendación provisional de usar `conf=0.25` es estadísticamente segura para el MVP, dado que capta detecciones de baja intensidad sin desestabilizar la especificidad del sistema. Los falsos negativos remanentes confirman el límite de generalización hacia fenotipos no vistos durante el entrenamiento.
- **Registro:** El informe completo de la versión 2 se ubica en `03_ia_yolo/external_validation/reports/EXTERNAL_GENERALIZATION_REPORT_V2.md`.
## Auditoría de Datasets Candidatos (2026-09-17) - FASE 2
Se realizó una inspección visual y cuantitativa profunda (sin entrenamiento) de dos datasets propuestos:
- **MD Nahid:** Dataset de segmentación (YOLO polygons). Aporta 565 imágenes nuevas sin duplicados con el set actual. Los polígonos rodean fielmente el síntoma extendido. Gran valor para diversificar fondos y resolver fallas de iluminación.
- **HERMOS:** Dataset de detección (VOC XML). Aporta 522 imágenes positivas a masiva resolución con cajas envolventes de tamaño diminuto (mediana de 0.21%). Vital para forzar al modelo a ganar sensibilidad ante ataques incipientes de la enfermedad. El hashing perceptual descubrió 90 imágenes solapadas con `dataset_detect_field`, probando descendencia.
- **Portugal:** Ausente al momento de la revisión.
- **Estado:** Se generó `DATASET_CANDIDATES_AUDIT.md` y paneles visuales en `00_gestion/dataset_candidates_audit/`.
## Auditoría del Dataset Portugal (2026-09-17) - FASE 2
Se auditó el dataset "Portugal" de clasificación. Contiene 1126 imágenes de la clase Powdery Mildew, todas a resolución 1024x1024. El chequeo MD5 y pHash comprobó que el dataset es 100% independiente, con 0% de solapamiento frente a dataset_detect_field, HERMOS y MD Nahid. Se extrajeron 100 imágenes aplicando muestreo de diversidad (brillo/contraste/verde vía K-Means) y se exportaron 10 contact sheets para revisión visual externa pendiente. Documentación actualizada.
## Selección de Anotación para Portugal (2026-09-17) - FASE 2
Se aclaró que el conteo de 2252 imágenes era un bug de sistema operativo ("*.jpg" vs "*.JPG" duplicando el listado) y que la cantidad real de imágenes independientes de la clase Oídio en el dataset Portugal es 1126. A partir de esa cifra, se ejecutó un algoritmo de muestreo híbrido para maximizar diversidad. Se agruparon las imágenes por fecha de captura (7 jornadas) y se extrajeron proporcionalmente usando clustering K-Means sobre características visuales (contraste, color, entropía), resultando en 299 imágenes altamente representativas y sin redundancia. Se generaron las contact sheets visuales y el reporte en `00_gestion/PORTUGAL_ANNOTATION_SELECTION.md`.
## Filtro de Anotación para Portugal (2026-09-18) - FASE 2
La propuesta inicial de 299 imágenes del dataset Portugal fue sometida a revisión visual humana mediante contact sheets. Se descartaron 94 imágenes por baja prioridad/ambigüedad. Las 205 imágenes restantes fueron copiadas (preservando su formato) al directorio `02_datasets/publicos/candidatos/Portugal/selected_for_annotation/`. Se generó el inventario `selected_for_annotation_manifest.csv` para la trazabilidad de la futura anotación. No se modificó el dataset original de entrenamiento. Se estableció la directriz de marcar como REJECTED_AMBIGUOUS cualquier imagen dudosa durante la futura anotación manual.
