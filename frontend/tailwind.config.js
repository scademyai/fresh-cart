module.exports = {
  content: [
    './src/**/*.{html,ts}',
  ],
  theme: {
    
    extend: {
      colors: {
        'primary': '#93cba3',
        'secondary':'#0f585a',
        'orange': '#f5bc62',
      },
      backgroundImage: {
        'hero-pattern': "url('/assets/hero-photo-fresh-cart.png')"
      }
    },
  },
  plugins: [],
  important: true
}
