"""
Auditoría visual de semántica de Bounding Boxes.
Genera paneles comparativos: Original | GT | Predicción.
No modifica ningún dataset ni anotación.
"""
import os
import cv2
import numpy as np
import glob
import random
import json
from pathlib import Path
from ultralytics import YOLO

# ─── CONFIG ──────────────────────────────────────────────────────────────────
DATASET_DIR   = Path("02_datasets/procesados/dataset_detect_field")
MODEL_PATH    = Path("runs/detect/yolo11m_detect_field_v1/weights/best.pt")
OUT_DIR       = Path("00_gestion/auditoria_semantica_bbox")
CONF_MAIN     = 0.50
CONF_LOW      = 0.25
RANDOM_SEED   = 42
N_PER_SOURCE  = 15   # 15 Roboflow + 15 Italy

GT_COLOR      = (0,   200,  0)   # green  – Ground Truth
PRED_COLOR    = (0,   128, 255)  # blue   – Prediction (high conf)
PRED_LOW_COLOR= (0,   200, 200)  # cyan   – Prediction (low conf)
FONT          = cv2.FONT_HERSHEY_SIMPLEX
# ─────────────────────────────────────────────────────────────────────────────

def load_labels(label_path, img_w, img_h):
    boxes = []
    if not label_path.exists():
        return boxes
    with open(label_path) as f:
        for line in f:
            parts = list(map(float, line.strip().split()))
            if len(parts) < 5:
                continue
            cx, cy, w, h = parts[1], parts[2], parts[3], parts[4]
            x1 = int((cx - w/2) * img_w)
            y1 = int((cy - h/2) * img_h)
            x2 = int((cx + w/2) * img_w)
            y2 = int((cy + h/2) * img_h)
            area_pct = w * h * 100
            boxes.append({"x1": x1, "y1": y1, "x2": x2, "y2": y2,
                          "w_rel": w, "h_rel": h, "area_pct": area_pct})
    return boxes

def draw_boxes_gt(img, boxes, color=GT_COLOR):
    out = img.copy()
    for b in boxes:
        cv2.rectangle(out, (b["x1"], b["y1"]), (b["x2"], b["y2"]), color, 2)
        label = f"GT {b['area_pct']:.1f}%"
        cv2.putText(out, label, (b["x1"], max(b["y1"]-6, 12)), FONT, 0.5, color, 2)
    return out

def draw_boxes_pred(img, results, conf_thr):
    out = img.copy()
    boxes = results.boxes
    pred_info = []
    for box in boxes:
        conf = float(box.conf[0])
        if conf < conf_thr:
            continue
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        h_img, w_img = out.shape[:2]
        bw = (x2 - x1) / w_img
        bh = (y2 - y1) / h_img
        area_pct = bw * bh * 100
        color = PRED_COLOR if conf >= CONF_MAIN else PRED_LOW_COLOR
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        label = f"conf={conf:.2f} {area_pct:.1f}%"
        cv2.putText(out, label, (x1, max(y1-6, 12)), FONT, 0.45, color, 2)
        pred_info.append({"conf": conf, "area_pct": area_pct, "x1": x1, "y1": y1, "x2": x2, "y2": y2})
    return out, pred_info

def make_header(text, w, h=30, bg=(30, 30, 30)):
    bar = np.full((h, w, 3), bg, dtype=np.uint8)
    cv2.putText(bar, text, (6, h-8), FONT, 0.55, (220,220,220), 1)
    return bar

def compute_iou(gt_box, pred_box):
    """IoU between a single GT box and a single pred box (both as x1,y1,x2,y2 dicts)."""
    ix1 = max(gt_box["x1"], pred_box["x1"])
    iy1 = max(gt_box["y1"], pred_box["y1"])
    ix2 = min(gt_box["x2"], pred_box["x2"])
    iy2 = min(gt_box["y2"], pred_box["y2"])
    inter = max(0, ix2-ix1) * max(0, iy2-iy1)
    union = ((gt_box["x2"]-gt_box["x1"])*(gt_box["y2"]-gt_box["y1"]) +
             (pred_box["x2"]-pred_box["x1"])*(pred_box["y2"]-pred_box["y1"]) - inter)
    return inter / union if union > 0 else 0.0

