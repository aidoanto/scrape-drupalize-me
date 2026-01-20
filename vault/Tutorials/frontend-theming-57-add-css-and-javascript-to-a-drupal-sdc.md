---
title: "Add CSS and JavaScript to a Drupal SDC"
url: "https://drupalize.me/tutorial/add-css-and-javascript-drupal-sdc?p=3329"
guide: "[[frontend-theming]]"
order: 57
---

# Add CSS and JavaScript to a Drupal SDC

## Content

One of the benefits of using Drupal single directory components is that Drupal automatically builds and attaches an asset library whenever it is used. Adding CSS styles and JavaScript interactivity to a *single directory component (SDC)* is as simple as dropping *component-name.css* and *component-name.js* files into the root directory of the component. Drupal detects these files, creates an [asset library](https://drupalize.me/tutorial/define-asset-library), and [attaches it](https://drupalize.me/tutorial/attach-asset-library) when the component is rendered. This means when you want to add additional CSS or JavaScript assets, you will **override** the asset library created for your component instead of defining a new one.

In this tutorial, we will:

- Add component-scoped CSS and JavaScript files.
- Learn how to override a component's existing asset library to add additional assets.
- Discuss how to integrate common front-end asset build tools (Gulp, Webpack, Vite, etc.) while working with Drupal single directory components.

By the end of this tutorial, you'll be able to attach CSS and JavaScript assets to an SDC and validate that they load only when the component is in use.

## Goal

Attach CSS and JavaScript assets to a card component to give it style and interactivity.

## Prerequisites

We’ll be expanding the card component created in [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc) and [Add a Twig template to your Single Directory Component](https://drupalize.me/tutorial/add-twig-template-your-single-directory-component). If you’re following along, complete those first. Or, use this tutorial to learn how to add CSS and JavaScript to any component.

## Add CSS and JavaScript to an SDC

If a file with the **exact same basename** as the SDC, and an extension of *.css* or *.js*, lives in the component directory, Drupal will:

- **Build a library** using those files. You can include only a *.css*, only a *.js*, or both.
- **Attach that library** only when the component renders.

### Create a *card.css* file

Inside your card component directory, create the file, *card.css*.

```
my_theme_or_module/
└── components/
    └── card/
        ├── card.component.yml
        ├── card.css
        └── card.twig
```

Populate *components/card/card.css* with the following content:

```
/* card.css */
.card {
  position: relative;
  width: 300px;
  margin: 2rem;
  perspective: 1200px;
}

/* COUNT BADGE */
.card .card-count {
  background: #ff00cc;
  border-bottom: 4px solid #111111;
  box-shadow: -4px 4px 0 0 #111111;
  color: #fafafa;
  font-size: 0.875rem;
  font-weight: 800;
  padding: 0.25rem 0.5rem;
  position: absolute;
  right: 0;
  top: 0;
  z-index: 3;
}

.card .card-inner {
  display: grid;
  grid-template-areas: "face";
  grid-template-columns: 1fr;
  grid-template-rows: auto;
  transform-style: preserve-3d;
  transition: transform 0.8s cubic-bezier(.4,.2,.2,1);
  width: 100%;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card .card-front,
.card .card-back {
  grid-area: face;
  backface-visibility: hidden;
  background: #fafafa;
  border: 6px solid #111111;
  box-shadow: 6px 6px 0 0 #111111;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 1rem;
}

/* META BAR */
.card .card-meta {
  border-bottom: 2px solid #111111;
  display: flex;
  font-size: 0.875rem;
  gap: 1rem;
  justify-content: space-between;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
}

.card .card-author,
.card .card-date {
  font-weight: 700;
}

/* TITLES & TEXT */
.card .card-title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  line-height: 1.75rem;
  margin: 0.75rem 0;
}

.card .card-content {
  flex-grow: 1;
  line-height: 1.4;
  padding: 0 1rem;
}

/* BACK SIDE */
.card .card-back {
  background: #ffdd00;
  transform: rotateY(180deg);
}

/* FLIP BUTTON */
.card .flip-button {
  align-self: flex-end;
  background: #00ccff;
  border: 4px solid #111111;
  box-shadow: 6px 6px 0 0 #111111;
  cursor: pointer;
  font-weight: 700;
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  text-transform: uppercase;
}

.card .flip-button:hover {
  background: #ff00cc;
  color: #fafafa;
}
```

**Tip:** Scope your CSS to the component by giving the wrapper a unique class.

### Add a *card.js* file

Inside your card component directory, create the *card.js* file.

Example *components/card/card.js*:

```
(function (Drupal) {
  Drupal.behaviors.cardFlip = {
    attach(context) {
      // Simple first pass: no `once()` yet.
      context.querySelectorAll('.card .flip-button').forEach((button) => {
        button.addEventListener('click', () => {
          const card = button.closest('.card');
          if (card) {
            card.classList.toggle('flipped');
          }
        });
      });
    }
  };
})(Drupal);
```

**Tip:** When working with JavaScript, use the `Drupal.behaviors` pattern so your code re-runs when Drupal attaches behaviors. Learn more in [Load JavaScript in Drupal with Drupal.behaviors](https://drupalize.me/tutorial/load-javascript-drupal-drupalbehaviors). In this first example we’re keeping it simple and **not** using `once()`. In the next section, we’ll refactor to use `once()` and demonstrate how to add the `core/once` dependency to our component's asset library.

### Clear the cache

Clear the cache so Drupal can discover your new files. Then reload any page that displays your component, and it should now include the CSS and JavaScript you added.

## Override a component asset library

Sometimes you need finer control over the asset library that gets created. Maybe you need to add JavaScript dependencies, split CSS by media, or point to pre-built assets. You can override the automatically generated library by adding a `libraryOverrides` key in the *.component.yml* file. We need to use `libraryOverrides` because Drupal auto-creates an asset library for your component. We're not creating a new library—we're overriding the one that Drupal automatically generates for this component.

When you declare a top-level key under `libraryOverrides`—such as `css`, `js`, or `dependencies`—Drupal replaces that part of the auto-generated library with what you specify. You must list every file or dependency you want included **for that key**, including those that were previously auto-attached. Keys you don’t override will still be generated automatically.

### Update *card.component.yml* to list all assets

Add a `libraryOverrides` section to the end of *card.component.yml*:

```
# card.component.yml (excerpt)
name: card
...
libraryOverrides:
  dependencies:
    - core/once
```

The keys we didn't override (`css` and `js`) continue to work exactly as before—Drupal still auto-detects and attaches *card.css* and *card.js*. If we had overridden either the `css` or `js` keys, we would need to list the auto-attached files as well. **Once you override a key, you are responsible for all assets for that key.** See also [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc) for a code example of that scenario.

### Refactor the behavior to use `once()`

Now that we’ve declared `core/once` as a dependency, refactor the behavior to avoid duplicate event bindings when the component is re-attached via AJAX/BigPipe.

Update *card.js* with the following code:

```
(function (Drupal, once) {
  Drupal.behaviors.cardFlip = {
    attach(context) {
      once('cardFlip', '.card .flip-button', context).forEach((button) => {
        button.addEventListener('click', () => {
          const card = button.closest('.card');
          if (card) {
            card.classList.toggle('flipped');
          }
        });
      });
    }
  };
})(Drupal, once);
```

### Clear the cache

Rebuild caches, since we've updated the *card.component.yml*. Then reload any page that displays your component, and it should now include the refactored code and new dependency.

```
drush cr
```

### Test that all asset files are embedded in HTML

Let's test out that all our asset files are embedded as expected.

1. Turn off CSS and JavaScript aggregation. Go to *Configuration* > *Performance* > *Bandwidth optimization* (*/admin/config/development/performance*) and ensure that both *Aggregate CSS files* and *Aggregate JavaScript files* are unchecked.
2. View source and search for your dependencies. You may need to first locate the asset definition in the asset provider's *\*.libraries.yml* file (e.g. *core/core.libraries.yml*) to identify the filename and path. In this example, you should see the following files embedded in the HTML:

- `core/once`: */core/assets/vendor/once/once.min.js*
- `neo_brutalism:card` CSS: */core/../themes/custom/neo\_brutalism/components/card/card.css*
- `neo_brutalism:card` JavaScript: */core/../themes/custom/neo\_brutalism/components/card/card.js*

Image

![HTML source showing embedded component CSS file](../assets/images/add-css-js--view-source-card-css.png)

Image

![HTML source showing embedded component JavaScript file](../assets/images/add-css-js--view-source-card-js.png)

Because we only overrode `dependencies`, the card component's CSS and JavaScript assets remain auto-attached by Drupal core. That's why the paths to those files start with `/core/..`. If we had overridden `css` or `js` keys under `libraryOverrides`, we would list all asset files including those previously auto-attached, and the paths to those files would no longer start with `/core/..`.

## Quick checks if assets don’t load

- Do your component's file names match `{component}.css` and `{component}.js` in the component directory?
- If you added `css` or `js` keys under `libraryOverrides`, did you list all assets, even ones that were auto-attached? (See also [Add a Component YAML File for a Drupal SDC](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc).)
- Did you clear caches after adding or renaming files (`drush cr`)?

## Using front-end build tools

Modern projects often compile SCSS, TypeScript, or ES modules. This works with Drupal single directory components, too. As long as the **output files** are named *{component}.css* and *{component}.js* and land in the correct component directory, Drupal’s automatic library generation still works—regardless of which build tool you use.

**Example directory layout** for a custom theme that uses build tools like Gulp or Webpack:

```
my_theme/
└── components/
    └── card/
        ├── card.twig
        ├── card.component.yml
        ├── card.scss    # source
        ├── card.ts      # source
        ├── card.css     # compiled by build tool
        └── card.js      # compiled by build tool
├── gulpfile.js / webpack.config.js / vite.config.js
└── my_theme.info.yml
```

Below are a couple examples of configuring common build tools to work with SDCs. These configurations assume the tools are installed, and run, from the root directory of a custom theme. And are intended to serve as examples (not final working configuration) for how you can set this up for your projects.

### Use Gulp to compile SDC assets

Install Gulp and Sass to compile a *card/card.scss* file to *card/card.css*.

```
npm install --save-dev gulp gulp-sass sass
```

Example configuration in *gulpfile.js*:

```
// gulpfile.js
'use strict';

const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));

function buildStyles() {
  // Grab every .scss file directly inside a component directory and compile it
  // to a .css file in the same location as the .scss file.
  return gulp.src('components/**/*.scss', { sourcemaps: true })
    .pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
    .pipe(gulp.dest('./components', { sourcemaps: '.' }));
};

exports.buildStyles = buildStyles;
exports.watch = function () {
  gulp.watch('./components/**/*.scss', buildStyles);
};
```

Use it:

```
gulp watch
# Or ...
gulp buildStyles
```

### Use Webpack to compile SDC assets

This example uses Webpack to compile both a *card.scss* Sass file, and a *card.ts* TypeScript file.

Install the necessary tools:

```
npm install --save-dev webpack webpack-cli glob mini-css-extract-plugin css-loader sass-loader sass ts-loader typescript
```

Example *webpack.config.js* configuration file:

```
// webpack.config.js
import path from 'path';
import { glob } from 'glob';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';

// Build an object like { card: './components/card/card.ts', banner: './components/banner/banner.ts' }
const entries = Object.fromEntries(
  glob.sync('components/*/*.ts').map((file) => {
    const name = path.basename(path.dirname(file));
    return [name, `./${file}`];
  })
);

export default {
  mode: process.env.NODE_ENV === 'development' ? 'development' : 'production',
  context: path.resolve('.', ''), // theme root
  entry: entries,
  output: {
    filename: 'components/[name]/[name].js',
    path: path.resolve('.', ''), // theme root
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
      },
      {
        test: /\.ts$/,
        use: 'ts-loader',
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: 'components/[name]/[name].css' }),
  ],
  resolve: { extensions: ['.ts', '.js'] },
};
```

Use it:

```
./node_modules/.bin/webpack-cli
```

Here are a few things to keep in mind when configuring your build tool of choice:

- Make sure the output directory mirrors the source *components/* directory.
- Output filenames need to match the component basename. e.g. *card/card.scss* outputs to *card/card.css*
- Clear Drupal caches after the first build so any new files are detected.

## Recap

In this tutorial, you learned that you can include CSS and JavaScript assets in a Drupal single directory component by ensuring the *.css* and *.js* files follow the *{component}.css* naming convention. If you do so, Drupal will find and include them when the component is rendered. We also looked at ways to override the automatically generated asset library if you need more control over dependencies or which files are included. Finally, we walked through examples of configuring common front-end build tools to work with Drupal SDCs.

## Further your understanding

- What build tool(s) do you like to use with your projects? How would you configure them to work with SDCs in a custom theme?
- How would you approach using CSS variables to, for example, share a color palette between components in a theme?

## Additional resources

- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Overview: JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal) (Drupalize.Me)
- [Single Directory Components documentation](https://www.drupal.org/docs/develop/theming-drupal/using-single-directory-components) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Twig Template to Your Single Directory Component](/tutorial/add-twig-template-your-single-directory-component?p=3329)

Next
[Use a Component in a Module via Render Arrays](/tutorial/use-component-module-render-arrays?p=3329)

Clear History

Ask Drupalize.Me AI

close