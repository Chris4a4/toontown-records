const colors = require('tailwindcss/colors')

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      backgroundImage: {
        'custom-background': "url('/background.png')"
      }
    },
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      'raisinblack': '#332E3C',
      'lightpink': '#D5C5C8',
      'royalblue': '#5A70BF',
      'emeraldgreen': '#77ACA2',

      'white': colors.white,
      'blue': colors.blue,
      'gray': colors.gray
    },
    fontFamily: {
      'minnie': ['Minnie'],
      'righteous': ['Righteous'],
    }
  },
  plugins: [],
}

