---
title: "Use Vite to Start a Decoupled React Application"
url: "https://drupalize.me/tutorial/use-vite-start-decoupled-react-application?p=2798"
guide: "[[decoupled-headless-drupal]]"
---

# Use Vite to Start a Decoupled React Application

## Content

Using [Vite](https://vite.dev/) we can scaffold a stand-alone React application with modern tooling, instant dev-server startup, and hot module replacement. It's a great way to get started with React and works perfectly for decoupled apps that talk to Drupal's JSON:API. After creating the scaffold, we'll port code from previous tutorials to the new structure.

In this tutorial we'll:

- Use **Vite** to scaffold a new React project
- Refactor existing code into Vite's project structure
- Confirm that our code runs

By the end of this tutorial, you'll know what Vite is and how to get started using it for a decoupled React app.

## Goal

Use **Vite** to set up a boilerplate React application with hot reloading and build tools already configured.

## Prerequisites

- **Node.js 18+** installed (we recommend `nvm`). See [Install Node.js Locally with Node Version Manager (nvm)](https://heynode.com/tutorial/install-nodejs-locally-nvm).
- Drupal installed, with some *article* nodes created, [JSON:API module installed and enabled](https://drupalize.me/tutorial/install-jsonapi-module), and [configured to allow CORS](https://drupalize.me/tutorial/access-api-browser-cross-origin-resource-sharing). (In recent Drupal versions, JSON:API is included in core but may not be enabled by default.)

## What is Vite?

[Vite](https://vite.dev/) is a fast, modern build tool and dev server. It uses native ES modules in development for instant startup and bundles for production using [Rollup](https://rollupjs.org/). You get a boilerplate React project with hot reloading, a minimal configuration surface, and first-class TypeScript support—all without the legacy overhead of older toolchains.

If you're familiar with Drush's `generate` commands for scaffolding a module/theme, Vite plays a similar role for front-end apps.

You can also use other frameworks (Next.js, Remix, etc.). For a simple Single Page Application (SPA) talking to Drupal's JSON:API, Vite + React is an excellent default.

## Overview

Our goal is to focus on integrating a fully decoupled React application with Drupal. We'll reuse code from earlier tutorials and run it as a separate app.

We're going to:

- Use **Vite** to start a new React project
- Migrate our components from the Drupal theme into the new app
- Run the hot-reloading dev server
- Create a production build (and preview it locally)

### Scaffold a project with Vite

- In a terminal, navigate to where your React application should live, e.g. `cd ~/Sites/decoupled-drupal`.
- Run the Vite scaffolder and choose **React** (TypeScript optional) following the prompts.

  ```
  npm create vite@latest react-decoupled
  ```

  This will create a new directory, *react-decoupled/* with a Vite application inside.
- Finish the installation.

  ```
  cd react-decoupled/
  npm install
  npm run dev
  ```

When finished, a browser window should open at the dev URL with your React app. Try editing `src/App.jsx`--the page should update instantly via hot module replacement (HMR).

### Get the example code

If you're just starting the project now you can grab the completed [example code from previous tutorials here](https://github.com/DrupalizeMe/react-and-drupal-examples/tree/master/drupal/web/themes/react_example_theme).

If you've been following along and already wrote an example application inside a Drupal theme or module, copy your *js/src/components* and *js/src/utils* folders into the new app's *src/* directory. Or, create an empty *src/components/* directory. This is where your custom React components will live.

### Update src/App.jsx (and *src/main.jsx* if using routes)

Edit the *src/App.jsx* created by Vite, and render your `NodeReadWrite` component (or your own component).

```
import React from 'react';
import './App.css';
import NodeReadWrite from './components/NodeReadWrite';

export default function App() {
  return <NodeReadWrite />;
}
```

### Run the dev server

Use Vite's dev server while building features:

```
npm run dev
```

You should now see your app, but it may not yet be able to `GET` or `POST` data to Drupal. Because the app is fully decoupled (served from a different origin), you will need proper **CORS** settings and **OAuth** tokens for mutating requests.

When making a `GET` request to Drupal you might see an error like:

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://drupal.ddev.site/jsonapi/node/article?... (Reason: CORS header 'Access-Control-Allow-Origin' missing).
```

Additionally, `POST` requests will fail with authorization errors until you add OAuth to your requests. See the [OAuth tutorial in this course](https://drupalize.me/tutorial/make-api-requests-oauth) for the Authorization Code + PKCE flow and the `fetchWithAuthentication()` wrapper.

At this point your application should load, but cross-origin requests and authenticated writes may still be blocked. Configure **CORS** and set up **OAuth** by following along with the following tutorials in this course:

- [Make API Requests with OAuth](https://drupalize.me/tutorial/make-api-requests-oauth)
- [Use Fetch and OAuth to Make Authenticated Requests](https://drupalize.me/tutorial/use-fetch-and-oauth-make-authenticated-requests)

## Recap

In this tutorial we used **Vite** to scaffold a new React application, moved our existing components into it, and ran the dev server to confirm everything "works", with the caveat that authenticated requests still require the OAuth setup (see next two tutorials).

## Further your understanding

- Explore Vite's project files: what does *index.html* do, and how does *src/main.jsx* mount your app?
- Try the TypeScript variant when scaffolding (`React + TypeScript`).
- Add ESLint, Prettier, or Tailwind--Vite plays nicely with them.

## Additional resources

- [Vite Official Docs](https://vite.dev/guide/) (<https://vite.dev/>)
- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react) (github.com)
- [Rollup](https://rollupjs.org/) (Vite's production bundler) (rollupjs.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Fully Decoupled React Application](/tutorial/create-fully-decoupled-react-application?p=2798)

Next
[Use create-react-app to Start a Decoupled React Application](/tutorial/use-create-react-app-start-decoupled-react-application?p=2798)

Clear History

Ask Drupalize.Me AI

close