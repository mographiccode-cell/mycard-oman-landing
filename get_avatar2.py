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

        # Go to profile
        print("Opening profile page...")
        await page.goto('https://www.instagram.com/mycard.oman/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(4000)

        # Find profile img
        imgs = await page.query_selector_all('img')
        profile_url = None
        for img in imgs:
            src = await img.get_attribute('src')
            alt = (await img.get_attribute('alt') or '').encode('ascii', 'replace').decode()
            if src and '718481071' in src and 'scontent' in src:
                profile_url = src
                print(f"Found profile: {alt[:40]} | URL: {src[:100]}...")
                break

        if not profile_url:
            print("No profile image found!")
            await browser.close()
            return

        # Download using browser's own fetch (has proper cookies/session)
        print("\nDownloading via browser fetch...")
        js_code = """
            async (url) => {
                try {
                    const r = await fetch(url, {credentials: 'include'});
                    const blob = await r.blob();
                    const ab = await blob.arrayBuffer();
                    const bytes = new Uint8Array(ab);
                    let binary = '';
                    for (let i = 0; i < bytes.length; i++) {
                        binary += String.fromCharCode(bytes[i]);
                    }
                    return btoa(binary);
                } catch(e) {
                    return null;
                }
            }
        """
        result = await page.evaluate(js_code, profile_url)
        
        if result:
            data = base64.b64decode(result)
            fpath = 'images/profile/avatar-original.jpg'
            with open(fpath, 'wb') as f:
                f.write(data)
            size = os.path.getsize(fpath)
            print(f"SAVED: {fpath} ({size} bytes)")
            
            # Copy to profile-logo
            import shutil
            shutil.copy(fpath, 'images/profile/profile-logo.jpg')
            print(f"Copied to profile-logo.jpg")
        else:
            print("Browser fetch returned None, trying requests with cookies...")
            cookies = await ctx.cookies()
            cdict = {c['name']: c['value'] for c in cookies}
            h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.instagram.com/'}
            r = requests.get(profile_url, headers=h, cookies=cdict, timeout=20)
            print(f"requests: status={r.status_code}, size={len(r.content)}")
            if r.status_code == 200 and len(r.content) > 5000:
                with open('images/profile/profile-logo.jpg', 'wb') as f:
                    f.write(r.content)
                print(f"Saved: {len(r.content)} bytes")

        await browser.close()

asyncio.run(main())
