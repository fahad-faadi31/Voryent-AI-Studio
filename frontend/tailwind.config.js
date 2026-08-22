/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        voryent: {
          50: '#f0f4ff',
          100: '#dbe4ff',
          200: '#bac8ff',
          300: '#8aa2ff',
          400: '#5a72ff',
          500: '#3b4aeb',
          600: '#2d34c9',
          700: '#252a9e',
          800: '#21267d',
          900: '#1a1e5c',
        },
      },
    },
  },
  plugins: [],
}