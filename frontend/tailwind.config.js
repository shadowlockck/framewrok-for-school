/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: 'var(--color-primary, #1e40af)',
          hover: 'var(--color-primary-hover, #1d4ed8)',
          light: 'var(--color-primary-light, #dbeafe)',
        },
        secondary: {
          DEFAULT: 'var(--color-secondary, #047857)',
          hover: 'var(--color-secondary-hover, #065f46)',
          light: 'var(--color-secondary-light, #d1fae5)',
        },
        accent: {
          DEFAULT: 'var(--color-accent, #b45309)',
        },
        accessible: {
          bg: 'var(--acc-bg, #ffffff)',
          text: 'var(--acc-text, #111827)',
          link: 'var(--acc-link, #0000ee)',
        }
      },
      fontFamily: {
        sans: ['var(--font-family-base, Inter, system-ui, sans-serif)'],
      }
    },
  },
  plugins: [],
}
