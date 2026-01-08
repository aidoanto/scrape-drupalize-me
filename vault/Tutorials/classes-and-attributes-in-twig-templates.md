---
title: "Classes and Attributes in Twig Templates"
url: "https://drupalize.me/tutorial/classes-and-attributes-twig-templates?p=2464"
guide: "[[frontend-theming]]"
---

# Classes and Attributes in Twig Templates

## Content

Theme developers often need to add or remove classes and other attributes from an HTML tag. Template files handle this with a special **Attributes** object that contains the attributes and their values, as well as a handful of powerful methods to help manage these attributes.

In this tutorial we’ll cover:

- Adding/removing classes from elements in a Twig template
- The attributes object
- Examples of common tasks using various helper methods on the attributes object

## Goal

Understand how to add and remove HTML classes and attributes in Twig template files.

## Prerequisites

- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)
- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions)

## The attributes object

Attribute objects ([Drupal\Core\Template\Attribute](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Template!Attribute.php/class/Attribute)) are used to store one or more attributes for an HTML tag and provide theme developers with helpful utility methods for modifying the value(s) of any attribute. Attribute objects can be printed just like any other variable in a Twig template, but are unique in that when printed the object itself is smart enough to output the attribute name/value pairs in the correct format.

Although an actual attribute object doesn't look exactly like this, I think it helps to illustrate how it works. Given an object with the following key/value pairs:

```
attributes:
  classes:
    - node
    - node--article
  id: node-42
  data-custom: a string of custom data
```

Printing it out in a template like this: `<div{{ attributes }}></div>` results in valid HTML output like this:

```
<div class="node node--article" id="node-42" data-custom="a string of custom data"></div>
```

The attributes object should be output without any additional space between the object and the tag name. The space will be included automatically as necessary.

```
<div{{ attributes }}></div>` not `<div {{ attributes }}></div>
```

Attributes are drillable. This means that you can print all of them at once by printing the attributes object directly, or you can print each attribute individually. Examples of both methods can be found below.

## Classes should be set in template files

For consistency and ease of discovery, it's best practice to put all CSS classes related to style and presentation (not behavioral or state JavaScript classes) in the relevant template file. By using this pattern of defining the `classes` value with the Twig `set` tag at the top of the template file, anyone reading the file can immediately see which presentation classes will be applied.

Example from *core/themes/olivero/templates/content/node--teaser.html.twig*:

```
{%
set classes = [
'node',
'node--type-' ~ node.bundle|clean_class,
node.isPromoted() ? 'node--promoted',
node.isSticky() ? 'node--sticky',
not node.isPublished() ? 'node--unpublished',
view_mode ? 'node--view-mode-' ~ view_mode|clean_class,
]
%}

<article{{ attributes.addClass(classes) }}>
```

