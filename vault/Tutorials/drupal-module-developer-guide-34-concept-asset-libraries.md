---
title: "Concept: Asset Libraries"
url: "https://drupalize.me/tutorial/concept-asset-libraries?p=3239"
guide: "[[drupal-module-developer-guide]]"
order: 34
---

# Concept: Asset Libraries

## Content

Asset libraries in Drupal associate CSS and JavaScript files with components, which enhances performance because the assets will only be loaded when they're needed.

In this tutorial, we'll:

- Define asset libraries and their purpose.
- Learn how to define an asset library in a module.
- Examine how asset libraries attach to components.

By the end of this tutorial, you should understand how asset libraries optimize resource loading and facilitate component-based development in Drupal.

## Goal

Understand the purpose of asset libraries and how they are implemented in Drupal modules.

## Prerequisites

- [Concept: Themeable Output](https://drupalize.me/tutorial/concept-themeable-output)
- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)

## What are asset libraries?

Asset libraries bundle CSS and JavaScript files, which provide style and functionality for components. Organizing assets into reusable libraries ensures that CSS and JavaScript files load only when their respective components appear on the page which helps site performance.

Asset libraries allow Drupal to:

- Load only the necessary CSS and JavaScript for a specific page.
- Manage dependencies between libraries, ensuring proper load order and functionality.

Targeted loading of assets reduces page size and speeds up rendering as browsers avoid processing unused CSS and JavaScript. With Drupal's knowledge of all required asset libraries, further optimizations, like aggregating multiple files into a single large file that requires fewer network requests, become possible.

## Defining asset libraries

Image

![Parts of an asset library](../assets/images/define-an-asset-library.png)

Asset libraries consist of CSS and JavaScript files defined in a *MODULE\_NAME.libraries.yml* file. This YAML file specifies the library's name, file locations, and settings, telling Drupal when and how to include the files. CSS assets are grouped into [SMACSS (Scalar and Modular Architecture for CSS) groupings](http://smacss.com/book/categorizing/) to help maintain the appropriate order when adding them to the page.

Here's an example of what it looks like to define an asset library in a *MODULE\_NAME.libraries.yml* file:

```
my_component:
  css:
    theme:
      css/my_component.css: {}
  js:
    js/my_component.js: {}
  dependencies:
    - core/jquery
```

This code snippet defines an asset library named `my_component`, which includes CSS and JavaScript files, and a dependency on jQuery.

Nested under the `css` key is the SMACSS group. Possible values for the SMACSS group for the CSS asset are listed below. SMACSS groups don't apply to `js` assets. For a module's CSS assets, if you're unsure, choose `component`:

- `base`: CSS reset/normalize plus HTML element styling.
- `layout`: Macro arrangement of a web page, including any grid systems.
- `component`: Discrete, reusable UI elements.
- `state`: Styles that deal with client-side changes to components.
- `theme`: Purely visual styling ("look-and-feel") for a component.

## Attaching asset libraries to components

Asset libraries can be attached to render arrays or templates to ensure the associated CSS and JavaScript load with the component.

Example:

```
$build['#attached']['library'][] = 'my_module/my_component';
```

This code snippet attaches the `my_component` library provided by `my_module` to a Drupal render array, loading its CSS and JavaScript files with the component.

## Theme overrides

Themes can extend or override module-defined asset libraries, allowing for customization of component styles and functionality. This capability ensures themes can alter the appearance and behavior of components, maintaining control over the site's look and feel.

## Recap

Asset libraries streamline the management and loading of CSS and JavaScript in Drupal. By defining and attaching these libraries to components, developers can achieve efficient, component-specific resource loading. This approach also empowers themes to modify or enhance the styling and functionality provided by modules.

## Further your understanding

- Explore how asset libraries impact the loading order and dependencies of CSS and JavaScript files.
- Consider the benefits of asset libraries in modular and themeable Drupal development.

## Additional resources

- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Adding assets (CSS, JS) to a Drupal module via \*.libraries.yml](https://www.drupal.org/docs/develop/creating-modules/adding-assets-css-js-to-a-drupal-module-via-librariesyml) (Drupal.org)
- [SMACSS: Categorizing CSS Rules](http://smacss.com/book/categorizing/) (smacss.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Template File](/tutorial/add-template-file?p=3239)

Next
[Add CSS and JavaScript to a Module's Output](/tutorial/add-css-and-javascript-modules-output?p=3239)

Clear History

Ask Drupalize.Me AI

close