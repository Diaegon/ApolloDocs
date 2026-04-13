import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#fff7ed",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
          800: "#9a3412",
          900: "#7c2d12",
          950: "#431407",
        },
        // Semantic accent tokens for each document card type.
        // Change a color here and it propagates to every use-site automatically.
        doc: {
          memorial:   { icon: "#2563eb", bg: "#eff6ff", border: "#dbeafe" },
          procuracao: { icon: "#16a34a", bg: "#f0fdf4", border: "#dcfce7" },
          unifilar:   { icon: "#ca8a04", bg: "#fefce8", border: "#fef9c3" },
          formulario: { icon: "#ea580c", bg: "#fff7ed", border: "#ffedd5" },
          inversores: { icon: "#9333ea", bg: "#faf5ff", border: "#f3e8ff" },
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
