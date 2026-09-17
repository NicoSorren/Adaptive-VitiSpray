from pathlib import Path
from PIL import Image
from collections import Counter
import csv

def analyze_dataset(dataset_name, images_dirs):
    print(f"Analyzing {dataset_name}...")
    widths = []
    heights = []
    resolutions = []
    less_320 = 0
    b_320_479 = 0
    b_480_639 = 0
    b_640_799 = 0
    gte_800 = 0
    
    total = 0
    for d in images_dirs:
        if not d.exists(): continue
        for img_path in d.glob("*.*"):
            if img_path.suffix.lower() not in ['.jpg', '.png', '.jpeg']: continue
            try:
                with Image.open(img_path) as img:
                    w, h = img.size
                    widths.append(w)
                    heights.append(h)
                    resolutions.append(f"{w}x{h}")
                    
                    min_dim = min(w, h)
                    if min_dim < 320: less_320 += 1
                    elif 320 <= min_dim <= 479: b_320_479 += 1
                    elif 480 <= min_dim <= 639: b_480_639 += 1
                    elif 640 <= min_dim <= 799: b_640_799 += 1
                    else: gte_800 += 1
                    total += 1
            except:
                pass

    if total == 0:
        return None
    
    widths.sort()
    heights.sort()
    
    res = {
        "name": dataset_name,
        "total": total,
        "min_res": f"{widths[0]}x{heights[0]}",
        "max_res": f"{widths[-1]}x{heights[-1]}",
        "median_res": f"{widths[total//2]}x{heights[total//2]}",
        "most_common": Counter(resolutions).most_common(3),
        "less_320": f"{(less_320/total)*100:.1f}%",
        "b_320_479": f"{(b_320_479/total)*100:.1f}%",
        "b_480_639": f"{(b_480_639/total)*100:.1f}%",
        "b_640_799": f"{(b_640_799/total)*100:.1f}%",
        "gte_800": f"{(gte_800/total)*100:.1f}%",
    }
    return res

datasets = {
    "dataset_detect_field": [
        Path("02_datasets/procesados/dataset_detect_field/train/images"),
        Path("02_datasets/procesados/dataset_detect_field/valid/images"),
        Path("02_datasets/procesados/dataset_detect_field/test/images")
    ],
    "dataset_monoclass_powdery_mildew": [
        Path("02_datasets/procesados/dataset_monoclass_powdery_mildew/train/images"),
        Path("02_datasets/procesados/dataset_monoclass_powdery_mildew/valid/images"),
        Path("02_datasets/procesados/dataset_monoclass_powdery_mildew/test/images")
    ],
    "Final Grape Leaf Disease Detection": [
        Path("02_datasets/publicos/Final Grape Leaf Disease Detection and Classification.v1i.yolov11/train/images"),
        Path("02_datasets/publicos/Final Grape Leaf Disease Detection and Classification.v1i.yolov11/valid/images"),
        Path("02_datasets/publicos/Final Grape Leaf Disease Detection and Classification.v1i.yolov11/test/images")
    ]
}

results = []
for name, dirs in datasets.items():
    r = analyze_dataset(name, dirs)
    if r:
        results.append(r)

# Generar MD
md_path = Path("00_gestion/DATASET_IMAGE_RESOLUTIONS.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# Informe de Resoluciones de Datasets\n\n")
    for r in results:
        f.write(f"## {r['name']}\n")
        f.write(f"- **Total imágenes:** {r['total']}\n")
        f.write(f"- **Resolución mínima:** {r['min_res']}\n")
        f.write(f"- **Resolución máxima:** {r['max_res']}\n")
        f.write(f"- **Resolución mediana:** {r['median_res']}\n")
        f.write(f"- **Más frecuentes:** {', '.join([f'{res} ({count})' for res, count in r['most_common']])}\n\n")
        f.write("### Distribución por dimensión menor\n")
        f.write(f"- `< 320`: {r['less_320']}\n")
        f.write(f"- `320-479`: {r['b_320_479']}\n")
        f.write(f"- `480-639`: {r['b_480_639']}\n")
        f.write(f"- `640-799`: {r['b_640_799']}\n")
        f.write(f"- `>= 800`: {r['gte_800']}\n\n")

# Generar CSV
csv_path = Path("00_gestion/dataset_image_resolutions.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"Reportes generados en {md_path} y {csv_path}")
