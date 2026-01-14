---
title: "Twig Template Inheritance"
url: "https://drupalize.me/tutorial/twig-template-inheritance?p=2464"
guide: "[[frontend-theming]]"
order: 31
---

# Twig Template Inheritance

## Content

More often than not, templates in a theme share common elements: the header, footer, sidebar, or more. In Drupal, themes created with a Twig template can be decorated by another one. This template inheritance allows you to build a base "layout" template that contains all the common elements of your layout defined as blocks. A child template can extend the base layout and override any of its defined blocks. This helps prevent code duplication, and keeps your theme more organized.

This tutorial is for theme developers who want to reduce code duplication in their themes, or anyone seeking to better understand how Twig template inheritance works. We'll cover:

- What the Twig `block` and `extends` tags do
- An example use-case for template inheritance
- How to extend a Twig template from another theme or module
- How to include other Twig templates

## Goal

Learn how to reduce code duplication in your theme and understand how Drupal themes utilize Twig's `block` and `extends` tags.

## Prerequisites

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Inspect Variables Available in a Template](https://drupalize.me/tutorial/inspect-variables-available-template)
- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)

Sprout Video

## What is the `extends` tag in Twig?

The Twig `extends` tag can be used to create a parent/child relationship between two Twig templates, and works in conjunction with `block` tags to define parts of the parent template that can be overridden by the child template. This is easiest to understand with a simple example.

### block.html.twig

```
<div class="block">
  <h2>{{ label }}</h2>
  {% block content %}
    {{ content }}
  {% endblock %}
</div>
```

