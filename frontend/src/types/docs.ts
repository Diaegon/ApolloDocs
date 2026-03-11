// ─── Shared ────────────────────────────────────────────────────────────────

export type NumeroFases = "monofasico" | "bifasico" | "trifasico";
export type TipoInversor = "string" | "micro";
export type ClasseConsumo = "residencial" | "comercial" | "industrial" | "rural";
export type TipoFornecimento = "monofasico" | "bifasico" | "trifasico";
export type RamalEnergia = "aereo" | "subterraneo";
export type QuantidadeSistemas = 1 | 2 | 3;

// ─── Sub-models ─────────────────────────────────────────────────────────────

export interface Cliente {
  id_cliente?: number;
  nome_cliente: string;
  cpf: string;
  data_nascimento: string;
  razao_social?: string;
  nome_fantasia?: string;
  cnpj?: string;
  rg: string;
  telefone_cliente: string;
  email_cliente: string;
}

export interface EnderecoCliente {
  logradouro_cliente: string;
  numero_casa_cliente: string;
  complemento_casa_cliente?: string;
  cep_cliente: string;
  bairro_cliente: string;
  cidade_cliente: string;
  estado_cliente: string;
}

export interface EnderecoObra {
  logradouro_obra: string;
  numero_obra: string;
  complemento_obra?: string;
  cep_obra: string;
  bairro_obra: string;
  cidade_obra: string;
  estado_obra: string;
  latitude_obra?: string;   // str | None in backend
  longitude_obra?: string;  // str | None in backend
}

export interface Procurador {
  id_procurador?: number;
  nome_procurador: string;
  cpf_procurador: string;
  rg_procurador: string;
  telefone_procurador: string;
  email_procurador: string;
  logradouro_procurador: string;
  numero_casa_procurador: string;
  complemento_procurador?: string;
  cep_procurador: string;
  bairro_procurador: string;
  cidade_procurador: string;
  estado_procurador: string;
}

export interface Inversor {
  id_inversor: number | null; // int | None, no default → required by Pydantic v2
  marca_inversor: string;
  modelo_inversor: string;
  potencia_inversor: number;
  numero_fases: NumeroFases;
  tipo_de_inversor: TipoInversor;
  numero_mppt?: number;
}

export interface Placa {
  id_placa: number | null;        // int | None, no default → required by Pydantic v2
  marca_placa: string;
  modelo_placa: string;
  potencia_placa: number;
  tipo_celula: string;
  tensao_pico: number;
  corrente_curtocircuito: number;
  tensao_maxima_potencia: number;
  corrente_maxima_potencia: number;
  eficiencia_placa: number | null; // float | None, no default → required by Pydantic v2
}

export interface QuantidadePlacas {
  quantidade_placas: number;
  quantidade_placas2?: number;
}

export interface ConfiguracaoSistema {
  inversor: Inversor;
  quantidade_inversor: number;
  quantidade_total_placas_do_sistema: QuantidadePlacas;
  placa: Placa;
  placa2?: Placa;
}

// ─── Project types ──────────────────────────────────────────────────────────

export interface ProjetoMemorial {
  id_projeto: number | null;        // int | None, no default → required by Pydantic v2
  cliente: Cliente | null;          // Cliente | None, no default → required by Pydantic v2
  endereco_obra: EnderecoObra | null; // EnderecoObra | None, no default → required by Pydantic v2
  numero_unidade_consumidora: string;
  carga_instalada_kw: number;
  disjuntor_geral_amperes: number;
  energia_media_mensal_kwh: number;
  classe_consumo1: ClasseConsumo;
  tipo_fornecimento: TipoFornecimento;
  ramal_energia: RamalEnergia;
  data_projeto: string;
  quantidade_sistemas_instalados: QuantidadeSistemas;
  sistema_instalado1: ConfiguracaoSistema;
  sistema_instalado2?: ConfiguracaoSistema;
  sistema_instalado3?: ConfiguracaoSistema;
}

export interface ProjetoProcuracao {
  id_projeto: number | null; // int | None, no default → required by Pydantic v2
  cliente: Cliente;
  endereco_cliente: EnderecoCliente;
  endereco_obra: EnderecoObra;
  procurador: Procurador;
}

export interface ProjetoUnifilar {
  nome_projetista: string;
  cft_crea_projetista: string;
  nome_cliente: string;
  quantidade_sistemas_instalados: QuantidadeSistemas;
  disjuntor_geral_amperes: number;
  tensao_local: number; // int in backend, not string
  endereco_obra: EnderecoObra;
  sistema_instalado1: ConfiguracaoSistema;
  sistema_instalado2?: ConfiguracaoSistema;
  sistema_instalado3?: ConfiguracaoSistema;
}

export interface ProjetoFormularioEnelCe {
  numero_uc: string;
  classe: ClasseConsumo;
  ramal_energia: RamalEnergia;
  nome_cliente: string;
  cpf: string;
  telefone_cliente: string;
  email_cliente: string;
  endereco_obra: EnderecoObra;
  tensao_local: number; // int in backend, not string
  carga_instalada_kw: number;
  potencia_geracao: number;
  nome_procurador: string;
  cpf_procurador: string;
  email_procurador: string;
  data_hoje: string;
  telefone_procurador: string;
}

// ─── API response ────────────────────────────────────────────────────────────

export type DocType = "memorial" | "procuracao" | "unifilar" | "formulario";

export interface GenerateDocResult {
  pdfUrl: string;
  filename: string;
}
