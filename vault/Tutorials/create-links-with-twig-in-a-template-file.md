---
title: "Create Links with Twig in a Template File"
url: "https://drupalize.me/tutorial/create-links-twig-template-file?p=2464"
guide: "[[frontend-theming]]"
---

# Create Links with Twig in a Template File

## Content

If you want to create a link to an internal page in a Twig template--and there's not already a variable in the template that contains the URL you want to link to--you'll need to determine the *route* of the thing you want to link to and then use the Twig `url()` or `path()` functions to generate appropriate URLs. In most cases when you want to create a link to an entity that is being output by the current template there's an existing helper variable to use. For example, in a *node.html.twig* template file there's a `url` variable that points to the current node. For other scenarios, like hard-coding a link to the */about* page, you'll need to do a little more work.

In this tutorial, we'll:

- Get the absolute URL value
- Get the relative path value
- Generate HTML for a link
- Get the URI to a file, like an image in the Media library
- Get the active theme path

By the end of this tutorial you should be able to create links to any internal page via Twig.

## Goal

With the *route* of an internal page, create a link to it in a Twig template.

## Prerequisites

- [How to Find a Route in Drupal](https://drupalize.me/tutorial/how-find-route-drupal)
- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions)

## Check for an existing variable

If you're editing a template for a specific entity type, like a content type, there will almost always be a variable already set up containing the value of the URL to the current entity. [Inspect the variables in a template](https://drupalize.me/tutorial/inspect-variables-available-template) or check the documentation in the comments of the file for an existing variable containing the URL value. For example, in the core Olivero theme's node template file, a variable called `url` stores a string value of the URL for the node being viewed. If you're [overriding that template](https://drupalize.me/tutorial/override-template-file), you'll also have access to this variable. Here it is being used inside the `href` attribute of an anchor tag:

```
<h2{{ title_attributes.addClass('node__title') }}>
  <a href="{{ url }}" rel="bookmark">{{ label }}</a>
</h2>
```

If you don't already have a URL variable, then read on to learn how to get URL and path-related values in a Twig template.

## What is a route?

Drupal-specific Twig functions like `url()` and `path()` require you to pass in the route name. A route is the configuration that declares the existence of a path (or URL) and tells the system which code to call to generate the content for that path. Each route has a name, and optionally parameters and options. They are defined by modules in a *MODULE\_NAME.routing.yml* file.

