# VitiSpray - Módulo de Prescripción MVP

Prototipo modular para generar mapas de prescripción para la pulverización selectiva de oídio en viñedos.

## Arquitectura

El módulo está diseñado para separar la lógica de fusión espacial y generación de prescripciones del modelo matemático epidemiológico subyacente.

*   `models.py`: Estructuras de datos base (Focos, Entorno, Zonas).
*   `config.py`: Parámetros experimentales de distancia (MVP) y configuración de la hilera.
*   `risk_model.py`: **Punto de extensión futuro**. Aquí reside el modelo MVP asimétrico. Este es el archivo donde se integrarán los modelos epidemiológicos científicos.
*   `prescription.py`: Algoritmos genéricos de generación de zonas, fusión y exportación, agnósticos del modelo de riesgo específico.
*   `visualization.py`: Rutinas de graficación usando Matplotlib.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución del MVP

```bash
python main.py
```
Esto generará los gráficos y el archivo JSON en el directorio `outputs/`.

## Pruebas

```bash
pytest tests/
```
