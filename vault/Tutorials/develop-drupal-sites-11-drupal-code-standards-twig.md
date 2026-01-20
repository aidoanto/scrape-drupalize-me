---
title: "Drupal Code Standards: Twigfree"
url: "https://drupalize.me/tutorial/drupal-code-standards-twig?p=2458"
guide: "[[develop-drupal-sites]]"
order: 11
---

# Drupal Code Standards: Twigfree

## Content

Twig is the theme template engine in Drupal as of version 8. Like any code, there are guidelines and standards that dictate both the style and the structure of the code. In this tutorial we will explain how to adhere to the Drupal code standards while implementing Twig templating.

By the end of this tutorial you will be able to adhere to Drupal's coding standards when writing Twig, and know where to find more information about the guidelines when necessary.

## Goal

Write Twig code that adheres to Drupal's coding standards.

## Prerequisites

- [What Are Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)
- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)

## Contents

- [The docblock](#docblock)
- [Variables](#variables)
- [Expressions](#expressions)
- [Attributes](#attributes)
- [Whitespace control](#whitespace)
- [Filters](#filters)
- [Comments](#comments)
- [Syntax](#syntax)

## The docblock

Twig files should include a docblock like any other Drupal file. A docblock is a specially formatted block of information that goes at the top of every file, class, and function. See [Code Standards Documentation](https://drupalize.me/tutorial/drupal-code-standards-documentation) to brush up if you’ve forgotten the finer points of docblocks.

Sections such as `@see`, `@ingroup`, etc, still apply as they did before Twig, so use those as appropriate. You can consult [the Drupal documentation](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#templates).

A note on `@ingroup themeable` from Drupal.org:

> Twig template docblocks should only include @ingroup themeable if the template is providing the default themeable output. For themes overriding default output the @ingroup themeable line should not be included.

## Variables

Variables should be referenced only by name, with no prefix. For example, `foo` instead of `$foo` or `{{ foo }}`. The type should not be included, as this does not affect theming.

Here’s an example from [the Token contributed module](https://www.drupal.org/project/token):

```
{#
/**
 * @file
 * Default theme implementation for the token tree link.
 *
 * Available variables:
 * - url: The URL to the token tree page.
 * - text: The text to be displayed in the link.
 * - attributes: Attributes for the anchor tag.
 * - link: The complete link.
 *
 * @see template_preprocess_token_tree_link()
 *
 * @ingroup themeable
 */
#}
{% if link -%}
  {{ link }}
{%- endif %}
```

In the above code, you can see that the docblock lists the available variables. They are listed without a prefix or type. This is the default template, so it uses `@ingroup themeable`. Also notice that there is no period at the end of any line starting with an `@` tag.

Variables referenced inline in a docblock should be wrapped in single quotes.

Here's an example from Drupal core, the Comment module:

```
/*
...
 * - created: Formatted date and time for when the comment was created.
 *   Preprocess functions can reformat it by calling format_date() with the
 *   desired parameters on the 'comment.created' variable.
 * - changed: Formatted date and time for when the comment was last changed.
 *   Preprocess functions can reformat it by calling format_date() with the
 *   desired parameters on the 'comment.changed' variable.
...
*/
```

The above code is from *comment.html.twig*, which has a very lengthy docblock, but you can see from this snippet that these variables are properly referenced and wrapped in single quotes.

## Expressions

Twig makes it easy to check if a variable is available before using it. Just use `if`. Here's an example from Drupal core:

```
  {% if label %}
    <h2{{ title_attributes }}>{{ label }}</h2>
  {% endif %}
```

In the above code, we can see that the code checks for the availability of `label` with `if label` before printing it. This is a lot simpler than previous methods of checking, which required more complex structures and more code.

Loops are also much simpler in Twig. You can easily use `for` loops in Twig. Here's an example from [the Devel contributed module](https://www.drupal.org/project/devel):

```
{% for item in collector.links %}
  <div class="sf-toolbar-info-piece">
    <span><a href="{{ item.url }}" title="{{ item.description|default(item.title) }}">{{ item.title }}</a></span>
  </div>
{% endfor %}
```

The above code will loop through and print out each `item` in `collector.links`.

If you need to use a key and a value in your `for` loop, you can accomplish that as well. Here's an example from [the Ctools contributed module](https://www.drupal.org/project/ctools):

```
{% if trail %}
  &lt;div class="wizard-trail"&gt;
    {% for key, value in trail %}
      {% if key is same as(step) %}
        <strong>{{ value }}</strong>
      {% else %}
        {{ value }}
      {% endif %}
      {% if value is not same as(trail|last) %}
        {{ divider }}
      {% endif %}
    {% endfor %}
  &lt;/div&gt;
{% endif %}
```

In the above code, you can see that `for key, value in trail` gives us the expected key and value pair for a foreach loop, and they can be used throughout the body of the loop.

Another simple expression that can be done in Twig is variable assignment. If a variable is needed only in the template, it can be declared directly, as you would anywhere else. Like this:

```
{% myvariable = 'myvariable value' %}
```

For more on how to translate variables, see [Code Standards `t()` function](https://drupalize.me/tutorial/drupal-code-standards-t-function), and the section on Drupal and Twig.

## HTML attributes

HTML attributes in Drupal are drillable. They can be printed all at once, or one at a time, using dot notation. If you do not print them all, they should all be included at the end, so that any other attributes added by other modules will be included. If you're not familiar with HTML attributes in Twig template files see [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates).

Here's an example from Drupal core:

```
{% if link_path -%}
  <a{{ attributes }}>{{ name }}{{ extra }}</a>
{%- else -%}
  <span{{ attributes }}>{{ name }}{{ extra }}</span>
{%- endif -%}
```

In the above code, the full attributes are printed for the `<a>` and `<span>` tags.

You can also add or remove a class in Twig. For more information see [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates).

```
{%
  set classes = [
    dom_id ? 'js-view-dom-id-' ~ dom_id,
  ]
%}
<div{{ attributes.addClass(classes) }}>
```

In the above code, an array of classes is created and added to the HTML attributes.

## Whitespace control

The `{% spaceless %}` tag removes whitespace between HTML tags. Wrap your code in this tag wherever you want to remove whitespace.

Here’s an example from [the Devel contributed module](https://www.drupal.org/project/devel):

```
{% spaceless %}
  <div class="sf-toolbar-info-piece">
    <b>{{ 'Status'|t }}</b>
    <span class="sf-toolbar-status sf-toolbar-status-{{ request_status_code_color }}">{{ collector.statuscode }}</span> {{ collector.statustext }}
  </div>
  <div class="sf-toolbar-info-piece">
    <b>{{ 'Controller'|t }}</b>
    {{ request_handler }}
  </div>
  <div class="sf-toolbar-info-piece">
    <b>{{ 'Route name'|t }}</b>
    <span>{{ request_route }}</span>
  </div>
{% endspaceless %}
```

The whitespace control character (`-`) removes whitespace at the tag level. Here’s an example from Drupal core:

```
<span{{ attributes }}>
  {%- for item in items -%}
    {{ item.content }}
  {%- endfor -%}
</span>
```

In the above code, we can see the `-` character added to the delimiters, indicating the whitespace should be removed. This can also be used to remove the space from both sides or just one, if the character is only on one side.

For more on whitespace see [Whitespace Control with Twig](https://drupalize.me/tutorial/whitespace-control-twig).

## Caveat regarding newlines at the end of files

Drupal coding standards require that all files have a newline at their end, and if you have PHP CodeSniffer or any other tests set up for Drupal standards, it will flag this as well. However, in Twig, this may not be wanted in your template output. Until a better community-wide solution is reached, you can alter your tests if you need them to pass, or add a twig template tag to the end of the file. For some background, you can read [this issue](https://www.drupal.org/node/2082845) for more clarification.

## Filters

A filter in twig uses the pipe character - `|`. In [Code Standards for the t() function](https://drupalize.me/tutorial/drupal-code-standards-t-function), we talked about using the new `|t` filter to translate text, but there are other filters that you can use as well.

Here's an example from Drupal core:

```
<li class="project-update__release-notes-link">
  <a href="{{ version.release_link }}">{{ 'Release notes'|t }}</a>
</li>
```

In the above code, we can see a simple `|t` filter. The text 'Release notes' is being piped through and is now available for translation, as well as being escaped and safely processed.

There are a variety of [Twig filters](https://twig.symfony.com/doc/3.x/filters/index.html) and [Drupal-specific filters](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/filters-modifying-variables-in-twig-templates).

Here's an example of a Twig filter, `join`, from Drupal core:

```
<div class="sf-toolbar-info-piece">
  <b>{{ 'Roles'|t }}</b>
  <span>{{ collector.roles|join(', ') }}</span>
</div>
```

In the above code, the [`join`](https://twig.symfony.com/doc/3.x/filters/join.html) filter is applied to `collector.roles`. It concatenates the items and separates them with a comma and space, as indicated.

For more on Twig filters see [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions).

## Comments

Comments are wrapped in the Twig comment indicator, `{# ... #}`. Short and long comments use the same indicator, but long comments should be wrapped so that they do not exceed 80 characters per line. Comments on one line should have the indicator on the same line. Comments that span several lines should have the indicators on separate lines.

Here's an example of a short comment from Drupal core, the Field UI module:

```
{# Add Ajax wrapper. #}
```

Here's an example of a long comment from Drupal core, the Book module:

```
{#
  The given node is embedded to its absolute depth in a top level section. For example, a 
  child node with depth 2 in the hierarchy is contained in (otherwise empty) div elements 
  corresponding to depth 0 and depth 1. This is intended to support WYSIWYG output - e.g., 
  level 3 sections always look like level 3 sections, no matter their depth relative to 
  the node selected to be exported as printer-friendly HTML.
#}
```

## Syntax

These standards are taken from the [Twig Documentation](https://twig.symfony.com/doc/3.x/coding_standards.html).

1. Put one (and only one) space after the start of a delimiter (`{{`, `{%`, and `{#`) and before the end of a delimiter (`}}`, `%}`, and `#}`). 1a. When using the whitespace control character, do not put any spaces between it and the delimiter.
2. Put one (and only one) space before and after the following operators: comparison operators (`==`, `!=`, `<`, `>`, `>=`, `<=`), math operators (`+`,`-`, `/`, `*`, `%`, `//`, `**`), logic operators (`not`, `and`, `or`), `~`, `is`, `in`, and the ternary operator (`?:`).
3. Put one (and only one) space after the `:` sign in hashes and `,` in arrays and hashes.
4. Do not put any spaces after an opening parenthesis and before a closing parenthesis in expressions.
5. Do not put any spaces before and after string delimiters.
6. Do not put any spaces before and after the following operators: `|`, `.`, `..`, `[]`.
7. Do not put any spaces before and after the parenthesis used for filter and function calls.
8. Do not put any spaces before and after the opening and the closing of arrays and hashes.
9. Use lowercase and underscored variable names (not camel case).
10. Indent your code inside tags using two spaces, as throughout Drupal.

### Syntax Examples

Here’s an example from Drupal core demonstrating [#1a](#q1a):

```
&lt;article{{ attributes }}&gt;
  {% if content %}
    {{- content -}}
  {% endif %}
&lt;/article&gt;
```

In the above code, on line 3, you can see that there is no space between the delimiter, `{{`, and the whitespace control character, `-`.

Here’s an example from [the Display Suite contributed module](https://www.drupal.org/project/ds) demonstrating [#2](#q2) and [#4](#q4):

```
{% set left = left|render %}
{% set middle = middle|render %}
{% set right = right|render %}
{% if (left and not right) or (right and not left) %}
  {% set layout_class = 'group-one-sidebar' %}
{% elseif (left and right) %}
  {% set layout_class = 'group-two-sidebars' %}
{% elseif (left) %}
  {% set layout_class = 'group-sidebar-left' %}
{% elseif (right) %}
  {% set layout_class = 'group-sidebar-right' %}
{% endif %}
```

In the above code, you can see that all of the comparison operators throughout the snippet have one space on either side. You can also see that the expressions, like `(left and not right)` do not have any spaces after their opening parenthesis or before their closing parenthesis.

Here's an example from Drupal core, the Classy theme, demonstrating [#3](#q3), [#8](#q8):

```
{%
  set row_classes = [
    not no_striping ? cycle(['odd', 'even'], loop.index0),
  ]
%}
```

In the above code, you can see that there are no spaces before or after the opening or closing of the array (`['odd', 'even']`), and there is only one space after the comma in the array.

Here’s an example from [the CTools contributed module](https://www.drupal.org/project/ctools) demonstrating[#1](#q1), [#5](#q5), [#6](#q6), [#9](#q9), [#10](#q10):

```
{% if trail %}
  &lt;div class="wizard-trail"&gt;
    {% for key, value in trail %}
      {% if key is same as(step) %}
        &lt;strong&gt;{{ value }}&lt;/strong&gt;
      {% else %}
        {{ value }}
      {% endif %}
      {% if value is not same as(trail|last) %}
        {{ divider }}
      {% endif %}
    {% endfor %}
  &lt;/div&gt;
{% endif %}
```

In the above code, you can see that there is only one space after the start of the delimiter, `{%` and before the end of the delimiter, `%}`, throughout the code snippet.

On line 7, you can see that there is no space before or after string delimiters `{{ .. }}`.

On line 9, you can see that there is no space on either side of the pipe operator.

Lower-case variable names are used throughout the snipped, as well as proper indentation.

Here’s an example from [the Devel contributed module](https://www.drupal.org/project/devel) demonstrating [#7](#q7):

```
<div class="sf-toolbar-block">
  <div class="sf-toolbar-icon">{{ icon|default('') }}</div>
  <div class="sf-toolbar-info">{{ text|default('') }}</div>
</div>
```

In the above code, you can see that there are no spaces on either sides of the parentheses. The space after is technically the space before the end of the delimiter.

## Recap

In this tutorial we looked at some of the Twig coding standards used inside of all *.html.twig* files in Drupal. These standards start from the the official Twig coding standards, and then add some additional guidelines regarding the use of Twig with Drupal. Namely the docblock at the top of each template file, and how HTML attributes are represented. We also looked at some common syntax patterns and provided examples of how they should be formatted in a Twig template file.

## Further your understanding

- Review the official [Twig coding standards](https://twig.symfony.com/doc/3.x/coding_standards.html) (twig.symfony.org). Drupal inherits these standards, and then adds some of its own.

## Additional resources

- [Drupal Twig standards](https://www.drupal.org/node/1823416) (Drupal.org) - Official Twig standards for Drupal

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Code Standards: The t() Function](/tutorial/drupal-code-standards-t-function?p=2458)

Next
[How to Implement Drupal Code Standards](/tutorial/how-implement-drupal-code-standards?p=2458)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Drupal Training Resources by Alanna Burke of [Chromatic](https://chromatichq.com) are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://chromatichq.com/blog>.

Clear History

Ask Drupalize.Me AI

close