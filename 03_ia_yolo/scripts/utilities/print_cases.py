import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('00_gestion/bbox_size_analysis.json') as f:
    data = json.load(f)

targets = [
    'IMG_2720_JPG.rf.6843b1270845a417fa4c553dbb7d21e6.jpg',
    'IMG_2075_JPG.rf.dcfab8f864bd8ab67eb10dfd5ea777b5.jpg'
]
for fn in targets:
    recs = [r for r in data if r['filename'] == fn]
    if not recs:
        print(f'{fn}: NOT FOUND')
        continue
    r0 = recs[0]
    ow, oh = r0['orig_w'], r0['orig_h']
    s640, s800 = r0['scale_640'], r0['scale_800']
    print(f'\nFILE: {fn}')
    print(f'  orig: {ow}x{oh}  scale@640={s640}  scale@800={s800}')
    print(f'  canvas@640: {int(round(ow*s640))}x{int(round(oh*s640))}')
    print(f'  canvas@800: {int(round(ow*s800))}x{int(round(oh*s800))}')
    for i, r in enumerate(recs):
        print(f'  box[{i}]: orig={r["orig_bw_px"]:.0f}x{r["orig_bh_px"]:.0f}px  '
              f'area={r["area_pct"]:.3f}%  '
              f'@640: {r["resized_bw_640"]:.1f}x{r["resized_bh_640"]:.1f}px [{r["class_640"]}]  '
              f'@800: {r["resized_bw_800"]:.1f}x{r["resized_bh_800"]:.1f}px [{r["class_800"]}]')
