---
title: "Twig Filters and Functions"
url: "https://drupalize.me/tutorial/twig-filters-and-functions?p=2464"
guide: "[[frontend-theming]]"
---

# Twig Filters and Functions

## Content

In Twig, you can modify variables using functions or filters. Twig has a bunch of built-in [functions](https://twig.symfony.com/doc/3.x/functions/index.html) and [filters](https://twig.symfony.com/doc/3.x/filters/index.html). Drupal extends Twig to provide a few handy Drupal-specific functions and filters.

In this tutorial, we'll look at:

- What are functions and filters?
- How to use functions and filters in Twig
- Detailed information about the Drupal-specific functions and filters, and their use case

## Goal

Understand how functions and filters work in Twig.

## Prerequisites

- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Basics](https://drupalize.me/tutorial/twig-syntax-delimiters)

## Get the most out of this tutorial

This tutorial contains both a video and a written component. The video tutorial describes Twig functions and filters in the context of a generic PHP application. Watch the video to get an overview of how Twig functions and filters work. Then, read on to learn about Drupal-specific Twig functions and filters and how Drupal both implements Twig and extends it using the `TwigExtension` class.

Sprout Video

## Twig function basics

Functions in Twig work just like functions in other languages, like PHP or JavaScript. You can call them in either a say-something Twig delimiter `{{ random() }}` or in an `if` statement in a do-something delimiter `{% if random(10) < 5 %}`. You can see what parameters are available for Twig functions in the Twig documentation for each function.

## Drupal-specific Twig functions

Drupal provides some Drupal-specific Twig functions that should be called within a Twig file. These correspond to PHP methods in Drupal. You can't just call any Drupal API method in a Twig file; you can call only those that have been registered with the `TwigExtension::getFunctions()` (see [TwigExtension::getFunctions](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/lib/Drupal/Core/Template/TwigExtension.php#L97)).

Find a further explanation of these Drupal-specific functions in the Drupal handbook: [List of Drupal functions for Twig Templates](https://www.drupal.org/node/2486991)

### `url($name, $parameters, $options)`

Generates an absolute URL, given a route name and optional parameters.

```
<a href="{{ url('view.frontpage.page_1 }}">{{ 'View front page content'|t }}</a>

<!-- Output -->
<a href="https://example.com/d8-theming-twig/node">View front page content</a>
```

### `path($name, $parameters, $options)`

Generates a relative URL path given a route name and parameters.

```
<a href="{{ path('entity.user.canonical', {'user': user.id}) }}">
  {{ 'View user profile'|t }}
</a>

<!-- Output -->
<a href="/user/1">View user profile</a>
```

### `link($text, $url, $attributes)`

Create a link in HTML.

```
{{ link('Drupalize.Me', 'https://drupalize.me', {'class': ['external'], 'role':['link']}) }}

<!-- Output -->
<a href="https://drupalize.me" class="external" role="link">Drupalize.Me</a>
```

### `file_url($uri)`

Accepts a relative path from the root and creates an absolute path to the file.

```
<img
  src="{{ file_url(node.field_image.entity.uri.value) }}"
  alt="{{ node.field_image.alt }}"
  height="{{ node.field_image.height }}"
  width="{{ node.field_image.width }}"
/>

<!-- Output -->
<img src="https://example.com/sites/default/files/path/to/file.jpg" alt="My image alt" height="640" width="480" />
```

### `attach_library($library)`

Attaches a library to the template. For a more in-depth look at how this works, see [Attach a Library](https://drupalize.me/tutorial/attach-asset-library).

```
{{ attach_library('class/node') }}
```

For a more in-depth tutorial on how to add links to Twig templates, see the tutorial [Create Links with Twig in a Template File](https://drupalize.me/tutorial/create-links-twig-template-file).

### `add_suggestion`

The `add_suggestion` filter allows you to add a [theme suggestion](https://drupalize.me/course/theme-hook-suggestions-drupal-templates) to a [render array rendered with `#theme`](https://drupalize.me/tutorial/concept-render-api). For example, if `content.body` has a render array with `'#theme' => 'field'`, using the `| add_suggestion` filter with the variable `{{ content.body | add_suggestion('details') }}` would allow loading a template *field--details.html.twig*.

The theme suggestion added with `| add_suggestion` will have the highest priority and will take precedence over any pre-existing theme suggestions.

See also this change record: [New Twig |add\_suggestion filter for adding a theme suggestion](https://www.drupal.org/node/3301862).

## Note about Twig functions and api.drupal.org

If you want to look up Drupal-specific Twig functions on [api.drupal.org](https://api.drupal.org/api/drupal), see the list of methods in the [`TwigExtension` class](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/class/TwigExtension/).

## Define your own custom Twig functions

You can also define your own custom Twig functions. For an example of how to do this, see [core/modules/system/tests/modules/twig\_extension\_test/src/TwigExtension/TestExtension.php](https://api.drupal.org/api/drupal/core%21modules%21system%21tests%21modules%21twig_extension_test%21src%21TwigExtension%21TestExtension.php/10).

## Filter basics

Similar to functions – but with much more flexibility – are Twig filters.

Filters are applied using the `|` pipe character inside a Twig expression, and can operate either on variables or literals.

```
   <div>{{ 3.14159|round }}</div>
   # Or as a variable.
   <div>{{ pi|round }}</div>
```

This expression applies the `round` filter to the number 3.14159, which will cause Twig to output `<div>3</div>`.

Some filters take additional arguments that change how the filter functions. The `round` filter rounds to the nearest whole number by default, but by using arguments, you can make it always round up or down, and change the precision. Find out what arguments each filter accepts by reading the documentation for that filter.

```
   <div>{{ 3.14159|round(2) }}</div>
```

This argument changes the precision to two decimal points and would result in the following output: `<div>3.14</div>`.

Filters can be applied to an entire block using the special `filter` section.

```
  {% filter upper %}
    All of this text will become uppercase.
  {% endfilter %}
```

## Applying multiple filters

Multiple filters can be chained together.

```
  <div>{{ user.name|lower|escape }}</div>
```

## Using named arguments

Arguments to filters can be named, so that a filter can be used without specifying a value for all arguments. This is useful when using filters like `round`, which takes two arguments: `round(precision, method)`. Perhaps you only want to specify a value for the second argument and leave the first one as the default. Writing your function like the example can make your templates more readable.

```
  <div>{{ 3.14159|round(method="ceil") }}</div>
```

## Drupal-specific filters

Drupal defines the following filters, which are not part of the standard Twig engine. These filters are smart about Drupal conventions, such as renderable arrays, and make it easier to work with variables provided by Drupal modules.

### t

The `t` filter allows user interface strings to be translated. This filter should be used for any interface strings manually added to the template that will appear to users. Strings contained within a variable are considered already translated (when the variable is set) and should be output directly.

```
    <a href="//default/" title="{{ 'Home'|t }}">{{ 'Home'|t }}</a>
```

For more on ensuring that your theme is translatable, see [Make Strings Translatable](https://drupalize.me/tutorial/make-strings-translatable).

### safe\_join

The `safe_join` filter joins several strings together with a supplied separator. See [TwigExtension::safeJoin()](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/lib/Drupal/Core/Template/TwigExtension.php#L591).

Example:

```
<p>{{ items|safe_join(", ") }}</p>
```

This outputs each string in the `items` variable, concatenated, with a comma and space separating each item.

### without

The `without` filter creates a copy of a renderable array and removes the specified child elements. This preserves the original renderable array. Child elements can still be printed from the original in their entirety.

For the Drupal 8 API, see [twig\_without](https://api.drupal.org/api/drupal/core%21themes%21engines%21twig%21twig.engine/function/twig_without/8.9.x) ([deprecated](https://www.drupal.org/node/3011154)) and for the latest Drupal API, see [TwigExtension::withoutFilter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/function/TwigExtension%3A%3AwithoutFilter/). (Usage of the `without` filter in Twig templates is unaffected, however the `twig_without` function is deprecated and [was removed in 9.0.0](https://www.drupal.org/node/3096454).)

Example:

```
<p>{{ content|without('links') }}</p>
```

This prints everything in the content variable except `content.links`.

### drupal\_escape

The `drupal_escape` filter is a replacement for Twig's `escape` filter and can be used to escape HTML strings before displaying them. See [TwigExtension::escapeFilter()](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/lib/Drupal/Core/Template/TwigExtension.php#L409).

### clean\_class

The `clean_class` filter prepares a string for use as a valid HTML class name. See [Html::getClass()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Utility%21Html.php/function/Html%3A%3AgetClass/)

### clean\_id

The `clean_id` filter prepares a string for use as a valid HTML ID. See [Html::getID()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Component%21Utility%21Html.php/function/Html%3A%3AgetId/).

## How filters are registered with Twig

Filters are just PHP callables that Twig invokes on our behalf.

You can't, however, go about calling any PHP function. `{{ 'Big cheese.'|drupal_rebuild }}`, for example, isn't going to call the `drupal_rebuild()` function, even though it is indeed defined. Rather, you're limited to the filters registered with Twig. This is done by implementing the `Twig_Extension::getFilters()` method and returning an array of `\Twig_SimpleFilter` or `\Twig_Filter_Function` objects, one for each new filter you want to declare. See `\Drupal\Core\Template\TwigExtension::getFilters()`, where Drupal core adds in all its extra filters like `t`, and `drupal_escape`.

If you want to add your own, the *core/modules/system/tests/twig\_extension\_test/* module provides a good example of how to do so.

To see a list of all functions and filters defined in Drupal's TwigExtension class, see Drupal core's [TwigExtension class](https://git.drupalcode.org/project/drupal/-/blob/10.1.x/core/lib/Drupal/Core/Template/TwigExtension.php).

## Recap

In this tutorial, we explored the filters and functions specific to Drupal's implementation of Twig.

## Further your understanding

- Explain the function that Twig filters perform
- Locate the appropriate filter for rounding a float value and apply it to a variable in a Twig template
- Recall the Drupal-specific Twig filters and their use-cases

## Additional resources

- Topic: [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- Course: [Using Twig in Drupal Templates](https://drupalize.me/course/using-twig-drupal-templates) (Drupalize.Me)
- [List of Twig 3.x functions](https://twig.symfony.com/doc/3.x/functions/index.html) (twig.symfony.com)
- [List of Drupal functions for Twig Templates](https://www.drupal.org/node/2486991) (Drupal.org)
- [List of Twig 3.x filters](https://twig.symfony.com/doc/3.x/filters/index.html) (twig.symfony.com)
- [List of Drupal filters for Twig Templates](https://www.drupal.org/node/2357633) (Drupal.org)
- [Filters - Modifying Variables In Twig Templates](https://www.drupal.org/node/2357633) (Drupal.org)
- [Change record: Procedural function twig\_without() is deprecated](https://www.drupal.org/node/3011154) (Drupal.org)
- [Change record: New Twig |add\_suggestion filter for adding a theme suggestion](https://www.drupal.org/node/3301862) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Print Values from a Field with a For Loop](/tutorial/print-values-field-loop?p=2464)

Next
[Whitespace Control with Twig](/tutorial/whitespace-control-twig?p=2464)

Clear History

Ask Drupalize.Me AI

close