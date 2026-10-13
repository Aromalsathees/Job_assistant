/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eefaf6',
          100: '#d7f2e8',
          200: '#b1e5d3',
          300: '#7ed2ba',
          400: '#46b89c',
          500: '#15967d',
          600: '#147764',
          700: '#145f51',
          800: '#144c42',
          900: '#143f38',
        },
      },
    },
  },
  plugins: [],
}
