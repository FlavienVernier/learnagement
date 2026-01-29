import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        'usmb-blue': '#10069f',
        'usmb-dark-blue': '#002542',
        'usmb-cyan' : '#009cdd',
        'usmb-red' : '#ef3340',
        'usmb-green' : '#009956',
        'usmb-grey' : '#939598',
        'cm-red' : '#ff6666',
        'td-green' : '#80ff00',
        'tp-yellow' : '#ffff00',
        'exam-blue' : '#00ffff',
        'other-pink': '#ff6fcf'
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
} satisfies Config;