If you're editing a template file, and you need a URL to use for a link or path, you'll need to know how to [find the route for the destination](https://drupalize.me/tutorial/how-find-route-drupal). You'll pass that route name as an argument into the `url()` or `path()` Twig functions. Each of these functions are smart about converting a canonical path like *node/42* to a URL alias like */about*.

## Common function arguments: route, parameters, options

The Drupal-specific Twig functions `url()` and `path()` use common arguments:

- `$route_name`: [The name of the route](https://drupalize.me/tutorial/how-find-route-drupal).
- `$parameters`: An associative array of route parameter key names and values. Parameters that reference [placeholders](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes) will be substituted per the route definition. Extra parameters are added as query strings to the URL.
- `$options`: An associative array of additional URL options. **The `absolute` option is forced to be TRUE in the `url()` Drupal-specific Twig function**. Options include:
  - `'query'`: An array of query key/value-pairs (without any URL-encoding) to append to the URL.
  - `'fragment'`: A fragment identifier (named anchor) to append to the URL. Do not include the leading '#' character.
  - `'absolute'`: Forced to be TRUE in Twig's `url()` function. Whether to force the output to be an absolute link (beginning with `http:`). Useful for links that will be displayed outside the site, such as in an RSS feed.
  - `language`: An optional language object used to look up the alias for the URL. If `$options['language']` is omitted, it defaults to the current language declared in the constant, [LanguageInterface::TYPE\_URL](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Language%21LanguageInterface.php/constant/LanguageInterface%3A%3ATYPE_URL/).
  - `https`: (`TRUE` or `FALSE`) Whether this URL should point to a secure location. If not defined, the current scheme is used. `TRUE` enforces `HTTPS` and `FALSE` enforces `HTTP`.

## Generate an absolute URL

- Use `url($route_name, $parameters = array(), $options = array())`.
- The `url()` function generates an absolute URL given a route name and parameters.

```
{# Generic example #}
{%
  set url_generic_example = url('route.name', {'paramKey': 'paramValue'}, {'optionKey': 'optionValue'})
%}

{# Absolute URL with fragment example (jump link) #}
{%
  set url_fragment_example = url('user.admin_permissions', {}, {'fragment': 'module-node'})
%}

{# Absolute URL to RSS feed #}
{%
  set rss_feed_url = url('view.frontpage.feed_1')
%}

{# Usage: #}
<a href="{{ url_generic_example }}">Link Text</a>
<a href="{{ url_fragment_example }}">Configure Node module permissions</a>
<a href="{{ rss_feed_url}}">RSS feed</a>
```

## Generate a relative URL

- Use `path($route_name, $parameters = array(), $options = array())`
- Generates a *relative URL* given a route name and parameters.
- Best used when you want to create links internal to your site.

Example: Link to the home page

```
<a href="{{ path('<front>') }}">
  {{ 'Home'|t }}
</a>

# Output:
<a href="/">Home</a>
```

Example: Link to a specific node

```
<a href="{{ path('entity.node.canonical', {'node': node.id}) }}">
  {{ 'Read more'|t }}
</a>

# Output:
<a href="/node/42">Read more</a>

# If the node being viewed has a URL alias, the alias will be used.
<a href="/blog/2016-03-04/blog-post-title">Read more</a>
```

Example: Link to a specific user's profile page

```
<a href="{{ path('entity.user.canonical', {'user': user.id}) }}">
  {{ 'User profile'|t }}
</a>

# Output:
<a href="/user/42">User profile</a>
```

## Generate HTML for a link

- Use `link($text, $uri, $attributes)` to generate a link that includes link text, a URI, and (optionally) other attributes.
- Assumes you already have variables for the title, URI, and attribute values.
- Best used when you want to generate all the HTML for a link.

Usage:

```
{{ link(item.title, item.uri, { 'class':['foo', 'bar', 'baz']} ) }}
```

Example from *core/modules/book/templates/book-tree.html.twig*:

```
{% for item in items %}
  <li{{ item.attributes }}>
    {{ link(item.title, item.url) }}
      {% if item.below %}
        {{ book_tree.book_links(item.below, attributes, menu_level + 1) }}
      {% endif %}
  </li>
{% endfor %}
```

## Get the path to the active theme

In Drupal 7, there is `path_to_theme()` and `$theme_path` to get the path of the active theme in a template. The current equivalent is `{{ active_theme_path }}`.

Usage:

```
{{ active_theme_path }}
```

Example:

```
<div class="menu-main-togglewrap">
  <button type="button" name="menu_toggle" class="menu-main-toggle" data-drupal-selector="menu-main-toggle" aria-label="Toggle the menu">{% include active_theme_path() ~ '/images/svg/menu-icon.svg' %}</button>
</div>
```

### Get the URI to a file

- Use `file_url($uri)`
- Accepts a URI to a file and creates a relative URL path to the file.

Usage:

```
{{ file_url(node.field_example_image.entity.uri.value) }}
```

Example:

```
{% set background_image = file_url(content.field_media_image[0]['#media'].field_media_image.entity.uri.value) %}
```

## Recap

In this tutorial, we learned about Drupal-specific Twig functions that are used to generate links and URLs in Twig files.

## Further your understanding

- What is the difference between the `url()` and `path()` Twig functions?
- Read more about the decision to standardize on using route names for links instead of paths in [this issue](https://www.drupal.org/node/2073811). Warning: it's long.
- Custom Twig functions are defined by extending *Twig\Extension\AbstractExtension*. Dig into the code behind Drupal's Twig functions in *Drupal\Core\Template\TwigExtension*.

## Additional resources

- Topic: [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- Course: [Using Twig in Drupal Templates](https://drupalize.me/course/using-twig-drupal-templates) (Drupalize.Me)
- [Functions in Twig Templates](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/functions-in-twig-templates) (Drupal.org)
- [Generate URLs and Output Links](https://drupalize.me/tutorial/generate-urls-and-output-links) (Drupalize.Me)
- [Inspect Variables Available in a Template](https://drupalize.me/tutorial/inspect-variables-available-template) (Drupalize.Me)
- [Concept: Routes](https://drupalize.me/tutorial/concept-routes) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Classes and Attributes in Twig Templates](/tutorial/classes-and-attributes-twig-templates?p=2464)

Next
[Twig Template Inheritance](/tutorial/twig-template-inheritance?p=2464)

Clear History

Ask Drupalize.Me AI

close