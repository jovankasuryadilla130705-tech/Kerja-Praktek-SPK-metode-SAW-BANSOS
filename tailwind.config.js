/** @type {import('tailwindcss').Config} */
module.exports = {
  // Scan semua file HTML di templates dan JS di static
  // agar hanya class yang benar-benar dipakai yang di-compile
  content: [
    "./frontend/templates/**/*.html",
    "./frontend/static/js/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
