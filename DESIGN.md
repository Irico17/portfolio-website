---
name: Cristhofer Alegre
description: Tonight's flyer — xerox paste-up portfolio
colors:
  paper: "#d2ceca"
  toner: "#232324"
  dust: "#a7a39f"
  pink: "#e74879"
  ransom-scrap: "#ebe6df"
  biro: "#2a4580"
  stamp: "#dc376e"
  type-ink: "#19191a"
  dense: "#090a0a"
  scrap-hot: "#f7eef2"
typography:
  display:
    fontFamily: "Tilt Prism, Times New Roman, serif"
    fontSize: "52cqh"
    fontWeight: 400
    lineHeight: 0.82
    letterSpacing: "0"
  headline:
    fontFamily: "Archivo Black, Arial Black, sans-serif"
    fontSize: "clamp(4.2rem, 12.5vw, 8.6rem)"
    fontWeight: 400
    lineHeight: 0.78
    letterSpacing: "-0.04em"
  title:
    fontFamily: "Intel One Mono, Courier New, monospace"
    fontSize: "clamp(1.4rem, 2.6vw, 2.4rem)"
    fontWeight: 300
    lineHeight: 1
    letterSpacing: "0.1em"
  body:
    fontFamily: "Intel One Mono, Courier New, monospace"
    fontSize: "1rem"
    fontWeight: 300
    lineHeight: 1.45
    letterSpacing: "normal"
  label:
    fontFamily: "Intel One Mono, Courier New, monospace"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "0.04em"
  note:
    fontFamily: "Segoe Script, cursive"
    fontSize: "34px"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "normal"
rounded:
  none: "0px"
spacing:
  xs: "0.4rem"
  sm: "0.55rem"
  md: "0.9rem"
  lg: "1.1rem"
  xl: "1.5rem"
  2xl: "4rem"
components:
  stamp:
    backgroundColor: "transparent"
    textColor: "#dc376e"
    rounded: "{rounded.none}"
    padding: "0.15rem 0.4rem"
  stamp-hover:
    backgroundColor: "transparent"
    textColor: "#dc376e"
  skip:
    backgroundColor: "{colors.toner}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.6rem 0.8rem"
  sheet:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.toner}"
    rounded: "{rounded.none}"
    padding: "1.4rem 1.5rem 1.6rem"
  sheet-pink:
    backgroundColor: "{colors.pink}"
    textColor: "{colors.toner}"
    rounded: "{rounded.none}"
    padding: "1.4rem 1.5rem 1.6rem"
  ransom-tile:
    backgroundColor: "{colors.ransom-scrap}"
    textColor: "{colors.toner}"
    rounded: "{rounded.none}"
    padding: "0.05em 0.07em 0.02em"
  ransom-tile-hot:
    backgroundColor: "{colors.pink}"
    textColor: "#f7eef2"
    rounded: "{rounded.none}"
    padding: "0.05em 0.07em 0.02em"
  ransom-tile-invert:
    backgroundColor: "{colors.toner}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
  card-title:
    backgroundColor: "transparent"
    textColor: "{colors.toner}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
  work-label:
    backgroundColor: "transparent"
    textColor: "{colors.toner}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0 0.4em"
  scrap-link:
    backgroundColor: "transparent"
    rounded: "{rounded.none}"
    padding: "0"
    height: "44px"
  mini:
    backgroundColor: "transparent"
    textColor: "{colors.toner}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
---

# Design System: Tonight's Flyer

## Overview

**Creative North Star: "Tonight's Flyer"**

The page is a paste-up desk: cheap xerox stock still warm from the copier, toner, torn scraps, and one day-glo pink stamp. It is a scene first. Recruiter, peer, or friend should feel the table, name Cristhofer Alegre, and reach work, path, skills, and contact without hunting.

Density is flyer-tight, not dashboard-airy. Type is cut, stamped, or typed on a typewriter. The first viewport is overlapping sheets on a 1536×1024 desk; everything below is more xerox pages in a stack. Spanish chrome. Honest slots stay slots.

Confirmed rejections: the SaaS card grid, the amp-gadget hero, and the dark recinto / chrome-neon translation. Atmosphere is identity, but spectacle never hides Trabajo, Camino, Skills, or Contacto.

**Key Characteristics:**
- Cheap xerox paper ground, tiled grain, thin noise overlay
- Toner black for type and cuts; one day-glo pink for action
- Ransom-cut name, Archivo Black shouts, Intel One Mono for typed matter
- Overlapping scraps on a 3:2 desk; mobile restacks the same pieces
- Placeholders read as placeholders (Proyecto 01, Slot pendiente)

## Colors

Four inks on copy paper: toner, dust, day-glo pink, and the paper itself. Chroma is rare on purpose.

