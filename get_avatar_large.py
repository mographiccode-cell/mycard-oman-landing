import asyncio, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1200, 'height': 1200},
            device_scale_factor=2
        )
        page = await ctx.new_page()

        # Navigate directly to the profile image URL (browser will render it)
        await page.goto('https://www.instagram.com/mycard.oman/', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(4000)

        # Try to find the header area with larger avatar
        # On Instagram profile page, the avatar in the header is usually the largest
        header = await page.query_selector('header')
        if header:
            await header.screenshot(path='images/profile/header-area.png')
            print(f"Header screenshot: {os.path.getsize('images/profile/header-area.png')} bytes")
        
        # Also try to get the avatar by clicking on it (opens story-like view)
        # Or find it in a section that might be bigger
        all_imgs = await page.query_selector_all('img')
        for i, img in enumerate(all_imgs):
            src = await img.get_attribute('src')
            if src and '718481071' in src:
                # Get the bounding box
                box = await img.bounding_box()
                if box:
                    print(f"Avatar img [{i}]: {box['width']}x{box['height']}px at ({box['x']},{box['y']})")
                    
                    # Try to get a larger version by navigating to the image directly
                    # in a new page with viewport sized to the image
                    page2 = await ctx.new_page()
                    # Set viewport to match or exceed image size
                    await page2.set_viewport_size({'width': 600, 'height': 600})
                    
                    # Create an HTML that shows just the image larger
                    html = f'<html><body style="margin:0;display:flex;align-items:center;justify-content:center;background:#fff;"><img src="{src}" style="width:400px;height:400px;object-fit:cover;border-radius:50%;"></body></html>'
                    await page2.set_content(html)
                    await page2.wait_for_timeout(2000)
                    
                    # Screenshot the img element
                    big_img = await page2.query_selector('img')
                    if big_img:
                        await big_img.screenshot(path='images/profile/avatar-large.png')
                        size = os.path.getsize('images/profile/avatar-large.png')
                        print(f"Large avatar PNG: {size} bytes")
                        import shutil
                        shutil.copy('images/profile/avatar-large.png', 'images/profile/profile-logo.png')
                    
                    await page2.close()
                    break

        await browser.close()

asyncio.run(main())
