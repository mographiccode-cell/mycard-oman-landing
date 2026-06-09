import requests
import json
import os
import re

# Known post IDs from @mycard.oman
POSTS = [
    "DXztHbzDKaN",  # Marriage carousel
    "DXkaS0ODHX6",  # Engagement carousel  
    "DXkZhrRjLRc",  # Image
    "DXkZQYxjCsy",  # Carousel
    "DZUBly3sb9w",  # Video (recent)
    "DZN0mqlswGj",  # Video
]

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
})

# Approach 1: Try oEmbed API
print("=" * 60)
print("APPROACH 1: Instagram oEmbed API")
print("=" * 60)
for pid in POSTS:
    url = f"https://api.instagram.com/oembed?url=https://www.instagram.com/p/{pid}/"
    try:
        r = session.get(url, timeout=10)
        print(f"[{pid}] Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"  Title: {data.get('title', 'N/A')[:80]}")
            thumb = data.get('thumbnail_url', 'N/A')
            print(f"  Thumbnail: {thumb[:120]}")
            # Try to download thumbnail
            if thumb and thumb.startswith('http'):
                try:
                    img_r = session.get(thumb, timeout=15)
                    if img_r.status_code == 200 and len(img_r.content) > 2000:
                        fname = f"images/posts/{pid}.jpg"
                        with open(fname, 'wb') as f:
                            f.write(img_r.content)
                        print(f"  >> DOWNLOADED: {fname} ({len(img_r.content)} bytes)")
                    else:
                        print(f"  >> Thumb DL failed: status={img_r.status_code}, size={len(img_r.content)}")
                except Exception as e2:
                    print(f"  >> Thumb DL error: {e2}")
        else:
            print(f"  Response: {r.text[:200]}")
    except Exception as e:
        print(f"[{pid}] Error: {e}")

# Approach 2: Try graphql/embedded data from Instagram page source
print("\n" + "=" * 60)
print("APPROACH 2: Instagram page source scraping")
print("=" * 60)
for pid in POSTS[:3]:
    url = f"https://www.instagram.com/p/{pid}/"
    try:
        r = session.get(url, timeout=15)
        print(f"[{pid}] Page status: {r.status_code}, size: {len(r.text)}")
        if r.status_code == 200:
            # Look for display_url in the page source
            img_urls = re.findall(r'"(display_url|display_src)":"([^"]+)"', r.text)
            for tag, img_url in img_urls:
                print(f"  Found {tag}: {img_url[:150]}")
                # Try to download
                try:
                    clean_url = img_url.replace('\\u0026', '&')
                    img_r = session.get(clean_url, timeout=15, headers={'Referer': url})
                    if img_r.status_code == 200 and len(img_r.content) > 2000:
                        fname = f"images/posts/{pid}_src.jpg"
                        with open(fname, 'wb') as f:
                            f.write(img_r.content)
                        print(f"  >> DOWNLOADED: {fname} ({len(img_r.content)} bytes)")
                except Exception as e2:
                    print(f"  >> DL error: {e2}")
            
            # Also look for video_url
            vid_urls = re.findall(r'"video_url":"([^"]+)"', r.text)
            for vurl in vid_urls[:2]:
                print(f"  Found video: {vurl[:150]}")
            
            # Check if login wall
            if 'login' in r.text.lower() and len(r.text) < 5000:
                print(f"  >> LIKELY LOGIN WALL - page too small ({len(r.text)} bytes)")
    except Exception as e:
        print(f"[{pid}] Error: {e}")

# Approach 3: Try Imginn CDN directly with different referrer
print("\n" + "=" * 60)
print("APPROACH 3: Imginn CDN with different referrers")
print("=" * 60)
imginn_urls = [
    ("profile", "https://s7.imginn.com/718481071_17893059534496983_9166723829481300056_n.jpg"),
    ("post1", "https://s7.imginn.com/683643467_17887649667496983_4766680050615816011_n.jpg"),
    ("post2", "https://s7.imginn.com/674458225_17887633206496983_8493468561119901525_n.jpg"),
]

referrers = [
    "https://imginn.com/mycard.oman/",
    "https://imginn.com/",
    "https://www.instagram.com/",
    "",  # No referrer
]

for label, url in imginn_urls:
    for ref in referrers:
        try:
            headers = {'Referer': ref} if ref else {}
            img_r = session.get(url, timeout=10, headers=headers)
            size = len(img_r.content)
            status = img_r.status_code
            if status == 200 and size > 3000:
                fname = f"images/posts/{label}_dl.jpg"
                with open(fname, 'wb') as f:
                    f.write(img_r.content)
                print(f"[{label}] SUCCESS with Referer='{ref}': {size} bytes -> {fname}")
                break
            else:
                print(f"[{label}] Referer='{ref[:50]}': status={status}, size={size}")
        except Exception as e:
            print(f"[{label}] Referer='{ref[:50]}': Error={e}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
