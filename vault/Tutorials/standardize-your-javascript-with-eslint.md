---
title: "Standardize Your JavaScript with ESLint"
url: "https://drupalize.me/tutorial/standardize-your-javascript-eslint?p=2883"
guide: "[[integrate-javascript-drupal]]"
---

# Standardize Your JavaScript with ESLint

## Content

ESLint is the linting tool of choice for JavaScript in Drupal. In this tutorial we’ll show how to install the ESLint application and then use it to verify that your JavaScript files are meeting the Drupal coding standards.

Drupal (as of version 8.4) has adopted the Airbnb JavaScript coding standards. In this tutorial, we'll walk through how to install the necessary package dependencies to run eslint on JavaScript files within your Drupal site.

## Goal

Install the ESLint application to verify your custom JavaScript files are meeting the Drupal coding standards.

## Prerequisites

- [Command line basics](https://drupalize.me/series/command-line-basics-series)
- Node.js - Ensure that you are using at least the latest long-term support (LTS) release of Node.js, which is available at the [Node.js downloads page](https://nodejs.org/en/download/). Alternatively, you can [install Node.js via a package manager on many OS platforms](https://nodejs.org/en/download/package-manager/).
- Yarn - The Drupal JavaScript developer community recommends Yarn (over NPM) for managing dependencies. To install Yarn, either:
  - Follow the installation instructions from the Yarn website, or
  - Install Yarn using NPM: `npm install -g yarn`

Source: [JavaScript Developer tools for Drupal core](https://www.drupal.org/node/2996785)

## What is linting?

Before we dive into installing ESLint, you may find yourself asking, "Self, what is linting anyway?" [ESLint](http://eslint.org/docs/about/) provides us with an answer:

> Code linting is a type of static analysis that is frequently used to find problematic patterns or code that doesn’t adhere to certain style guidelines. There are code linters for most programming languages, and compilers sometimes incorporate linting into the compilation process.

[Drupal.org](https://www.drupal.org/node/1955232)'s definition is a bit more simple and straightforward:

> ESLint is a tool to detect errors and potential problems in JavaScript code.

Another way of looking at it is that ESLint helps ensure your custom JavaScript meets [Drupal's JavaScript coding standards](https://www.drupal.org/node/172169).

## Install ESLint

With Node.js and Yarn installed (see Prerequisites section), install package dependencies from the root of your Drupal installation:

`cd core && yarn install`

With these packages installed, you're ready to start using it to test JavaScript on your Drupal site. This is because Drupal core already ships with the configuration files ESLint uses to define coding standards for the project. This configuration is defined in a few files: in the root directory of your Drupal site you'll notice *.eslintrc.json* and *.eslintignore* files. *.eslintrc.json* tells ESLint to also include *core/.eslintrc.json*, which exends `airbnb` and `plugin:prettier/recommended`. Let's take a look at \_core/.eslintrc.json.

*core/.eslintrc.json*:

```
{
  "extends": [
    "airbnb",
    "plugin:prettier/recommended"
  ],
  "root": true,
  "env": {
    "browser": true,
    "es6": true,
    "node": true
  },
  "globals": {
    "Drupal": true,
    "drupalSettings": true,
    "drupalTranslations": true,
    "domready": true,
    "jQuery": true,
    "_": true,
    "matchMedia": true,
    "Backbone": true,
    "Modernizr": true,
    "CKEDITOR": true
  },
  "rules": {
    "prettier/prettier": "error",
    "consistent-return": ["off"],
    "no-underscore-dangle": ["off"],
    "max-nested-callbacks": ["warn", 3],
    "import/no-mutable-exports": ["warn"],
    "no-plusplus": ["warn", {
      "allowForLoopAfterthoughts": true
    }],
    "no-param-reassign": ["off"],
    "no-prototype-builtins": ["off"],
    "valid-jsdoc": ["warn", {
      "prefer": {
        "returns": "return",
        "property": "prop"
      },
      "requireReturn": false
    }],
    "no-unused-vars": ["warn"],
    "operator-linebreak": ["error", "after", { "overrides": { "?": "ignore", ":": "ignore" } }]
  }
}
```

## Test custom code with ESLint

The custom JavaScript we'll evaluate in this tutorial is the `friendly-greeting` asset library we worked with in [Use Drupal.theme for HTML Markup in JavaScript](https://drupalize.me/tutorial/use-drupaltheme-html-markup-javascript).

As a refresher, here is the current contents of the *themes/custom/friendly/js/friendly-greeting.js* file:

```
(function (Drupal) {
  // Override the default implementation of Drupal.theme.placeholder with our
  // own custom one.
  Drupal.theme.placeholder = function (str) {
    return '<em class="friendly-placeholder">' + Drupal.checkPlain(str) + '</em>';
  };

  // If we have a nice user name, let's replace the
  // site name with a greeting.
  if (drupalSettings.friendly.name) {
    var siteName = document.getElementsByClassName('site-branding__name')[0];
    siteName.getElementsByTagName('a')[0].innerHTML = '<h1>Howdy, ' + Drupal.theme('placeholder', drupalSettings.friendly.name) + '!</h1>';
  }

})(Drupal);
```

Run ESLint on *friendly-greeting.js* from the root of your Drupal site, like so:

```
$ core/node_modules/.bin/eslint themes/custom/friendly/js/friendly-greeting.js
```

ESLint discovers the following 13 problems (11 errors, 2 warnings) in the current state of *friendly-greeting.js*:

```
/Library/WebServer/Documents/drupal-project-sandbox/some-dir/web/themes/custom/friendly/js/friendly-greeting.js
   1:2   warning  Unexpected unnamed function                                                                                                                                                                                                                           func-names
   1:10  error    Delete `·`                                                                                                                                                                                                                                            prettier/prettier
   4:30  warning  Unexpected unnamed function                                                                                                                                                                                                                           func-names
   4:38  error    Delete `·`                                                                                                                                                                                                                                            prettier/prettier
   5:11  error    Replace `·'<em·class="friendly-placeholder">'·+·Drupal.checkPlain(str)·+·'</em>'` with `·(⏎······'<em·class="friendly-placeholder">'·+·Drupal.checkPlain(str)·+·"</em>"⏎····)`                                                                        prettier/prettier
   5:12  error    Unexpected string concatenation                                                                                                                                                                                                                       prefer-template
  11:5   error    All 'var' declarations must be at the top of the function scope                                                                                                                                                                                       vars-on-top
  11:5   error    Unexpected var, use let or const instead                                                                                                                                                                                                              no-var
  11:52  error    Replace `'site-branding__name'` with `"site-branding__name"`                                                                                                                                                                                          prettier/prettier
  12:35  error    Replace `'a')[0].innerHTML·=·'<h1>Howdy,·'·+·Drupal.theme('placeholder',·drupalSettings.friendly.name)·+·'!</h1>'` with `"a")[0].innerHTML·=⏎······"<h1>Howdy,·"·+⏎······Drupal.theme("placeholder",·drupalSettings.friendly.name)·+⏎······"!</h1>"`  prettier/prettier
  12:55  error    Unexpected string concatenation                                                                                                                                                                                                                       prefer-template
  13:4   error    Delete `⏎`                                                                                                                                                                                                                                            prettier/prettier
  15:12  error    Insert `⏎`                                                                                                                                                                                                                                            prettier/prettier

✖ 13 problems (11 errors, 2 warnings)
  10 errors, 0 warnings potentially fixable with the `--fix` option.
```

Thankfully, these are all easy problems to fix and are potentially fixable if we run the command again with the `--fix` option.

```
$ core/node_modules/.bin/eslint themes/custom/friendly/js/friendly-greeting.js --fix

/L/W/D/d/project/web/themes/custom/friendly/js/friendly-greeting.js
  1:2   warning  Unexpected unnamed function  func-names
  4:30  warning  Unexpected unnamed function  func-names

✖ 2 problems (0 errors, 2 warnings)
```

After fixing these errors (and ignoring the warnings), our *friendly-greeting.js* file now looks like this:

```
(function(Drupal) {
  // Override the default implementation of Drupal.theme.placeholder with our
  // own custom one.
  Drupal.theme.placeholder = function(str) {
    return `<em class="friendly-placeholder">${Drupal.checkPlain(str)}</em>`;
  };

  // If we have a nice user name, let's replace the
  // site name with a greeting.
  if (drupalSettings.friendly.name) {
    const siteName = document.getElementsByClassName("site-branding__name")[0];
    siteName.getElementsByTagName(
      "a"
    )[0].innerHTML = `<h1>Howdy, ${Drupal.theme(
      "placeholder",
      drupalSettings.friendly.name
    )}!</h1>`;
  }
})(Drupal);
```

And if we run ESLint on this file again we should see it return error-free (but still with 2 warnings).

## Recap

In this tutorial we learned how to install and use ESLint to check for code linting errors and warnings.

## Further your understanding

If you'd like, you can read all about the ESLint configuration options on the [ESLint.org site](http://eslint.org/docs/rules/).

- Explain what ESLint is
- Install ESLint and confirm that it’s available
- Use ESLint to test JavaScript files in your theme
- Add ESLint to your favorite front-end task runner (gulp, grunt, npm scripts, etc)

## Additional resources

- [JavaScript Developer tools for Drupal core](https://www.drupal.org/node/2996785) (Drupal.org)
- [JavaScript Coding Standards](https://www.drupal.org/node/172169) (Drupal.org)
- [ESLint settings](https://www.drupal.org/node/1955232) (Drupal.org)
- Change record: [Adopt airbnb JavaScript style guide v14.1 as new baseline JavaScript coding standards for Drupal 8 core and contrib](https://www.drupal.org/node/2873849) (Drupal.org)
- [Eslint with Airbnb style (eslint-config-airbnb-bundle)](https://www.npmjs.com/package/eslint-config-airbnb-bundle) (npmjs.org)
- [Installing Node.js and npm](https://docs.npmjs.com/getting-started/installing-node) (docs.npmjs.com)
- [ESLint documentation](http://eslint.org/) (eslint.org)
- [PhpStorm ESLint plugin](https://www.jetbrains.com/help/phpstorm/10.0/eslint.html) (jetbrains.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Drupal.theme for HTML Markup in JavaScript](/tutorial/use-drupaltheme-html-markup-javascript?p=2883)

Next
[Modernizr.js in a Theme or Module](/tutorial/modernizrjs-theme-or-module?p=2883)

Clear History

Ask Drupalize.Me AI

close