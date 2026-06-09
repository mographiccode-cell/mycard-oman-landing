import asyncio
import os
import requests
from playwright.async_api import async_playwright

async def get_highres_profile():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            viewport={'width': 1200, 'height': 900}
        )
        page = await context.new_page()

        # Go to profile page
        print("Loading profile page...")
        await page.goto('https://www.instagram.com/mycard.oman/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(5000)

        # Get all img elements
        imgs = await page.query_selector_all('img')
        print(f"Found {len(imgs)} img elements")

        best_src = None
        best_size = 0
        profile_img_idx = -1

        for i, img in enumerate(imgs):
            src = await img.get_attribute('src')
            width = await img.get_attribute('width')
            height = await img.get_attribute('height')
            alt = await img.get_attribute('alt') or ''
            
            if src and 'scontent' in src:
                # This is a CDN image
                print(f"  [{i}] {alt[:60]} | {width}x{height} | {src[:120]}")
                
                # Look for profile picture specifically
                if 'profile' in alt.lower() or '718481071' in src:
                    # Try downloading with browser's session cookies
                    profile_img_idx = i
                    best_src = src
                    print(f"    >>> PROFILE CANDIDATE!")

        if best_src:
            print(f"\nDownloading profile image from browser session...")
            # Use page.evaluate to fetch via browser's own fetch (uses browser cookies)
            img_data = await page.evaluate("""
                async (url) => {
                    const response = await fetch(url, { credentials: 'include' });
                    if (!response.ok) return null;
                    const blob = await response.blob();
                    const buffer = await blob.arrayBuffer();
                    const bytes = new Uint8Array(buffer);
                    const binary = Array.from(bytes).map(b => String.fromCharCode(b)).join('');
                    return btoa(binary);
                }
            """, best_src)

            if img_data:
                import base64
                with open('images/profile/avatar-original.jpg', 'wb') as f:
                    f.write(base64.b64decode(img_data))
                file_size = os.path.getsize('images/profile/avatar-original.jpg')
                print(f"  Saved avatar-original.jpg: {file_size} bytes")

                # Also save as main profile pic
                import shutil
                shutil.copy('images/profile/avatar-original.jpg', 'images/profile/profile-logo.jpg')
                print(f"  Copied to profile-logo.jpg")
            else:
                print(f"  Browser fetch failed, trying requests with cookies...")
                # Get cookies from browser and use requests
                cookies = await context.cookies()
                cookie_dict = {c['name']: c['value'] for c in cookies}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://www.instagram.com/'
                }
                r = requests.get(best_src, headers=headers, cookies=cookie_dict, timeout=20)
                print(f"  requests status: {r.status_code}, size: {len(r.content)}")
                if r.status_code == 200 and len(r.content) > 5000:
                    with open('images/profile/avatar-original.jpg', 'wb') as f:
                        f.write(r.content)
                    import shutil
                    shutil.copy('images/profile/avatar-original.jpg', 'images/profile/profile-logo.jpg')
                    print(f"  Saved: {len(r.content)} bytes")

        # Also try to get the direct CDN URL without stp for higher quality
        print("\n=== Trying CDN URL variations ===")
        base_cdn = "https://scontent-mct1-2.cdninstagram.com/v/t51.82787-19/718481071_17893059534496983_9166723829481300056_n.jpg"
        cookies = await context.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        
        for q in ['', '_nc_cat=101']:
            url = f"{base_cdn}?{q}" if q else base_cdn
            try:
                r = requests.get(url, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Referer': 'https://www.instagram.com/'
                }, cookies=cookie_dict)
                print(f"  [{q[:30]}]: status={r.status_code}, size={len(r.content)}")
                if len(r.content) > 10000:
                    with open('images/profile/avatar-hq.jpg', 'wb') as f:
                        f.write(r.content)
                    import shutil
                    shutil.copy('images/profile/avatar-hq.jpg', 'images/profile/profile-logo.jpg')
                    print(f"  >>> SAVED HQ: {len(r.content)} bytes")
                    break
            except Exception as e:
                print(f"  Error: {e}")

        await browser.close()
        print("\nDone!")

asyncio.run(get_highres_profile())