In this example, the [Twig `set` tag](https://twig.symfony.com/doc/3.x/tags/set.html) is used to declare a new variable named `classes`, which is an array of class names to use on the `article` tag. The actual contents of the array will vary depending on the variables passed to the template file. This line, for example, `node.isSticky() ? 'node--sticky',` will add "node--sticky" to the array only if the node being viewed has been flagged as "sticky". This allows for contextual classes to be added in addition to always-present classes like "node".

## Working with the attributes object

Common uses of the attributes object within a Twig template include the following:

### Print all attributes for a tag

```
<div{{ attributes }}></div>
```

### Add classes

`attributes.addClass($class)`: Adds classes or merges them on to array of existing CSS classes. Accepts either an individual string, or an array of class names.

```
<div{{ attributes.addClass('my-class') }}>
```

Add multiple classes by first creating an array with `set`, and then passing that array to the `addClass()` method:

```
{%
  set classes = [
    'my-class',
    'my-other-class',
  ]
%}
<div{{ attributes.addClass(classes) }}></div>
```

### Remove classes

`attributes.removeClass($class)`: Removes a class. Accepts either an individual string, or an array of class names. Can be chained with other methods such as `addClass`. For example:

```
{%
  set classes = [
    'my-class',
    'my-other-class',
    'my-special-class',
  ]
%}
<div{{ attributes.addClass(classes).removeClass('my-special-class') }}></div>
```

### Set any attribute

`attributes.setAttribute($attribute, $value)`: Set the value of any attribute. The first parameter should be the name of the attribute, and the second parameter should be a string or array of one or more values for this attribute.

```
<div{{ attributes.setAttribute('id', 'myID') }}>
<div{{ attributes.setAttribute('data-bundle', node.bundle) }}>
```

### Remove any attribute

```
<div{{ attributes.removeAttribute('id') }}>
```

### Check for the existence of a specific class

```
{% if attribute.hasClass('myClass') %}
  {# do stuff #}
{% endif %}
```

### Chaining methods

Any of these "dot methods" may be chained together. For example:

```
<div{{ attributes.addClass('hello').removeClass('goodbye') }}>
```

### Using Twig's `without` filter

When printing out individual attributes to customize them within a Twig template, you can use the `without` filter to prevent attributes that have already been printed from being printed again:

```
<div class="{{ attributes.class }} my-custom-class"{{ attributes|without('class') }}>
```

In the above example, Twig's dot syntax is used in `attributes.class` to print out classes in a hard-coded HTML class attribute. Then the attributes object is printed again within the same HTML tag, but without the class attribute.

## Adding attributes outside a template

There are other ways (outside a template file) to programmatically add classes and HTML attributes to render elements.

### Adding attributes in a preprocess function

You can add to the class attributes array inside a preprocess function with:

```
$variables['attributes']['class'][] = 'my value'
```

Here's an example from [Custom Theme Settings](https://drupalize.me/tutorial/customize-theme-settings):

```
/**
 * Implements hook_preprocess_region().
 */

function icecream_preprocess_region(&$variables) {
  if ($variables['region'] == 'header') {
    $variables['attributes']['class'][] = theme_get_setting('site_branding_bg_color');
  }
}
```

### Adding attributes in a module

In a module, you'll probably want to [Add Classes and HTML Attributes to Render Arrays](https://drupalize.me/tutorial/add-classes-and-html-attributes-render-arrays) for your module's custom render elements.

## Recap

In this tutorial, we learned how to add and remove classes from elements in a template file. We learned how to use the `set` keyword to define values classes and how to add and remove classes using helper methods on the attributes object.

## Further your understanding

- [Hands-On Theming Exercises for Drupal](https://drupalize.me/course/hands-theming-exercises-drupal) contains several exercises where you can practice adding classes in templates.
- Add a new class that will be applied to the `article` tag wrapping nodes in your *node.html.twig* template.
- If you use `attributes.setAttribute()` to set a value on an attribute that has already been set, what happens to the existing value?
- Browse through the templates in the Classy theme to find examples of different ways that contextual classes can be added to an element based on variables in a template file.
- Learn about how attributes objects are added to template files in [Add Classes and HTML Attributes to Render Arrays](https://drupalize.me/tutorial/add-classes-and-html-attributes-render-arrays).

## Additional resources

- [Using attributes in templates](https://www.drupal.org/node/2513632) (Drupal.org)
- Attribute objects are instances of [Drupal\Core\Template\Attribute](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21Attribute.php/class/Attribute/) (api.drupal.org)
- [Modifying assets in a .theme file](https://www.drupal.org/node/2638200) (Drupal.org)
- [This change record](https://www.drupal.org/node/2315471) has some good before-and-after examples comparing how classes are added to a template in Drupal 7 and Drupal 8 (Drupal.org)
- [Read about the decision to control classes in template files](https://drupalize.me/blog/201411/controlling-css-classes-classy-theme-drupal-8) (Drupalize.Me). [This thread](https://www.drupal.org/node/2289511) also provides a lot of background information about the decision. (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Whitespace Control with Twig](/tutorial/whitespace-control-twig?p=2464)

Next
[Create Links with Twig in a Template File](/tutorial/create-links-twig-template-file?p=2464)

Clear History

Ask Drupalize.Me AI

close