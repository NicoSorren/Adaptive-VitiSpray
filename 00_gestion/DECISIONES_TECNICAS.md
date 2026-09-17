# Decisiones Técnicas (ADR)

| Fecha | Contexto / Problema | Opciones Consideradas | Decisión Tomada | Justificación |
|---|---|---|---|---|
| 2026-09-16 | Selección de modelo base de detección YOLO | YOLOv11s vs YOLOv11m | YOLOv11s | Mejor balance entre Precisión (90%), Recall (78%) e inferencia rápida (~135 FPS), superior a v11m para este caso. |
| 2026-09-17 | Organización de estructura de repositorio | Estructura plana vs Estructura modular numerada | Estructura modular numerada (00 a 06) | Facilita la trazabilidad del PFE, separando datos, modelo IA, MVP, Simulación y Documentación. |
