/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        customMagenta: "#AB00AC",
        /** customLightBlack: "#4F5453", */
        customLightBlack: "#000000",
      }
    },
  },
  plugins: [],
}

