import requests
import re
import os
import json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

# Get imginn profile page
r = session.get('https://imginn.com/mycard.oman/', timeout=20)
print(f'Profile page: {r.status_code}, size: {len(r.text)}')

# Extract image URLs
img_urls = re.findall(r'(https?://[^\s<>"]+\.(?:jpg|jpeg|png|webp)[^\s<>"]*)', r.text, re.IGNORECASE)
video_urls = re.findall(r'(https?://[^\s<>"]+\.(?:mp4)[^\s<>"]*)', r.text, re.IGNORECASE)
print(f'Found {len(img_urls)} image URLs, {len(video_urls)} video URLs')

for i, u in enumerate(img_urls[:10]):
    # Clean URL
    u = u.rstrip('.,;:)')
    print(f'  [{i}] IMG: {u[:150]}')

for i, u in enumerate(video_urls[:5]):
    u = u.rstrip('.,;:)')
    print(f'  [{i}] VID: {u[:150]}')

# Try to download profile image
profile_urls = [u for u in img_urls if 'profile' in u.lower() or 'avatar' in u.lower() or '718481071' in u or '916672382' in u]
if not profile_urls:
    # Look for first image that might be profile
    profile_urls = [u for u in img_urls if 'scontent' in u.lower() or 'cdninstagram' in u.lower()]
    
print(f'\nProfile candidates: {len(profile_urls)}')

# Download first few images
downloaded = 0
for i, url in enumerate(img_urls[:8]):
    url = url.rstrip('.,;:)')
    try:
        img_r = session.get(url, headers={'Referer': 'https://imginn.com/'}, timeout=20, stream=True)
        if img_r.status_code == 200 and int(img_r.headers.get('Content-Length', 0)) > 2000:
            ext = url.split('.')[-1].split('?')[0]
            if ext not in ('jpg', 'jpeg', 'png', 'webp'):
                ext = 'jpg'
            fname = f'images/posts/post-{i+1}.{ext}'
            with open(fname, 'wb') as f:
                for chunk in img_r.iter_content(8192):
                    f.write(chunk)
            print(f'  Downloaded: {fname} ({len(img_r.content)} bytes)')
            downloaded += 1
        else:
            print(f'  Skipped [{i}]: status={img_r.status_code}, size={len(img_r.content)}')
    except Exception as e:
        print(f'  Error [{i}]: {e}')

print(f'\nTotal downloaded: {downloaded}')

# Also try profile image directly
try:
    profile_r = session.get('https://s7.imginn.com/718481071_17893059534496983_9166723829481300056_n.jpg',
                           headers={'Referer': 'https://imginn.com/mycard.oman/'}, timeout=20)
    if profile_r.status_code == 200 and len(profile_r.content) > 1000:
        with open('images/profile/profile-logo.jpg', 'wb') as f:
            f.write(profile_r.content)
        print(f'Profile image downloaded: {len(profile_r.content)} bytes')
    else:
        print(f'Profile image failed: {profile_r.status_code}, size={len(profile_r.content)}')
except Exception as e:
    print(f'Profile image error: {e}')
