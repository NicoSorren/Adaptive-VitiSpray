"""
Calcula dimensiones exactas de cada bounding box del dataset_detect_field
después del letterbox de Ultralytics para imgsz=640 e imgsz=800.

No modifica nada. Solo lee labels e imágenes.
"""
import cv2
import glob
import os
import json
from pathlib import Path

DATASET_DIR = Path("02_datasets/procesados/dataset_detect_field")
IMGSZ_LIST  = [640, 800]

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp"}

def letterbox_dims(orig_w, orig_h, imgsz):
    """
    Reproduce el letterbox de Ultralytics:
    - Escala el lado más largo a imgsz, manteniendo aspect ratio.
    - Retorna (new_w, new_h, scale) antes de aplicar padding.
    La escala se aplica por igual a w y h.
    """
    scale = imgsz / max(orig_w, orig_h)
    new_w = int(round(orig_w * scale))
    new_h = int(round(orig_h * scale))
    return new_w, new_h, scale

def classify_size(px_val):
    if px_val < 8:
        return "tiny"
    elif px_val < 16:
        return "very_small"
    elif px_val < 32:
        return "small"
    elif px_val < 96:
        return "medium"
    else:
        return "large"

records = []

for split in ["train", "valid", "test"]:
    img_dir = DATASET_DIR / split / "images"
    lbl_dir = DATASET_DIR / split / "labels"

    if not img_dir.exists():
        continue

    for img_path in sorted(img_dir.glob("*")):
        if img_path.suffix.lower() not in IMG_EXTS:
            continue

        stem = img_path.stem
        lbl_path = lbl_dir / (stem + ".txt")
        if not lbl_path.exists():
            continue

        with open(lbl_path) as f:
            lines = [l.strip() for l in f if l.strip()]
        if not lines:
            continue

        # Read actual image dimensions
        img = cv2.imread(str(img_path))
        if img is None:
            continue
        orig_h, orig_w = img.shape[:2]

        source = "Italia" if stem.startswith("italy_") else "Roboflow"

        for line in lines:
            parts = list(map(float, line.split()))
            if len(parts) < 5:
                continue
            _, cx, cy, bw_rel, bh_rel = parts[:5]

            # Original pixel dimensions
            orig_bw_px = bw_rel * orig_w
            orig_bh_px = bh_rel * orig_h

            rec = {
                "split": split,
                "source": source,
                "filename": img_path.name,
                "orig_w": orig_w,
                "orig_h": orig_h,
                "cx": cx, "cy": cy,
                "bw_rel": round(bw_rel, 6),
                "bh_rel": round(bh_rel, 6),
                "orig_bw_px": round(orig_bw_px, 1),
                "orig_bh_px": round(orig_bh_px, 1),
                "area_pct": round(bw_rel * bh_rel * 100, 3),
            }

            for isz in IMGSZ_LIST:
                new_w, new_h, scale = letterbox_dims(orig_w, orig_h, isz)
                resized_bw = orig_bw_px * scale
                resized_bh = orig_bh_px * scale
                min_side = min(resized_bw, resized_bh)
                rec[f"resized_bw_{isz}"] = round(resized_bw, 2)
                rec[f"resized_bh_{isz}"] = round(resized_bh, 2)
                rec[f"scale_{isz}"]       = round(scale, 6)
                rec[f"min_side_{isz}"]    = round(min_side, 2)
                rec[f"class_{isz}"]       = classify_size(min_side)

            records.append(rec)

# ─── Save JSON ────────────────────────────────────────────────────────────────
out_json = Path("00_gestion/bbox_size_analysis.json")
with open(out_json, "w") as f:
    json.dump(records, f, indent=2)
print(f"Total bboxes analyzed: {len(records)}")
print(f"Saved: {out_json}")

# ─── Summary stats ────────────────────────────────────────────────────────────
from collections import defaultdict

def summarize(recs, key, imgsz):
    counts = defaultdict(int)
    for r in recs:
        counts[r[f"class_{imgsz}"]] += 1
    total = len(recs)
    cats = ["tiny","very_small","small","medium","large"]
    print(f"\n  [{key} | imgsz={imgsz}]  total={total}")
    for c in cats:
        n = counts[c]
        print(f"    {c:12s}: {n:5d}  ({n/total*100:.1f}%)")

# By source
for src in ["Roboflow", "Italia"]:
    recs = [r for r in records if r["source"] == src]
    for isz in IMGSZ_LIST:
        summarize(recs, src, isz)

# By split
for sp in ["train","valid","test"]:
    recs = [r for r in records if r["split"] == sp]
    for isz in IMGSZ_LIST:
        summarize(recs, sp, isz)

# ─── Specific cases: IMG_2720 and IMG_2075 ────────────────────────────────────
print("\n" + "="*60)
print("CASOS ESPECÍFICOS: IMG_2720 e IMG_2075")
print("="*60)
for fname in ["IMG_2720_JPG.rf.6843b1270845a417fa4c553dbb7d21e6.jpg",
              "IMG_2075_JPG.rf.dcfab8f864bd8ab67eb10dfd5ea777b5.jpg"]:
    recs_f = [r for r in records if r["filename"] == fname]
    if not recs_f:
        print(f"\n  {fname}: NOT FOUND")
        continue
    r0 = recs_f[0]
    print(f"\n  File : {fname}")
    print(f"  Orig : {r0['orig_w']}x{r0['orig_h']} px")
    print(f"  Scale@640: {r0['scale_640']}  → canvas {int(round(r0['orig_w']*r0['scale_640']))}x{int(round(r0['orig_h']*r0['scale_640']))}")
    print(f"  Scale@800: {r0['scale_800']}  → canvas {int(round(r0['orig_w']*r0['scale_800']))}x{int(round(r0['orig_h']*r0['scale_800']))}")
    print(f"  BBoxes ({len(recs_f)} total):")
    for r in recs_f:
        print(f"    orig={r['orig_bw_px']:.0f}x{r['orig_bh_px']:.0f}px  area={r['area_pct']:.3f}%"
              f"  →@640: {r['resized_bw_640']:.1f}x{r['resized_bh_640']:.1f}px [{r['class_640']}]"
              f"  →@800: {r['resized_bw_800']:.1f}x{r['resized_bh_800']:.1f}px [{r['class_800']}]")
