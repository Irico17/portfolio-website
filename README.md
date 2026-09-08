# Portfolio — Cristhofer Alegre

Sitio paste-up (Astro 5 + TypeScript). El diseño vive en `PRODUCT.md` y `DESIGN.md`. Los huecos de obra son intencionales: no inventar proyectos.

## Local

```bash
npm ci
npm run dev
```

El dev server queda en `http://localhost:4321/portfolio-website/` (el `base` de GitHub Pages también aplica en local).

```bash
npm run build
npm run preview
```

## Otra máquina

Clonar este repo es suficiente para seguir. Lleva:

- Código y plates en `src/` y `public/`
- Lockfile (`package-lock.json`)
- Skills e Impeccable en `.cursor/skills`, `.agents/skills`, `.impeccable/`
- Scripts de plates en `scripts/` (Pillow si regeneras tintas)

No commitear `node_modules/`, `dist/` ni `.env`.

## GitHub Pages

El workflow `.github/workflows/deploy.yml` publica `dist/` desde `main`.

URL: https://irico17.github.io/portfolio-website/
