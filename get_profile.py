import asyncio
import os
import requests
from playwright.async_api import async_playwright

async def get_profile_and_missing():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1200, 'height': 900}
        )
        page = await context.new_page()

        download_count = 0

        # Get profile picture
        print("=== PROFILE PICTURE ===")
        await page.goto('https://www.instagram.com/mycard.oman/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(4000)
        
        imgs = await page.query_selector_all('img')
        for i, img in enumerate(imgs):
            src = await img.get_attribute('src')
            if src and 'scontent' in src and '718481071' in src:
                # Try to get higher res by removing stp parameter
                base_url = src.split('?')[0]
                print(f"  Profile URL: {base_url}")
                for quality in ['', '?stp=dst-jpg_s640x640', '?stp=dst-jpg_s480x480']:
                    try_url = base_url + quality
                    try:
                        img_r = requests.get(try_url, timeout=20, headers={
                            'User-Agent': 'Mozilla/5.0',
                            'Referer': 'https://www.instagram.com/'
                        })
                        size = len(img_r.content)
                        print(f"    Quality '{quality[:30]}': {size} bytes")
                        if size > 5000:
                            with open('images/profile/profile-logo.jpg', 'wb') as f:
                                f.write(img_r.content)
                            print(f"    >>> SAVED profile: {size} bytes")
                            download_count += 1
                            break
                    except Exception as e:
                        print(f"    Error: {e}")
                break

        # Get posts from the profile page feed
        print("\n=== PROFILE PAGE POSTS ===")
        post_links = await page.query_selector_all('a[href*="/p/"]')
        post_ids = set()
        for link in post_links:
            href = await link.get_attribute('href')
            if href and '/p/' in href:
                pid = href.split('/p/')[1].split('/')[0]
                if pid:
                    post_ids.add(pid)
        print(f"  Found {len(post_ids)} post links: {list(post_ids)[:10]}")

        await browser.close()
        print(f"\nTotal new downloads: {download_count}")

asyncio.run(get_profile_and_missing())
