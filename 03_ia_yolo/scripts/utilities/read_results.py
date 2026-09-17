import csv, sys

csv_path = 'runs/detect/yolo11m_detect_field_v1/results.csv'
with open(csv_path, 'r') as f:
    rows = list(csv.DictReader(f))

rows = [{k.strip(): v.strip() for k, v in r.items()} for r in rows]
print(f'Total epochs completed: {len(rows)}')
print('Columns:', list(rows[0].keys()))
print()

best = max(rows, key=lambda r: float(r.get('metrics/mAP50(B)', 0)))
last = rows[-1]

def fmt(r):
    lines = [
        f'  Epoch:     {r["epoch"]}',
        f'  Box Loss:  {float(r["train/box_loss"]):.4f}',
        f'  Cls Loss:  {float(r["train/cls_loss"]):.4f}',
        f'  Precision: {float(r["metrics/precision(B)"])*100:.2f}%',
        f'  Recall:    {float(r["metrics/recall(B)"])*100:.2f}%',
        f'  mAP50:     {float(r["metrics/mAP50(B)"])*100:.2f}%',
        f'  mAP50-95:  {float(r["metrics/mAP50-95(B)"])*100:.2f}%',
        f'  val/box:   {float(r["val/box_loss"]):.4f}',
        f'  val/cls:   {float(r["val/cls_loss"]):.4f}',
    ]
    return '\n'.join(lines)

print('=== MEJOR EPOCH (por mAP50) ===')
print(fmt(best))
print()
print('=== ULTIMO EPOCH ===')
print(fmt(last))
