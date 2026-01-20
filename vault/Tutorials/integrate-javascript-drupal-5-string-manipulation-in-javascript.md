---
title: "String Manipulation in JavaScript"
url: "https://drupalize.me/tutorial/string-manipulation-javascript?p=2883"
guide: "[[integrate-javascript-drupal]]"
order: 5
---

# String Manipulation in JavaScript

## Content

You may know that Drupal provides utility PHP functions for manipulating and sanitizing strings. Drupal also provides JavaScript functions for the same purpose. The two most useful are `Drupal.checkPlain` and `Drupal.formatPlural`. `Drupal.checkPlain` lets you ensure a string is safe for output into the DOM; it is useful when working with user-provided input. `Drupal.formatPlural` ensures that a string containing a count of items is pluralized correctly. This tutorial will show you where you can find documentation for and example use-cases of both.

## Goal

Learn how to use common string-manipulation functions in JavaScript running in a Drupal site.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)

## `Drupal.checkPlain`

Like most of the other JavaScript utility functions, `Drupal.checkPlain` can be found in the *core/misc/drupal.js* file. Let's take a look at the actual code itself:

```
  /**
   * Encodes special characters in a plain-text string for display as HTML.
   *
   * @param {string} str
   *   The string to be encoded.
   *
   * @return {string}
   *   The encoded string.
   *
   * @ingroup sanitization
   */
  Drupal.checkPlain = function (str) {
    str = str.toString()
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    return str;
  };
```

As you can probably see, `checkPlain` handles replacing any instance of `&amp;`, `&quot;`, `&lt;`, or `&gt;` with their HTML-encoded counterparts ([documentation for the PHP equivalent, `HTML::escape`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Utility%21Html.php/function/Html%3A%3Aescape/)). Using `Drupal.checkPlain` in your JavaScript will help ensure that any HTML entities in user provided text are properly encoded before being displayed.

## `Drupal.formatPlural`

Find the source for `Drupal.formatPlural` in *core/misc/drupal.js*:

```
  /**
   * Formats a string containing a count of items.
   *
   * This function ensures that the string is pluralized correctly. Since
   * {@link Drupal.t} is called by this function, make sure not to pass
   * already-localized strings to it.
   *
   * See the documentation of the server-side
   * \Drupal\Core\StringTranslation\TranslationInterface::formatPlural()
   * function for more details.
   *
   * @param {number} count
   *   The item count to display.
   * @param {string} singular
   *   The string for the singular case. Please make sure it is clear this is
   *   singular, to ease translation (e.g. use "1 new comment" instead of "1
   *   new"). Do not use @count in the singular string.
   * @param {string} plural
   *   The string for the plural case. Please make sure it is clear this is
   *   plural, to ease translation. Use @count in place of the item count, as in
   *   "@count new comments".
   * @param {object} [args]
   *   An object of replacements pairs to make after translation. Incidences
   *   of any key in this array are replaced with the corresponding value.
   *   See {@link Drupal.formatString}.
   *   Note that you do not need to include @count in this array.
   *   This replacement is done automatically for the plural case.
   * @param {object} [options]
   *   The options to pass to the {@link Drupal.t} function.
   *
   * @return {string}
   *   A translated string.
   */
  Drupal.formatPlural = function (count, singular, plural, args, options) {
    args = args || {};
    args['@count'] = count;

    var pluralDelimiter = drupalSettings.pluralDelimiter;
    var translations = Drupal.t(singular + pluralDelimiter + plural, args, options).split(pluralDelimiter);
    var index = 0;

    // Determine the index of the plural form.
    if (typeof drupalTranslations !== 'undefined' && drupalTranslations.pluralFormula) {
      index = count in drupalTranslations.pluralFormula ? drupalTranslations.pluralFormula[count] : drupalTranslations.pluralFormula['default'];
    }
    else if (args['@count'] !== 1) {
      index = 1;
    }

    return translations[index];
  };
```

The example used in the docblock for `Drupal.formatPlural` mentions comments, so lets see how Drupal's comment module makes use of this function. The comment module defines an asset library (in *core/modules/comment/comment.libraries.yml*) called `drupal.node-new-comments-link`. Looking at the JavaScript file for this library *core/modules/comment/js/node-new-comments-link.js* we can see it makes use of `Drupal.formatPlural` inside a `render` function:

```
    /**
     * Renders the "X new comments" links.
     *
     * Either use the data embedded in the page or perform an AJAX request to
     * retrieve the same data.
     *
     * @param {object} results
     *   Data about new comment links indexed by nodeID.
     */
    function render(results) {
      for (var nodeID in results) {
        if (results.hasOwnProperty(nodeID) && $placeholdersToUpdate.hasOwnProperty(nodeID)) {
          $placeholdersToUpdate[nodeID]
            .attr('href', results[nodeID].first_new_comment_link)
            .text(Drupal.formatPlural(results[nodeID].new_comment_count, '1 new comment', '@count new comments'))
            .removeClass('hidden');
          show($placeholdersToUpdate[nodeID]);
        }
      }
    }
```

Here we can see `formatPlural` is passed the total new comment count (an integer) as well as the string to use when the count is singular and another to use for the plural case. The optional additional `args` and `options` arguments are not used in this case. Looking back at the source of `Drupal.formatPlural` we can see that it first loads `drupalTranslations`. It then compares the number passed in via the first count parameter to see if its value is 1. If it is, the singular case (properly translated) is used. If the count parameter is more than 1, the plural translation is used instead.

Perhaps unsurprisingly, `Drupal.formatPlural` has an equivalent in PHP in [TranslationInterface::formatPlural](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21StringTranslation%21TranslationInterface.php/function/TranslationInterface%3A%3AformatPlural/).

## Recap

In this tutorial, we learned about the two most useful are `Drupal.checkPlain` and `Drupal.formatPlural`. `Drupal.checkPlain` lets you ensure a string is safe for output into the DOM; it is useful when working with user-provided input. `Drupal.formatPlural` ensures that a string containing a count of items is pluralized correctly.

## Further your understanding

- Understand the use-case for `Drupal.checkPlain`
- Understand the use-case for `Drupal.formatPlural`
- Find documentation and usage examples for both functions

## Additional resources

- [Documentation for HTML::escape](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Utility%21Html.php/function/Html%3A%3Aescape/) (api.drupal.org)
- [TranslationInterface::formatPlural](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21StringTranslation%21TranslationInterface.php/function/TranslationInterface%3A%3AformatPlural/) (api.drupal.org)
- [JavaScript best practices](https://www.drupal.org/node/2297057) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Server-Side Settings with drupalSettings](/tutorial/use-server-side-settings-drupalsettings?p=2883)

Next
[Use Drupal.theme for HTML Markup in JavaScript](/tutorial/use-drupaltheme-html-markup-javascript?p=2883)

Clear History

Ask Drupalize.Me AI

close