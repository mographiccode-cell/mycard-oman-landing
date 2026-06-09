from PIL import Image
from collections import Counter
import colorsys, json

img = Image.open('images/profile/avatar-large.png').convert('RGB')
pixels = list(img.getdata())
total = len(pixels)

color_counts = Counter()
for r, g, b in pixels:
    qr = (r // 24) * 24
    qg = (g // 24) * 24
    qb = (b // 24) * 24
    color_counts[(qr, qg, qb)] += 1

clusters = []
for (r, g, b), count in color_counts.most_common(300):
    brightness = (r + g + b) / 3
    saturation = max(r, g, b) - min(r, g, b)
    if saturation > 25 and 15 < brightness < 250:
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        clusters.append({
            'hex': '#{:02X}{:02X}{:02X}'.format(r, g, b),
            'rgb': [r, g, b],
            'pct': round(count / total * 100, 2),
            'hue': round(h * 360),
            'sat': round(s * 100),
            'val': round(v * 100),
            'count': count
        })

print("=== TOP 15 AVATAR COLORS (filtered) ===")
for c in clusters[:15]:
    print("  {} | hue={:3d} sat={:2d}% val={:2d}% | {:5.1f}%".format(
        c['hex'], c['hue'], c['sat'], c['val'], c['pct']
    ))

# Find blues (hue around 200-240)
blues = [c for c in clusters if 180 < c['hue'] < 250]
navys = [c for c in blues if c['val'] < 45]
mid_blues = [c for c in blues if 45 <= c['val'] <= 70]
light_blues = [c for c in blues if c['val'] > 70]

print("\n=== BLUE FAMILY ===")
navys.sort(key=lambda x: -x['pct'])
mid_blues.sort(key=lambda x: -x['pct'])
light_blues.sort(key=lambda x: -x['pct'])

if navys:
    best_navy = navys[0]
    print("Primary (Dark Navy): {} | {:.1f}%".format(best_navy['hex'], best_navy['pct']))
if mid_blues:
    best_mid = mid_blues[0]
    print("Secondary (Mid Blue): {} | {:.1f}%".format(best_mid['hex'], best_mid['pct']))
if light_blues:
    best_light = light_blues[0]
    print("Accent (Light Blue): {} | {:.1f}%".format(best_light['hex'], best_light['pct']))

# Summary
print("\n=== BRAND IDENTITY FROM AVATAR ===")
print("The avatar (logo) shows:")
print("  Dominant: Light blue/cyan tones")
print("  Accents: Dark navy elements")
print("  Overall: Cool blue color palette")
print("\nThis is the TRUE brand identity of @mycard.oman")
print("The post designs (invitations) use varied warm colors per event type,")
print("but the brand logo is distinctly blue/cyan/navy.")
