---
title: "Add Webpack and React Fast Refresh to a Drupal Theme"
url: "https://drupalize.me/tutorial/add-webpack-and-react-fast-refresh-drupal-theme?p=2798"
guide: "[[decoupled-headless-drupal]]"
order: 34
---

# Add Webpack and React Fast Refresh to a Drupal Theme

## Videos

- [Video](https://drupalize.me/sites/default/files/tutorials/webpack-hmr-demo.mp4)

## Content

React Fast Refresh (formerly Hot Module Replacement) is a technique for using Webpack to update the code that your browser renders without requiring a page refresh. With fast refresh configured it's possible to edit your JavaScript (and CSS) files in your IDE and have the browser update the page without requiring a refresh, allowing you to effectively see the results of your changes in near real time. If you're editing JavaScript or CSS it's amazing. And, it's one of the reasons people love the developer experience of working with React so much.

If you're writing React code as part of a Drupal theme it's possible configure fast refresh to work with Drupal. Doing so will allow live reloading of any JavaScript and CSS processed by Webpack.

In this tutorial we'll:

- Walk through configuring Webpack and fast refresh for a Drupal theme
- Add an `npm run start:hmr` command that will start the *webpack-dev-server* in *hot* mode
- Configure the *webpack-dev-server* to proxy requests to Drupal so we can view our normal Drupal pages

By the end of this tutorial you should know how to configure Webpack to allow the use of React's fast refresh feature to your Drupal theme and preview changes to your React code in real time.

## Goal

Configure Webpack and React Fast Refresh for use with a Drupal theme.

## Prerequisites

- [Connect React to a Drupal Theme or Module](https://drupalize.me/tutorial/connect-react-drupal-theme-or-module)

## Fast refresh

There's a detailed technical explanation of what Fast Refresh is, and how it works in [What the heck is React Fast Refresh](https://mariosfakiolas.com/blog/what-the-heck-is-react-fast-refresh/).

Our implementation consists of the following components:

- [webpack-dev-server](https://github.com/webpack/webpack-dev-server) to create a development server that can handle the requirements of fast refresh. Standard Apache for example can not.
- [@pmmmwh/react-refresh-webpack-plugin](https://github.com/pmmmwh/react-refresh-webpack-plugin) to integrate `webpack-dev-server` with `react-refresh` and our React code.

**Note:** We used to recommend using [react-hot-loader](https://github.com/gaearon/react-hot-loader) to integrate Webpack's HMR features with React however that plugin is deprecated and no longer supported for React 18. The ecosystem continues to evolve, and it's good to be aware of Hot Module Replacement (HMR) as it's still frequently used to accomplish this same thing.

## Add Webpack HMR to a Drupal theme

These steps assume that you've setup and configured Webpack using the guidelines in [Connect React to a Drupal Theme or Module](https://drupalize.me/tutorial/connect-react-drupal-theme-or-module).

### Install the required modules

Install `webpack-dev-server`, `react-refresh`, and `@pmmmwh/react-refresh-webpack-plugin`.

From the root directory of your Drupal theme run:

```
npm install --save-dev webpack-dev-server
npm install --save-dev @pmmmwh/react-refresh-webpack-plugin react-refresh
```

### Update webpack.config.js

Edit the *webpack.config.js* file, here's the final version, we'll explain the changes in detail below:

```
const path = require('path');
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');
const isDevMode = process.env.NODE_ENV !== 'production';

const PROXY = 'https://react-tutorials-2.ddev.site/';
const PUBLIC_PATH = '/themes/react_example_theme/js/dist_dev/';

const config = {
  entry: {
    main: [
      "./js/src/index.jsx"
    ]
  },
  devtool: (isDevMode) ? 'source-map' : false,
  mode: (isDevMode) ? 'development' : 'production',
  output: {
    path: isDevMode ? path.resolve(__dirname, "js/dist_dev") : path.resolve(__dirname, "js/dist"),
    filename: '[name].min.js',
    publicPath: PUBLIC_PATH
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        include: path.join(__dirname, 'js/src'),
        options: {
          // This is a feature of `babel-loader` for webpack (not Babel itself).
          // It enables caching results in ./node_modules/.cache/babel-loader/
          // directory for faster rebuilds.
          cacheDirectory: true,
          plugins: [
            isDevMode && require.resolve('react-refresh/babel')
          ].filter(Boolean),
        },
      }
    ],
  },
  plugins: [
    isDevMode && new ReactRefreshWebpackPlugin(),
  ].filter(Boolean),
  devServer: {
    port: 8181,
    hot: true,
    headers: { 'Access-Control-Allow-Origin': '*' },
    devMiddleware: {
      writeToDisk: true,
    },
    // Settings for http-proxy-middleware.
    proxy: [
      {
        index: '',
        context: ['/'],
        target: PROXY,
        publicPath: PUBLIC_PATH,
        secure: false,
        // These settings allow Drupal authentication to work, so you can sign
        // in to your Drupal site via the proxy. They require some corresponding
        // configuration in Drupal's settings.php.
        changeOrigin: true,
        xfwd: true
      }
    ]
  },
};

module.exports = config;
```

In comparison to the *webpack.config.js* from [Connect React to a Drupal Theme or Module](https://drupalize.me/tutorial/connect-react-drupal-theme-or-module) here are the things we've modified:

- Added `const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');`
- Use a [Webpack resolver alias](https://webpack.js.org/configuration/resolve/#resolvealias) to replace instances of `react-dom` with `@hot-loader/react-dom` to enable support for React hooks.
- Change the `babel-loader` configuration, and tell it to enable caching, and to use the `ReactRefreshWebpackPlugin` babel plugin when in development mode.
- Include `ReactRefreshWebpackPlugin` as a `plugin` in development mode.
- Add the `devServer` configuration for `webpack-dev-server`. [Configuration options](https://webpack.js.org/configuration/dev-server/).

**Note:** Unlike HMR which required using the `hot()` function, React Fast Refresh does not require any modifications to your applications code to work.

### Tell webpack-dev-server to proxy requests to Drupal

For HMR to work we need to view the pages of our site through the lens of the webpack-dev server. However, in this scenario we only want webpack-dev-server to serve the JavaScript files that are processed by Webpack. And for everything else to come from Drupal.

You request `/node/42` from the webpack-dev-server it needs to be able to recognize that this is a request it's not configured to handle, and instead pass the request to Drupal. Drupal can then process the request, and pass the resulting HTML page back to webpack-dev-server, which in turn passes it back to your browser.

The resulting page includes tags like `<img>`, `<link>`, and `<script>` that instruct your browser to retrieve additional resources. Like this:

```
<script src="/themes/react_example_theme/js/dist_dev/main.min.js?v=8.8.2"></script>
```

So the browser requests that file from webpack-dev-server. The dev server recognizes this as file that it is responsible for, and instead of proxying the request to Drupal it returns the version it has.

In the end it'll look just like you're browsing your normal Drupal site, but some of the files will actually be coming from *webpack-dev-server*.

Change the following variables in your *webpack.config.js*:

```
// The base path of your Drupal development server. This is what you would
// normally navigate to in your browser when working on the site.
const PROXY = 'https://react-tutorials-2.ddev.site/';
// The absolute path to the directory, relative to the PROXY path above, to the
// directory that contains the files that you want webpack-dev-server to NOT
// pass on to Drupal.
// For example, if your .js file is normally accessed via http://a.com/src/script.js
// and you want webpack-dev-server to handle all the .js files in the src
// directory set this to '/src/'.
const PUBLIC_PATH = '/themes/react_example_theme/js/dist_dev/';
```

Behind the scenes this uses the powerful [http-proxy-middleware](https://github.com/chimurai/http-proxy-middleware). And you can find [more options in its documentation](https://github.com/chimurai/http-proxy-middleware#options). In our testing we've used DDEV-local for hosting our Drupal development site, you may need to change the settings a bit depending on the specifics of your development environment.

### Configure Drupal to accept requests from the proxy

Edit your Drupal site's *settings.php*, or *settings.local.php* file and add the following options:

```
$settings['reverse_proxy'] = TRUE;
$settings['reverse_proxy_addresses'] = array($_SERVER['REMOTE_ADDR']);
```

### Add a helper script to start the development server

Update your *package.json* file to include a helper script for starting the *webpack-dev-server*. The command to do so is: `webpack-dev-server --hot --progress --colors`. The final *package.json* with all the necessary packages and changes looks like the following. Exact package versions will vary:

```
{
  "name": "react_example_theme",
  "version": "1.0.0",
  "description": "",
  "main": "js/src/index.jsx",
  "scripts": {
    "build": "NODE_ENV=production webpack --mode=production",
    "build:dev": "webpack",
    "start": "webpack --watch",
    "start:hmr": "webpack-dev-server --hot --progress --color"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/core": "^7.23.9",
    "@babel/preset-env": "^7.23.9",
    "@babel/preset-react": "^7.23.3",
    "@pmmmwh/react-refresh-webpack-plugin": "^0.5.11",
    "babel-loader": "^9.1.3",
    "react-refresh": "^0.14.0",
    "webpack": "^5.90.1",
    "webpack-cli": "^5.1.4",
    "webpack-dev-server": "^4.15.1"
  },
  "dependencies": {
    "prop-types": "^15.8.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

### Start the development server and test it out

From the root directory of your theme, where the *package.json* file is run:

```
npm run start:hmr
```

This will output something like the following:

```
> [email protected] start:hmr
> webpack-dev-server --hot --progress --color

<i> [webpack-dev-server] [HPM] Proxy created: /  -> https://react-tutorials-2.ddev.site/
<i> [webpack-dev-server] Project is running at:
<i> [webpack-dev-server] Loopback: http://localhost:8181/
<i> [webpack-dev-server] On Your Network (IPv4): http://192.168.1.220:8181/
<i> [webpack-dev-server] On Your Network (IPv6): http://[fe80::1]:8181/
```

In which you can see that the development server is now accessible at `http://localhost:8181`. If you visit the address you should see your Drupal site.

If you make changes to any of the React code in your theme those changes should update on the site in near real time.

Example of live updates in a Drupal theme:

[

Your browser does not support HTML5 video. You can [download the video to watch it.](https://drupalize.me/sites/default/files/tutorials/webpack-hmr-demo.mp4)
](https://drupalize.me/sites/default/files/tutorials/webpack-hmr-demo.mp4)

## Recap

In this tutorial we learned how to perform live reloading of changes to our React code without requiring a page refresh. We configured Webpack, and the `webpack-dev-server` to use React Fast Refresh (`react-refresh`). Then we set things up so our Webpack development server can proxy requests to our Drupal development environment, and we can see changes to our Drupal theme's JavaScript in near real time.

## Further your understanding

- Can you update your Webpack toolchain to compile Sass/SCSS files and perform hot reloading of those?
- You still need to build the final production assets using `npm run build` when using this approach. Why?

## Additional resources

- [webpack-dev-server documentation](https://webpack.js.org/configuration/dev-server/) (webpack.js.org)
- [@pmmmwh/react-refresh-webpack-plugin documentation](https://github.com/pmmmwh/react-refresh-webpack-plugin) (github.com)
- [An example showing HMR for CSS in a Drupal theme](https://github.com/csymlstd/drupal-8-webpack-hmr) (github.com)

Downloads

[webpack-hmr-demo.mp4](/sites/default/files/tutorials/webpack-hmr-demo.mp4)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a React Component](/tutorial/create-react-component?p=2798)

Next
[Retrieve Data from an API with React](/tutorial/retrieve-data-api-react?p=2798)

Clear History

Ask Drupalize.Me AI

close