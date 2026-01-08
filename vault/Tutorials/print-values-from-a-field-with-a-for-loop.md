---
title: "Print Values from a Field with a For Loop"
url: "https://drupalize.me/tutorial/print-values-field-loop?p=2464"
guide: "[[frontend-theming]]"
---

# Print Values from a Field with a For Loop

## Content

The ability to loop over an array of values in a Twig template and print out each value individually is an important skill for anyone developing themes for Drupal. Common scenarios include: loop over the values of a multiple value field; iterate through a list of links; and display error messages at the top of forms. This tutorial will provide an example of using the Twig `for` function to iterate over a list, or a subset of a list.

In this tutorial we'll cover how to:

- Output values from a multi-value field in an unordered list.
- Add first and last classes to the first and last items in a list by using the Twig `loop` variable.

By the end of this tutorial you should be able to print out the values of an array as individual list items using a loop in Twig.

## Goal

Use a `for` loop in a Twig template to print out values in a list or array.

## Prerequisites

- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)
- [Install and Uninstall Themes](https://drupalize.me/tutorial/download-install-and-uninstall-themes)
- [Configure Your Site for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file)

In order to examine how loops work in Twig templates, let's make some changes to the template used to output a set of tags on a blog post. This serves as a good example because a tag field generally has multiple values which are passed to Twig as an array.

This tutorial assumes that you've got a content type on your site named Blog Post (blog\_post) with a field attached to it named Tags (field\_tags).

The default output for multi-value fields uses nested divs. In our template we will print the list of tags in an unordered list, and apply a **first** and **last** class to the first and last elements in the list.

### Create a template file

Start by creating a new template file. We will use the *core/modules/system/templates/field.html.twig* base file as a starting point, and create a new file by copying the base file to *themes/icecream/templates/field--node--field-tags--blog-post.html.twig*. See [Override a Template File](https://drupalize.me/tutorial/override-template-file) if this process is new to you.

### Loop over the field variable

Create an unordered list using a `for` loop:

```
  <ul class='blog-post__tags field__items'>
    {% for item in items %}
      <li{{ item.attributes.addClass('blog-post__tag') }}>{{ item.content }}</li>
    {% endfor %}
  </ul>
```

Anytime you're dealing with the values of a field inside of a field template file, the `items` array contains all of the values set for that field, even if it's just one value. Each row of the `items` array contains an `item.content` and an `item.attributes` property. This is true of any field type.

### Add first/last classes

Use the special `loop` variable to determine when this is the first or last iteration and add new first/last classes to the appropriate list items.

Inside each `for` loop Twig creates a `loop` variable with contextual information for that specific block. This includes `loop.first`, and `loop.last` which are set to TRUE if the current iteration through the loop is the first, or last, respectively.

Example:

```
  <ul class='blog-post__tags field__items'>
  {% for item in items %}
    {% if loop.first %}
      <li{{ item.attributes.addClass(['blog-post__tag', 'first']) }}>{{ item.content }}</li>
    {% elseif loop.last %}
      <li{{ item.attributes.addClass(['blog-post__tag', 'last']) }}>{{ item.content }}</li>
    {% else %}
      <li{{ item.attributes.addClass('blog-post__tag') }}>{{ item.content }}</li>
    {% endif %}

  {% endfor %}
  </ul>

This should result in output like the following:

  <ul class='blog-post__tags field__items'>
    <li class="blog-post__tag first">drupal</li>
    <li class="blog-post__tag">weekly updates</li>
    <li class="blog-post__tag">unicorns</li>
    <li class="blog-post__tag last">chad</li>
  </ul>
```

Your final template file should include output for the field label and element attributes. Here's an example of the complete template:

(Note: The tilde (`~`) is the concatenation operator in Twig. See also the tutorial [Twig Tricks and HTML Escaping](https://drupalize.me/videos/twig-tricks-and-html-escaping).)

```
  {#
  /**
   * @file
   * Theme override for a field, specific to the tags field on blog posts.
  #}
  {%
  set classes = [
  'field',
  'field--name-' ~ field_name|clean_class,
  'field--type-' ~ field_type|clean_class,
  'field--label-' ~ label_display,
  ]
  %}
  {%
  set title_classes = [
  'field__label',
  label_display == 'visually_hidden' ? 'visually-hidden',
  ]
  %}

  <div{{ attributes.addClass(classes) }}>
    {% if not label_hidden %}
      <h3{{ title_attributes.addClass(title_classes) }}>{{ label }}</h3>
    {% endif %}
    <ul class='blog-post__tags field__items'>
      {% for item in items %}
        {% if loop.first %}
          <li{{ item.attributes.addClass(['blog-post__tag', 'first']) }}>{{ item.content }}</li>
        {% elseif loop.last %}
          <li{{ item.attributes.addClass(['blog-post__tag', 'last']) }}>{{ item.content }}</li>
        {% else %}
          <li{{ item.attributes.addClass('blog-post__tag') }}>{{ item.content }}</li>
        {% endif %}

      {% endfor %}
    </ul>
  </div>
```

Sprout Video

## Recap

In this tutorial we learned how to use the `for` function to loop over an array (or other list variable) and output then print out the individual items inside an `<li>` tag. We also learned about the `loop` variable that exists inside the scope of every `for` loop and provides additional context about the current iteration. This allows us to do things like know if an item is the first or last, or how many items are in the array.

## Further your understanding

- What happens if you try to loop over a variable that is not an array? What happens if you try and loop over an object like `{{ node }}` in the node template?

## Additional resources

- [Loops and Iterators in Twig](https://drupalize.me/tutorial/loops-and-iterators-twig) (Drupalize.Me)
- [Twig `for` tag documentation](https://twig.symfony.com/doc/3.x/tags/for.html) (twig.symfony.com)

## Continue to explore Twig in Drupal

- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Basics](https://drupalize.me/tutorial/twig-syntax-delimiters)
- [Arrays and Objects in Twig](https://drupalize.me/tutorial/arrays-and-objects-twig)
- [Loops and Iterators in Twig](https://drupalize.me/tutorial/loops-and-iterators-twig)
- [Use a For Loop to Print Values from a Field](https://drupalize.me/tutorial/print-values-field-loop) (You are here.)
- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable)
- [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates)
- [How to Find a Route in Drupal](https://drupalize.me/tutorial/how-find-route-drupal) (Drupalize.Me)
- [Create Links with Twig in a Template File](https://drupalize.me/tutorial/create-links-twig-template-file) (Drupalize.Me)
- [Twig Template Inheritance](https://drupalize.me/tutorial/twig-template-inheritance)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Loops and Iterators in Twig](/tutorial/loops-and-iterators-twig?p=2464)

Next
[Twig Filters and Functions](/tutorial/twig-filters-and-functions?p=2464)

Clear History

Ask Drupalize.Me AI

close