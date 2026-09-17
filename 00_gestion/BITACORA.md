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
