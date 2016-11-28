var webpack = require('webpack')
var path = require('path')

var buildPath = path.resolve(__dirname, 'testsuite', 'static', 'build');
var mainPath = path.resolve(__dirname, 'assets', 'main.js');

module.exports = {
  devtool: 'eval',
  entry: {
    app: [mainPath],
  },
  output: {
    path: buildPath,
    filename: '[name].js',
    publicPath: '/static/build/',
  },
  module: {
    loaders: [
      {
        test: /\.less$/,
        loaders: ['style', 'css', 'less'],
      },
      {
        test: /\.css$/,
        loaders: ['style', 'css'],
      },
      {
        test: /\.hbs$/,
        loaders: ['handlebars-loader'],
      },
      // the url-loader uses DataUrls.
      // the file-loader emits files.
      {test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/font-woff'},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'},

    ],
  },

  resolve: {
    extensions: ['', '.webpack.js', '.js'],
    alias: {
      'handlebars': 'handlebars/dist/handlebars.js',
    },
  },

  node: {
    fs: 'empty' // avoids error messages
  },
};
