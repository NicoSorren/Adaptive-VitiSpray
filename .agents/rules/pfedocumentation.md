---
trigger: always_on
---

# Regla permanente de documentación del PFE

Este repositorio corresponde al Proyecto Final de Ingeniería "Adaptive-VitiSpray".

Cada vez que realices una tarea que produzca información útil para la memoria final del PFE, debés evaluar si corresponde actualizar la documentación de gestión.

Archivos de gestión:

- `00_gestion/BITACORA.md`
  Registrar qué se hizo, cuándo, qué archivos se modificaron y resultado general.

- `00_gestion/DECISIONES_TECNICAS.md`
  Registrar decisiones metodológicas, arquitectónicas o técnicas, incluyendo:
  - problema que motivó la decisión;
  - alternativas consideradas;
  - decisión adoptada;
  - justificación;
  - consecuencias o limitaciones.

- `00_gestion/EXPERIMENTOS.csv`
  Registrar experimentos de entrenamiento, evaluación o comparación cuantitativa.
  No registrar simples inspecciones o tareas administrativas.

- `00_gestion/PROMPTS_CLAVE.md`
  Registrar solamente prompts de IA que hayan producido código relevante,
  decisiones importantes, cambios metodológicos o análisis reproducibles.

- `00_gestion/NOTAS_PARA_MEMORIA_PFE.md`
  Este es el archivo principal para conservar información que probablemente
  deba incorporarse posteriormente a la memoria final del PFE.

Actualizar `NOTAS_PARA_MEMORIA_PFE.md` cuando aparezca cualquiera de estos casos:

1. Un hallazgo técnico relevante.
2. Una limitación descubierta.
3. Una corrección de una hipótesis o interpretación anterior.
4. Una decisión metodológica importante.
5. Una comparación de alternativas.
6. Un resultado cuantitativo significativo.
7. Una modificación del dataset o del pipeline.
8. Una conclusión derivada de un experimento.
9. Una justificación de diseño.
10. Un problema encontrado y su solución.
11. Una observación que pueda ser útil para Metodología, Resultados,
    Discusión, Limitaciones o Trabajo Futuro del informe final.

Reglas de calidad:

- No inventar información.
- No convertir hipótesis en hechos.
- Distinguir claramente:
  - hecho observado;
  - interpretación;
  - hipótesis;
  - decisión;
  - trabajo pendiente.
- Mantener métricas exactas cuando estén disponibles.
- Indicar dataset, modelo, versión o experimento asociado.
- Registrar correcciones de errores anteriores en lugar de ocultarlas.
- Conservar trazabilidad hacia scripts, informes, datasets, runs o artefactos.
- No exagerar resultados.
- Si una muestra es pequeña, indicarlo.
- Si algo no está verificado, escribir `pendiente de verificar`.
- No borrar conclusiones históricas; marcar cuando fueron reemplazadas o corregidas.

Al finalizar una tarea relevante, revisar si corresponde actualizar uno o más
de estos archivos. No es obligatorio modificar todos en cada tarea.

Además, antes de dar por terminada una tarea importante, informar brevemente:

`Documentación PFE actualizada: [archivos]`

o, si no corresponde:

`Documentación PFE: sin actualización necesaria`.