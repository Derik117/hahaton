module.exports = {
  devServer: {
    disableHostChek: true,
    proxy: {
      '^/api/': {
        target: 'http://127.0.0.1:8000/api/',
        ws: false,
      }
    }
  },
  // outputDir must be added to Django's TEMPLATE_DIRS
  outputDir: './dist/',
  // assetsDir must match Django's STATIC_URL
  assetsDir: 'static',
}