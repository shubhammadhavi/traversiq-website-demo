/** Same theme as the inline CDN config. Used only to compile /assets/site.css. */
module.exports = {
  content: ["./*.html", "./*/index.html", "./_source/template.html"],
  theme: {
    extend: {
      colors: {
        ivory: "#FAF8F3",
        navy: "#0B1F3A",
        navyLight: "#16325B",
        gold: "#C59B27",
        goldLight: "#FBF6E8",
        crimson: "#C8102E",
        whatsapp: "#15803D",
      },
      fontFamily: {
        serif: ["Libre Baskerville", "Georgia", "serif"],
        sans: ["Plus Jakarta Sans", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
};
