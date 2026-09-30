# VoiceShield CyberDemo Design System Specification (DESIGN.md)

---

## 🎨 1. Design Philosophy & Brand Identity

**VoiceShield CyberDemo** is an advanced cybersecurity dual-module interface designed for real-time zero-shot voice cloning threat simulation and deepfake detection telemetry.

The design system combines **Cyberpunk Tactical Engineering** with **Modern Glassmorphism Aesthetics**:
- Deep slate/obsidian dark mode base (`#080c14`)
- Dynamic glowing neon accents (Cyan `#06b6d4`, Indigo `#6366f1`, Emerald `#10b981`, Amber `#f59e0b`, Crimson `#ef4444`)
- Frosted glass cards (`rgba(15, 23, 42, 0.75)` with `backdrop-filter: blur(16px)`)
- High-contrast precision typography (**Outfit** for UI & headers, **JetBrains Mono** for numerical telemetry & frequency data)
- Micro-interactions, smooth CSS transitions, glowing borders, and real-time audio canvas visualizations

---

## 🎛️ 2. Color Tokens & Theme Palette

### Core Backgrounds & Surfaces
```css
--bg-darkness: #06090e;
--bg-surface: #0b0f19;
--card-bg: rgba(15, 23, 42, 0.75);
--card-bg-solid: #0f172a;
--card-hover: rgba(30, 41, 59, 0.85);
--border-subtle: rgba(255, 255, 255, 0.08);
--border-active: rgba(6, 182, 212, 0.4);
--border-glow: rgba(99, 102, 241, 0.5);
```

### Brand & Functional Accents
```css
--accent-primary: #06b6d4;      /* Cyber Cyan */
--accent-secondary: #6366f1;    /* Deep Indigo */
--accent-success: #10b981;      /* Emerald / Authentic */
--accent-warning: #f59e0b;      /* Amber / Suspicious */
--accent-danger: #ef4444;       /* Crimson / Deepfake Alert */
--accent-purple: #a855f7;       /* Voice Conversion Gradient */
```

### Typography Colors
```css
--text-primary: #f8fafc;
--text-secondary: #94a3b8;
--text-muted: #64748b;
--text-accent: #38bdf8;
```

---

## 📐 3. Typography Scale & Spacing

### Font Families
- **Display & UI**: `'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Telemetry & Monospace Data**: `'JetBrains Mono', 'Fira Code', monospace`

### Typography Hierarchy
- `Heading 1` (Brand Title): `1.6rem / 25.6px`, `font-weight: 800`, `letter-spacing: -0.5px`
- `Heading 2` (Section Headers): `1.15rem / 18.4px`, `font-weight: 700`
- `Gauge Value` (Big Numerical Metrics): `3.2rem / 51.2px`, `font-weight: 800`, `font-family: JetBrains Mono`
- `Body Large`: `1rem / 16px`, `font-weight: 500`
- `Body Regular`: `0.875rem / 14px`, `font-weight: 400`
- `Caption / Monospace Tag`: `0.75rem / 12px`, `font-weight: 600`, `letter-spacing: 0.5px`

### Spacing Scale
- `space-xs`: `4px`
- `space-sm`: `8px`
- `space-md`: `16px`
- `space-lg`: `24px`
- `space-xl`: `32px`

---

## ✨ 4. Component Guidelines & Interactive States

### 1. Interactive Audio Waveform & Canvas
- Real-time oscilloscope visualization with dynamic cyan gradient trails (`canvasCtx.strokeStyle = gradient`).
- Equalizer bar visualizations for STFT Mel-Spectrogram summaries with dynamic color interpolation based on amplitude.

### 2. Voice Cloning Controls (Module 1)
- **Reference Voice Profile Selector**: Drag-and-drop reference audio upload area + preloaded voice targets (Cyber Security Officer, AI Assistant, Neutral Voice).
- **Pitch Shift Slider**: Range `-12.0` to `+12.0` semitones with live numerical readout.
- **Formant Shift Slider**: Range `0.5x` to `1.8x` ratio with live numerical readout.
- **Synthesize & Stream Button**: High-contrast action button with pulsing gradient ring state.

### 3. Deepfake Defense Telemetry (Module 2)
- **Synthetic Risk Index Gauge**: SVG circular progress meter with smooth offset transitions and dynamic color thresholds (Green <40%, Yellow 40–65%, Red >65%).
- **Verdict Banner**: Glowing pill badge showing detection confidence and categorical status (`AUTHENTIC`, `SUSPICIOUS`, `DEEPFAKE DETECTED`, `SILENCE`).
- **Telemetry Grid**: 6 metric cards with progress bars for Phase Anomaly, Spectral Cutoff, Pitch Rigidity, Centroid, Rolloff, and RMS Energy.

---

## ⚡ 5. Elevation, Shadow & Glassmorphism Levels

```css
--box-shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.3);
--box-shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.5);
--box-shadow-cyan-glow: 0 0 20px rgba(6, 182, 212, 0.35);
--box-shadow-red-glow: 0 0 20px rgba(239, 68, 68, 0.35);
--backdrop-blur: blur(16px);
```
