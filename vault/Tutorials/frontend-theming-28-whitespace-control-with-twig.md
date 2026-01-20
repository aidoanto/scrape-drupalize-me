---
title: "Whitespace Control with Twig"
url: "https://drupalize.me/tutorial/whitespace-control-twig?p=2464"
guide: "[[frontend-theming]]"
order: 28
---

# Whitespace Control with Twig

## Content

Do you cringe at the sight of untidy whitespace or (*gasp*) no whitespace at all when you View Source? Learn how to tame whitespace in Twig template files in this tutorial. By the end of this lesson, you will be able to recognize how Twig controls whitespace and how you can do the same in your Drupal template files.

## Goal

Understand and apply appropriate methods for controlling whitespace in a template file with Twig.

## Prerequisites

- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)
- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)

## Whitespace inside Twig syntax delimiters

Inside any Twig code delimiter, any extra whitespace won’t affect the HTML output or Drupal’s ability to render any Twig code. However, it’s a good idea to put one space between the Twig delimiters and their contents, for better human-readability.

```
{{ good }}
{{bad}}
```

## Whitespace control in Twig

Whitespace control exists so that you can keep your code readable. One way to enhance readability is by putting Twig statements on their own lines. Another common practice is to put HTML elements on separate lines and indented to show how tags are nested. But these practices can create extra whitespace in the output HTML source, which you can tidy up with Twig's whitespace controls.

But first, we need to understand how Twig normally handles whitespace. While the first newline after a template tag is removed, no further whitespace is modified by Twig. But if you want, you can remove extra whitespace, like spaces, tabs, or newlines from the resulting HTML output.

First, you need to decide whether you want to remove whitespace from **between** HTML tags or **leading or trailing** whitespace on either side of a Twig code delimiter.

To remove whitespace **between** HTML tags, use Twig's `spaceless` filter. This filter will remove all whitespace between HTML tags, excluding spaces inside blocks of text or space inside an HTML tag.

There are 2 ways to use the `spaceless` filter: using the pipe syntax (`|spaceless`), or using the `apply` tag. (The `apply` tag can be used to apply any Twig filter on a large block of HTML in a more readable way.)

### Example with `|spaceless`

```
{{ 
    "<div>
        <strong>bold text goes here</strong>
    </div>
    "|spaceless }}

{# output will be <div><strong>bold text goes here</strong></div> #}
```

### Example with `apply spaceless`

To use spaceless on **large blocks of HTML**, use the `apply` tag with `spaceless`. This will remove whitespace between HTML tags.

```
{% apply spaceless %}
    <div>
        <strong>bold text goes here</strong>
    </div>
{% endapply %}

{# output will be <div><strong>bold text goes here</strong></div> #}
```

## Remove leading or trailing whitespace

To trim leading or trailing whitespace on either side of Twig delimiters, use Twig's whitespace modifier, a dash `-` next to an opening or closing delimiter tag.

Image

![Twig whitespace modifiers](../assets/images/twig-whitespace-modifers.png)

For example, to remove both leading and trailing whitespace on either side of a Twig code block, add a dash inside and next to the Twig delimiter outside of which you want to trim whitespace.

Example from *core/themes/classy/templates/field/field--node--title.html.twig*:

```
<span{{ attributes.addClass(classes) }}>
  {%- for item in items -%}
    {{ item.content }}
  {%- endfor -%}
</span>
```

Output:

Image

![Twig no extra whitespace demo](../assets/images/twig-no-extra-whitespace.png)

Compare with when we remove the whitespace modifier (`-`):

```
<span{{ attributes.addClass(classes) }}>
  {% for item in items %}
    {{ item.content }}
  {% endfor %}
```

Notice the whitespace in the output around the title:

Image

![Twig extra whitespace demo](../assets/images/twig-extra-whitespace.png)

## Guidelines for whitespace in Drupal’s Twig template files

- If you can remove whitespace legibly, do so. For example: Remove the space before attributes `<div{{ attributes }}>`
- Don’t remove or add whitespace in a class attribute. For example: `class="no {{ attributes.class }} no"`. (Instead, learn how to properly [add classes and attributes](https://drupalize.me/tutorial/classes-and-attributes-twig-templates).)
- Keep one space after the opening Twig delimiter and before the closing one.

Source: [Twig's coding standards on Drupal.org](https://www.drupal.org/node/1823416).

## Recap

In this tutorial, we learned how Twig handles whitespace and what we can do to control whitespace in the output of a Twig template file. We learned about the different types of whitespace control, including whitespace between HTML tags and leading/trailing whitespace on either side of a Twig syntax delimiter. By controlling whitespace using the provided tools, we can keep our Twig files readable by putting tags and Twig syntax delimiters on their own lines when it enhances readability.

## Further your understanding

- What do you think is easier to read and understand in a Twig file, the `{% spaceless %}` tag or the dash `-` modifier? Does the Twig coding standards on Drupal.org agree with you?
- In what kinds of situations does the dash `-` modifier make sense to use? Open *core/themes/stable/templates/navigation/links.html.twig*. What characterizes this template file and warrants its liberal use of the dash `-` modifier?

## Additional resources

- Topic: [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- Course: [Using Twig in Drupal Templates](https://drupalize.me/course/using-twig-drupal-templates) (Drupalize.Me)
- Twig 3.x documentation: [spaceless filter](https://twig.symfony.com/doc/3.x/filters/spaceless.html)). (twig.symfony.com)
- Learn about Drupal's coding standards and recommendations regarding whitespace in Twig files on the [Twig coding standards handbook page](https://www.drupal.org/node/1823416). (Drupal.org)
- Change record: [Twig updated from 2.x to 3.x](https://www.drupal.org/node/3256890) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Twig Filters and Functions](/tutorial/twig-filters-and-functions?p=2464)

Next
[Classes and Attributes in Twig Templates](/tutorial/classes-and-attributes-twig-templates?p=2464)

Clear History

Ask Drupalize.Me AI

close