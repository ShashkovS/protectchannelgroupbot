const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');


let WebpackObfuscator;

module.exports = (env, argv) => {
  const publicPath = '/';
  const isDev = argv.mode === 'development';

  const OBFUSTATE = !isDev; // = false;// !isDev;
  if (OBFUSTATE) {
    WebpackObfuscator = require('webpack-obfuscator');
  } else {
    class Dum {
      loader = null;
    }

    WebpackObfuscator = new Dum();
  }


  const config = {
    entry: {
      diploma1: './frontend/src/diploma1.js',
      diploma2: './frontend/src/diploma2.js',
      diploma3: './frontend/src/diploma3.js',
      // diplomaCheck: './frontend/src/diploma/checker.js',
      memegen: './frontend/src/memegen.js',
    },
    output: {
      filename: 'static/js/[name].[contenthash:8].js', // Use contenthash for cache busting,
      chunkFilename: 'static/js/[name].[contenthash:8].js',
      assetModuleFilename: 'static/assets/[name].[hash:8][ext][query]',
      path: path.resolve(__dirname, isDev ? 'build' : 'dist'),
      clean: process.env.NODE_ENV === "production",
      // clean: true,
      publicPath,
    },
    // Enable webpack-dev-server to get hot refresh of the app.
    devServer: {
      static: './build',
    },
    module: {
      rules: [
        {
          // Load CSS files. They can be imported into JS files.
          test: /\.css$/i,
          use: [MiniCssExtractPlugin.loader, 'css-loader'],
        },
        {
          test: /\.(png|svg|jpg|jpeg|gif|mp4|webp|ico|xml)$/i,
          type: 'asset/resource',
        },
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader',
          },
        },
        {
          test: /\.html$/,
          use: [
            {
              loader: 'html-loader',
              options: {
                minimize: false,  // This will prevent minification of HTML files
              },
            },
          ],
        },
      ],
    },
    resolve: {
      alias: {
        src: path.resolve(__dirname, 'frontend/src'),
      },
    },
    plugins: [
      // Generate the HTML index page based on our template.
      // This will output the same index page with the bundle we
      // created above added in a script tag.
      new HtmlWebpackPlugin({
        filename: 'static/diploma1.html',
        template: 'frontend/src/diploma1.html',
        chunksSortMode: 'auto', // Ensures chunks are sorted in the correct order
        chunks: ['diploma1'],
      }),
      new HtmlWebpackPlugin({
        filename: 'static/diploma2.html',
        template: 'frontend/src/diploma2.html',
        chunksSortMode: 'auto', // Ensures chunks are sorted in the correct order
        chunks: ['diploma2'],
      }),
      new HtmlWebpackPlugin({
        filename: 'static/diploma3.html',
        template: 'frontend/src/diploma3.html',
        chunksSortMode: 'auto', // Ensures chunks are sorted in the correct order
        chunks: ['diploma3'],
      }),
      new HtmlWebpackPlugin({
        filename: 'static/memegen.html',
        template: 'frontend/src/memegen.html',
        // favicon: 'frontend/src/images/favicon/favicon-192x192.png',
        chunksSortMode: 'auto', // Ensures chunks are sorted in the correct order
        chunks: ['memegen'],
      }),
      new webpack.DefinePlugin({
        BACKEND_URL: JSON.stringify(isDev ? 'http://localhost:3000' : 'https://communitysimplebot.shashkovs.ru'),
      }),
      new webpack.HotModuleReplacementPlugin(),
      new BundleAnalyzerPlugin({
        logLevel: 'warn',

        openAnalyzer: false,
        analyzerMode: argv.report ? 'static' : 'disabled',
        reportFilename: `report.html`,
        statsFilename: `report.json`,
        generateStatsFile: !!argv['report-json'],
      }),
      new MiniCssExtractPlugin({
        filename: 'static/css/[name].[contenthash:8].css',
        // chunkFilename: 'static/css/[name].[contenthash:8].css',
      }),
      // new CopyWebpackPlugin({
      //   patterns: [
      //     {
      //       from: 'frontend/src/images/tester.jpg', to: 'static/',
      //     },
      //   ],
      // }),
    ],
    optimization: {
      splitChunks: {
        chunks: 'async', // Split all chunks that can be shared between entry points
        maxSize: 20000, // Max size for chunks in bytes (this is just an example value)
      },
    },
  };
  if (OBFUSTATE) {
    config.module.rules.push({
          test: /\.js$/,
          exclude: [
            path.resolve(__dirname, 'node_modules'),
          ],
          enforce: 'post',
          use: {
            loader: WebpackObfuscator.loader,
            options: {
              rotateStringArray: true,
            },
          },
        },
    );
    config.plugins.push(new WebpackObfuscator({
      rotateStringArray: true,
      stringArray: true,
      splitStrings: true,
      splitStringsChunkLength: 7,
      identifierNamesCache: {},
      identifierNamesGenerator: 'mangled-shuffled',
      debugProtection: false,
      // debugProtectionInterval: 4000,
    }, ['node**', 'chunk**']));
  }

  if (isDev) {
    // Set the output path to the `build` directory
    // so we don't clobber production builds.
    config.output.path = path.resolve(__dirname, 'build');

    // Generate source maps for our code for easier debugging.
    // Not suitable for production builds. If you want source maps in
    // production, choose a different one from https://webpack.js.org/configuration/devtool
    config.devtool = 'eval-cheap-module-source-map';

    // Include the source maps for Blockly for easier debugging Blockly code.
    config.module.rules.push({
      test: /(blockly\/.*\.js)$/,
      use: [require.resolve('source-map-loader')],
      enforce: 'pre',
    });

    // Ignore spurious warnings from source-map-loader
    // It can't find source maps for some Closure modules and that is expected
    config.ignoreWarnings = [/Failed to parse source map/];
  } else {
    // config.optimization.splitChunks.cacheGroups = {
    //   vendors: {
    //     name: 'chunk-vendors',
    //     test: /[\\/]node_modules[\\/]/,
    //     priority: -10,
    //     chunks: 'initial',
    //   },
    //   common: {
    //     name: 'chunk-common',
    //     minChunks: 2,
    //     priority: -20,
    //     chunks: 'initial',
    //     reuseExistingChunk: true,
    //   },
    // };
  }
  return config;
};
