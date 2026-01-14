---
title: "Use Drupal.theme for HTML Markup in JavaScript"
url: "https://drupalize.me/tutorial/use-drupaltheme-html-markup-javascript?p=2883"
guide: "[[integrate-javascript-drupal]]"
---

# Use Drupal.theme for HTML Markup in JavaScript

## Content

In Drupal, whenever we output markup it's best practice to use a Twig template or a theme function. But whenever you need to output DOM elements within JavaScript the best practice is to use the `Drupal.theme` function. This function ensures that the output can be overridden just like the HTML output by Twig. This tutorial covers how to use the `Drupal.theme` function in your JavaScript when inserting DOM elements, as well as how to replace the markup output by other JavaScript code that is using the `Drupal.theme` function.

## Goal

Understand how to use `Drupal.theme` to properly output markup from JavaScript running in your Drupal code base.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)
- [Attach a Library](https://drupalize.me/tutorial/attach-asset-library)
- A custom theme: Use the Drush command `drush generate theme` command to create the theme called `friendly`.

## What is `Drupal.theme`?

Perhaps the best place to start learning about `Drupal.theme` is right from the source. We can find the definition of `Drupal.theme` in the *core/misc/drupal.js* file:

```
  /**
   * Generates the themed representation of a Drupal object.
   *
   * All requests for themed output must go through this function. It examines
   * the request and routes it to the appropriate theme function. If the current
   * theme does not provide an override function, the generic theme function is
   * called.
   *
   * @example
   * <caption>To retrieve the HTML for text that should be emphasized and
   * displayed as a placeholder inside a sentence.</caption>
   * Drupal.theme('placeholder', text);
   *
   * @namespace
   *
   * @param {function} func
   *   The name of the theme function to call.
   * @param {...args}
   *   Additional arguments to pass along to the theme function.
   *
   * @return {string|object|HTMLElement|jQuery}
   *   Any data the theme function returns. This could be a plain HTML string,
   *   but also a complex object.
   */
  Drupal.theme = function (func) {
    var args = Array.prototype.slice.apply(arguments, [1]);
    if (func in Drupal.theme) {
      return Drupal.theme[func].apply(this, args);
    }
  };
```

The description of this function should be very familiar if you've ever worked with the PHP function `hook_theme`. The JavaScript version works much the same way. First you register the name of the theme function for the output you'd like to generate. In the documentation for `Drupal.theme` the placeholder theme function is mentioned. You can find the definition of `Drupal.theme.placeholder` also in the *core/misc/drupal.js* file.

```
  /**
   * Formats text for emphasized display in a placeholder inside a sentence.
   *
   * @param {string} str
   *   The text to format (plain-text).
   *
   * @return {string}
   *   The formatted text (html).
   */
  Drupal.theme.placeholder = function (str) {
    return '<em class="placeholder">' + Drupal.checkPlain(str) + '</em>';
  };
```

In order to invoke this theme function, and generate the placeholder markup, in our own custom theme we use the following:

```
Drupal.theme('placeholder', text);
```

The first argument we pass in to `Drupal.theme` is the name of the theme function we're invoking: `'placeholder'`, in this case. The second argument can be either a string, object, HTML element or jQuery object. Generally speaking, as a best practice, it's best to use an object for this second argument if you require more than one element to be passed in. In the placeholder example we only have a single argument, the text to be used in the placeholder, so a simple string will be sufficient.

Since a function has been defined for `Drupal.theme.placeholder`, any time `Drupal.theme('placeholder', text)` is called that function will be executed. The default `Drupal.theme.placeholder` function simply wraps the text that is passed to it with an `<em>` tag with the placeholder class. If we want to override this behavior we can implement our own version of `Drupal.theme.placeholder` in our own custom theme.

Use the Drush command `drush generate theme` command to create the theme called `friendly`. We're going to make a few modifications to the *js/friendly-greeting.js* asset library to override `Drupal.theme.placeholder`.

The new *friendly/js/friendly-greeting.js* is as follows:

```
(function (Drupal) {
  // Override the default implementation of Drupal.theme.placeholder with our
  // own custom one.
  Drupal.theme.placeholder = function(str) {
    return '<em class="friendly-placeholder">' + Drupal.checkPlain(str) + '</em>';
  }

  // If we have a nice user name, let's replace the
  // site name with a greeting.
  // Note: The exact class name `site-branding__name` can vary depending on the
  // theme, and version of Drupal used. View the page source to verify the
  // class name.
  if (drupalSettings.friendly.name) {
    var siteName = document.getElementsByClassName('site-branding__name')[0];
    siteName.getElementsByTagName('a')[0].innerHTML = '<h1>Howdy, ' + Drupal.theme('placeholder', drupalSettings.friendly.name) + '!</h1>';
  }

})(Drupal);
```

After saving this file, [rebuild the cache](https://drupalize.me/tutorial/clear-drupals-cache).

First we've provided a new implementation of `Drupal.theme.placeholder` which changes the class on the wrapping `<em>` element to `friendly-placeholder`. Then in the code that replaces our site name with a friendly greeting we're calling `Drupal.theme('placeholder')`. If you're following along on your own development site, you'll notice that this friendly greeting does indeed have the `friendly-placeholder` class applied.

Image

![friendly placeholder override](../assets/images/drupalsettings-placeholder-demo.png)

Congratulations, you've successfully replaced a core `Drupal.theme` implementation with your own custom output. Remember, any time you need to output complex markup from within JavaScript, it's best to define a `Drupal.theme` function. This not only makes your code more readable, but also helps you replace outputting complex markup with a simple call to a `Drupal.theme` function.

## Recap

In this tutorial we learned how to implement `Drupal.theme` in JavaScript running within a Drupal site in a way that ensures that the markup output from our script is still overrideable by other themes or modules.

## Further your understanding

- Try using `Drupal.theme` to output HTML markup into the DOM from your theme.
- Try overriding another module's or theme's `Drupal.theme` output with your own.

## Additional resources

- [Use Server-Side Settings with drupalSettings](https://drupalize.me/tutorial/use-server-side-settings-drupalsettings) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[String Manipulation in JavaScript](/tutorial/string-manipulation-javascript?p=2883)

Next
[Standardize Your JavaScript with ESLint](/tutorial/standardize-your-javascript-eslint?p=2883)

Clear History

Ask Drupalize.Me AI

close