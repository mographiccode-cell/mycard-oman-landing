# MyCard Oman - Landing Page

## About
Premium landing page for **MyCard Oman** (@mycard.oman), the Sultanate's premier NFC smart business card service. Built as a complete brand extension of the Instagram account, this RTL Arabic landing page showcases the full product lineup, brand identity, and provides a seamless conversion experience.

## Features
- **RTL Arabic** full layout optimized for GCC/Omani market
- **Premium 3D card animations** with interactive hover/tilt effects
- **Tailwind CSS** as the primary styling system
- **Custom CSS** for advanced animations & brand identity
- **Material selector tabs** (PVC, Metal, Wood, Corporate, Digital)
- **Responsive design** - mobile-first, works on all devices
- **Light/Dark mode** toggle with persistence
- **Interactive FAQ accordion**
- **Testimonial carousel** with auto-play
- **Floating WhatsApp button** for instant contact
- **SEO optimized** with proper meta tags
- **NFC pulse animation** & parallax effects
- **Accessible** - respects prefers-reduced-motion

## Brand Identity
Colors extracted from the account's Omani premium aesthetic:
- **Primary:** Deep Navy `#0D2B5E`
- **Secondary:** Warm Gold `#C8A951`
- **Background:** Cream `#FDFBF7`
- **Text:** Charcoal `#1A1A2E`

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
