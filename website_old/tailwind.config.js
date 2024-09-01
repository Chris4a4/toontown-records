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
      'lavender': '#EAE8FF',
      'platinum': '#D8D5D8',
      'frenchgray': '#ADACB5',
      'gunmetal': '#2D3142',
      'uranianblue': '#B0D7FF',

      'white': colors.white,
      'blue': colors.blue,
      'gray': colors.gray,
      'black': colors.black
    },
    fontFamily: {
      'minnie': ['Minnie'],
      'righteous': ['Righteous'],
      'poppins': ['Poppins'],
    }
  },
  plugins: [],
}

