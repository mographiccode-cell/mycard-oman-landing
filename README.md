# MyCard Oman - Landing Page

## About
Premium landing page for **MyCard Oman** (@mycard.oman), an electronic invitation card design service based in Muscat, Oman. The page showcases the full range of digital invitation cards for weddings, engagements, henna nights, newborn celebrations, and Eid — all priced at 3 OMR per design.

Built as a complete brand extension of the Instagram account, this RTL Arabic landing page features the actual brand identity extracted from the account's posts, colors, and content.

## Features
- **RTL Arabic** full layout optimized for GCC/Omani market
- **Premium invitation card 3D animation** with interactive hover/tilt effects
- **Tailwind CSS** as the primary styling system
- **Embedded Instagram gallery** — real posts from @mycard.oman
- **Service cards** for all event types (Marriage, Engagement, Henna, Newborn, Eid)
- **5-step order process** visual guide
- **Interactive FAQ accordion**
- **Floating WhatsApp button** for instant contact
- **SEO optimized** with proper Arabic meta tags
- **Responsive design** — mobile-first, all devices
- **Accessible** — respects prefers-reduced-motion

## Brand Identity
Colors extracted from actual account posts (real emoji usage: 🤎💚💛❤️):
- **Primary:** Warm Brown `#7B5B3A`
- **Secondary:** Olive Green `#4A7C59`
- **Accent:** Warm Gold `#D4A853`
- **Rose:** Soft Rose `#D4838F`
- **Background:** Cream `#FEF9F3`

## Project Structure
```
mycard.oman/
├── landing-page.html          # Main landing page
├── styles.css                 # Custom styles & animations
├── script.js                  # JavaScript interactivity
├── README.md                  # This file
├── deployment-report.md       # Deployment status
├── account-research.json      # Instagram account analysis
├── account-summary.md         # Human-readable summary
├── data/
│   ├── account-data.json      # Structured account data
│   ├── products.json          # Product catalog
│   ├── images-manifest.json   # Image asset inventory
│   ├── videos-manifest.json   # Video asset inventory
│   └── brand-identity.json    # Visual identity specs
├── content/
│   ├── brand-copy.md          # Marketing copy & messaging
│   ├── brand-guidelines.md    # Design system guidelines
│   └── raw-instagram-notes.md # Research documentation
└── .github/
    └── workflows/
        └── deploy.yml         # GitHub Pages deployment
```

## How to Run Locally
1. Clone the repository:
```bash
git clone https://github.com/mographiccode-cell/mycard-oman-landing.git
cd mycard-oman-landing
```

2. Open `landing-page.html` in your browser, or use a local server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .
```

3. Visit `http://localhost:8000/landing-page.html`

## How to Update
1. Edit `landing-page.html` for content/layout changes
2. Edit `styles.css` for visual changes
3. Edit `script.js` for interactivity changes
4. Commit and push - GitHub Pages auto-deploys

## Source Account
- **Instagram:** [@mycard.oman](https://www.instagram.com/mycard.oman/)
- All images/videos referenced are from this account only

## Live URL
**[https://mographiccode-cell.github.io/mycard-oman-landing/landing-page.html](https://mographiccode-cell.github.io/mycard-oman-landing/landing-page.html)**

## Tech Stack
- HTML5
- Tailwind CSS (CDN)
- Vanilla JavaScript
- Google Fonts (Tajawal, Inter)
- GitHub Pages (deployment)

## License
All rights reserved © 2026 MyCard Oman
