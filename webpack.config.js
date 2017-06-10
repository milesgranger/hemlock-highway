/**
 * Created by milesg on 09.06.17.
 */

const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: [
        './src/index.jsx'
    ],
    output: {
        path: path.resolve(__dirname, 'static', 'js'),
        filename: 'bundle.js',
        publicPath: 'static/js/'
    },
    module: {
        loaders: [
            {
                exclude: /node_modules/,
                loader: 'babel-loader',
                query: {
                    presets: ['react', 'es2015', 'stage-1']
                }
            }
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    devServer: {
        historyApiFallback: true,
        contentBase: './templates',
        inline: true
    }
};