In this example template, the `{% block content %}` tag is used to define a single region named *content* that child templates can optionally override, as well as a default value to use, `{{ content }}`, if the template is used directly without being extended. When Drupal goes to display a block it will use the list of available [theme hook suggestions](https://drupalize.me/tutorial/what-are-template-files) for the block being displayed. In most cases this will just use the above *block.html.twig* template. In our theme, we might have a template named *block--system-branding-block.html.twig*, so when the system branding block is displayed that template is used instead.

If all we want to do is change the markup used in the main content area--rather than duplicate the *block.html.twig* template above--we can extend it, and override just the parts we care about.

### block--system-branding-block.html.twig

```
{% extends "block.html.twig" %}

{% block content %}
  <div class="system--branding-wrapper">{{ content }}</div>
{% endblock %}
```

Image

![Twig Template Inheritance illustrated](../assets/images/twig-template-inheritance.png)

In this case, the content inside the `block` tag in our child template will be used in place of whatever is inside the `block` in the parent template. This allows us to override the parts we care about, without needing to duplicate the rest of the template.

The official [Twig extends documentation](https://twig.symfony.com/doc/3.x/tags/extends.html) is really good, and worth reading.

For examples of `extends` being used in Drupal, look at the templates provided by the core Block module.

## A word of caution

A template that extends another template cannot have a body of its own. All content in the child template must be contained within block tags. Any content outside of block tags will cause Twig to throw a `Twig_Error_Syntax` exception.

```
{% extends "block.html.twig" %}

<p>This paragraph is outside of a block tag and will cause an error!</p>

{% block content %}
  <div class="system--branding-wrapper">{{ content }}</div>
{% endblock %}
```

## Specify the parent template file

The `extends` tag takes a single argument: a path to the template that is being extended.

This can be a relative path. This example assumes that *block.html.twig* is in the same directory as the extending template.

```
{% extends "block.html.twig" %}
```

You can also use namespaced paths, like this:

```
{% extends "@classy/block/block.html.twig" %}
```

In this case, `@classy` is the name of the theme or module that contains the template you want to extend with an "@" prefix. Twig will automatically expand this alias to point to the templates subdirectory of the module or theme. So, here, the template being extended is */core/themes/classy/templates/block/block.html.twig*. You should use `@namespace` paths whenever you're referencing a template from another theme or module. You don't need to use it if you're referencing a template in your own theme.

If you want to know more about how this works, Drupal module and theme namespaces are added by [Drupal\Core\Template\Loader\FilesystemLoader::\_construct](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21Loader%21FilesystemLoader.php/function/FilesystemLoader%3A%3A__construct/). These namespaces are then used by Twig when loading files in [FilesystemLoader::parseName](https://api.drupal.org/api/drupal/vendor%21twig%21twig%21src%21Loader%21FilesystemLoader.php/function/FilesystemLoader%3A%3AparseName/9.0.x).

## Examples in Drupal core themes

You can find examples of Twig's `block` and `extends` tags in use in Drupal core themes, commonly in templates related to Drupal's block system (not to get the two uses of the word "block" confused!)

For example, in *core/themes/classy/templates/block/* you'll find *block.html.twig*. This template defines the template or base layout for blocks and indicates with Twig's `block` tag where the `block content` should go from any template file that `extends` this particular template.

All other files in this directory use `extends` and define the Twig `block` named `content`.

This pattern is repeated in the core themes Bartik and Stable.

## Tips for using extends

When working with template inheritance, here are some additional tips to keep in mind:

- Templates can use as many levels of inheritance as you want, but each child template can only have a single parent.
- The `{% extends %}` tag **must** be the first tag in that template.
- Child templates don't have to define all parent blocks, so create as many blocks in your base templates as you want and give each a sensible default.
- If you find yourself duplicating content in a number of templates, it probably means you should move that content to a `{% block %}` in a parent template.
- A child template can get the content of a block from the parent template using the `{{ parent() }}` function. This is useful if you want to add to the contents of a parent block instead of completely overriding it.

## Include other Twig templates

You can use Twig's `include` function to include templates on select pages. Learn about Twig's `include` function in the tutorial, [Include Other Twig Templates](https://drupalize.me/videos/include-other-twig-templates). Also check out these 3 examples of the use of `include` in Drupal core themes:

*core/themes/seven/templates/image-widget.html.twig*:

```
{% include '@classy/content-edit/image-widget.html.twig' %}
{{ attach_library('classy/image-widget') }}
```

Note again in the above example, `@classy` is the name of the theme or module that contains the template you want to extend with an "@" prefix. Twig will automatically expand this alias to point to the templates subdirectory of the module or theme.

*core/themes/classy/templates/content/links--node.html.twig*:

```
{% if links %}
  <div class="node__links">
    {% include "links.html.twig" %}
  </div>
{% endif %}
```

*core/themes/stable/templates/admin/field-ui-table.html.twig*:

```
{# Add Ajax wrapper. #}
<div id="field-display-overview-wrapper">
  {% include 'table.html.twig' %}
</div>
```

## Template inheritance with base themes

Another type of template inheritance is possible in Drupal by using base themes. Learn more about base themes in these related tutorials:

- [Theme Inheritance with Base Themes](https://drupalize.me/tutorial/theme-inheritance-base-themes)
- [Drupal Base Themes: Stable and Classy](https://drupalize.me/tutorial/drupal-base-themes-stable-and-classy)
- [Use a Base Theme](https://drupalize.me/tutorial/use-base-theme)

## Recap

In this tutorial, we sought to understand how Twig template inheritance works to reduce code duplication. We learned:

- What the Twig `block` and `extends` tags do
- An example use-case for template inheritance
- How to extend a Twig template from another theme or module
- How to include other Twig templates

## Further your understanding

- Can you create a *node.html.twig* file in your theme with a `block` for the main content area, and then a *node--article.html.twig* template that uses an `extends` tag to wrap the main content of article nodes in an additional `<div>` tag?
- In addition to `extends`, Twig also has an `include` tag. Can you explain the difference between `extends` and `include` and define a use-case for each?
- Explore how Classy, Bartik and Stable core themes makes use of `extends` in block templates.

## Additional resources

- Topic: [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- Course: [Using Twig in Drupal Templates](https://drupalize.me/course/using-twig-drupal-templates) (Drupalize.Me)
- [Twig extends documentation](https://twig.symfony.com/doc/3.x/tags/extends.html) (twig.symfony.com)
- [Twig block documentation](https://twig.symfony.com/doc/3.x/tags/block.html) (twig.symfony.com)
- The Symfony documentation has [a good explanation of how Twig extends are used in the Symfony Framework](https://symfony.com/doc/current/templates.html#template-inheritance-and-layouts).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create Links with Twig in a Template File](/tutorial/create-links-twig-template-file?p=2464)

Clear History

Ask Drupalize.Me AI

close