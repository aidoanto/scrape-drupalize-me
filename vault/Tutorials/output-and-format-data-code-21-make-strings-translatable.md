---
title: "Make Strings Translatable"
url: "https://drupalize.me/tutorial/make-strings-translatable?p=3253"
guide: "[[output-and-format-data-code]]"
order: 21
---

# Make Strings Translatable

## Content

Any text that will be displayed to user as part of your application's user interface should be passed through the `t()` function, or an equivalent, so that it can be translated into other languages as needed. This tutorial will look at how to use the `t()` function.

This tutorial contains information that applies to anyone writing modules or themes. And many of the tutorials you read on this site and on the web in general will expect that you understand how basic string translation works.

In this tutorial we'll look at:

- Passing strings through the `t()` function or equivalent so they are available for translation
- Using placeholders for dynamic content in translatable strings
- Tips for making your code's interface strings easier to translate

## Goal

Understand how to use the `t()` function or equivalent to ensure the strings your custom code outputs is translatable.

## Prerequisites

- None

## The translation function

All user interface strings should be passed through the `t` function, or an equivalent, in order to ensure that everything presented to users can be translated.

```
t($string, array $args = array(), array $options = array());
```

In case you didn't guess it already, "t" is shorthand for "translation."

The `t` function takes three arguments, in most cases you'll use the first two.

### $string string

The user interface string with placeholders representing dynamic portions of the string.

### $args array()

An associative array keyed by placeholder names and their corresponding value for substitution. Replacements are processed after translation.

### $options array()

An array of additional context arguments that provide additional information to translators about the meaning of a string that is being translated.

Rather then directly inserting dynamic text into a translatable string you should instead use placeholders. The placeholder gives translators a better indicator of the context in which the translated string is being used. This also ensures that dynamic text can be escaped, and sanitized for output as HTML. Something that's especially important when display user input.

Note: calling `t($variable)` will not sanitize a variable, you must use the appropriate placeholder.

### A bad example

```
// Bad.
$title = $user->getDisplayName() . t(' Blog');
```

### A good example

```
// Good.
$title = t('@name Blog', array('@name' => $user->getDisplayName()));
```

This also gives the translator the opportunity to move the placeholder around within the sentence. For example, "Joe's Blog" in English, vs. "Blog de Joe" in Spanish.

## Placeholders

### @variable

Use this style of placeholder for most use-cases. Special characters in the text will be converted to HTML entities.

```
t('Hello @name, welcome back!', array('@name' => $user->getDisplayName()));
```

Output example:

```
Hello Dries, welcome back!
```

### %variable

Use this style of placeholder to pass text through `drupal_placeholder()` which will result in the text being HTML escaped, and then wrapped with `<em>` tags.

```
t('The file was saved to %path.', array('%path' => $path_to_file));
```

Output example:

```
The file was saved to <em class="placeholder">sites/default/files/myfile.txt</em>.
```

### :variable

Use this style of placeholder when substituting the value of an `href` attribute. Values will be HTML escaped and filtered for dangerous protocols.

```
t('Hello <a href=":url">@name</a>', array(':url' => 'http://example.com', '@name' => $name));
```

Output example:

```
Hello <a href="http://example.com">Dries</a>
```

## Working with controllers

When you're writing code in the context of a controller you'll be able to use `$this->t()` instead of the global `t()` function to access the translation function. This is provided via the [\Drupal\Core\StringTranslation\StringTranslationTrait](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21StringTranslation%21StringTranslationTrait.php/trait/StringTranslationTrait/)

## Tips for translating user interface text

As a basic rule Drupal assumes that all UI strings in modules or themes are in English. While technically there is nothing that prevents you from writing a module in Turkish or Chinese, the assumption of English as a default language creates a common ground for translation.

You do not need to use `t` to localize user provided content. The localization API is only for fixed strings in code. User provided content is handled via a different mechanism. (Related: [How to Contribute Translations to Drupal.org Projects](https://drupalize.me/videos/how-contribute-translations-drupalorg-projects).)

Whenever possible, make strings for translation full sentences or phrases, and never begin or end with a blank space. Instead of breaking up strings or embedding variables in the middle, use placeholders. Strings that may have several meanings in English can take a context attribute in the `$options` array passed as a third argument to the `t` function to make it easier for translators to understand the meaning of the word.

## Recap

Any text that will be displayed to user as part of your application's user interface should be passed through the `t()` function, or an equivalent, so that it can be translated into other languages as needed. This tutorial looked at how to use the `t()` function.

## Further your understanding

- Define a use case for each of the placeholder types.

## Additional resources

- [API documentation for the `t()` function](https://api.drupal.org/api/drupal/core%21includes%21bootstrap.inc/function/t/) (api.drupal.org)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable) (Drupalize.Me)
- More information about [placeholder formats](https://api.drupal.org/api/drupal/core!lib!Drupal!Component!Render!FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderFormat/) (api.drupal.org)
- [Localization API overview](https://www.drupal.org/docs/7/api/localization-api/localization-api-overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Use Drupal.t() for Translatable Strings in JavaScript](/tutorial/use-drupalt-translatable-strings-javascript?p=3253)

Clear History

Ask Drupalize.Me AI

close