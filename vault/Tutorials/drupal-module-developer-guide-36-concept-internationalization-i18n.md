---
title: "Concept: Internationalization (i18n)"
url: "https://drupalize.me/tutorial/concept-internationalization-i18n?p=3239"
guide: "[[drupal-module-developer-guide]]"
order: 36
---

# Concept: Internationalization (i18n)

## Content

Drupal modules need to ensure that any strings of text they add in code can be localized by Drupal's translation system. When our code creates a new `<button>` element with the text "Toggle forecast" it needs to be done in a way that would allow changing that text to another string, like "Alternar pronóstico", depending on the user's preferred language.

In this tutorial, we'll:

- Define the difference between internationalization and localization and how they allow a Drupal site to be translated.
- Explore the utilities available to module developers to ensure that the user interface strings in their code are translatable.

By the end of this tutorial, you should be able to explain how and why to internationalize the code in your Drupal modules.

## Goal

Understand how you can ensure that the user interface strings output from a module's code can be localized.

## Prerequisites

- None.

## Internationalization vs. localization

A multilingual site is any site that has content in more than 1 language that users can switch between. Common terms you will hear used with multilingual sites are *internationalization* (abbreviated as *i18n*) and *localization* (abbreviated as *l10n*). Internationalization is the underlying structure that allows software to be adapted to different languages, and localization is the process of actually translating the software for use by a specific locale.

When we write code that adds UI elements to the page, we're concerned with internationalization. That is, we want to make sure that all user interface strings in our application are translatable using Drupal's localization system. As a rule, any text you add to templates, or strings you add in render arrays need to be translatable.

Essentially, you want to ensure that any user interface strings *can* be dynamically swapped out for the same string in a different language.

## Internationalizing your code

Any time you display UI text using PHP code in a Drupal module, pass it through either the global `t()` function or the `t()` method on the class, for example:

```
// Simple string.
$build = [
  '#markup' => $this->t('Hello, World!')
];
```

If the string involves plurals (like 1 degree, 2 degrees), it should be passed through either the global `\Drupal\Core\StringTranslation\PluralTranslatableMarkup::createFromTranslatedString()` or a `formatPlural()` method on the class. Classes can use the `\Drupal\Core\StringTranslation\StringTranslationTrait` to get these methods.

Example:

```
use Drupal\Core\StringTranslation\StringTranslationTrait;

class MyClass {
  use StringTranslationTrait;

  public function myMethod() {
    // Simple translation in a render array.
    $output_simple = [
      '#markup' => $this->t('Hello, World!')
    ];

    // With placeholders for dynamic content.
    $output_with_placeholder = [
      '#markup' => $this->t('Hello, @name!', ['@name' => $username])
    ];
    
    // To account for plural variation of the string.
    $output_plural = [
        '#markup' => $this->formatPlural($count, '@count degree', '@count degrees', ['@count' => $count])
    ];

  }
}
```

Pass any dates displayed in the UI through the `'date'` service class' `\Drupal\Core\Datetime\Date::format()` method.

Example:

```
$date_service = \Drupal::service('date');
$formatted_date = $date_service->format($timestamp, 'custom', 'Y-m-d H:i:s', NULL, $langcode);

$output_date = [
  '#markup' => $formatted_date
];
```

For Twig templates, use the `t` or `trans` filters to indicate translatable text. Use the `plural` tag to define a plural variation of a variable's value.

Example:

```
{# Simple translation #}
{{ 'Hello, World!'|t }}

{# With placeholders for dynamic content #}
{{ 'Hello, @name!'|t({'@name': username}) }}

{# Or use the set tag #}
{% set title = '@label Introduction'|t({'@label': node.title.value}) %}
<h1>{{ title }}</h1>

{# Use trans filter for longer texts or with HTML #}
{% trans %}
  Hello, <strong>@name</strong>!
{% endtrans %}

{# With plural variation #}
{% trans %}
There is 1 comment.
{% plural count %}
There are {{ count }} comments.
{% endtrans %}
```

In JavaScript code, use `Drupal.t()` and `Drupal.formatPlural()` to translate UI text.

```
// For a simple translation of a string.
Drupal.t('Hello, World!');

// With placeholders for dynamic content.
Drupal.t('Hello, @name!', {'@name': username});

// Handling plurals.
Drupal.formatPlural(count, '@count apple', '@count apples', {'@count': count});
```

All these methods accept placeholders to allow for substituting dynamic content into a translated string. Placeholders can take the following form:

- `@variable`: Use for most strings, supplied value is escaped using `\Drupal\Component\Utility\Html::escape()`. Can also be used to substitute HTML via `\Drupal\Component\Render\MarkupInterface` objects.
- `%variable`: Escapes and then wraps supplied string in `<em>` tags.
- `:variable`: Supplied string is escaped and filtered for dangerous URL protocols. Use for scenarios where the supplied string is used in an HTML attribute. Example `<a href=":url">Click here</a>`.

For more about how placeholders work see the documentation for [FormattableMarkup::placeholderFormat](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Render%21FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderFormat/).

## Localizing your application's interface

Just because your code allows user interface strings to be translated doesn't mean that they will be. By default, Drupal only uses the string as-entered in your code. Best practice is to use English. To allow users of another language to see the strings in their own language, you'll need to configure Drupal's localization modules. Learn more about doing so in [Chapter 10: Making Your Site Multilingual](https://drupalize.me/course/user-guide/multilingual-chapter) from the Drupal User Guide.

## Recap

In this tutorial, we learned about the difference between internationalization and localization and the role that each plays in allowing an applications interface to be translated. Then, we explored the ways in which user interface strings provided by Drupal modules can be internationalized via functions like `t()`, the use of placeholders for dynamic content, and how to indicate plural variations of strings.

## Further your understanding

- Why is it important to internationalize your code?
- Can you give some example use cases for placeholders in translatable user interface strings?

## Additional resources

- [Translation API overview](https://www.drupal.org/docs/8/api/translation-api/overview) (Drupal.org)
- [Internationalization](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Language%21language.api.php/group/i18n) (api.drupal.org)
- [Chapter 10: Making Your Site Multilingual](https://drupalize.me/course/user-guide/multilingual-chapter) (Drupalize.Me)
- [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable) (Drupalize.Me)
- [Use Drupal.t() for Translatable Strings in JavaScript](https://drupalize.me/tutorial/use-drupalt-translatable-strings-javascript) (Drupalize.Me)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add CSS and JavaScript to a Module's Output](/tutorial/add-css-and-javascript-modules-output?p=3239)

Next
[Output Translatable Strings](/tutorial/output-translatable-strings?p=3239)

Clear History

Ask Drupalize.Me AI

close