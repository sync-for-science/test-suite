var webpack = require('webpack')
var path = require('path')

var buildPath = path.resolve(__dirname, 'testsuite', 'static', 'build');
var mainPath = path.resolve(__dirname, 'assets', 'main.js');

module.exports = {
  devtool: 'cheap-module-source-map',
  entry: {
    app: [mainPath],
    vendor: [
      'bootstrap',
      'handlebars',
      'jquery',
      'js-yaml',
      'socket.io-client',
      'underscore',
      'uuid',
    ],
  },
  output: {
    path: buildPath,
    filename: '[name].bundle.js',
    publicPath: '/static/build/',
  },
  module: {
    rules: [
      {
        test: /\.less$/,
        use: ['style-loader', 'css-loader', 'less-loader'],
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.hbs$/,
        use: ['handlebars-loader'],
      },
      // the url-loader uses DataUrls.
      // the file-loader emits files.
      {test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=application/font-woff'},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=application/octet-stream'},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, use: 'file-loader'},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, use: 'url-loader?limit=10000&mimetype=image/svg+xml'},

    ],
  },

  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      filename: 'vendor.bundle.js',
      minChunks: Infinity,
      chunks: ['app'],
    }),
  ],

  resolve: {
    extensions: ['.js'],
    alias: {
      'handlebars': 'handlebars/dist/handlebars.js',
    },
  },
};
