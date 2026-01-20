---
title: "Twig Syntax Delimiters"
url: "https://drupalize.me/tutorial/twig-syntax-delimiters?p=2464"
guide: "[[frontend-theming]]"
order: 23
---

# Twig Syntax Delimiters

## Content

To read a Twig template file, you'll need to recognize Twig's syntax delimiters. Twig has three syntax delimiters: one for printing out variables, another for performing actions or logic, and lastly, one for comments, also used for *docblocks*.

In this tutorial we'll:

- Explore each of Twig's 3 syntax delimiters.
- Show examples of each from Drupal's core template files.

By the end of this tutorial you should be able to recognize each of Twig's syntax delimiters and understand what the engine will do when it encounters them.

## Goal

Recognize each of Twig's 3 syntax delimiters in Drupal template files (*templates/FILENAME.html.twig*).

## Prerequisites

- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)

## Watch: Twig Syntax Delimiters

Sprout Video

## Twig's syntax delimiters

Skip to:

- [Print variables or the results of an expression](#print_variables)
- [Control structures](#control_structures)
- [Comments and docblocks](#comments_and_docblocks)

## Print variables or the results of an expression

To print out a variable or the results of an expression, use the double-curly-brace syntax: `{{ }}`.

### Print out a variable

```
{{ name_of_variable }}
```

For example, print out the `title_prefix` variable:

Line 15 in *core/themes/stable/templates/content/page-title.html.twig*:

```
{{ title_prefix }}
```

Note that the double-curly braces (`{{ }}`) aren't part of the variable name. The double-curly braces are there to wrap the variable name and tell the Twig engine: print this out.

Another example: print out the header region in your theme's *page.html.twig*:

```
<header role="banner">
  {{ page.header }}
</header>
```

[Learn more about accessing values in arrays in Twig](https://drupalize.me/tutorial/arrays-and-objects-twig).

### Print out the results of an expression

When you print out variables using the double-curly-brace syntax, you can apply filters to the variable the result will be output:

```
{{ name_of_variable|name_of_filter }}
```

Or with a filter that accepts arguments:

*core/themes/stable/templates/layout/html.html.twig*

```
<title>{{ head_title|safe_join(' | ') }}</title>
```

You also use the double-curly-brace syntax if you're applying a filter to a string that you want to print out:

```
{{ 'Home'|t }}
```

### Print out a variable appended with a function

```
<div{{ attributes.addClass('banner') }}>
```

Any time you want to output a variable, with or without filters or functions appended to it, use the double-curly-brace syntax.

[Learn more about filters in Twig](https://drupalize.me/tutorial/twig-filters-and-functions).

## Control structures

For control structures, use the curly-brace-percent syntax: `{% %}`.

For example, to set the value of a variable:

```
{%
  set classes = [
    'block',
    'block-' ~ configuration.provider|clean_class,
    'block-' ~ plugin_id|clean_class,
  ]
%}
```

Or, to add a bit of logic to your template with an `if` statement, wrap both `if` and `endif` (and `else` or `elseif`) in `{% %}` on their own lines, around the conditional code block.

```
{% if page.footer %}
  <footer role="contentinfo">
    {{ page.footer }}
  </footer>
{% endif %}
```

Notice that the `if` and `endif` statements are wrapped in their own set of delimiters.

You will need to wrap `if`, `set`, or `block` statements, `for` loops, and other control structures with `{% ... %}`.

This example shows how `if`/`else` statements, `for` loops, `set` and `trans` can be used in a template file. Notice how HTML and `{{ }}` or `{% %}` syntax delimiters are interwoven in this template:

*core/themes/classy/templates/content-edit/node-add-list.html.twig*:

```
{% if types is not empty %}
  <dl class="node-type-list">
    {% for type in types %}
      <dt>{{ type.add_link }}</dt>
      <dd>{{ type.description }}</dd>
    {% endfor %}
  </dl>
{% else %}
  <p>
    {% set create_content = path('node.type_add') %}
    {% trans %}
      You have not created any content types yet. Go to the <a href="{{ create_content }}">content type creation page</a> to add a new content type.
    {% endtrans %}
  </p>
{% endif %}
```

Anything that is a *tag* in Twig will use the `{% %}` delimiter. For the full list of Twig tags (as well as filters and functions), see the section [Twig Reference section on the Twig 3.x Documentation home page](https://twig.symfony.com/doc/3.x/).

## Comments and docblocks

Comments and docblocks in Twig templates are surrounded by `{# #}`. Use this in-line or to make a multiple-line comment. Comments are not executed by the Twig engine, but are used by automated API documentation software to describe system template files.

Docblock comments in a Twig template file follow [Drupal's API and documentation code standards](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards).

All template files should have a docblock at the top, wrapped in `{# #}` describing the template file and which variables are available to it, as in the following example:

*core/themes/stable/templates/content/page-title.html.twig*

```
{#
/**
 * @file
 * Theme override for page titles.
 *
 * Available variables:
 * - title_attributes: HTML attributes for the page title element.
 * - title_prefix: Additional output populated by modules, intended to be
 *   displayed in front of the main title tag that appears in the template.
 * - title: The page title, for use in the actual content.
 * - title_suffix: Additional output populated by modules, intended to be
 *   displayed after the main title tag that appears in the template.
 */
#}
{{ title_prefix }}
{% if title %}
  <h1{{ title_attributes }}>{{ title }}</h1>
{% endif %}
{{ title_suffix }}
```

## Recap

In this tutorial, you learned about the 3 syntax delimiters in Twig. The double-curly-brace syntax `{{ }}` is used for printing out variables or the results of expressions, the curly-brace-percent syntax is used to execute statements, like `if` statements or `for` loops, and the curly-brace-pound `{# #}` syntax is used for comments and docblocks in Drupal's Twig template files.

## Further your understanding

- Use your knowledge of overriding a template files and inspecting variables available in a template, use the appropriate Twig syntax delimiter to print out a variable in a template file that you've overridden in your custom theme.
- In a code editor or IDE, browse through the *template* directories of Drupal's core themes (in *core/themes*) especially Stable, Classy, and Bartik, and notice how Twig syntax delimiters are used in these files.

## Additional resources

- Topic: [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- Course: [Using Twig in Drupal Templates](https://drupalize.me/course/using-twig-drupal-templates) (Drupalize.Me)
- [Twig coding standards](https://twig.symfony.com/doc/3.x/coding_standards.html) (twig.symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Twig in Drupal](/tutorial/twig-drupal?p=2464)

Next
[Arrays and Objects in Twig](/tutorial/arrays-and-objects-twig?p=2464)

Clear History

Ask Drupalize.Me AI

close