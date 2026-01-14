---
title: "Drupal Code Standards: The t() Functionfree"
url: "https://drupalize.me/tutorial/drupal-code-standards-t-function?p=2458"
guide: "[[develop-drupal-sites]]"
order: 10
---

# Drupal Code Standards: The t() Functionfree

## Content

Translations have their own special functions in both Drupal 7 and 8, and there are some rules for standardizing how they are used that make things clearer for everyone.

In this tutorial we'll look at:

- When to use, and when not to use, translation utilities to output translatable strings
- How placeholders work in translatable strings
- Tips for creating links inside of translatable strings

By the end of this tutorial you should know when, and how, to make strings in your code translatable using Drupal's translation utility functions.

## Goal

Write code that follows Drupal's best practices for ensuring that user-facing strings can be translated.

## Contents

- [What is the `t()` function?](#what)
- [Using placeholders](#placeholders)
- [`t()` and links](#links)
- [Translation best practices](#best-practices)
- [Concatenation dos and don'ts](#concatenation)
- [Drupal and Twig](#twig)

## Prerequisites

- [What Are Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)

## What is the t() function?

The `t()` function allows for localization and translates a given string to a given language at run-time. When coding, you wrap your user-facing strings in this function so that they can be translated.

### When do I use it?

Use it for just about every user-facing string. This ensures that your site can be localized. When in doubt, translate everything. You might be thinking, "Oh, this string will never need to be translated," but 2 years later, when you're trying to find a certain string that's showing up untranslated on the site, and your shareholders want it changed, you'll be much happier if it's already ready to translate. I may be speaking from [experience](https://chromatichq.com/blog/theatermania-lessons-learned-localization) here.

### What does it do?

First, `t()` translates text at runtime if you have more than one language enabled. Depending on which placeholder you use, it runs different sanitization functions.

The function takes 3 parameters, 2 of which are optional. The first is the string to be translated, the second is the array of replacements, if any, and the third is an array of options. Options are defined as:

```
$options: An associative array of additional options, with the following elements:
  * 'langcode' (defaults to the current language): The language code to translate to a language other than what is used to display the page.
  * 'context' (defaults to the empty context): A string giving the context that the source string belongs to.
```

String context (or translation context) is a way to organize translations when words have one-to-many translations.

The Drupal.org handbook [String context page](https://www.drupal.org/node/1369936) states:

> What is string context?
>
> When translating Drupal's user interface to other languages, each original (English) string can have only one translation. This is a problem when one English word has several meanings, like "order", which can mean the order of elements in a list, to order something in a shop, or an order someone has placed in a shop. For many languages, the string "order" needs a different translation for each of these meanings.

### When should I not use it?

In **Drupal 7**, there are some instances where `t()` is not available.

During the installation phase, `t()` isn't available, so you must use [`get_t()`](https://api.drupal.org/api/drupal/includes%21bootstrap.inc/function/get_t/7.x). You can do something like this:

```
$t = get_t();
$t(‘my string');
```

Translation is also not used inside of `hook_schema()` or `hook_menu()`.

In Drupal, [`t()` is always available](https://www.drupal.org/node/2021435), so you can always use it. Though similar to above, there are some instances where you don't need to. These are generally well documented.

## Using placeholders

Placeholders come from [`Drupal\Component\Render\FormattableMarkup::placeholderFormat()`](https://api.drupal.org/api/drupal/core!lib!Drupal!Component!Render!FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderFormat/) ([`format_string`](https://api.drupal.org/api/drupal/includes%21bootstrap.inc/function/format_string/7.x) in Drupal 7).

The most common placeholder is probably `@variable`. This placeholder runs [`Drupal\Component\Render\FormattableMarkup::placeholderEscape()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Render%21FormattableMarkup.php/function/FormattableMarkup%3A%3AplaceholderEscape/) on the text before replacing it. Never pass a variable through `t()` directly -- only string literals. The short explanation for this is that the string to be translated needs to be available at runtime, and a variable may not be available or may change its value. You can find an in-depth explanation [in this Stack Exchange thread](http://drupal.stackexchange.com/questions/9362/is-it-always-bad-to-pass-a-variable-through-t).

You use a placeholder to insert a value into the translated text, like in this example from the [Advanced Forum contributed module](https://www.drupal.org/project/advanced_forum):

```
$block->title = t(
  'Most active poster in @forum', array('@forum' => $forum->name)
);
```

You may also use `%variable`, which both escapes the text and formats it as emphasized text.

The **Drupal 7** `!variable`, which inserts your value exactly as is, without running any sanitization functions, was **deprecated**. Use `:variable` instead.

The `:variable` placeholder is escaped with [`\Drupal\Component\Utility\Html::escape()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Utility%21Html.php/function/Html%3A%3Aescape/) and filtered for dangerous protocols using [`UrlHelper::stripDangerousProtocols()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Utility%21UrlHelper.php/function/UrlHelper%3A%3AstripDangerousProtocols/).

The `:variable` placeholder is meant to be used to filter URIs.

## t() and links

There are a lot of times that you may want to translate the text in a link. There are a lot of ways to do this, and most of them aren't the best way. Here are some bad examples, and a good (and simple!) one.

Bad:

```
$do_not_do_this = t('Do not ')."&lt;a href="api.drupal.org"&gt;" . t('link ') . "&lt;/a&gt;"  .t('to something like this.');
```

```
$bad = t('This is not a good way to make a @link.', array('@link' => '&lt;a href="https://api.drupal.org"&gt;'. t('link') .'&lt;/a&gt;'));
```

```
$dreadful = t('This is a dreadful way to make a link pointing to the &lt;a href="https://api.drupal.org"&gt;Drupal API t() documentation&lt;/a&gt;.');
```

```
$awful = t('This may seem good, but it's an awful way to link to this @doc.', array('@doc => l(t(‘documentation'), 'https://api.drupal.org'));
```

Good:

```
$good = t('Read about the t() function <a href=":api">here</a>', [':api' => Drupal\Core\Url::fromUri('https://api.drupal.org')]);
// Drupal 7
$good = t('Read about the t() function <a href="!api">here</a>', array('!api' => 'https://api.drupal.org'));
```

Here's an example from Drupal core, in the function [`install_check_translations()`](https://api.drupal.org/api/drupal/core%21includes%21install.core.inc/function/install_check_translations/) in `install.core.inc`:

```
// If the translations directory is not readable, throw an error.
    if (!$readable) {
      $requirements['translations directory readable'] = array(
        'title'       => t('Translations directory'),
        'value'       => t('The translations directory is not readable.'),
        'severity'    => REQUIREMENT_ERROR,
        'description' => t('The installer requires read permissions to %translations_directory at all times. The <a href=":handbook_url">webhosting issues</a> documentation section offers help on this and other topics.', array('%translations_directory' => $translations_directory, ':handbook_url' => 'https://www.drupal.org/server-permissions')),
      );
    }
```

In this code you can see that the `<a href>` tags are inside the `t()` function, and the URL is escaped using the `:variable` placeholder.

It's okay to put a little HTML in your `t()` function to simplify this. The element can easily be moved around if the translation requires it, without needing to know any code other than which word is being linked. Our next section will talk more about keeping your text translatable.

## Translation best practices

Writing your code and content to be translatable isn't just a best practice, it may very well be used to actually translate your site! Sometimes you need to think from the point of view of a translator. Try not to abstract pieces of content too much. Here's an example. In English, you may have a blog titled "Bob's Homepage." You might abstract that into the following:

```
$username . "'s " . t('Homepage.');
```

What's the problem here? In other languages, this phrase may be re-arranged. For example, in French or Spanish, it would be "Homepage de Bob." The above example would require a translator to change the code. We don't want that. So we write this:

```
t("@username's Homepage.", ['@username' => 'Bob']);
```

Now this string can easily be changed to:

```
t('Homepage de @username.', ['@username' => 'Bob']);
```

## Concatenation dos and don'ts

In the example in the previous section, we showed where concatenating a translated string with another string can make trouble. There are some other things you want to avoid.

Don't concatenate strings within `t()`. For example, don't do this:

```
t("Don't try to join" . ' ' . @num . ' ' . 'strings.', ['@num' => 'multiple']);
```

Even if you think you have to, there is a better way.

And don't concatenate `t()` strings and variables - you don't need to!

Don't do this:

```
t('This is a complicated way to join ') . $mystring . t(' and translated strings');
```

Additionally, the above would give you a CodeSniffer error because you should not have leading or trailing whitespace in a translatable string.

Do this:

```
t('This is a simple way to join @mystring and translated strings', ['@mystring' => 'whatever my string is']);
```

This is how the `t()` function is designed to be used. Going around it defeats the purpose of using it at all.

## Drupal and Twig

The essential function and its use are the same. Wrap text in your module code in `t('')`, with the same optional placeholder and options arrays. As noted in the placeholders section, `!variable` has been deprecated and replaced with `:variable`.

In Drupal we use the Twig templating engine, and with that, new ways to format our text for translation.

The simplest way is to pipe your text through `|t`. Here's an example from the [Devel contributed module](https://www.drupal.org/project/devel):

```
<thead>
 <tr>
    <th>{{ 'Name'|t }}</th>
    <th>{{ 'Path'|t }}</th>
    <th>{{ 'Info file'|t }}</th>
  </tr>
</thead>
```

In the above code, we can see the text in the table headers piped into the translation function, just as it would be passed through `t()` in Drupal 7. You can also use `|trans` interchangeably with `|t`. You can use a `{% trans %}` block to translate a larger chunk of text or use placeholders. These blocks can also handle logic for plurals. Here's an example from Drupal core:

```
<h3 class="views-ui-view-title" data-drupal-selector="views-table-filter-text-source">{{ view.label }}</h3>
<div class="views-ui-view-displays">
  {% if displays %}
    {% trans %}
      Display
    {% plural displays %}
      Displays
    {% endtrans %}:
    <em>{{ displays|safe_join(', ') }}</em>
  {% else %}
    {{ 'None'|t }}
  {% endif %}
</div>
```

Here we can see that the template appropriately shows the translated text for “Display” or the plural, “Displays.”

Here is the explanation from [Drupal.org's localization documentation](https://www.drupal.org/developing/api/8/localization):

> Values are escaped by default. The 'passthrough' filter can be used to skip escaping. The 'placeholder' filter can be used to form a placeholder. The default behavior is equivalent to @ in t(), while 'passthrough' matches ! and 'placeholder' matches %.

This comes from Twig, and is not yet commonly used in Drupal, but its usage with placeholders is similar to `t()`. Here's an example from Drupal core:

```
 {% set includes = includes|join(', ') %}
  {% if disabled %}
    {{ 'Includes:'|t }}
    <ul>
      <li>
        {% trans %}
          Enabled: {{ includes|placeholder }}
        {% endtrans %}
      </li>
      <li>
        {% set disabled = disabled|join(', ') %}
        {% trans %}
          Disabled: {{ disabled|placeholder }}
        {% endtrans %}
      </li>
    </ul>
  {% else %}
    {% trans %}
      Includes: {{ includes|placeholder }}
    {% endtrans %}
  {% endif %}
</div>
```

In the above code, we can see the use of the placeholder in Twig. The `set` lines set the placeholders to be used later in the code. The `|placeholder` filter indicates that a replacement is to be made.

Learn more in our tutorial [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable).

## Recap

This tutorial shows a lot of what *not* to do, but you'll run into a lot of creatively incorrect code when it comes to translation, and now you'll know it when you see it. Simple is best. If you remember that this function exists to give translators a list of strings to translate, then you'll be in the right frame of mind when assembling these strings to keep them flexible and translatable.

## Further your understanding

- In the above examples that demonstrate how not to create links, can you explain what is wrong with each example?
- How do each of the `@`, `%`, and `:` style placeholders differ from one another?

## Additional resources

- [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable)
- [Use Drupal.t() for Translatable Strings in JavaScript](https://drupalize.me/tutorial/use-drupalt-translatable-strings-javascript)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Code Standards: Object-Oriented Programming](/tutorial/drupal-code-standards-object-oriented-programming?p=2458)

Next
[Drupal Code Standards: Twig](/tutorial/drupal-code-standards-twig?p=2458)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Drupal Training Resources by Alanna Burke of [Chromatic](https://chromatichq.com) are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://chromatichq.com/blog>.

Clear History

Ask Drupalize.Me AI

close