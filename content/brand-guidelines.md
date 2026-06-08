# MyCard Oman - Brand Guidelines

## Brand Essence
MyCard Oman represents the fusion of Omani heritage and cutting-edge NFC technology. We empower professionals across the Sultanate to network smarter, not harder—with premium smart business cards that make every introduction memorable.

## Logo Usage
- **Primary Logo:** Wordmark "MyCard" in Arabic/English with NFC signal icon
- **Logo Colors:** Navy (#0D2B5E) on light backgrounds, Gold (#C8A951) on dark backgrounds
- **Clear Space:** Minimum 1x logo height on all sides
- **Minimum Size:** 32px height for digital, 15mm for print
- **Don'ts:** Don't stretch, recolor, add effects, or place on busy backgrounds

## Color Palette

### Primary Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Deep Navy | #0D2B5E | Primary buttons, headers, key UI elements, trust signals |
| Warm Gold | #C8A951 | Accent elements, hover states, premium highlights, CTAs |

### Secondary Colors
| Color | Hex | Usage |
|-------|-----|-------|
| Soft Gold | #E8D5A3 | Subtle backgrounds, hover accents, divider lines |
| Cream White | #FDFBF7 | Page backgrounds, card surfaces |
| Charcoal | #1A1A2E | Primary text, headings |
| Medium Gray | #4A4A5A | Secondary text, descriptions |
| Success Green | #2D7D46 | Success states, checkmarks |
| Border Gray | #E8E0D0 | Card borders, input borders, subtle dividers |

### Color Application Rules
- Navy dominates for trust/professionalism (60%)
- Gold accents for premium feel (30%)
- Cream/white for breathing space (10%)
- Never use gold on gold or navy on navy without sufficient contrast

## Typography

### Arabic: Tajawal
- **Headings:** Tajawal Bold (700) / ExtraBold (800)
- **Body:** Tajawal Medium (500) / Regular (400)
- **UI Labels:** Tajawal Medium (500)

### Latin: Inter
- **Headings:** Inter Bold (700) / ExtraBold (800)
- **Body:** Inter Medium (500) / Regular (400)
- **UI Labels:** Inter Medium (500)

### Scale (Mobile → Desktop)
- H1: 32px → 48px
- H2: 24px → 36px
- H3: 20px → 28px
- Body: 16px → 18px
- Small: 14px → 14px

## Visual Style

### Photography
- **Product Shots:** Cards on marble, walnut, leather, concrete
- **Lighting:** Natural window light, subtle rim light on edges
- **Angles:** 45° hero, top-down flat lay, close-up material detail
- **Color Grading:** Warm shadows, cool highlights, slight desaturation

### Lifestyle
- **Settings:** Muscat Corniche, Al Mouj Marina, OCEC, Grand Mall, business lounges
- **People:** Omani professionals in dishdasha/kumma, business attire
- **Action:** Tapping card to phone, exchanging cards, networking conversations
- **Mood:** Confident, successful, connected, proud

### Graphic Elements
- **Geometric Patterns:** Subtle Omani-inspired geometric motifs (kummah patterns, Islamic geometry)
- **NFC Icon:** Animated pulse/ripple on hover
- **Card Silhouettes:** Layered card stacks showing depth
- **Divider Lines:** Gold hairlines with occasional pattern accents

## Component Guidelines

### Buttons
```css
/* Primary - Main CTA */
.btn-primary {
  background: #0D2B5E;
  color: #FDFBF7;
  border: 2px solid #0D2B5E;
  transition: all 0.3s ease;
}
.btn-primary:hover {
  background: #C8A951;
  border-color: #C8A951;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(200, 169, 81, 0.3);
}

/* Secondary - Outline */
.btn-secondary {
  background: transparent;
  color: #0D2B5E;
  border: 2px solid #C8A951;
}
.btn-secondary:hover {
  background: #C8A951;
  color: #0D2B5E;
}

/* Ghost - Text only */
.btn-ghost {
  background: transparent;
  color: #0D2B5E;
  border: none;
}
.btn-ghost:hover {
  color: #C8A951;
}
```

### Cards
- **Elevation:** `box-shadow: 0 4px 24px rgba(13, 43, 94, 0.08)`
- **Hover:** `transform: translateY(-4px); box-shadow: 0 12px 40px rgba(13, 43, 94, 0.15)`
- **Border:** `1px solid #E8E0D0`
- **Radius:** `16px` (comfortable, not sharp)
- **Padding:** `24px` (mobile), `32px` (desktop)

### Inputs
- **Rest:** Border `#E8E0D0`, bg `#FDFBF7`
- **Focus:** Border `#C8A951`, ring `rgba(200, 169, 81, 0.2)`
- **Error:** Border `#C0392B`, ring `rgba(192, 57, 43, 0.15)`

## Motion & Animation

### Principles
- **Duration:** 200-400ms for UI, 600-1000ms for hero
- **Easing:** `cubic-bezier(0.25, 0.46, 0.45, 0.94)` (smooth, natural)
- **Stagger:** 80-120ms between elements
- **Respect:** `prefers-reduced-motion`

### Key Animations
1. **Hero Card Reveal:** Staggered slide-up + fade (600ms)
2. **NFC Pulse:** Continuous subtle scale pulse on hero card (2s loop)
3. **Scroll Reveal:** IntersectionObserver fade-up (400ms)
4. **Hover Lift:** Transform + shadow (200ms)
5. **Button Ripple:** Gold ripple from click point (300ms)
6. **Card Flip:** 3D flip on tap (mobile) / hover (desktop) - 500ms

## Layout System

### Grid
- **Mobile:** 4-column → 12-column at 640px
- **Container:** Max-width 1280px, padding 24px (mobile), 48px (desktop)
- **Section Spacing:** 80px (mobile), 120px (desktop)

### Breakpoints
- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px
- `2xl:` 1536px

## Voice & Tone

### Arabic
- **Professional:** نستخدم لغة عربية فصحى معاصرة، واضحة ومباشرة
- **Premium:** كلمات تعكس الجودة: "متميز"، "فاخر"، "رائد"، "أصيل"
- **Trustworthy:** عبارات تبني الثقة: "مضمون"، "معتمد"، "آمن"
- **Inspiring:** ندعو للعمل: "ابدأ الآن"، "انضم للنخبة"، "ارتقِ بتواصلك"

### English
- **Professional:** Clear, contemporary business English
- **Premium:** "Exquisite", "distinguished", "premier", "authentic"
- **Trustworthy:** "Guaranteed", "certified", "secure", "reliable"
- **Inspiring:** "Elevate your network", "Join the elite", "Make every tap count"

## Do's and Don'ts

### Do's ✓
- Use navy as primary action color
- Gold for premium accents only
- Generous whitespace
- High-quality product imagery
- Bilingual content (AR/EN)
- Subtle Omani cultural references
- Smooth, purposeful animations

### Don'ts ✗
- Don't use bright/saturated colors
- Don't overuse gold (cheapens the premium feel)
- Don't crowd elements
- Don't use stock photos unrelated to Oman
- Don't mix more than 2 fonts
- Don't animate everything
- Don't use generic tech imagery

## Application Examples

### Hero Section
- Full viewport height
- Animated 3D card floating center
- Navy background with subtle geometric pattern
- Gold accent CTA button
- Staggered text reveal

### Product Cards
- White/cream surface
- Soft shadow elevation
- Product image top
- Specs below with gold checkmarks
- Hover: lift + glow

### Testimonials
- Card carousel
- Avatar + name + role
- Quote in navy text
- Gold quote mark accent
- Auto-advance with pause on hover

### Footer
- Navy background
- Gold divider lines
- Cream text
- Social icons in gold (hover: navy bg)
- Newsletter input with gold focus ring