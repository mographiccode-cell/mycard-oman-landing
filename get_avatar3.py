import asyncio, os, sys, base64
sys.stdout.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright
import requests

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1200, 'height': 900}
        )
        page = await ctx.new_page()

        await page.goto('https://www.instagram.com/mycard.oman/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(4000)

        imgs = await page.query_selector_all('img')
        for img in imgs:
            src = await img.get_attribute('src')
            alt = (await img.get_attribute('alt') or '').encode('ascii', 'replace').decode()
            if src and '718481071' in src and 'scontent' in src:
                print(f"FULL URL: {src}")
                print(f"Alt: {alt}")
                
                # Get cookies
                cookies = await ctx.cookies()
                cdict = {c['name']: c['value'] for c in cookies}
                h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.instagram.com/'}
                
                # Try different stp values for higher resolution
                base = src.split('?')[0]
                stp_variants = [
                    'stp=dst-jpg_e35_p1080x1080_tt6',
                    'stp=dst-jpg_e35_p720x720_tt6', 
                    'stp=dst-jpg_e35_p640x640_tt6',
                    'stp=dst-jpg_e35_p480x480_tt6',
                    'stp=dst-jpg_e35_p320x320_tt6',
                    'stp=dst-jpg_s640x640_tt6',
                    'stp=dst-jpg_s480x480_tt6',
                    'stp=dst-jpg_s320x320_tt6',
                ]
                
                for var in stp_variants:
                    url = base + '?' + var
                    r = requests.get(url, headers=h, cookies=cdict, timeout=15)
                    size = len(r.content)
                    print(f"  [{size:>6}B] {var}")
                    if size > 10000:
                        with open('images/profile/profile-logo.jpg', 'wb') as f:
                            f.write(r.content)
                        print(f"  >>> SAVED HIGH RES! ({size} bytes)")
                        await browser.close()
                        return
                
                # Also try with just the original URL
                r = requests.get(src, headers=h, cookies=cdict, timeout=15)
                print(f"  [original] {len(r.content)} bytes")
                if len(r.content) > 10000:
                    with open('images/profile/profile-logo.jpg', 'wb') as f:
                        f.write(r.content)
                    print(f"  >>> SAVED!")
                
                break

        await browser.close()

asyncio.run(main())
