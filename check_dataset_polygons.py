import os
import glob
import cv2
import numpy as np

LABEL_DIR = "Final Grape Leaf Disease Detection and Classification.v1i.yolov11/train/labels"
IMG_DIR = "Final Grape Leaf Disease Detection and Classification.v1i.yolov11/train/images"
OUT_DIR = "inspeccion_ground_truth"
os.makedirs(OUT_DIR, exist_ok=True)

CLASS_NAMES = {0: "Birds_Eye_Rot", 1: "Healthy", 2: "Powdery_Mildew"}
COLORS = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255)} # BGR

label_files = glob.glob(os.path.join(LABEL_DIR, "*.txt"))
print(f"Total label files: {len(label_files)}")

areas_by_class = {0: [], 1: [], 2: []}
# Compute stats fast without opening large images
for lf in label_files:
    with open(lf, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    for line in lines:
        parts = list(map(float, line.split()))
        cls_id = int(parts[0])
        coords = np.array(parts[1:]).reshape(-1, 2)
        
        # Polygon area (normalized)
        x = coords[:, 0]
        y = coords[:, 1]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        areas_by_class[cls_id].append(area)

print("\n--- RESUMEN DE ÁREAS NORMALIZADAS ---", flush=True)
for cls_id, name in CLASS_NAMES.items():
    arr = areas_by_class[cls_id]
    if arr:
        print(f"{name} ({cls_id}): {len(arr)} polígonos | Promedio: {np.mean(arr)*100:.2f}% del frame | Mediana: {np.median(arr)*100:.2f}% | Min: {np.min(arr)*100:.4f}% | Max: {np.max(arr)*100:.2f}%", flush=True)

# Now draw 5 images from different subsets (e.g. PlantVillage vs Field)
drawn = 0
for lf in label_files:
    if drawn >= 5:
        break
    base_name = os.path.splitext(os.path.basename(lf))[0]
    img_path = os.path.join(IMG_DIR, base_name + ".jpg")
    if not os.path.exists(img_path):
        continue
    with open(lf, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if any(int(l.split()[0]) == 2 for l in lines):
        img = cv2.imread(img_path)
        if img is None:
            continue
        h, w = img.shape[:2]
        # Resize to max 1024 for quick visualization
        scale = 1024.0 / max(h, w)
        if scale < 1.0:
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
            h, w = img.shape[:2]
        
        for line in lines:
            parts = list(map(float, line.split()))
            cls_id = int(parts[0])
            coords = np.array(parts[1:]).reshape(-1, 2)
            pts = (coords * np.array([w, h])).astype(np.int32)
            color = COLORS.get(cls_id, (255, 255, 255))
            overlay = img.copy()
            cv2.fillPoly(overlay, [pts], color)
            cv2.addWeighted(overlay, 0.35, img, 0.65, 0, img)
            cv2.polylines(img, [pts], isClosed=True, color=color, thickness=2)
            label_text = CLASS_NAMES.get(cls_id, "Cls")
            cv2.putText(img, label_text, (pts[0,0], pts[0,1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            
        cv2.imwrite(os.path.join(OUT_DIR, f"gt_{drawn}_{base_name[:20]}.jpg"), img)
        drawn += 1
        print(f"Generada imagen {drawn}: {base_name[:20]}.jpg (orig {w/scale:.0f}x{h/scale:.0f})", flush=True)

