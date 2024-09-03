const colors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        minnie: ["Minnie"],
        poppins: ["Poppins"],
        lexend: ["Lexend"],
        fredoka: ["Fredoka"],
      },
    },
    colors: {
      transparent: "transparent",
      current: "currentColor",
      raisinblack: "#332E3C",
      lightpink: "#D5C5C8",
      royalblue: "#5A70BF",
      emeraldgreen: "#77ACA2",
      lavender: "#EAE8FF",
      platinum: "#D8D5D8",
      frenchgray: "#ADACB5",
      uranianblue: "#B0D7FF",

      gunmetal: "#2D3142",
      discordblue: "#5769E9",
      amethystsmoke: "#A09DC0",


      white: colors.white,
      blue: colors.blue,
      gray: colors.gray,
      black: colors.black,
    },
  },
  plugins: [],
};
