---
title: "Concept: Render APIfree"
url: "https://drupalize.me/tutorial/concept-render-api?p=3239"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Render APIfree

## Content

Drupal's Render API plays a crucial role in how content is presented on a site. The Render API manages how content is rendered through render arrays and render elements.

In this tutorial, we'll:

- Define render arrays, highlighting properties and elements.
- Explain how render elements are used as shorthand for complex structures.
- Describe the primary types of data we can use in a render array.
- Touch on the role of renderers and special methods for rendering entities.

By the end of this tutorial, you'll better understand how Drupal constructs a page's output through render arrays and streamlines rendering with render elements.

## Goal

Introduce the central elements of Drupal's Render API including render arrays and render elements.

## Prerequisites

- [Concept: Themeable Output](https://drupalize.me/tutorial/concept-themeable-output)

## Render arrays

*Render arrays* are central to Drupal's rendering process. Render arrays are associative arrays that define data and its presentation method. Drupal constructs the entire page as a render array before converting it to HTML, enabling dynamic content changes and display alterations by modules and themes.

Render arrays consist of *properties* and *elements*. Properties, denoted by a hash (`#`), carry metadata or rendering instructions. Elements represent actual data chunks for rendering.

For module developers, render arrays are how we define output for a chunk of data. Here's an example showing the render array's child elements, `list` and `paragraph` and their properties:

```
$render_array = [
   'list' => [
      '#theme' => 'item_list',
      '#items' => ['Item 1', 'Item 2', 'Item 3'],
      '#type' => 'ul',
   ],
   'paragraph' => [
      '#markup' => '<p>This is an example paragraph.</p>',
   ],
];
```

Each of these elements (`list` and `paragraph`) uses properties to define how they should be rendered by Drupal. The properties, `#theme`, `#items`, and `#type`, describe how the `list` element should be rendered. The `#markup` property applies to the `paragraph` element.

For more on render arrays, see [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays).

## Render elements

*Render elements*, or element types, are shorthand for complex render array structures. They offer defaults for common UI patterns. Identifiable in a render array by the `#type` property, render elements expand during rendering to include its properties.

For example, a text field in a form:

```
$form['example_text'] = [
   '#type' => 'textfield',
   '#title' => t('Example text field'),
   '#required' => TRUE,
];
```

Using the `textfield` render element simplifies how we define this form field. The render element includes default properties for the `textfield` like validation and theming.

For more on render elements, see [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements).

## Primary types of data in a render array

Data associated with a theme hook for rendering can typically use one of 3 methods: `#theme`, `#type`, and `#markup`.

- Use `#markup` to provide simple HTML markup.
- For complex markup, use `#theme` or `#type` (render element) to enable theme customization.
- Use `#plain_text` for safe, non-HTML content.

### `#markup`

Provide simple HTML markup.

Example:

```
'#markup' => '<p>Hello world!</p>'
```

### `#theme`

Passes data to a specific theme hook, usually a Twig template, with properties typically serving as template variables. Modules define `#theme` values through `hook_theme()`.

Example:

```
'#theme' => 'item_list'
```

### `#type`

Indicates the render element type, detailing data and rendering options.

Example:

```
'#type' => 'table'
```

Read more in [Render API overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/theme_render/).

## Role of renderers

In Drupal's Render API, *renderers* convert render arrays into its final output, such as HTML. Renderers process arrays, apply transformations, and use theme functions or templates for HTML generation. This ensures consistent output and allows customization and alterations.

For more on renderers, see [Render API Renderers](https://drupalize.me/tutorial/render-api-renderers).

## Rendering entities and other special data types

When working with Drupal data types like entities or links, the objects that represent the data will often have a helper method that returns the renderable array representation of the item.

For example, link objects can be rendered like so:

```
$link = Link::fromTextAndUrl('This is a link', Url::fromUri('http://example.com'));
$build['external_link'] = $link->toRenderable();
```

We will see some more examples of rendering entities in [Display a List of Vendors](https://drupalize.me/tutorial/display-list-vendors).

## Recap

In this tutorial, we learned that the Render API in Drupal, through its render arrays and render elements, provides a structured and flexible way to manage content presentation. As module developers, anytime our module needs to output something that is intended to be displayed to the user, we should do so using renderable arrays.

## Further your understanding

- How do render arrays and elements keep Drupal's content presentation flexible?
- What are the benefits of using render elements over direct render array definitions?

## Additional resources

- [Render API Overview](https://drupalize.me/tutorial/render-api-overview) (Drupalize.Me)
- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays) (Drupalize.Me)
- [What Are Render Elements?](https://drupalize.me/tutorial/what-are-render-elements) (Drupalize.Me)
- [Render API Renderers](https://drupalize.me/tutorial/render-api-renderers) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Themeable Output](/tutorial/concept-themeable-output?p=3239)

Next
[Output Content Using Render API](/tutorial/output-content-using-render-api?p=3239)

Clear History

Ask Drupalize.Me AI

close