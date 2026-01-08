---
title: "What Are Asset Libraries?"
url: "https://drupalize.me/tutorial/what-are-asset-libraries?p=2860"
guide: "[[integrate-javascript-drupal]]"
---

# What Are Asset Libraries?

## Content

An asset library is a bundle of CSS and/or JavaScript files that work together to provide a style and functionality for a specific component. They are frequently used to isolate the functionality and styling of a specific component, like the tabs displayed at the top of each node, into a reusable library. If you want to include CSS and/or JavaScript in your Drupal theme or module you'll need to declare an asset library that tells Drupal about the existence, and location, of those files. And then *attach* that library to a page, or specific element, so that it gets loaded when needed.

In this tutorial we’ll:

- Define what an asset library is.
- Explain why asset libraries are used to include JavaScript and CSS files.
- Look at some example asset library definitions.

By the end of this tutorial you should be able to define what asset libraries are, and when you'll need to create one.

## Goal

Explain what asset libraries are and the role they play in a Drupal theme.

## Prerequisites

- [Structure of a Theme](https://drupalize.me/tutorial/structure-theme)
- [An Introduction to YAML](https://drupalize.me/videos/introduction-yaml)

## What are asset libraries?

The asset library system exists to make it possible for Drupal to:

- Include only the CSS and JavaScript required for a specific page.
- Vary what is included depending on the content of the page.

This approach reduces the overall size of the page which can have a performance impact. It speeds up rendering by ensuring that the browser doesn't need to spend time processing CSS and JavaScript that's never used.

Image

![Parts of an asset library](/sites/default/files/styles/max_800w/public/tutorials/images/define-an-asset-library.png?itok=fYSLQ02Y)

An asset library is a YAML data structure inside a *THEMENAME.libraries.yml* file that specifies one or more CSS and JavaScript files, and their settings, bundled together under a uniquely identified library name. Once the library has been defined adding it to a page, or attaching it to a particular type of element, is done in the same fashion regardless of the contents of the library. This means there is now one unified mechanism for adding CSS and JavaScript whether it's being added in a module or a theme.

Both modules and themes can define asset libraries, and use them, in the same way. Themes can override or extend an asset library provided by a parent theme or a module.

As a theme developer you'll define new asset libraries that point to the location of your custom CSS and JavaScript code. And then tell Drupal when to include the library by associating it with a template file, a specific render element, or globally for every page.

## Core libraries

Drupal core contains many examples of asset library definitions and is a good place to look for examples. Check out the [*core/themes/olivero/olivero.libraries.yml* file in the Olivero theme](https://api.drupal.org/api/drupal/core%21themes%21olivero%21olivero.libraries.yml/11.x).

We can see more complex examples in */core/core.libraries.yml*. This file has an example of a JavaScript library as well as one that provides a dependency on another library:

```
drupal.vertical-tabs:
  version: VERSION
  js:
    # Load before core/drupal.collapse.
    misc/vertical-tabs.js: { weight: -1 }
  css:
    component:
      misc/vertical-tabs.css: {}
  dependencies:
    - core/jquery
    - core/once
    - core/drupal
    - core/drupalSettings
    - core/drupal.form
```

Here we can see the definition of the `core/drupal.vertical-tabs` library, including version information, settings indicating its weight relative to other JavaScript files, and a dependency on the `core/jquery` and other libraries.

Take a look at some of the libraries defined in */core/core.libraries.yml* to see examples of a libraries that contain both CSS and JavaScript files. Learn more about the contents of the *.libraries.yml* file in [Define An Asset Library](https://drupalize.me/tutorial/define-asset-library).

## Recap

In this tutorial we learned that asset libraries are how Drupal modules and themes tell Drupal about the CSS and JavaScript that they include. Libraries allow related CSS and JavaScript assets to be bundled together. They are defined via YAML, in a *{THEMENAME}.libraries.yml* file. Then they are attached to individual templates, or render elements, so that Drupal can be smart about only including what is necessary for the current page.

## Further your understanding

- Learn how to [Define An Asset Library](https://drupalize.me/tutorial/define-asset-library), and then [Attach A Library](https://drupalize.me/tutorial/attach-asset-library) to a template or other element.
- Learn how to [extend or override an existing asset library](https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries).
- Using your existing design see if you can identify elements, or templates, where it would make sense to bundle the related CSS and JavaScript into a library. Hint: look for things that appear on some but not all pages vs. things that appear globally.

## Additional resources

- [Adding stylesheets (CSS) and JavaScript (JS) to a Drupal module](https://www.drupal.org/node/2274843) (Drupal.org)
- [Adding stylesheets (CSS) and JavaScript (JS) to a Drupal theme](https://www.drupal.org/docs/theming-drupal/adding-stylesheets-css-and-javascript-js-to-a-drupal-theme) (Drupal.org)
- [Themes should use libraries, not individual stylesheets](https://www.drupal.org/node/2377397) (Drupal.org)
- [Performance improvements with Drupal 8 Libraries](https://www.previousnext.com.au/blog/performance-improvements-drupal-8-libraries) (previousnext.com.au)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library) (Drupalize.Me)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library) (Drupalize.Me)
- [Extend or Alter Existing CSS and JavaScript Asset Libraries](https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Define an Asset Library](/tutorial/define-asset-library?p=2860)

Clear History

Ask Drupalize.Me AI

close