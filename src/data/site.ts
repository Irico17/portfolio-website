export const site = {
  name: "Cristhofer Alegre",
  legalName: "Cristhofer Arhon Alegre Cotrina",
  roleLine: "diseño + desarrollo + dirección",
  title: "Cristhofer Alegre — portafolio",
  description:
    "Ingeniero informático PUCP. Portafolio de Cristhofer Alegre: trabajo, camino y skills.",
  links: {
    linkedin: "https://www.linkedin.com/in/cristhoferalegre/",
    github: "https://github.com/Irico17",
  },
} as const;

export const camino = [
  {
    kind: "estudio",
    label: "Estudio",
    place: "PUCP",
    detail: "Ingeniería Informática",
    dates: "2021 — actualidad",
    note: "10.º ciclo, cerrando la carrera.",
  },
  {
    kind: "rol",
    label: "Rol",
    place: "Municipalidad de Lima",
    detail: "Analista de datos",
    dates: "enero — junio 2025",
    note: null,
  },
  {
    kind: "rol",
    label: "Rol",
    place: "IBM",
    detail: "Technical Software Sales Student",
    dates: "mayo 2026 — actualidad",
    note: "POCs y demos para América Móvil, Credicorp, Intercorp y otras.",
  },
] as const;

export const skills = [
  "Análisis de datos",
  "Demos y POCs",
  "Technical sales",
] as const;

export const projects = Array.from({ length: 10 }, (_, i) => ({
  id: String(i + 1).padStart(2, "0"),
  title: `Proyecto ${String(i + 1).padStart(2, "0")}`,
  status: "Slot pendiente",
})) as readonly { id: string; title: string; status: string }[];
