import asyncio
import os
from playwright.async_api import async_playwright
import requests

POSTS = [
    ("DXztHbzDKaN", "marriage_carousel"),
    ("DXkaS0ODHX6", "engagement_carousel"),
    ("DXkZhrRjLRc", "henna_image"),
    ("DV1kEIIDCjz", "newborn_image"),
    ("DXkZQYxjCsy", "engagement_carousel2"),
    ("DXzJbvqjA34", "general_image"),
]

async def extract_images():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            viewport={'width': 1200, 'height': 900}
        )
        page = await context.new_page()

        download_count = 0

        for post_id, label in POSTS:
            url = f"https://www.instagram.com/p/{post_id}/"
            print(f"\n[{label}] Loading {url}...")
            
            try:
                # Navigate to post
                await page.goto(url, wait_until='networkidle', timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Check if login wall appeared
                page_text = await page.content()
                if 'login' in page_text.lower() and len(page_text) < 20000:
                    print(f"  >> LOGIN WALL detected")
                    continue

                # Extract all img src URLs
                img_elements = await page.query_selector_all('img')
                print(f"  Found {len(img_elements)} img elements")
                
                for i, img in enumerate(img_elements):
                    src = await img.get_attribute('src')
                    alt = await img.get_attribute('alt') or ''
                    if src and ('scontent' in src or 'cdninstagram' in src) and '.jpg' in src.lower():
                        print(f"  [{i}] IMG: {src[:150]}")
                        print(f"       Alt: {alt[:80]}")
                        
                        # Download the image
                        try:
                            img_r = requests.get(src, timeout=20, headers={
                                'User-Agent': 'Mozilla/5.0',
                                'Referer': 'https://www.instagram.com/'
                            }, stream=True)
                            if img_r.status_code == 200 and int(img_r.headers.get('Content-Length', 0)) > 5000:
                                fname = f"images/posts/{label}_{i}.jpg"
                                with open(fname, 'wb') as f:
                                    for chunk in img_r.iter_content(8192):
                                        f.write(chunk)
                                file_size = os.path.getsize(fname)
                                print(f"  >>> DOWNLOADED: {fname} ({file_size} bytes)")
                                download_count += 1
                            else:
                                print(f"  >> DL failed: status={img_r.status_code}, size={len(img_r.content)}")
                        except Exception as e:
                            print(f"  >> DL error: {e}")

                # Extract video elements
                video_elements = await page.query_selector_all('video')
                print(f"  Found {len(video_elements)} video elements")
                for i, vid in enumerate(video_elements):
                    src = await vid.get_attribute('src')
                    poster = await vid.get_attribute('poster')
                    if src:
                        print(f"  [{i}] VIDEO: {src[:150]}")
                    if poster and '.jpg' in poster:
                        print(f"  [{i}] POSTER: {poster[:150]}")
                        # Try downloading poster
                        try:
                            img_r = requests.get(poster, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
                            if img_r.status_code == 200 and len(img_r.content) > 3000:
                                fname = f"images/posts/{label}_poster_{i}.jpg"
                                with open(fname, 'wb') as f:
                                    f.write(img_r.content)
                                print(f"  >>> POSTER DOWNLOADED: {fname} ({len(img_r.content)} bytes)")
                                download_count += 1
                        except:
                            pass

                # Also try to get profile picture
                if post_id == POSTS[0][0]:  # Only on first post
                    # Try clicking the profile link or getting header
                    header_imgs = await page.query_selector_all('header img')
                    for hi in header_imgs:
                        psrc = await hi.get_attribute('src')
                        if psrc and ('scontent' in psrc or 'cdninstagram' in psrc):
                            print(f"\n  PROFILE IMG: {psrc[:150]}")
                            try:
                                img_r = requests.get(psrc, timeout=20, headers={'User-Agent': 'Mozilla/5.0'})
                                if img_r.status_code == 200 and len(img_r.content) > 2000:
                                    with open('images/profile/profile-logo.jpg', 'wb') as f:
                                        f.write(img_r.content)
                                    print(f"  >>> PROFILE DOWNLOADED: {len(img_r.content)} bytes")
                                    download_count += 1
                            except Exception as e:
                                print(f"  >> Profile DL error: {e}")

            except Exception as e:
                print(f"  Error: {e}")

        await browser.close()
        print(f"\n{'='*50}")
        print(f"TOTAL DOWNLOADED: {download_count} images")
        print(f"{'='*50}")

asyncio.run(extract_images())
