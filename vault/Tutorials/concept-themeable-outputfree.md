---
title: "Concept: Themeable Outputfree"
url: "https://drupalize.me/tutorial/concept-themeable-output?p=3239"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Themeable Outputfree

## Content

One of the features of any content management system's architecture is the separation of presentation and data. In Drupal, **modules** are responsible for figuring out *what* should be on the page, and **themes** are responsible for the final look and feel of anything shown in the browser. It's vital for a module to return themeable output, so that the active theme can determine how it's presented.

In this tutorial, we'll:

- Define *themeable output*.
- Show how modules can avoid embedding presentation data in their output.
- Explain why Drupal favors structured arrays over HTML strings for data presentation.

By the end of this tutorial, you will be able to articulate the role modules play in enabling themes to customize a Drupal site's appearance.

## Goal

Understand how Drupal modules output content in a way that allows the theme layer to modify it.

## Prerequisites

- None.

## How Drupal renders structured data chunks

Modules (and themes) define *theme hooks* by implementing `hook_theme()`. These hooks connect the structured data from a module to the HTML template for rendering. A *theme hook* is a unique identifier that specifies how a chunk of data should be rendered. During page rendering, Drupal uses the theme hook associated with each data chunk to determine the appropriate template file.

Drupal then calls any *preprocess* functions related to the template. Implemented by modules or themes, preprocess functions transform data and create new variables for use in templates. For instance, a preprocess function for a block template might determine the block's region and user authentication status, and add appropriate contextual classes.

Finally, data is converted to variables for the Twig template file linked to the theme hook. Twig renders the template, producing HTML. Drupal determines which template file gets used for each theme hook, giving themes the last opportunity to override the presentation of data for each theme hook.

Modules should provide a basic HTML template for their content or reuse a core theme hook. This ensures a module's output is displayed, regardless of which theme is active.

In [Add a Template File](https://drupalize.me/tutorial/add-template-file), we'll implement `hook_theme()` in a module, define a Twig template file, and link it to the `WeatherPage` controller's output.

## Modules output renderable arrays

Modules should output content as *renderable arrays*, not HTML strings. These Drupal-specific arrays contain the content itself and metadata that defines how it should be rendered. The use of structured arrays allows modules and themes to modify content without performing complex string replacements.

For more on renderable arrays, see [Concept: Render API](https://drupalize.me/tutorial/concept-render-api). In [Output Content Using Render API](https://drupalize.me/tutorial/output-content-using-render-api), we'll adjust the `WeatherPage` controller to return a renderable array instead of a hard-coded HTML string.

## CSS and JavaScript asset libraries

Modules can add CSS and JavaScript through *asset libraries*. Like theme hooks, asset libraries let themes and modules alter or extend CSS and JavaScript. We'll get into more details about asset libraries in [Concept: Asset Libraries](https://drupalize.me/tutorial/concept-asset-libraries). And we'll create an asset library and add custom CSS and JavaScript in [Add CSS and JavaScript to a Module's Output](https://drupalize.me/tutorial/add-css-and-javascript-modules-output).

## Cacheability of output

Though not directly related to theming, modules outputting content must also define its cacheability. This involves specifying when to cache, for how long, and when the cache should be invalidated. We'll delve into caching in [Add Cache Context and Tags to Renderable Arrays](https://drupalize.me/tutorial/add-cache-context-and-tags-renderable-arrays). Keep in mind that any module that outputs content will need to address caching.

## Recap

In this tutorial, we introduced the concept of themeable output in Drupal. We briefly defined theme hooks, renderable arrays, and asset libraries as strategies that we can use as module developers to ensure our module's output is themeable. The theme system allows modules to establish output requirements while giving themes control over its final presentation.

## Further your understanding

- Why do Drupal modules invest effort in defining theme hooks and asset libraries for their content?
- Can you think of scenarios where a theme might need to modify a module's output?

## Additional resources

- [How Drupal Turns a Request into a Response](https://drupalize.me/tutorial/how-drupal-turns-request-response) (Drupalize.Me)
- [Theme system overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/themeable/) (api.drupal.org)
- [Render API overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/theme_render/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: Render API](/tutorial/concept-render-api?p=3239)

Clear History

Ask Drupalize.Me AI

close