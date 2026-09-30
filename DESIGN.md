# VoiceShield CyberDemo Design System Specification (DESIGN.md)

---

## 🎨 1. Design Philosophy & Brand Identity

**VoiceShield CyberDemo** — **Modern Executive Light Theme**

The interface is built for professional cybersecurity threat analysis and executive voice cloning operations:
- **Clean Light Palette**: Pure white cards (`#ffffff`) on soft slate backgrounds (`#f8fafc`).
- **Royal Blue Accents**: Primary royal blue (`#2563eb`), deep indigo (`#4f46e5`), emerald green (`#059669`), ruby red (`#dc2626`).
- **Precision Typography**: High-contrast **Plus Jakarta Sans / Outfit** for UI headers and **JetBrains Mono** for numerical telemetry data.
- **Subtle Elevation & Crisp Borders**: 1px subtle slate borders (`#e2e8f0`) with soft multi-layered drop shadows (`0 10px 25px -5px rgba(15, 23, 42, 0.08)`).

---

## 🎛️ 2. Color Tokens & Theme Palette

### Core Backgrounds & Surfaces
```css
--bg-lightness: #f8fafc;
--bg-surface: #ffffff;
--card-bg: #ffffff;
--card-hover: #ffffff;
--border-subtle: #e2e8f0;
--border-active: #2563eb;
--border-focus: #3b82f6;
```

### Brand & Functional Accents
```css
--accent-primary: #2563eb;      /* Royal Blue */
--accent-secondary: #4f46e5;    /* Deep Indigo */
--accent-success: #059669;      /* Emerald Green / Authentic */
--accent-warning: #d97706;      /* Amber / Suspicious */
--accent-danger: #dc2626;       /* Ruby Red / Deepfake Alert */
--accent-purple: #7c3aed;       /* Royal Purple */
```

### Typography Colors
```css
--text-primary: #0f172a;        /* Deep Slate Pitch */
--text-secondary: #475569;      /* Muted Slate */
--text-muted: #64748b;          /* Light Slate */
--text-accent: #1d4ed8;        /* Vibrant Royal Blue */
```

---

## 📐 3. Typography Scale & Spacing

### Font Families
- **Display & UI**: `'Plus Jakarta Sans', 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif`
- **Telemetry & Monospace Data**: `'JetBrains Mono', 'Fira Code', monospace`

### Typography Hierarchy
- `Heading 1` (Brand Title): `1.5rem / 24px`, `font-weight: 800`, `color: #0f172a`
- `Heading 2` (Section Headers): `1.15rem / 18.4px`, `font-weight: 700`
- `Gauge Value` (Big Numerical Metrics): `3.2rem / 51.2px`, `font-weight: 800`, `font-family: JetBrains Mono`
- `Body Large`: `1rem / 16px`, `font-weight: 500`
- `Body Regular`: `0.875rem / 14px`, `font-weight: 400`
- `Caption / Monospace Tag`: `0.75rem / 12px`, `font-weight: 600`

---

## ⚡ 4. Elevation, Shadow & Component Guidelines

```css
--box-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
--box-shadow-md: 0 4px 12px rgba(15, 23, 42, 0.06);
--box-shadow-lg: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
--box-shadow-blue-glow: 0 4px 14px rgba(37, 99, 235, 0.25);
```
