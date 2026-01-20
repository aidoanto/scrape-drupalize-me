---
title: "Use Render Element Types in a Render Array"
url: "https://drupalize.me/tutorial/use-render-element-types-render-array?p=3252"
guide: "[[output-and-format-data-code]]"
order: 10
---

# Use Render Element Types in a Render Array

## Content

There are a bunch of [existing render elements](https://api.drupal.org/api/drupal/elements), most commonly Form API elements. You need to know how to discover and make use of existing elements. In this tutorial, we'll learn how to:

- Locate a list of elements provided by Drupal core
- Figure out what properties apply to each element
- Use any render element type when defining content or forms in our code

By the end of this tutorial you should know what render element types are available for you to use, and how to find the details you'll need in order to implement them in your own render arrays.

## Goal

Locate a list of existing render element types and use any of them when defining content with a render array.

## Prerequisites

- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements)
- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

## Watch: Use Render Elements in a Render Array

Sprout Video

## Use any render or form element

Using a render or form element type requires:

1. Finding the unique name of the element type you want to use
2. Defining a new element in render array with a `'#type'` property
3. Providing values for any element type-specific properties, and/or properties common to all render array elements

### Find an element type

You can get a list of all the render element types provided by Drupal core from <https://api.drupal.org/api/drupal/elements>. This list includes both standard render elements and form elements. Remember that form elements can only be used in the context of defining a Form API array and will not work properly in a non-Form API render array.

Image

![Section of the table showing list of render api elements with html_tag element highlighted](../assets/images/render-elements-list.png)

From this list you can discover the element name (the first column in the table) as well as the class that provides the render element plugin. The element name, `html_tag` in this example, is the value you'll use for the `'#type'` property in your render array.

**Note:** If you're looking at the class that defines the render element, you can get the element's unique name from the plugin attribute. Look for something like the following: `#[RenderElement("html_tag")]`.

Example:

```
$build['hello'] = [
  '#type' => 'html_tag',
];
```

### Fill in additional type-specific properties

With few exceptions, every render element type has type-specific properties that you can define in addition to the set of properties common to all elements in a render array. If you're using the `'#type'` property as part of the array element, you should avoid using `#theme` or `#markup` for this specific element.

To figure out what the type-specific properties are, look at the documentation for the class that defines the render element plugin. In this case, `\Drupal\Core\Render\Element\HtmlTag`. Find the documentation with either your IDE or by clicking the link from the table in the [API documentation](https://api.drupal.org/api/drupal/elements). This documentation should provide a list of element type-specific properties and some example code demonstrating how to use the element type.

Example:

```
/**
 * Provides a render element for any HTML tag, with properties and value.
 *
 * Properties:
 * - #tag: The tag name to output.
 * - #attributes: (array, optional) HTML attributes to apply to the tag. The
 *   attributes are escaped, see \Drupal\Core\Template\Attribute.
 * - #value: (string, optional) A string containing the textual contents of
 *   the tag.
 * - #noscript: (bool, optional) When set to TRUE, the markup
 *   (including any prefix or suffix) will be wrapped in a <noscript> element.
 *
 * Usage example:
 * @code
 * $build['hello'] = [
 *   '#type' => 'html_tag',
 *   '#tag' => 'p',
 *   '#value' => $this->t('Hello World'),
 * ];
 * @endcode
 */
#[RenderElement("html_tag")]
class HtmlTag extends RenderElementBase {
  // ...
}
```

In our experience, this documentation isn't always perfect, and you might notice there are cases where properties exist that are not defined here. First of all, we would consider this a bug, and as such, it should be reported. Secondly, if you're unsure about properties try looking at the code that defines the element type and see if you can find the related `#theme` hook. Then take a look at any `template_preprocess_HOOK()` functions associated with the element to discover any additional properties that might be used. An example of this is `template_preprocess_table()`.

See [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays) for more on common properties and the use of `#theme` or `#markup`.

### Use the element type in a render array

Once you know the unique name of the render element type, and the properties you can use to define elements of that type in a render array, you can define a new element in the render array for your custom code.

Example:

```
$build = [];
$build['hello'] = [
  '#type' => 'html_tag',
  '#tag' => 'p',
  '#value' => $this->t('Hello World'),
];
$build['guten_tag'] = [
  '#type' => 'html_tag',
  '#tag' => 'marquee',
  '#attributes' => ['direction' => 'right', 'scrollamount' => 10],
  '#value' => $this->t('Hallo Welt!'),
];
```

Resulting output:

```
<p>Hello World!</p>
<marquee direction="right" scrollamount="10">Hallo Welt!</marquee>
```

## Recap

In this tutorial, we looked at the list of render elements provided by Drupal core. Then, we walked through how to discover an element type's unique name and what custom properties apply to any given render element type. Finally, we showed an example of implementing a render element type using the `'#type'` property in a render array.

## Further your understanding

- [Learn about using `'#type' => 'table'` to define tables in a render array](https://drupalize.me/tutorial/output-table) (Drupalize.Me)
- Can you find the render element type that is used to describe a link? Can you then use it to output a link to this tutorial in a custom render array?

## Additional resources

- [List of render elements provided by Drupal core](https://api.drupal.org/api/drupal/elements) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use #prefix and #suffix Properties to Wrap an Element](/tutorial/use-prefix-and-suffix-properties-wrap-element?p=3252)

Next
[Output a List of Items](/tutorial/output-list-items?p=3252)

Clear History

Ask Drupalize.Me AI

close