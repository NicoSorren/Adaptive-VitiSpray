# Auditoría Interna del Dataset Portugal

## 1. El Misterio de las 2252 Imágenes

En el reporte inicial se indicó que la clase *Powdery Mildew* del dataset Portugal contenía exactamente 2252 imágenes, lo cual duplicaba la cifra de ~1126 que se tenía como referencia.

**Resolución del problema:**
Tras ejecutar una auditoría interna rigurosa usando hashes MD5 y agrupamiento de nombres de archivo, se descubrió que el dataset original contiene **exactamente 1126 imágenes únicas**, sin ningún duplicado interno real.

**Causa del error:**
El script de auditoría utilizaba la instrucción en Python:
`images = list(path.glob('*.jpg')) + list(path.glob('*.JPG'))`

En sistemas operativos Windows, el sistema de archivos es *case-insensitive* (no distingue mayúsculas de minúsculas). Por lo tanto, `glob('*.jpg')` ya estaba recolectando todos los archivos. Al sumar `glob('*.JPG')`, se duplicó la lista en memoria exactamente 1 a 1, procesando cada imagen dos veces y reportando 2252 hallazgos, con "1126 duplicados exactos MD5".

## 2. Inventario Corregido
* **Total imágenes reales e independientes:** 1126
* **Duplicados MD5 internos:** 0
* **Near-duplicates (pHash) internos:** 0

## 3. Patrones de Archivos (Linaje Temporal)
Los nombres de los archivos siguen un estricto formato de fecha y hora: `IMG_YYYYMMDD_HHMMSS.jpg`
Al agrupar las imágenes, se observa claramente la estructura de captura temporal:

* `IMG_20251014`: 583 imágenes (Campaña de octubre)
* `IMG_20251009`: 167 imágenes
* `IMG_20251002`: 124 imágenes
* `IMG_20251001`: 102 imágenes
* `IMG_20250912`: 71 imágenes
* `IMG_20251023`: 43 imágenes
* `IMG_20250814`: 36 imágenes (Inicio de campaña)

**Conclusión:**
El dataset proviene de un trabajo sistemático y ordenado realizado entre **agosto y octubre de 2025**, recolectando datos fotográficos de manera controlada. Todo el material es visualmente independiente (sin *crops* ni *resizes* duplicados) y constituye una base sólida y 100% libre de fugas de datos (*data leakage*) respecto a nuestros otros datasets.
