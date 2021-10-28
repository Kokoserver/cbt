const config = {
  mode: 'jit',
  purge: ['./src/**/*.{html,js,svelte,ts}'],
  daisyui: {},
  theme: {
    extend: {},
  },

  plugins: [require('daisyui')],
}

module.exports = config
