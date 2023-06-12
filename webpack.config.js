const path = require('path');
const webpack = require('webpack');

const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');
const SentryWebpackPlugin = require('@sentry/webpack-plugin');

const devMode = process.env.NODE_ENV !== 'production';
const hotReload = process.env.HOT_RELOAD === '1';

const vueRule = {
  test: /\.vue$/,
  use: 'vue-loader',
  exclude: /node_modules/,
};

const styleRule = {
  test: /\.(sa|sc|c)ss$/,
  use: [
    MiniCssExtractPlugin.loader,
    { loader: 'css-loader', options: { sourceMap: true } },
    { loader: 'postcss-loader', options: { postcssOptions: { plugins: ['autoprefixer'] } } },
    'sass-loader',
  ],
};

const jsRule = {
  test: /\.js$/,
  loader: 'babel-loader',
  include: path.resolve('./static/src/js'),
  exclude: /node_modules/,
};

const assetRule = {
  test: /.(jpg|png|woff(2)?|eot|ttf|svg|ico)$/,
  loader: 'file-loader',
};

const plugins = [
  new webpack.ProvidePlugin({
    'window.jQuery': 'jquery',
    jQuery: 'jquery',
    $: 'jquery',
  }),
  new BundleTracker({
    path: __dirname,
    filename: './webpack-stats/webpack-stats.json',
  }),
  new VueLoaderPlugin(),
  new MiniCssExtractPlugin({
    filename: devMode ? '[name].css' : '[name].[hash].css',
    chunkFilename: devMode ? '[id].css' : '[id].[hash].css',
  }),
  new BundleAnalyzerPlugin({ analyzerMode: 'static', openAnalyzer: false }),
  new webpack.HotModuleReplacementPlugin(),
  new CleanWebpackPlugin(),
  new CopyWebpackPlugin({
    patterns: [
      { from: './static/src/images/**/*', to: path.resolve('./static/dist/images/[name].[ext]'), toType: 'template' },
    ],
  }),
  new SentryWebpackPlugin({
    ignoreFile: '.sentrycliignore',
    ignore: ['node_modules', 'webpack.config.js'],
    configFile: 'sentry.properties',
    dryRun: true,
    release: 'v1.0.0',
    project: 'hedera',
    org: 'harvard-university-academic-te',
    include: './static/dist',
    authToken: process.env.SENTRY_AUTH_TOKEN,
  }),
];

if (devMode) {
  styleRule.use = ['css-hot-loader', ...styleRule.use];
} else {
  plugins.push(new webpack.EnvironmentPlugin(['NODE_ENV']));
}

module.exports = {
  context: __dirname,
  entry: './static/src/js/index.js',
  output: {
    path: path.resolve('./static/dist/'),
    filename: '[name]-[hash].js',
    publicPath: hotReload ? 'http://localhost:8080/' : 'https://s3.amazonaws.com/atg-hedera-dev-assets/static/',
  },
  devtool: devMode ? 'cheap-eval-source-map' : 'source-map',
  devServer: {
    hot: true,
    quiet: false,
    host: devMode ? '0.0.0.0' : 'localhost',
    headers: { 'Access-Control-Allow-Origin': '*' },
  },
  module: { rules: [vueRule, jsRule, styleRule, assetRule] },
  externals: { jquery: 'jQuery' },
  plugins,
  optimization: {
    minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true, // set to true if you want JS source maps
      }),
      new OptimizeCSSAssetsPlugin({}),
    ],
    splitChunks: {
      cacheGroups: {
        commons: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendor',
          chunks: 'initial',
        },
      },
    },
  },
};
