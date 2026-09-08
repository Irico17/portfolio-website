# Prompt maestro — diseño del portafolio

Pega esto en un chat de Agent **después** de recargar Cursor. `PRODUCT.md` ya existe. No vuelvas a inventar el producto.

---

## Prompt

```
Usa las skills de este repo. Empieza cargando Impeccable y no escribas UI hasta que el flujo de new-work esté resuelto.

Secuencia obligatoria:

1. Lee PRODUCT.md.
2. Ejecuta el launcher de Impeccable (Windows):
   .cursor\skills\impeccable\scripts\impeccable.cmd context
   Sigue sus directivas. No lo relances.
3. Lee .cursor/skills/impeccable/reference/new-work.md y .cursor/skills/impeccable/reference/craft-floor.md (craft-floor solo cuando ya haya dirección y vayas a codear).
4. Lee .cursor/skills/frontend-design/SKILL.md y .cursor/skills/emil-design-eng/SKILL.md.
5. Esto es greenfield. Modo de superficie: Experience (portafolio). El artefacto lidera desde el primer viewport; la UI recede. Hay un trabajo de Persuade secundario: que un recruiter encuentre trabajo, educación/carrera y skills en segundos.
6. Las Brand Commitments de PRODUCT.md son pinning visual. No las ignores, no las conviertas en un traje de World of Warcraft ni en cyberpunk púrpura de stock. Traduce esas culturas a un mundo propio. El roll de Impeccable sigue siendo obligatorio para topología, controles y ritual. Corre:
   .cursor\skills\impeccable\scripts\impeccable.cmd concept-seed --scope direction --mode experience
   Preséntame la mano. No construyas hasta que yo elija. Si no puedo elegir en la decision page, usa AskQuestion.

Restricciones del brief (ganan sobre el gusto del modelo):

- Temática fusionada, no collage: World of Warcraft (UI épica, metal, runas, vitral, oro sucio), cyberpunk (cromo, lluvia, CRT, ciudad de noche) y rock (escenario latinoamericano + Catfish and the Bottlemen: cartel de gira, vinilo, amp glow, offset print). Una sola tesis visual. No tres skins pegadas.
- Muy llamativo y único. Permitido 3D / WebGL / shaders / View Transitions, pero UN momento extraordinario (hero o transición de obra), no un carnaval.
- Paleta comprometida. Prohibido el slop: Inter/Geist/Space Grotesk/Instrument Serif; degradados púrpura-violeta; cyan sobre negro; cream+#D97757; glassmorphism decorativo; glow de box-shadow de neón; side-tab cards; cards nested; icon tile + heading; eyebrow/kicker; gradient text; bounce/elastic; marquee infinito; layout de hero-métricas.
- Tipografía: 2 familias máximo, ninguna de la lista de defaults de Impeccable/frontend-design. Display con carácter de cartel o de grimorio, body legible. Self-host o Google Fonts concretas, no system UI.
- Color: no dark+neon genérico. Oscuridad de recinto (club / catedral / instancia), acentos de metal caliente, sangre de escenario, ámbar de amp, no magenta/cyan. Neutros tintados, nunca gris puro ni negro puro.
- Layout asimétrico, overlap, ruptura de grid. Prohibido el kit SaaS de cards idénticas. Work no es un grid de 3 cards con icono.
- Copy de interfaz en español, consistente. Placeholders honestos. NO inventes empresas, escuelas, fechas, métricas, clientes ni screenshots reales. Etiqueta: Proyecto 01, Estudio / rol, Skill cluster.
- Secciones mínimas, con espacio diseñado (no lorem suelto):
  1. Hero / identidad
  2. Trabajo / portafolio (slots animados, placeholders)
  3. Educación y trabajo (timeline o ritual, no cards 01 02 03 a menos que la secuencia importe)
  4. Skills
  5. Contacto placeholder
- Stack ya decidido en PRODUCT.md: Vite + React + TypeScript. Motion: CSS + Motion. Un momento 3D con Three.js o OGL solo si overdrive lo necesita. Contenido en módulos tipados de placeholders.

Después de que yo elija dirección:

A. Escribe el surface brief + direction contract (THESIS / OWN-WORLD / STORY / FIRST VIEWPORT / FORM / FINISH) en .impeccable/surfaces/. No metas el contrato en el HTML.
B. Scaffold Vite React TS. Tokens CSS propios. Diseño code-first.
C. Construye la página completa, placeholders incluidos, responsive, focus visible, prefers-reduced-motion.
D. Entonces corre esta cadena, una a una, sobre el mismo artefacto (no las mezcles en un solo pass):
   - /impeccable overdrive el hero (propón 2–3 direcciones técnicas, espera mi pick, 60fps, fallback reduced-motion)
   - /impeccable animate el resto con tesis de motion (un momento focal; ease-out custom; no stagger de cada sección)
   - /impeccable bolder si aún se siente seguro
   - /impeccable distill si hay ruido
   - /impeccable adapt mobile
   - /impeccable audit
   - /impeccable polish
   - /impeccable document (DESIGN.md real, extraído del código)
   - npx impeccable detect src/
   - review-animations + emil-design-eng sobre el motion

Verifica en el navegador el flujo real: scroll, hover, teclado, mobile y reduced-motion. No declares listo con un screenshot.

Si el detector o el hook marcan slop, corrige. No ignores reglas para pasar el write.
```

---

## Cómo usarlo

1. Recarga la ventana de Cursor (las skills se acaban de instalar).
2. En Agent chat, escribe `/impeccable` para confirmar que aparece.
3. Pega el bloque de arriba.
4. Cuando Impeccable te muestre mundos, elige uno o pide `reroll` / `bolder`. No dejes que construya a ciegas.
5. Si quieres atajos: `/impeccable pin polish`, `/impeccable pin overdrive`, `/impeccable pin live`.

## Comandos Impeccable (referencia rápida)

| Cuándo | Comando |
|---|---|
| Empezar / no sabes | `/impeccable` |
| Plan sin código | `/impeccable shape` |
| Construir o rediseñar | describir la superficie a `/impeccable` |
| 3D, shaders, cinematic | `/impeccable overdrive` |
| Motion con oficio | `/impeccable animate` + skill `emil-design-eng` |
| Se ve genérico | `/impeccable bolder` |
| Hay ruido | `/impeccable distill` |
| Review UX | `/impeccable critique` |
| A11y / perf / slop | `/impeccable audit` y `npx impeccable detect src/` |
| Antes de ship | `/impeccable polish` |
| Iterar en el browser | `/impeccable live` |
| Congelar el sistema | `/impeccable document` |

Skills extra en este repo: `frontend-design` (anti-slop), `emil-design-eng`, `animate`, `animation-vocabulary`, `find-animation-opportunities`, `review-animations`.
