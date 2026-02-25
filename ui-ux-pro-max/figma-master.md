# Figma Master — Production Workflow Guide

Integrated with Jordan's Figma MCP (available in Claude Code). Use this guide to create, inspect, and pipeline production Figma files.

---

## 1. Production File Structure

Every production Figma file uses this page structure:
```
📄 Cover          — Thumbnail with project name, version, date
📄 Design System  — Tokens, colors, typography, spacing grid
📄 Components     — Atom/Molecule/Organism library
📄 Screens        — Actual product screens (flows organized by section)
📄 Prototypes     — Interactive flow overlays
📄 Archive        — Deprecated screens (never delete, archive)
```

Rule: Never put components in the Screens page. If you're copying a component manually, it belongs in the Components page.

---

## 2. Component Architecture (Atomic Design in Figma)

```
Atoms
  → Button (variants: primary/secondary/ghost/destructive, sizes: sm/md/lg)
  → Badge (variants: default/success/warning/destructive/outline)
  → Input (states: default/focus/error/disabled)
  → Avatar (sizes: sm/md/lg, with fallback initials)
  → Icon (from Lucide set, 16px/20px/24px)

Molecules
  → FormField (Label + Input + HelperText/Error)
  → StatCard (Icon + Value + Label + Delta)
  → MetricRow (Label + Value + optional Badge)
  → SearchBar (Input + Icon + clear button)

Organisms
  → DataTable (Header + rows + pagination + empty state)
  → NavigationSidebar (Logo + NavItems + user section)
  → PageHeader (Title + subtitle + actions)
  → StrategyCard (name + pair + status + mini-metrics)

Templates
  → DashboardLayout (Sidebar + TopBar + content area)
  → SettingsLayout (Sidebar nav + content panel)
  → AuthLayout (centered card, brand mark)
```

---

## 3. Auto Layout Rules (Production Patterns)

**Container pattern** (use for all frames):
- Direction: Vertical
- Padding: 24px (top/bottom), 24px (left/right) → matches Tailwind `p-6`
- Gap: 16px → matches `gap-4`
- Hug contents (height), Fill container (width)

**Horizontal toolbar/nav**:
- Direction: Horizontal
- Alignment: Space between
- Padding: 12px vertical, 16px horizontal
- Items: Fixed width or Hug

**Card component**:
- Direction: Vertical
- Padding: 16px → `p-4`
- Gap: 12px → `gap-3`
- Background: `--card` token
- Border radius: `--radius` token (8px default)
- Border: 1px `--border` token

**List items**:
- Direction: Vertical
- Gap: 0 (use dividers instead)
- Each item: Horizontal, Space between, padding 12px vertical

---

## 4. Variant Architecture (State Machines)

Build variants as explicit state machines. For every interactive component:

```
Button
  ├── State=Default, Size=sm/md/lg, Variant=primary/secondary/ghost/destructive
  ├── State=Hover (same grid)
  ├── State=Focus (add focus ring)
  ├── State=Disabled (opacity 0.5, cursor blocked)
  └── State=Loading (spinner replaces text/icon)

Input
  ├── State=Default
  ├── State=Focus (border = primary)
  ├── State=Error (border = destructive, helper text red)
  ├── State=Disabled (muted background)
  └── State=Filled (text present, clear icon appears)
```

Variant naming convention — always: `Property=Value`:
- ✅ `State=Hover, Size=md, Variant=primary`
- ❌ `hover-md-primary` (breaks Figma variant picker)

---

## 5. Token System (Figma → Tailwind/Shadcn Mapping)

Define these as Figma Variables (not just color styles):

```
Color tokens (map to Shadcn globals.css):
  color/background     → --background
  color/foreground     → --foreground
  color/primary        → --primary
  color/primary-fg     → --primary-foreground
  color/muted          → --muted
  color/muted-fg       → --muted-foreground
  color/destructive    → --destructive
  color/border         → --border
  color/card           → --card
  color/card-fg        → --card-foreground

Spacing tokens (map to Tailwind spacing):
  space/1   → 4px   (Tailwind space-1)
  space/2   → 8px
  space/3   → 12px
  space/4   → 16px  (p-4)
  space/6   → 24px  (p-6)
  space/8   → 32px

Radius tokens:
  radius/sm  → 4px  (rounded-sm)
  radius/md  → 8px  (rounded-md) ← Shadcn default
  radius/lg  → 12px (rounded-lg)
  radius/full → 9999px (rounded-full)

Font size tokens:
  text/xs   → 12px
  text/sm   → 14px
  text/base → 16px
  text/lg   → 18px
  text/xl   → 20px
  text/2xl  → 24px
```

**How to apply**: Use Variables panel (not color picker). Tokens in Variables auto-sync when you switch light/dark mode.

---

## 6. Dev Mode Handoff Conventions

Before handoff:
- All layers named (not "Rectangle 42")
- All text using text styles from Design System page
- All colors using Variables (not raw hex)
- Export settings on icons: SVG, 1x
- Export settings on images: PNG 2x
- Spacing annotations: use Figma's built-in measure tool (Option+hover)

Annotation pattern for complex layouts:
- Add a "Redlines" layer (hide by default)
- Red = spacing values, Blue = component names, Green = interaction notes

---

## 7. Figma MCP Integration

Jordan has the Figma MCP available. Use it to:

**Screenshot inspection**:
```
Use Figma MCP → take screenshot of selected frame
→ Analyze layout, identify spacing, component patterns
→ Map to Tailwind equivalents
```

**Component extraction**:
```
Use Figma MCP → get component properties
→ Extract variant names → map to Shadcn props
→ Generate TypeScript interface from variant grid
```

**Design token extraction**:
```
Use Figma MCP → get file variables
→ Export as CSS custom properties
→ Diff against globals.css to find mismatches
```

**Workflow for cloning a reference design**:
1. Find reference on Mobbin/Community (see figma-references.md)
2. Use Figma MCP to screenshot key screens
3. Analyze layout with Claude → identify grid, spacing, type scale
4. Map to Jordan's token system
5. Build in Figma using Variables (don't copy raw values)
6. Generate component with v0.dev using extracted specs

---

## 8. Quick Adjustment Patterns

**Token swap** (change primary color everywhere):
- Go to Variables panel → edit `color/primary` → all instances update

**Spacing change** (tighten all card padding):
- Edit `space/4` variable → all components using it update

**State override** (show error state in prototype):
- Select component → in Properties panel → change State to Error
- Never duplicate frames for states — use variants

**Dark/light mode**:
- Set up two Variable Modes: Light + Dark
- Toggle in View → Preferences → Variable Mode
- All tokens swap automatically if mapped correctly

**Non-destructive layer edit**:
- Always use Smart Animate or component override
- Never detach instances unless redesigning the component
- Keep originals in Components page; all screens use instances

---

## 9. Common Anti-Patterns

| Anti-Pattern | Correct Approach |
|--------------|------------------|
| Raw hex colors | Use Variables |
| Copy-paste styling | Use component instances |
| Frames without Auto Layout | Always use Auto Layout |
| Naming layers "Frame 42" | Name by content/role |
| Duplicating for states | Use Variants |
| Detaching instances | Override props instead |
| Multiple components for spacing variants | Use Auto Layout padding |
| Absolute positioning (no constraints) | Set constraints: left+right / top+bottom |
