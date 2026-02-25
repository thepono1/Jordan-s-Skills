# Figma Reference Library — Best-in-Class Design Sources

Use these sources to find production-quality design inspiration. Prioritize sources with real app screenshots over conceptual designs.

---

## Tier 1: Real App References (Highest Signal)

### Mobbin (mobbin.com)
**Best for**: Real app screenshots from production iOS/Android/Web apps
- Filter by: Platform (Web/iOS), Industry (Finance, SaaS, Productivity), Screen type (Dashboard, Onboarding, Empty states)
- For quant dashboard: Filter → Finance → Dashboard → Dark theme
- How to use: Screenshot, analyze layout with Claude, extract grid and spacing, map to tokens
- **Jordan's use case**: Find trading dashboard references, empty states, data table patterns

### Screenlane (screenlane.com)
**Best for**: Curated UI patterns by interaction type
- Organized by component: Tables, Charts, Modals, Navigation, Onboarding, Auth
- Better than Mobbin for component-specific search
- **Jordan's use case**: Find empty state patterns, data table interactions, form layouts

### Lookup.design (lookup.design)
**Best for**: Component-specific patterns with category filtering
- Categories: Buttons, Cards, Navigation, Tables, Forms, Charts, Modals
- Shows multiple variations side by side
- **Jordan's use case**: Compare button styles, find card layouts for StrategyCard

---

## Tier 2: Figma Community (Free Production Templates)

### Figma Community (figma.com/community)
Best search terms for Jordan's projects:
- `"dashboard dark"` — find dark SaaS dashboards
- `"design system shadcn"` — Shadcn-aligned systems
- `"trading dashboard"` — crypto/finance dashboards
- `"data table"` — production table components
- `"analytics dashboard"` — charts + metric cards

**Top templates to clone**:
- Shadcn/UI Figma Kit — matches Jordan's actual component library
- Linear Design System — reference for consistent spacing + dark theme
- Vercel Dashboard — clean, minimal, dark-first

**How to clone**:
1. Open community template → "Duplicate to drafts"
2. Open your draft → extract tokens (Colors panel + Variables panel)
3. Map to your token system
4. Use as reference only — never ship templates directly

---

## Tier 3: Premium Kits (Buy Once, Use Always)

### UI8 (ui8.net)
**Best for**: Production-quality design systems
- Search: "Dashboard Kit", "SaaS UI", "Analytics Dashboard"
- Price range: $20–$80 per kit
- Recommended: Dashify, Falcon (dark dashboards)
- **Worth buying if**: Building multiple projects, needs full component library

### Creative Tim (creative-tim.com)
**Best for**: React component kits with Figma source
- Has Tailwind + Shadcn-adjacent kits
- Often includes code + Figma (better ROI)
- Check "Dark Dashboard" and "Soft UI" lines

---

## Tier 4: Broader Inspiration

### Dribbble (dribbble.com)
**Search tips**: Filter by "Full Shot" + "Dark" + "Dashboard"
- Good for: Color palette ideas, overall aesthetic direction
- **Caution**: Many shots are conceptual (non-functional) — use for inspiration, not spec
- Don't copy directly — abstract the layout principle

### Layers.to (layers.to)
**Best for**: Web design (not mobile) inspiration
- Curated, high quality, filterable by color + style
- Good for landing page, marketing sections

### Awwwards (awwwards.com)
**Best for**: Exceptional web design
- Filter by category → SaaS, Web App
- **Caution**: Often over-designed for product UI — extract principles, not aesthetics

---

## How to Extract and Use References

### Workflow (15 minutes → usable spec):

1. **Find** — Browse Mobbin/Screenlane with specific filter (e.g., "Finance Dashboard Empty State")
2. **Screenshot** — Save 3–5 strong references
3. **Analyze with Claude**:
   ```
   "Analyze this UI screenshot. Identify:
   1. Grid system (columns, gutter, margin)
   2. Spacing rhythm (base unit, common multiples)
   3. Type scale (sizes used, weight hierarchy)
   4. Color roles (primary action, muted, destructive)
   5. Component patterns (card style, table style, badge usage)
   Map each to Tailwind equivalents."
   ```
4. **Extract tokens** — List found values mapped to your token system
5. **Build in Figma** — Use tokens, not raw values
6. **Generate component** — Use v0.dev with extracted spec

### Anti-patterns to avoid:
- Copying entire layouts (copyright risk, context mismatch)
- Using conceptual designs as specs (they skip hard problems like empty states)
- Extracting hex values directly (bypass token system)
- Building from multiple inconsistent references (visual incoherence)

---

## Reference Quality Tiers

| Signal | Source type | Use for |
|--------|-------------|---------|
| Highest | Mobbin real app | Layout, component patterns, states |
| High | Figma Community (production) | Token extraction, component architecture |
| Medium | Screenlane/Lookup | Component-specific patterns |
| Medium | UI8 premium kits | Full system reference |
| Low | Dribbble/Awwwards | Aesthetic direction only |
| Avoid | Unsplash/Pinterest | Not UI-specific |

---

## Jordan's Reference Bookmarks

For quant_v4 dashboard specifically:
- **Mobbin Finance** → Dark dashboard references for trading UIs
- **Figma Community "Shadcn"** → Component library matching current stack
- **Linear Design System** → Dark theme spacing + typography reference
- **Vercel Dashboard** → Clean minimal data display patterns (matches Vercel/Shadcn aesthetic)
