---
title: "Add Classes and HTML Attributes to Render Arrays"
url: "https://drupalize.me/tutorial/add-classes-and-html-attributes-render-arrays?p=3252"
guide: "[[output-and-format-data-code]]"
order: 14
---

# Add Classes and HTML Attributes to Render Arrays

## Content

We often need to add code to an [alter hook](https://drupalize.me/tutorial/what-are-hooks) or [preprocess function](https://drupalize.me/tutorial/what-are-preprocess-functions) that adds additional HTML attributes to items in a render array. Maybe you're developing a module that adds conditional classes to elements on the page under certain circumstances. Or perhaps your theme needs to add some data attributes to certain links, or form elements, in order to enable some custom JavaScript functionality.

Adding HTML attributes like `class`, `id`, or `data-*` to render array elements involves:

- Adding the desired values to the element in a render array as an array of key/value pairs
- Converting the values in the render array to an `Attribute` object
- Outputting the `Attribute` object inside a template file

In this tutorial, we'll cover all of these steps. By the end of this tutorial, you should be able to add new HTML attributes to elements in a render array and discover which property those values should be added to, depending on the element in question.

## Goal

Add HTML attributes (like `class` or `id`) to an HTML tag that is output by a render or form element.

## Prerequisites

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)
- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)

The method differs depending on whether you're dealing with a render element (`'#type' => 'textfield'`) or a Twig template (`'#theme' => 'item-list'`).

## Render elements

All render elements, including form elements, have the property `#attributes`. This is defined in the base class `Drupal\Core\Render\Element\RenderElementBase` from which all render and form elements are extended.

Here's what the documentation says about the `#attributes` property:

**#attributes:** (array) HTML attributes for the element. The first-level keys are attribute names, such as `class`, and the attributes are usually given as an array of string values to apply to that attribute (the rendering system will concatenate them into a string in the HTML output).

Example code:

```
$build['name'] = [
  '#type' => 'textfield',
  '#title' => $this->t('Name'),
  '#default_value' => isset($value) ? $value : 'Alice',
  '#attributes' => [
    'class' => ['name', 'custom-class'],
    'data-name' => isset($value) ? $value : 'Alice',
  ],
];
```

Result:

```
<input class="name custom-class form-text" data-name="Alice" type="text" size="60" maxlength="128" />
```

From the documentation: The attribute keys and values are automatically escaped for output with `\Drupal\Component\Utility\Html::escape()`. No protocol filtering is applied, so when using user-entered input as a value for an attribute that expects a URI (href, src, etc.), `\Drupal\Component\Utility\UrlHelper::stripDangerousProtocols()` should be used to ensure dangerous protocols (such as `javascript:`) are removed.

It's worth noting that this is convention, not an absolute. All render elements in core support the `#attributes` property, but there's no guarantee that render elements provided by non-core modules do. Remember, render elements are really just a method of providing a set of handy default values for other properties. Ultimately, they are converted to a `#theme` element and linked to a template file. Thus, their attributes are rendered just like any template file (see below) with the caveat being there's a consistent convention.

## `#theme` elements

In template files, attributes are handled by first converting the array of values for the attributes property in the render array to a `\Drupal\Core\Template\Attribute` object inside a preprocess function. Next, printing that attributes object inside a template file.

The *node.html.twig* template, for example, has `attributes`, `title_attributes`, and `content_attributes`. So in a render array you could do something like the following:

```
$build['node'] = [
  '#theme' => 'node',
  ...
  '#attributes' => [
    'data-node-id' => $node->id(),
  ],
  '#content_attributes' => [
    'class' => ['custom-node-class'],
    'id' => 'node-' . $node->id() . '-content',
  ],
];
```

Then in a [preprocess function](https://drupalize.me/tutorial/what-are-preprocess-functions), which receives the above properties inside the `$variables` array:

```
$variables['title_attributes'] = new Attribute($variables['title_attributes']);
```

And finally, in the [template file](https://drupalize.me/tutorial/what-are-template-files):

```
<h2{{ title_attributes }}>{{ title }}</h2>
```

Note that the variable names `attributes`, `title_attributes`, and `content_attributes` will be automatically converted to `Attribute` objects by the theme manager when not already converted by a preprocess function.

With all of that in mind, you should now be able to figure out what "attributes" property to assign values to in the render array you're constructing. It might take a little digging to figure out exactly how/where they're used in the final output, but the technique of assigning an array of values to the `#attributes` property is consistent.

## Recap

In this tutorial we learned how `#attributes` properties in a render array are converted first to `Attribute` objects and then output in template files in order to allow you to define custom HTML attributes for an element in a render array.

## Further your understanding

- Can you find the spot in `\Drupal\Core\Theme\ThemeManager::render` where `title_attributes`, and `content_attributes` are added for all templates?
- Learn more about how Twig uses `Attribute` objects in [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates)

## Additional resources

- [Drupal\Core\Template\Attribute](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21Attribute.php/class/Attribute) (api.drupal.org)
- [Using attributes in templates](https://www.drupal.org/docs/8/theming-drupal-8/using-attributes-in-templates) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Output Content with a Template File](/tutorial/output-content-template-file?p=3252)

Next
[Generate URLs and Output Links](/tutorial/generate-urls-and-output-links?p=3252)

Clear History

Ask Drupalize.Me AI

close