### Primary
- **Day-Glo Xerox Pink**: Action only — CONTACTO stamp, caret, selection, focus ring, scrollbar thumb, ransom hot letters, and the pink archivo sheet. Comp coverage sits near 7%. Its job is to pull the hand, not to tint the world.

### Neutral
- **Cheap Copy Stock** (`paper`): Page ground, theme color, skip-link type, inverted ransom glyphs. The desk is this stock, not white and not a night recinto.
- **Toner Black** (`toner`): Default type, inverted tiles, skip-link fill. Near-blacks used on live labels sit on this ink; do not split a new brand black per block.
- **Halftone Dust** (`dust`): Mid gray in the xerox grain; mixed into legal type so the footer looks faded, not designed-muted.
- **Ransom Scrap** (`ransom-scrap`): The slightly warmer off-white of cut letter tiles, sitting a step lighter than the desk.

### Named Rules
**The One Pink Rule.** Day-glo pink is the only chroma for action. If a surface needs emphasis, stamp it or invert it in toner. Do not add a second accent.

**The Copy-Stock Rule.** Grounds stay xerox paper. Dark shells, pure white boards, and cool SaaS gray are off the desk.

## Typography

**Display Font:** Tilt Prism (with Times New Roman)
**Body Font:** Intel One Mono (with Courier New)
**Poster Font:** Archivo Black (with Arial Black)
**Note Font:** Caveat (with Segoe Script)

**Character:** A flyer that was typed, then shouted, then annotated. Mono does the reading. Black poster type does the section yell. Prism is one ransom glyph, not a headline family for paragraphs. Caveat is the biro note, not UI chrome.

### Hierarchy
- **Display** (400, 52cqh on the name region / clamp(2.2rem, 12vw, 3.8rem) when stacked, line-height 0.82): Ransom-cut identity. Mix default mono tiles with one Prism glyph, some toner-invert tiles, some pink-hot tiles. Live hero may ship the name as a plate of this language; new name moments still build from tiles, not a clean wordmark.
- **Headline** (400, clamp(4.2rem, 12.5vw, 8.6rem), line-height 0.78, tracking -0.04em to -0.07em, uppercase): TRABAJO-scale shouts in Archivo Black. The hero region may run far larger (252px) to fill its sheet; the clamp is the portable poster size. Optional last-letter invert and a strip of fake tape on a cut glyph.
- **Title** (300, clamp(1.4rem, 2.6vw, 2.4rem) in the stack; hero CAMINO/SKILLS run ~52–63px, tracking 0.08–0.14em, uppercase, hairline underline): Section words on the scraps and sheet headings below the fold.
- **Body** (300, 1rem, line-height 1.45): Default document voice — path copy, skill lines, legal. Weight 300 is the typed page; do not bold for hierarchy.
- **Label** (400, 1rem / 16–18px on mini blocks, tracking 0.04–0.08em): Mini Estudio/Rol lines, project-row ids, uppercase mini strongs. Work-slot names (PROYECTO 01) share this family at a louder size (clamp 1.05–1.7rem on the strip; ~42–44px on the second slot).
- **Note** (400, 34px, line-height 1.05, underline 2px): Handwritten tagline voice (diseño + desarrollo + dirección). Live first viewport may rasterize it; CSS still treats Caveat as the biro.

### Named Rules
**The Cut-Letter Rule.** The name is ransom tiles, never a single clean wordmark and never a system UI display face as the lead.

**The Typewriter Body Rule.** Intel One Mono carries body, titles, and labels. Archivo Black and Tilt Prism shout; they do not set paragraphs.

## Layout

The first viewport is a paste-up frame: `min(100%, 1536px)`, landscape `1536 / 1024`, overlapping absolute scraps. Trabajo is the largest sheet; CONTACTO shares the top with the name; Camino and Skills tuck under as smaller sheets. Type regions sit above the rasters (z-index ~5–12). The desk does not use a 12-column grid.

Below the fold, `.more` is a single column at the same max width: gap 1.1rem (`lg`), horizontal padding ~1rem, sheet padding 1.4/1.5/1.6rem (`xl`), bottom margin 4rem (`2xl`). Lists are tight (0.55rem between project rows, 1rem between path/skill items). Contact scraps flex with a 0.4rem gap (`xs`) and a 12–18rem basis.

At `max-width: 860px` the frame becomes a column (gap 0.9rem, `md`), paper-ground and bleed hide, and the same scraps restack in a committed order: name, stamp, tagline, trabajo, slots, camino, skills. Mobile is a translation of the desk, not a different product. Touch targets on stamp, contacto, and scrap links hold 44px.

Spanish region names and skip target (`#trabajo`) stay findable in seconds on both widths.

## Elevation & Depth

Depth is physical stacking, not a card-shadow scale. On the desk, sheets overlap (trabajo z 1, camino/skills z 2, stamp/strip z 3, type z 5+) with a 7% overlay grain. Below the fold, each xerox sheet gets a soft drop and a fraction of a degree of rotation. Cut-letter tiles carry a 1–2px hard lip because they are glued scraps, not because the system is neubrutalist.