def process_image(img_path: Path, label_path: Path, model, out_dir: Path, idx: int, source: str):
    img_orig = cv2.imread(str(img_path))
    if img_orig is None:
        print(f"  [WARN] Cannot read {img_path}")
        return None

    h_orig, w_orig = img_orig.shape[:2]
    gt_boxes = load_labels(label_path, w_orig, h_orig)

    # Run inference (get both conf levels)
    results = model(str(img_path), verbose=False, conf=CONF_LOW)[0]

    # Build panels
    panel_orig = img_orig.copy()
    panel_gt   = draw_boxes_gt(img_orig, gt_boxes)
    panel_pred_high, pred_info_high = draw_boxes_pred(img_orig, results, CONF_MAIN)
    panel_pred_low,  pred_info_low  = draw_boxes_pred(img_orig, results, CONF_LOW)

    # Resize panels to equal height for side-by-side
    TARGET_H = 480
    TARGET_W = int(w_orig * TARGET_H / h_orig)
    resize = lambda x: cv2.resize(x, (TARGET_W, TARGET_H))
    p_o  = resize(panel_orig)
    p_gt = resize(panel_gt)
    p_ph = resize(panel_pred_high)
    p_pl = resize(panel_pred_low)

    # Headers
    h_o  = make_header(f"A - ORIGINAL  ({w_orig}x{h_orig})", TARGET_W)
    h_gt = make_header(f"B - GT ({len(gt_boxes)} boxes)", TARGET_W, bg=(0,50,0))
    h_ph = make_header(f"C - PRED conf>=0.50 ({len(pred_info_high)} dets)", TARGET_W, bg=(0,0,80))
    h_pl = make_header(f"D - PRED conf>=0.25 ({len(pred_info_low)} dets)", TARGET_W, bg=(0,40,60))

    row1 = np.hstack([np.vstack([h_o, p_o]),   np.vstack([h_gt, p_gt])])
    row2 = np.hstack([np.vstack([h_ph, p_ph]),  np.vstack([h_pl, p_pl])])

    # Title bar
    title_bar = np.full((40, row1.shape[1], 3), (15,15,15), dtype=np.uint8)
    title_txt = f"[{idx:02d}] {source} | {img_path.name}"
    cv2.putText(title_bar, title_txt, (10, 28), FONT, 0.6, (255,200,50), 2)

    composite = np.vstack([title_bar, row1, row2])

    out_filename = out_dir / f"{idx:02d}_{source}_{img_path.stem[:50]}.jpg"
    cv2.imwrite(str(out_filename), composite, [cv2.IMWRITE_JPEG_QUALITY, 88])

    # IoU computation (best match per GT box)
    iou_pairs = []
    for gb in gt_boxes:
        best_iou = 0.0
        for pb in pred_info_high:
            iou = compute_iou(gb, pb)
            if iou > best_iou:
                best_iou = iou
        iou_pairs.append(best_iou)

    return {
        "idx": idx,
        "source": source,
        "filename": img_path.name,
        "resolution": f"{w_orig}x{h_orig}",
        "gt_boxes": len(gt_boxes),
        "gt_areas_pct": [round(b["area_pct"], 2) for b in gt_boxes],
        "pred_high_count": len(pred_info_high),
        "pred_high_confs": [round(p["conf"], 3) for p in pred_info_high],
        "pred_low_count": len(pred_info_low),
        "iou_gt_vs_pred": [round(x, 3) for x in iou_pairs],
        "out_file": out_filename.name
    }

def collect_positive_images(split_dirs, source_prefix, n):
    """Collect n images that have at least one GT annotation."""
    candidates = []
    for split in split_dirs:
        img_dir = DATASET_DIR / split / "images"
        lbl_dir = DATASET_DIR / split / "labels"
        for img_path in img_dir.glob("*.*"):
            name = img_path.name
            is_match = (source_prefix == "italy_" and name.lower().startswith("italy_")) or \
                       (source_prefix == "robo_"  and not name.lower().startswith("italy_"))
            if not is_match:
                continue
            stem = img_path.stem
            lbl = lbl_dir / (stem + ".txt")
            if lbl.exists():
                with open(lbl) as f:
                    content = f.read().strip()
                if content:
                    candidates.append((img_path, lbl))
    random.seed(RANDOM_SEED)
    random.shuffle(candidates)
    return candidates[:n]

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[*] Loading model from {MODEL_PATH}")
    model = YOLO(str(MODEL_PATH))

    splits = ["train", "valid", "test"]

    print(f"[*] Collecting Roboflow samples...")
    robo_samples  = collect_positive_images(splits, "robo_",  N_PER_SOURCE)
    print(f"    Found {len(robo_samples)} Roboflow positives")

    print(f"[*] Collecting Italy samples...")
    italy_samples = collect_positive_images(splits, "italy_", N_PER_SOURCE)
    print(f"    Found {len(italy_samples)} Italy positives")

    all_samples = [(img, lbl, "Roboflow") for img, lbl in robo_samples] + \
                  [(img, lbl, "Italia")   for img, lbl in italy_samples]

    results_log = []
    for i, (img_path, lbl_path, source) in enumerate(all_samples, start=1):
        print(f"  [{i:02d}/{len(all_samples)}] {source}: {img_path.name}")
        info = process_image(img_path, lbl_path, model, OUT_DIR, i, source)
        if info:
            results_log.append(info)

    # Save JSON log
    log_path = OUT_DIR / "audit_data.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=2, ensure_ascii=False)

    print(f"\n[+] Done! Generated {len(results_log)} panels in {OUT_DIR}")
    print(f"[+] JSON log saved to {log_path}")
    return results_log

if __name__ == "__main__":
    main()
