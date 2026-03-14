/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        author: ['Author', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
extend: {
  fontFamily: {
    author: ['Author', 'sans-serif'],
    sugar: ['"More Sugar"', 'cursive'],
  },
}