### Shadow Vocabulary
- **Sheet drop** (`box-shadow: 0 10px 22px rgb(20 16 14 / 0.22)`): Below-fold xerox pages only.
- **Letter lip** (`box-shadow: 1px 2px 0 rgb(20 16 14 / 0.18)`): Ransom tiles (invert cuts may use `2px 3px 0 rgb(20 16 14 / 0.2)`). Do not put this lip on sheets, buttons, or layout frames.

### Named Rules
**The Overlap Rule.** Desk depth comes from overlapping scraps, z-index, and grain. Soft drops belong on stacked xerox sheets below the fold. Hard-offset lips belong on cut letters only.

## Shapes

Everything is a square cut (`0px` radius). Roundness is off the table. Silhouettes of torn paper live in the plate rasters, not in CSS radius. The CONTACTO stamp is a 3px square frame, rotated -7deg. Typed rules are 1px solid or dashed toner lines (mini underline dashed at 55% toner; project rows dashed at 35%; CAMINO title 1–2px solid). A translucent tape strip may cross one cut poster glyph. Sheets sit slightly crooked (-0.7deg to 0.55deg). Hover lifts a scrap 3px; it does not round it.

## Components

Flyer hardware: stamps, glued letters, xerox pages, typed labels. No form kit. No chips. No glyph-icon buttons.

### Buttons
- **Shape:** Square cut (0). Stamp is a framed word, not a filled pill.
- **Primary (CONTACTO stamp):** Transparent fill, 3px solid stamp ink, Archivo Black, 26px, tracking 0.1em, uppercase, padding 0.15rem 0.4rem (0.7rem 1rem and min-height 44px when stacked). Rotated -7deg. Live hero may paint this as a plate; the CSS stamp is the reusable action.
- **Hover / Focus:** On fine pointer, translateY(-3px) and contrast 1.18. Keyboard focus is a 2px pink outline with 3px offset (global). Active scrap links scale to 0.97.
- **Skip:** Toner fill, paper type, padding 0.6rem 0.8rem, parked off-canvas until focused. Copy stays Spanish (`Ir a trabajo`).
- **Scrap links:** Image-plate contact buttons (LinkedIn, GitHub), transparent, min 44×44px, no text chrome, no icon font.

### Cards / Containers
- **Corner Style:** Square cut (0)
- **Background:** Copy-stock xerox sheet image on `paper`; the archivo sheet is the pink xerox (`sheet-pink`)
- **Shadow Strategy:** Sheet drop below the fold; none on the hero plates (overlap does the work)
- **Border:** None. Edges are the raster tear.
- **Internal Padding:** 1.4rem 1.5rem 1.6rem
- **Behavior:** Alternate tiny rotations per sheet. Hover on fine pointer lifts 3px. Headings inside are title-case-as-uppercase tracked mono.

### Navigation
- **Style:** No persistent nav bar. The desk is the map. Skip link to Trabajo; CONTACTO stamp jumps to `#contacto`. Scrap links are the only outbound actions (LinkedIn, GitHub). Hover contrast, not underline-as-UI.

### Ransom name
Cut-letter identity. Flex wrap, 0.06em gap, per-letter rotation (~-2deg to 1.6deg), scrap fill, optional invert and hot tiles, one Prism glyph. Letters slap in (480ms, staggered). Hover on a tile adds ~2deg and -2px. Reduced motion holds the settled collage.

### Work label
Loud mono slot name on the strip (PROYECTO 01 / 02). Uppercase, tracking 0.04em, no kicker above it. Empty work stays `Proyecto NN` + `Slot pendiente`.

### Mini block
Two-line typed scrap: uppercase label (`Estudio`, `Rol`) then a dashed rule and the place (PUCP, IBM). 16–18px, weight 400. Do not invent extra employers or schools.

## Do's and Don'ts

### Do:
- **Do** keep the desk on cheap copy stock with toner type and a single pink for action.
- **Do** build identity as ransom tiles and section yells as Archivo Black; let Intel One Mono do the reading.
- **Do** stack overlapping xerox scraps on desktop and restack those same scraps below 860px.
- **Do** leave empty work as numbered slots. Spanish chrome; SKILLS may stay as shipped.
- **Do** slap scraps on enter (560ms ease-out) and kill motion when `prefers-reduced-motion: reduce`. Keep 44px hits and a visible pink focus ring.

### Don't:
- **Don't** introduce a second accent, a dark recinto shell, or a SaaS card grid.
- **Don't** set body copy in Tilt Prism or Archivo Black, or lead with a system UI display face.
- **Don't** use round corners, glyph-icon buttons, or a persistent product nav.
- **Don't** invent project titles, metrics, clients, employers, or schools.
- **Don't** autoplay sound, or ship a motion-only story with no still collage.
