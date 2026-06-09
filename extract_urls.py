import requests
import re
import json
import os

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
})

post_id = "DXztHbzDKaN"
r = session.get(f"https://www.instagram.com/p/{post_id}/", timeout=20)
print(f"Status: {r.status_code}, Size: {len(r.text)}")

# Find all scontent URLs (images)
sc_urls = re.findall(r'https?://scontent[^"\\\s<>]+\.jpg[^"\\\s<>]*', r.text)
print(f"\nFound {len(sc_urls)} scontent image URLs:")
for i, u in enumerate(sc_urls[:8]):
    print(f"  [{i}] {u[:200]}")

# Find video URLs  
vid_urls = re.findall(r'https?://scontent[^"\\\s<>]+\.mp4[^"\\\s<>]*', r.text)
print(f"\nFound {len(vid_urls)} video URLs:")
for i, u in enumerate(vid_urls[:4]):
    print(f"  [{i}] {u[:200]}")

# Find display_url in JSON
disp_pattern = re.compile(r'"display_url"\s*:\s*"([^"]+)"')
disp_urls = disp_pattern.findall(r.text)
print(f"\nFound {len(disp_urls)} display_urls:")
for i, u in enumerate(disp_urls[:6]):
    clean = u.replace('\\u0026', '&')
    print(f"  [{i}] {clean[:200]}")

# Also try image_versions2
iv2_pattern = re.compile(r'"image_versions2"\s*:\s*\{[^}]+\}')
iv2_matches = iv2_pattern.findall(r.text)
print(f"\nFound {len(iv2_matches)} image_versions2 blocks")

# Look for video_versions
vv_pattern = re.compile(r'"video_versions"\s*:\s*\[[^\]]+\]')
vv_matches = vv_pattern.findall(r.text)
print(f"Found {len(vv_matches)} video_versions blocks")

# Extract all URLs from video_versions
for vm in vv_matches:
    vid_urls_in_block = re.findall(r'"url"\s*:\s*"([^"]+)"', vm)
    for vu in vid_urls_in_block:
        clean = vu.replace('\\u0026', '&')
        print(f"  Video URL: {clean[:200]}")

# Check if the page is a login wall or has real content
if '"login' in r.text.lower() or 'login' in r.text[:1000].lower():
    print("\n>>> WARNING: Page might be login wall")
else:
    print(f"\n>>> Page appears to have actual content (first 500 chars):")
    print(r.text[:500])

# Save the URLs we found for downloading
found_urls = list(set(disp_urls))
if found_urls:
    print(f"\n>>> ATTEMPTING TO DOWNLOAD {len(found_urls)} IMAGES:")
    for i, url in enumerate(found_urls):
        clean = url.replace('\\u0026', '&')
        try:
            img_r = session.get(clean, timeout=20, headers={'Referer': 'https://www.instagram.com/'})
            print(f"  [{i}] Status: {img_r.status_code}, Size: {len(img_r.content)}")
            if img_r.status_code == 200 and len(img_r.content) > 3000:
                ext = 'jpg'
                if 'Content-Type' in img_r.headers:
                    ct = img_r.headers['Content-Type']
                    if 'png' in ct:
                        ext = 'png'
                    elif 'webp' in ct:
                        ext = 'webp'
                fname = f"images/posts/post_real_{i}.{ext}"
                with open(fname, 'wb') as f:
                    f.write(img_r.content)
                print(f"  >>> SAVED: {fname} ({len(img_r.content)} bytes)")
        except Exception as e:
            print(f"  [{i}] Error: {e}")
else:
    print("\n>>> NO display_urls found in page source")
    # Dump all JSON-like content
    json_matches = re.findall(r'window\.__INITIAL_STATE__\s*=\s*(\{.+?\});', r.text, re.DOTALL)
    print(f"Found __INITIAL_STATE__: {len(json_matches)}")
    for jm in json_matches:
        print(jm[:1000])
