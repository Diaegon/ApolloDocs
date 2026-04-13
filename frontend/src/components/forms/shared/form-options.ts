export const FASES_OPTIONS = [
  { value: "monofasico", label: "Monofásico" },
  { value: "bifasico", label: "Bifásico" },
  { value: "trifasico", label: "Trifásico" },
] as const;

export const TIPO_INVERSOR_OPTIONS = [
  { value: "string", label: "String" },
  { value: "micro", label: "Micro-inversor" },
] as const;

export const CLASSE_CONSUMO_OPTIONS = [
  { value: "residencial", label: "Residencial" },
  { value: "comercial", label: "Comercial" },
  { value: "industrial", label: "Industrial" },
  { value: "rural", label: "Rural" },
] as const;

export const RAMAL_OPTIONS = [
  { value: "aereo", label: "Aéreo" },
  { value: "subterraneo", label: "Subterrâneo" },
] as const;

export const QUANTIDADE_SISTEMAS_OPTIONS = [
  { value: "1", label: "1 sistema" },
  { value: "2", label: "2 sistemas" },
  { value: "3", label: "3 sistemas" },
] as const;
