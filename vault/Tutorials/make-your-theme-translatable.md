---
title: "Make Your Theme Translatable"
url: "https://drupalize.me/tutorial/make-your-theme-translatable?p=3253"
guide: "[[output-and-format-data-code]]"
order: 23
---

# Make Your Theme Translatable

## Content

In order to ensure that all user interface strings in your application can be translated using Drupal's localization system, any text you add to templates needs to use either the `t` filter or the `{% trans %}` tag. Anyone creating themes or editing template files associated with a theme or a module should know how to use these two utilities.

In this tutorial we'll look at:

- How to use the `t` filter and `{% trans %}` tag in a Twig template
- The differences between the two, and how to determine which one to use
- How to translate strings assigned to variables in preprocess functions using the PHP `t()` function

## Goal

Understand the various methods for ensuring text strings in your theme's template files are translatable.

## Prerequisites

- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)

## Translating strings in a template file

Whenever you add a string of text inside of your template file you should use the `t` filter, or the `{% trans %}` tag, to ensure the strings can be translated. Both the `t` filter and `trans` tag are wrappers for Drupal's `t()` function. See [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable) for more about using the `t()` function. Familiarity with this tutorial will make translating strings in your templates easier.

`t` and `{% trans %}` differ in that the `t` filter only allows for simple strings, while using a `{% trans %}` block allows the use of dynamic placeholders in the string. Here are a few examples to help illustrate this difference.

### Simple string translation via `t` filter

```
{{ 'Hello Drupalize.Me member!'|t }}
```

Use this style for simple and short strings in your template files.

### String translation with dynamic placeholders

```
{% trans %}Hello {{ user.name }}, today's date is {{ date|placeholder }}.{% endtrans %}
```

Use this style any time you've got long strings or need to substitute dynamic content into the string being translated.

Placeholders in a `{% trans %}` tag are escaped by default, but can also be formatted as a placeholder `{{ var|placeholder }}`. This is equivalent to using `@string`, and `%string` in the `t()` function respectively. For more about how placeholders work see the documentation for [FormattableMarkup::placeholderFormat](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Render%21FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderFormat/).

A `{% trans %}` block can also be used to format plural strings.

```
{% trans %}
There is 1 comment.
{% plural count %}
There are {{ count }} comments.
{% endtrans %}
```

The contents of variables within a template file should already have been translated, and thus should not be used in conjunction with the `t` filter or `{% trans %}` tags.

## Translating strings in a preprocess function

Strings assigned to a variable inside a preprocess function should be translated in the preprocess function so that they are ready for use in a template file without any additional work. The general rule of thumb is that any variable in a Twig template is already translated by the time it gets to the template file. Strings in preprocess functions can be translated with the `t()` function.

```
function icecream_preprocess_page(&$variables) {
  // This can be printed out with {{ custom_footer_text }} in the page.html.twig
  // template file.
  $variables['custom_footer_text'] = t('This site is copyleft 2016 by @name', array('@name' => $variables['user']->getDisplayName()));
}
```

For more on how to use the `t` function read [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable).

## Recap

In this tutorial, we covered the `trans` function and `t` filter which should be used to ensure that strings in your theme's template files are translatable.

## Further your understanding

- What is the primary difference between the `t` filter and the `{% trans %}` tag?
- Define a use case for each of the three placeholder types that can be used with a `{% trans %}` tag.

## Additional resources

- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions) (Drupalize.Me)
- [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable) (Drupalize.Me)
- Documentation on [using the t filter in Twig templates](https://www.drupal.org/node/2357633) (Drupal.org).
- [Translation API overview](https://www.drupal.org/developing/api/8/localization) (Drupal.org)
- These comments contains some useful [warnings about unsafe use of t](https://www.drupal.org/node/2488304#comment-10019485) (Drupal.org).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Drupal.t() for Translatable Strings in JavaScript](/tutorial/use-drupalt-translatable-strings-javascript?p=3253)

Clear History

Ask Drupalize.Me AI

close