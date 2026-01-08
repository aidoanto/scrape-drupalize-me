---
title: "Overview: JavaScript in Drupal"
url: "https://drupalize.me/tutorial/overview-javascript-drupal?p=2883"
guide: "[[integrate-javascript-drupal]]"
---

# Overview: JavaScript in Drupal

## Content

JavaScript is used and loaded in special ways within a Drupal site. JavaScript is loaded via *asset libraries* and Drupal core provides a bunch of different JavaScript libraries that you can load and use in your module or theme. This tutorial provides a brief orientation to some of the JavaScript included in core.

In this tutorial we'll:

- Preview the JavaScript ecosystem in Drupal
- Find pointers to tutorials where you can learn more about adding JavaScript to a theme or module
- Learn about examples of JavaScript in Drupal core that are useful to review for learning purposes

By the end of this tutorial you should have a good overview of how JavaScript is used throughout Drupal core.

## Goal

Introduce the JavaScript ecosystem within Drupal.

## Prerequisites

- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)

## Add JavaScript to a module or theme

JavaScript is loaded via [asset libraries](https://drupalize.me/tutorial/what-are-asset-libraries) in Drupal. In order to take a look at the JavaScript in Drupal's core, we first need to look for these asset libraries. Asset libraries are specified by modules or themes in a *THEMENAME.libraries.yml* (or *MODULENAME.libraries.yml*) file. While each module and theme can specify its own libraries, the majority of those used by core are documented in *core/core.libraries.yml*. In this tutorial we'll take a brief look at some of the larger and more significant libraries included in core, and how they are used within Drupal.

## jQuery

The library used most frequently throughout core is [jQuery](https://jquery.com). The jQuery library provides a simple API to make things like DOM manipulation, event handling, animation and AJAX easier to manage cross-browser.

### A note about using jQuery

While jQuery is included with Drupal core it's worth noting that at this point native JavaScript has equivalent functions for most of the core features of jQuery. We strongly recommend using native JavaScript features and not relying on jQuery whenever possible. Our best guess is that at some point in the future jQuery will also be removed from Drupal core.

Drupal 8 also contains, and uses jQuery UI, though it's been deprecated and will be removed in Drupal 9 and all core JavaScript libraries will be updated to use modern JavaScript.

## CKEditor

Another exciting JavaScript addition to Drupal core is [CKEditor](https://ckeditor.com/). The addition of CKEditor gives Drupal a What-You-See-Is-What-You-Get (WYSIWYG) editorial experience out of the box. If you'd like to give the editor a try and you don't have a Drupal installation set up yet, you can do so on their [demo page](https://ckeditor.com/ckeditor-4/demo/).

## Modernizr

The [Modernizr](https://modernizr.com) asset library provides simple in browser feature detection. This enables developers to tailor the user experience based on the available features of their users' actual browsers. This makes it much easier to build progressive enhancement into your site, ensuring users receive the best possible experience given the limitations of their browser.

## Picturefill

[Picturefill](https://github.com/scottjehl/picturefill) is a small polyfill for responsive images. This helps developers deliver the appropriate images assets to their users. The library fills in the functionality gaps for older browsers, so they're able to leverage the same markup that handles responsive images as newer browsers.

## Backbone.js and Underscore.js

**WARNING:** Both Backbone.js and Underscore.js have been deprecated in Drupal 9.4/10.0 and will eventually be removed. We do not recommend depending on them in your own code any longer. Drupal core is replacing its use of Backbone with Vanilla JS, and the library will be removed once that transition is complete.

Another popular JavaScript library included in Drupal core is [Backbone.js](https://backbonejs.org). Backbone is a popular choice for JavaScript developers looking for a way to add Models and Views to their application. The only hard dependency of Backbone is [Underscore.js](https://underscorejs.org). Underscore provides over 100 utility functions that make working with objects and arrays easier. In Drupal, Backbone models are used to represent data objects (like the toolbar) while Views are used to describe the actual user interface. Backbone's Views depend on a Model for the data they're responsible for rendering but they don't necessarily directly interact with each other.

Perhaps the best resource for really understanding the internals of Backbone is the well [annotated source code](https://backbonejs.org/docs/backbone.html) itself. There's a simple example of how Drupal makes use of Backbone's data binding in the blog post [Backbone.js and Underscore.js in Drupal 8](https://drupalize.me/blog/201504/backbonejs-and-underscorejs-drupal-8). Other uses of Backbone in Drupal core include:

- [The CKEditor's toolbar configuration](https://git.drupalcode.org/project/drupal/-/blob/9.5.7/core/modules/ckeditor/js/models/Model.js) use both Models and Views. (Note: This code example is from Drupal 9.5.7 as CKEditor 5 replaced CKEditor in Drupal 10.)
- [Contextual module](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/modules/contextual/js/models/StateModel.js) is covered in the previously mentioned blog post.
- [The Quick Edit module](https://git.drupalcode.org/project/drupal/-/tree/9.5.7/core/modules/quickedit/js/models) provides several Models and Views to help manage the complexity of in-place editing. (Note: This code example is from Drupal 9.5.7 as Quick Edit module was removed in Drupal 10.)
- [The Toolbar](https://git.drupalcode.org/project/drupal/-/tree/10.1.x/core/modules/toolbar/js/models) also uses Models to manage the toolbar menu.
- [The Tour module](https://git.drupalcode.org/project/drupal/-/tree/10.1.x/core/modules/tour/js) also uses Backbone to manage the various steps in a site tour. Tour also makes use of another library [Joyride](https://zurb.com/playground/jquery-joyride-feature-tour-plugin).

## Useful, but not required

It's important to keep in mind that Drupal doesn't necessarily require the use of any of these JavaScript asset libraries in the development of your own custom theme or module, but that they're available to you should you need them. Take a look at some of the other libraries defined in */core/core.libraries.yml*. There might be some additional useful libraries that will make your life a little easier.

Additionally, the JavaScript ecosystem continues to evolve and over time libraries will be removed or replaced. It's a good idea to never write new code that uses a deprecated library. Look for the `deprecated` key in the Drupal asset library defintion, or the `@deprecated` tag on a function or class before you make your code depend on it. [Learn more about Drupal's JavaScript deprecation policy](https://www.drupal.org/about/core/policies/core-change-policies/drupal-core-deprecation-policy#javascript).

## Recap

JavaScript is used and loaded in special ways within a Drupal site. JavaScript is loaded via *asset libraries* and Drupal core provides a bunch of different JavaScript libraries that you can load and use in your module or theme. This tutorial provided a brief orientation to some of the JavaScript included in core.

## Further your understanding

- Practice defining and attaching an asset library in [Exercise: Add an Asset Library](https://drupalize.me/tutorial/exercise-add-asset-library).

## Additional resources

- [Adding stylesheets (CSS) and JavaScript (JS) to a Drupal theme](https://www.drupal.org/docs/theming-drupal/adding-stylesheets-css-and-javascript-js-to-a-drupal-theme) (Drupal.org)
- [Backbone.js and Underscore.js in Drupal](https://drupalize.me/blog/201504/backbonejs-and-underscorejs-drupal-8) (Drupalize.Me)
- [What Are Libraries](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Define a Library](https://drupalize.me/tutorial/define-asset-library) (Drupalize.Me)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Load JavaScript in Drupal with Drupal.behaviors](/tutorial/load-javascript-drupal-drupalbehaviors?p=2883)

Clear History

Ask Drupalize.Me AI

close