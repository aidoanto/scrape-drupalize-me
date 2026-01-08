---
title: "Use Drupal.t() for Translatable Strings in JavaScript"
url: "https://drupalize.me/tutorial/use-drupalt-translatable-strings-javascript?p=3253"
guide: "[[output-and-format-data-code]]"
---

# Use Drupal.t() for Translatable Strings in JavaScript

## Content

Sometimes your JavaScript needs to insert new strings into the user interface. In order to ensure that those user-facing strings can be translated into other languages, just like the rest of Drupal's user interface, you should make sure and use the `Drupal.t` function anytime you output a string of text.

## Goal

Ensure that user-facing strings output from JavaScript running in Drupal are translatable.

## Prerequisites

- [JavaScript in Drupal](https://drupalize.me/tutorial/overview-javascript-drupal)

## How does string translation work in Drupal?

If you've written a custom module, or even just browsed through Drupal's source code, you've likely come across the `t()` [function in PHP](https://api.drupal.org/api/drupal/core%21includes%21bootstrap.inc/function/t/). Its job is to translate a particular string to the current or given language. Since all the user interface strings in Drupal are wrapped in the `t()` function, Drupal is able to keep track of a list of them for localization. Because this is used consistently throughout Drupal core, and the list of strings used in Drupal's interface is well known, there are already dozens of translation files available to help convert the interface into multiple languages. It shouldn't be much of a surprise to learn that Drupal's [Localization API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Language%21language.api.php/group/i18n) provides a method for translating strings from within JavaScript as well: the `Drupal.t()` function.

## What is `Drupal.t()`?

The `Drupal.t()` function is a utility function that takes an English language string and checks to see if — given the current page's configuration and context — it should return a version of that string translated into another language. Whenever JavaScript code outputs strings that are shown as text that a user might read it should ideally be wrapped with `Drupal.t()`.

Example:

```
// Bad
alert('Hello world');

// Good
alert(Drupal.t('Hello world'));
```

As long as the core *drupal.js* file is loaded, `Drupal.t()` is available in the global scope.

The JavaScript version of Drupal's translation function is so similar to the PHP version, that the inline documentation when it is defined refers to the PHP documentation as well. So if you know how the PHP `t()` function or `\Drupal\Core\StringTranslation\TranslatableMarkup` class work you already know most of what you need to use the JavaScript `Drupal.t()` function.

```
// Definition of Drupal.t() from drupal.js.
Drupal.t = function (str, args, options) {}
```

Looking at the parameters passed to `Drupal.t()` we can see we need the string containing the text to translate, an optional object of replacement pairs to make after the translation, additional options for translation, and the optional context the source string belongs to.

### {string} str

The user interface string with placeholders representing dynamic portions of the string.

### {Array} args

An associative array keyed by placeholder names and their corresponding value for substitution. Replacements are processed after translation.

### {Array} options

An array of additional context arguments that provide additional information to translators about the meaning of a string that is being translated.

## Placeholders and `Drupal.formatString()`

Rather then directly inserting dynamic text into a translatable string you should instead use placeholders. The placeholder gives translators a better indicator of the context in which the translated string is being used. This also ensures that dynamic text can be escaped, and sanitized for output as HTML — something that's especially important when displaying user input.

**Note:** calling `Drupal.t(variable)` will not sanitize a variable, you must use the appropriate placeholder.

### A bad example

```
// Bad.
const title = user.displayName + Drupal.t(' Blog');
```

### A good example

```
// Good.
const title = Drupal.t("@name's Blog", {'@name': user.displayName};
```

This also gives the translator the opportunity to move the placeholder around within the sentence. For example, "Joe's Blog" in English, vs. "Blog de Joe" in Spanish.

### @variable

Use this style of placeholder for most use-cases. Special characters in the text will be converted to HTML entities. This placeholder will often represent content that is dynamic, but could itself be translated via other means. For example, the title of an article may have both an English and a Farsi version.

```
Drupal.t('Hello @name, welcome back!', {'@name': user.displayName});
```

Output example:

```
Hello Sally, welcome back!
```

### %variable

Use this style of placeholder to pass text through `Drupal.placeholder()` which will result in the text being HTML-escaped, and then wrapped with `<em>` tags. This placeholder is most commonly used to represent dynamic content that can not be translated and therefore may appear to be a mistake rather than intentional. For example, you can not translate the path to a file on disk even though that path may contain words that could in theory be translated.

```
Drupal.t('The file was saved to %path.', {'%path': path_to_file});
```

Output example:

```
The file was saved to <em class="placeholder">sites/default/files/myfile.txt</em>.
```

### !variable

Use this style placeholder to pass a value through with no additional sanitization or formatting. Use with caution.

```
Drupal.t('Hello <a href="!url">@name</a>', {'!url': 'http://example.com', '@name': user.displayName});
```

Output example:

```
Hello <a href="http://example.com">Sally</a>
```

The types and purposes of each of these placeholders is again identical to the PHP equivalent [FormattableMarkup::placeholderFormat](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Render%21FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderFormat/).

## Examples of `Drupal.t()` in core

You can see examples of `Drupal.t()` throughout Drupal core. In *core/modules/node/node.js*, the function is used to help format the "posted by" information:

```
$context.find('.node-form-author').drupalSetSummary(function (context) {
var $authorContext = $(context);
var name = $authorContext.find('.field--name-uid input').val();
var date = $authorContext.find('.field--name-created input').val();

if (name && date) {
    return Drupal.t('By @name on @date', {'@name': name, '@date': date});
}
else if (name) {
    return Drupal.t('By @name', {'@name': name});
}
else if (date) {
    return Drupal.t('Authored on @date', {'@date': date});
}
});
```

Here you can see `Drupal.t()` in action, providing strings for translation that depend on dynamic values for the author's name and the current date.

JavaScript in the Editor module, makes use of `Drupal.t()` in a string that requires a dynamic placeholder variable (one that starts with `%`). In *core/modules/editor/js/editor.js* we can find the following implementation:

```
...
    if (hasContent && supportContentFiltering) {
      var message = Drupal.t('Changing the text format to %text_format will permanently remove content that is not allowed in that text format.<br><br>Save your changes before switching the text format to avoid losing data.', {
        '%text_format': $select.find('option:selected').text()
      });
```

In this implementation, the value of `%text_format` needs to be passed through both `Drupal.checkPlain()` as well as the `Drupal.theme('placeholder')` theme function. You can read more about using `Drupal.theme()` in our tutorial [Use Drupal.theme for HTML Markup in JavaScript](https://drupalize.me/tutorial/use-drupaltheme-html-markup-javascript).

The Tour module passes unescaped output through `Drupal.t()` in order to provide the progress string to the translation system. In *core/modules/tour/js/tour.js* we can see this in action:

```
var progress = Drupal.t('!tour_item of !total', {'!tour_item': index + 1, '!total': total});
```

Since both of the values in this string are guaranteed to be integers, they don't require any additional processing.

## Translation string options

The third argument passed to `Drupal.t()` is the ambiguously-named `options` object. The code documentation refers to this as "Additional options for translation". These additional options can include the *language code* you need to translate a particular string to, and a *context* in which the string is being used.

### Example: Providing a langcode to `Drupal.t()`

Assuming this Spanish string appears on an English site, a `langcode` is provided to inform translators of its language.

```
Drupal.t('Buenos días!', {}, { 'langcode': 'es' })
```

### Example: Providing a context for `Drupal.t()`

For example, `May` could represent a month name or a 3-letter month code. The translation system only stores one copy of the string which it swaps out for any call to `Drupal.t('May')`. The `context` option here can be used to differentiate between when `May` is being used as a "Long month name" and when it's simply an abbreviation.

```
Drupal.t('May', {}, {'context': 'Long month name'});
```

The [Internationalization topic on api.drupal.org](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Language!language.api.php/group/i18n/) has the full details about string contexts, but in short, it's a way for the translation system to keep track of how a potentially ambiguous string is being used so that a proper replacement can be used.

## Assemble strings for translation

Internally, Drupal maintains a list of all the strings passed through either the PHP `t()` or the `Drupal.t()` JavaScript function. For performance reasons this list of strings is cached, so Drupal doesn't have to discover every string available to translation on every page load. This means that whenever you add or change strings passed to `Drupal.t()` in a JavaScript file they won't be available to the translation system until the [cache has been rebuilt](https://drupalize.me/tutorial/clear-drupals-cache).

The internals of how translation works are beyond the scope of this tutorial, but as long as you wrap any user-facing strings in your JavaScript with calls to `Drupal.t()` you'll be doing your part to make them available to Drupal's translation interface.

## Recap

In this tutorial, we learned how to implement `Drupal.t()` in custom JavaScript running in a Drupal code base to ensure that the strings output in JavaScript files are translatable.

## Further your understanding

- Locate the documentation for `Drupal.t`
- Know when to use `Drupal.t` in your own code
- Use placeholders in strings passed to `Drupal.t`

## Additional resources

- [String Manipulation in JavaScript](https://drupalize.me/tutorial/string-manipulation-javascript)
- [Use Drupal.theme for HTML Markup in JavaScript](https://drupalize.me/tutorial/use-drupaltheme-html-markup-javascript)
- [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Make Strings Translatable](/tutorial/make-strings-translatable?p=3253)

Next
[Make Your Theme Translatable](/tutorial/make-your-theme-translatable?p=3253)

Clear History

Ask Drupalize.Me AI

close