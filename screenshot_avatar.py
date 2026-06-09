import asyncio, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1200, 'height': 900},
            device_scale_factor=2  # Retina quality
        )
        page = await ctx.new_page()

        await page.goto('https://www.instagram.com/mycard.oman/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(5000)

        # Find the profile picture img element
        imgs = await page.query_selector_all('img')
        avatar_img = None
        for img in imgs:
            src = await img.get_attribute('src')
            alt = (await img.get_attribute('alt') or '').encode('ascii', 'replace').decode()
            if src and '718481071' in src and 'profile' in alt.lower():
                avatar_img = img
                print(f"Found avatar: {alt}")
                break

        if avatar_img:
            # Screenshot the element
            await avatar_img.screenshot(path='images/profile/avatar-screenshot.png')
            size = os.path.getsize('images/profile/avatar-screenshot.png')
            print(f"Avatar screenshot saved: {size} bytes")
            
            # Also save as profile-logo (convert PNG to JPG quality)
            # The PNG will work fine as logo
            import shutil
            shutil.copy('images/profile/avatar-screenshot.png', 'images/profile/profile-logo.png')
            print("Copied to profile-logo.png")
            
            # Update the HTML to use PNG
            print("\nNOTE: Update <img> tags to use .png extension for profile image")
        else:
            print("Avatar img element not found!")

        await browser.close()

asyncio.run(main())
